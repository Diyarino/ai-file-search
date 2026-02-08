# -*- coding: utf-8 -*-
"""
Haupt-Einstiegspunkt der Anwendung.

Dieses Modul dient als Startpunkt für die Software. Es initialisiert
die grafische Benutzeroberfläche (GUI) und startet den Event-Loop.

Metadata:
    Author: Diyar Altinses, M.Sc.
    Created: 2026-02-03
"""

import os
import threading
import platform
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Importiere unsere eigenen Module
import config
from core.search_backend import SearchEngine

# Settings für CustomTkinter
ctk.set_appearance_mode(config.APPEARANCE_MODE)
ctk.set_default_color_theme(config.COLOR_THEME)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Backend initialisieren
        self.engine = SearchEngine()

        # Fenster Setup
        self.title(config.APP_TITLE)
        self.geometry(config.APP_SIZE)

        # Layout Grid Konfiguration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Row 2 ist der Ergebnisbereich

        self.setup_ui()

    def setup_ui(self):
        # --- 1. HEADER & ORDNER ---
        self.header_frame = ctk.CTkFrame(self, corner_radius=10)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.btn_folder = ctk.CTkButton(
            self.header_frame, 
            text="📂 Ordner Scannen", 
            command=self.select_folder_thread,
            fg_color="#2B2B2B", hover_color="#444444" # Dunkles Grau
        )
        self.btn_folder.pack(side="left", padx=15, pady=15)

        self.lbl_status = ctk.CTkLabel(self.header_frame, text=f"Bereit. {len(self.engine.index)} Dokumente im Index.", text_color="gray")
        self.lbl_status.pack(side="left", padx=10)

        # --- 2. SUCHE ---
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.entry_search = ctk.CTkEntry(self.search_frame, placeholder_text="Wonach suchst du?", height=40, font=("Arial", 14))
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_search.bind("<Return>", lambda e: self.start_search_thread())

        self.btn_search = ctk.CTkButton(self.search_frame, text="Suchen", height=40, font=("Arial", 14, "bold"), command=self.start_search_thread)
        self.btn_search.pack(side="right")

        # --- 3. ERGEBNISSE (Scrollbar) ---
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Ergebnisse")
        self.scroll_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

    # --- LOGIK & THREADING ---

    def select_folder_thread(self):
        folder = filedialog.askdirectory()
        if not folder: return
        
        self.btn_folder.configure(state="disabled")
        threading.Thread(target=self.run_indexing, args=(folder,), daemon=True).start()

    def run_indexing(self, folder):
        def update_status(msg):
            self.lbl_status.configure(text=msg)
        
        new_count = self.engine.index_folder(folder, progress_callback=update_status)
        
        self.lbl_status.configure(text=f"Fertig! {new_count} neue Dateien indexiert.")
        self.btn_folder.configure(state="normal")

    def start_search_thread(self):
        query = self.entry_search.get()
        if not query: return
        
        self.btn_search.configure(state="disabled")
        self.lbl_status.configure(text="Suche läuft...", text_color="#3B8ED0") # Blau
        
        # Alten Inhalt löschen
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        threading.Thread(target=self.run_search, args=(query,), daemon=True).start()

    def run_search(self, query):
        results = self.engine.search(query)
        
        self.after(0, lambda: self.display_results(results))

    def display_results(self, results):
        self.btn_search.configure(state="normal")
        self.lbl_status.configure(text="Suche abgeschlossen.", text_color="gray")

        if not results:
            ctk.CTkLabel(self.scroll_frame, text="Keine passenden Dokumente gefunden.", font=("Arial", 16)).pack(pady=20)
            return

        for score, path, data in results:
            self.create_result_card(score, path, data)

    def create_result_card(self, score, path, data):
        # Container
        card = ctk.CTkFrame(self.scroll_frame, fg_color=("white", "#2b2b2b"), corner_radius=10)
        card.pack(fill="x", pady=5, padx=5)

        # Header
        head = ctk.CTkFrame(card, fg_color="transparent")
        head.pack(fill="x", padx=10, pady=10)
        
        name = ctk.CTkLabel(head, text=data['filename'], font=("Arial", 16, "bold"))
        name.pack(side="left")
        
        perc = int(score * 100)
        col = "#2CC985" if perc > 70 else "#E1B000" # Grün oder Gelb
        match_lbl = ctk.CTkLabel(head, text=f"{perc}% Match", text_color=col, font=("Arial", 14, "bold"))
        match_lbl.pack(side="right")

        # Body
        summary = ctk.CTkLabel(card, text=data['summary'], wraplength=700, justify="left", font=("Arial", 12))
        summary.pack(fill="x", padx=10, pady=(0, 10))

        # Footer (Buttons)
        foot = ctk.CTkFrame(card, fg_color="transparent")
        foot.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(foot, text="📄 Öffnen", width=100, command=lambda p=path: self.open_file(p)).pack(side="left", padx=(0,10))
        ctk.CTkButton(foot, text="📂 Ordner", width=100, fg_color="transparent", border_width=1, command=lambda p=path: self.open_folder(p)).pack(side="left")

    # --- OS ACTION ---
    def open_file(self, path):
        try:
            if platform.system() == 'Windows': os.startfile(path)
            elif platform.system() == 'Darwin': subprocess.call(('open', path))
            else: subprocess.call(('xdg-open', path))
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    def open_folder(self, path):
        try:
            if platform.system() == 'Windows':
                subprocess.Popen(f'explorer /select,"{os.path.normpath(path)}"')
            elif platform.system() == 'Darwin':
                subprocess.call(['open', '-R', path])
            else:
                subprocess.call(['xdg-open', os.path.dirname(path)])
        except: pass

if __name__ == "__main__":
    app = App()
    app.mainloop()