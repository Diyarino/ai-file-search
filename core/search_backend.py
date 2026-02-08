# -*- coding: utf-8 -*-
"""
Modul für die Suche.

....

Metadata:
    Author: Diyar Altinses, M.Sc.
    Created: 2026-02-03
"""

import os
import json
import numpy as np
import ollama
from config import INDEX_FILE, MODEL_GEN, MODEL_EMBED
from core.file_reader import read_file_content

class SearchEngine:
    def __init__(self):
        self.index = {}
        self.load_index()

    def load_index(self):
        if os.path.exists(INDEX_FILE):
            try:
                with open(INDEX_FILE, "r", encoding="utf-8") as f:
                    self.index = json.load(f)
            except Exception as e:
                print(f"Index defekt, erstelle neu: {e}")
                self.index = {}

    def save_index(self):
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(self.index, f, ensure_ascii=False)

    def _get_embedding(self, text):
        try:
            # Text kürzen und Newlines entfernen für saubere Vektoren
            clean = text[:8000].replace("\n", " ")
            response = ollama.embeddings(model=MODEL_EMBED, prompt=clean)
            return response["embedding"]
        except Exception as e:
            print(f"Embedding Fehler: {e}")
            return None

    def _get_summary(self, text):
        if len(text) < 20: return "Kein Inhalt."
        try:
            prompt = f"Fasse diesen Inhalt extrem kurz (max 1 Satz) auf Deutsch zusammen:\n{text[:2500]}"
            res = ollama.chat(model=MODEL_GEN, messages=[{'role': 'user', 'content': prompt}])
            return res['message']['content']
        except:
            return "Zusammenfassung fehlgeschlagen."

    def index_folder(self, folder_path, progress_callback=None):
        """
        Scannt Ordner und aktualisiert den Index.
        progress_callback: Funktion, die Status-Updates empfängt (Text)
        """
        count_new = 0
        
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.pdf', '.docx', '.txt')):
                    path = os.path.join(root, file)
                    mtime = os.path.getmtime(path)

                    # Check: Datei schon aktuell im Index?
                    if path in self.index and self.index[path]['mtime'] == mtime:
                        continue

                    # Verarbeitung
                    if progress_callback:
                        progress_callback(f"Verarbeite: {file}...")
                    
                    text = read_file_content(path)
                    if not text.strip():
                        continue

                    vector = self._get_embedding(text)
                    if vector:
                        summary = self._get_summary(text)
                        self.index[path] = {
                            "mtime": mtime,
                            "filename": file,
                            "summary": summary,
                            "vector": vector
                        }
                        count_new += 1
                        
                        # Alle 5 Dateien speichern
                        if count_new % 5 == 0:
                            self.save_index()
        
        self.save_index()
        return count_new

    def search(self, query):
        """Gibt sortierte Liste von Ergebnissen zurück (Score, Pfad, Daten)"""
        query_vec = self._get_embedding(query)
        if not query_vec:
            return []

        results = []
        q_vec = np.array(query_vec)
        q_norm = np.linalg.norm(q_vec)

        if q_norm == 0: return []

        for path, data in self.index.items():
            if "vector" not in data: continue
            
            d_vec = np.array(data["vector"])
            d_norm = np.linalg.norm(d_vec)

            if d_norm > 0:
                # Cosinus Ähnlichkeit
                score = np.dot(q_vec, d_vec) / (q_norm * d_norm)
                results.append((score, path, data))

        # Sortieren nach Score (höchster zuerst)
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:15] # Top 15 Treffer