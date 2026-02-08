# -*- coding: utf-8 -*-
"""
Modul für Dateioperationen (IO-Layer).

Diese Klasse abstrahiert den Zugriff auf das Dateisystem. Sie stellt sicher,
dass nur valide Dateien geladen werden und behandelt Encoding-Probleme
beim Lesen von Quellcode-Dateien robust.

Metadata:
    Author: Diyar Altinses, M.Sc.
    Created: 2026-02-03
"""

import os
from pypdf import PdfReader
from docx import Document

def read_file_content(filepath):
    """Liest Text aus PDF, DOCX oder TXT."""
    text = ""
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == ".pdf":
            reader = PdfReader(filepath)
            # Begrenzung auf 15 Seiten für Performance
            for page in reader.pages[:15]:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        
        elif ext == ".docx":
            doc = Document(filepath)
            text = "\n".join([p.text for p in doc.paragraphs])
        
        elif ext == ".txt":
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
                
    except Exception as e:
        print(f"Fehler beim Lesen von {filename}: {e}")
        return ""

    return text