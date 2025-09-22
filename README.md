# 🎨 BrandChecker - AI-Powered Brand Analysis System

Ein umfassendes Docker-basiertes System für automatisierte Brand-Analyse mit KI-gestützter PDF-Verarbeitung, Farb- und Font-Erkennung sowie Logo-Detection.

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-green?logo=python)](https://python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue?logo=postgresql)](https://postgresql.org/)
[![N8N](https://img.shields.io/badge/N8N-Workflow-orange?logo=n8n)](https://n8n.io/)

## 🚀 Features

- **🤖 KI-gestützte PDF-Analyse** mit automatischer Text-, Font- und Farbextraktion
- **🎯 Intelligente Logo-Erkennung** mit Vector-basierter Ähnlichkeitssuche
- **📊 Umfassende Brand-Analyse** mit Layout- und Design-Bewertung
- **🔄 N8N Workflow-Integration** für automatisierte Prozesse
- **🗄️ PostgreSQL Datenbank** mit Vector Embeddings für semantische Suche
- **📈 Automatische Report-Generierung** mit visuellen Analysen

## Services

### n8n Service
- **Port**: 5680 (extern) -> 5678 (intern)
- **Login**: admin / brandchecker123
- **URL**: http://localhost:5680

### Python Service
- **Port**: 8000
- **Features**: PDF Text-Extraktion mit pdfminer.six
- **URL**: http://localhost:8000

## Installation und Start

```bash
# Container starten
docker-compose up -d

# Logs anzeigen
docker-compose logs -f

# Container stoppen
docker-compose down
```

## Python API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### PDF Text Extraktion
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/extract-text
```

### Erweiterte PDF Text Extraktion
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/extract-text-advanced
```

### PDF Font Extraktion
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/extract-fonts
```

### PDF Farben Extraktion
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/extract-colors
```

### PDF Bilder Extraktion
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/extract-images
```

### PDF Layout Analyse
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/extract-layout
```

### PDF Metadaten Extraktion
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/extract-metadata
```

### Komplette PDF Analyse
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/analyze-complete
```

### Service Information
```bash
curl http://localhost:8000/info
```

## Verzeichnisstruktur

```
brandchecker/
├── docker-compose.yml
├── python_app/
│   └── app.py
├── requirements.txt
├── shared/          # Gemeinsamer Ordner für beide Services
└── README.md
```

## Hinweise

- Der n8n Service läuft auf Port 5680 um Konflikte mit der bestehenden n8n Instanz auf Port 5678 zu vermeiden
- Beide Services teilen sich das `shared` Verzeichnis für Datenaustausch
- PDF-Dateien werden temporär verarbeitet und automatisch gelöscht

## ⚠️ WICHTIG für n8n Workflows:

**Verwende IMMER den Container-Namen statt localhost:**

**❌ Falsch:** `http://localhost:8000/extract-fonts`
**✅ Richtig:** `http://brandchecker-python:8000/extract-fonts`

Siehe `N8N_SETUP_GUIDE.md` für detaillierte Anweisungen.

## 🏗️ Architektur

Das System besteht aus mehreren Microservices:

- **🐍 Python App** - Hauptanwendung mit KI-Analysen
- **🎨 Color Profile Service** - Farbanalyse und -extraktion
- **🔤 Font Profile Service** - Font-Erkennung und -analyse
- **🖼️ Image Profile Service** - Bildverarbeitung und Logo-Detection
- **📄 PDF Measure Service** - PDF-Layout und -Messungen
- **🗄️ PostgreSQL** - Datenbank mit Vector Embeddings
- **🔄 N8N** - Workflow-Automatisierung

## 📋 Voraussetzungen

- Docker & Docker Compose
- Python 3.9+
- PostgreSQL 15+
- N8N (optional)

## 🚀 Quick Start

```bash
# Repository klonen
git clone https://github.com/CHBRDK/brandchecker.git
cd brandchecker

# Umgebungsvariablen setzen (optional)
export OPENAI_API_KEY="your_openai_api_key_here"

# Services starten
docker-compose up -d

# Status prüfen
docker-compose ps
```

### 🔑 Umgebungsvariablen

Erstelle eine `.env` Datei oder setze die folgenden Variablen:

```bash
# OpenAI API Key (für KI-Features)
OPENAI_API_KEY=your_openai_api_key_here

# PostgreSQL Konfiguration (optional, Standardwerte vorhanden)
POSTGRES_DB=brandchecker
POSTGRES_USER=brandchecker_user
POSTGRES_PASSWORD=brandchecker_password
```

## 📚 Dokumentation

- [N8N Setup Guide](N8N_SETUP_GUIDE.md) - N8N Integration
- [Knowledge Database Integration](KNOWLEDGE_DATABASE_INTEGRATION.md) - KI-Datenbank
- [PostgreSQL Integration](POSTGRES_INTEGRATION.md) - Datenbank Setup
- [N8N Workflow Tutorial](N8N_WORKFLOW_TUTORIAL.md) - Workflow-Erstellung

## 🤝 Contributing

1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Committe deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne eine Pull Request

## 📄 Lizenz

Dieses Projekt steht unter der MIT Lizenz. Siehe `LICENSE` für Details.

## 🆘 Support

Bei Fragen oder Problemen:
- Erstelle ein [Issue](https://github.com/CHBRDK/brandchecker/issues)
- Kontaktiere das Entwicklungsteam

---

⭐ **Star dieses Repository, wenn es dir gefällt!** 