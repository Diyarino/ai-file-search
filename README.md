# 🚀 AI File Search

**AI File Search** ist eine moderne, lokale Desktop-Suchmaschine für deine Dokumente. Sie nutzt künstliche Intelligenz, um Inhalte nicht nur nach Stichworten, sondern nach **Bedeutung** (semantische Suche) zu finden.

Die Anwendung läuft **zu 100% lokal** auf deinem PC. Deine Daten verlassen niemals deinen Computer.

## ✨ Features

* **Intelligente Suche:** Findet Dokumente anhand der Bedeutung, auch wenn das genaue Schlagwort nicht enthalten ist (Vektor-Suche).
* **KI-Zusammenfassungen:** Erstellt automatisch kurze Zusammenfassungen für jedes gefundene Dokument.
* **Unterstützte Formate:** PDF, Word (.docx) und Textdateien (.txt).
* **Modernes UI:** Schickes Design mit Dark/Light Mode Unterstützung (basierend auf CustomTkinter).
* **Direktzugriff:** Dateien öffnen oder direkt im Explorer anzeigen lassen.
* **Privatsphäre:** Nutzt Ollama lokal – keine Cloud, kein Internet nötig.

## 🛠️ Voraussetzungen

Bevor du startest, stelle sicher, dass folgende Software installiert ist:

1. **Python** (Version 3.10 oder neuer)
2. **Ollama**: Die KI-Engine im Hintergrund. [Hier herunterladen](https://ollama.com).

### KI-Modelle laden

Nach der Installation von Ollama musst du einmalig die benötigten Modelle herunterladen. Öffne dein Terminal (Eingabeaufforderung) und führe aus:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text

```

* `llama3.2`: Wird für die Zusammenfassungen genutzt.
* `nomic-embed-text`: Wird für die mathematische Vektor-Suche genutzt.

## 📦 Installation

1. **Repository klonen oder Dateien herunterladen:**
Stelle sicher, dass `main.py`, `config.py`, `search_backend.py` und `file_reader.py` in einem Ordner liegen.
2. **Abhängigkeiten installieren:**
Öffne das Terminal in diesem Ordner und führe aus:
```bash
pip install -r requirements.txt

```



## 🚀 Starten der App

Führe einfach die Hauptdatei aus:

```bash
python main.py

```

## 📖 Bedienungsanleitung

1. **Ordner wählen:** Klicke oben auf **"📂 Ordner wählen & Scannen"**. Wähle deinen Dokumentenordner aus.
2. **Warten:** Die App scannt nun alle Dateien (PDF/Word), liest den Text und berechnet die Vektoren. Dies passiert beim ersten Mal etwas langsamer, danach werden nur neue Dateien verarbeitet.
3. **Suchen:** Gib unten deine Suchanfrage ein (z.B. *"Rechnung Handwerker"* oder *"Projektplanung 2024"*) und drücke Enter.
4. **Ergebnisse:** Klicke auf **"📄 Öffnen"**, um das Dokument zu lesen, oder **"📂 Ordner"**, um den Speicherort im Explorer anzuzeigen.

## ⚙️ Konfiguration

Du kannst Einstellungen in der Datei `config.py` anpassen:

* **Modelle ändern:** Falls du andere Ollama-Modelle nutzen willst.
* **Design:** Ändere `COLOR_THEME` (z.B. auf "green" oder "dark-blue").
* **Fenstergröße:** Passe `APP_SIZE` an.

## 📂 Projektstruktur

Das Projekt ist sauber nach Zuständigkeiten getrennt:

* `main.py`: Das grafische Benutzerinterface (CustomTkinter).
* `search_backend.py`: Verwaltet den Index und die Kommunikation mit der KI.
* `file_reader.py`: Liest Texte aus PDF- und Word-Dateien.
* `config.py`: Zentrale Einstellungen.
* `search_index.json`: Hier wird der Such-Index (die "Datenbank") gespeichert.

## ❓ Troubleshooting

**Fehler: "Model not found"**
Stelle sicher, dass du `ollama pull ...` ausgeführt hast und die Namen in der `config.py` exakt stimmen.

**Fehler: Keine Zusammenfassung / 0% Match**
Das passiert oft bei eingescannten PDFs (Bilder). Die App benötigt Text, der markierbar ist. Für Bild-PDFs wäre eine OCR-Erweiterung nötig.

---
