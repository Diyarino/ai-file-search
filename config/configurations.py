# -*- coding: utf-8 -*-
"""
Zentrale Konfigurationsdatei der Anwendung.

In diesem Modul werden alle statischen Konstanten, UI-Parameter und
Design-Einstellungen verwaltet. Dies ermöglicht eine einfache Anpassung
des Look & Feel, ohne den Quellcode der Logik-Module ändern zu müssen.

Metadata:
    Author: Diyar Altinses, M.Sc.
    Created: 2026-02-03
"""

# KI-Modelle
MODEL_GEN = "llama3.2:latest"            # Für Zusammenfassungen
MODEL_EMBED = "nomic-embed-text:latest"  # Für Vektoren

# Speicherdatei
INDEX_FILE = "search_index.json"

# App-Einstellungen
APP_TITLE = "Diyarino AI Search"
APP_SIZE = "1000x800"
APPEARANCE_MODE = "System"  # "System", "Dark", "Light"
COLOR_THEME = "blue"        # "blue", "green", "dark-blue"