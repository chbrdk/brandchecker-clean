# 🎨 BrandChecker - AI-Powered Brand Analysis System

Ein umfassendes Docker-basiertes System für automatisierte Brand-Analyse mit KI-gestützter PDF-Verarbeitung, Farb- und Font-Erkennung sowie Logo-Detection. **Jetzt mit integrierter LLM-Funktionalität für intelligente Brand-Guideline-Befragung!**

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-green?logo=python)](https://python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue?logo=postgresql)](https://postgresql.org/)
[![N8N](https://img.shields.io/badge/N8N-Workflow-orange?logo=n8n)](https://n8n.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green?logo=openai)](https://openai.com/)

## 🚀 Features

- **🤖 KI-gestützte PDF-Analyse** mit automatischer Text-, Font- und Farbextraktion
- **🎯 Intelligente Logo-Erkennung** mit Vector-basierter Ähnlichkeitssuche
- **📊 Umfassende Brand-Analyse** mit Layout- und Design-Bewertung
- **🔄 N8N Workflow-Integration** für automatisierte Prozesse
- **🗄️ PostgreSQL Datenbank** mit Vector Embeddings für semantische Suche
- **📈 Automatische Report-Generierung** mit visuellen Analysen
- **🧠 LLM-Integration** mit GPT-5 für intelligente Brand-Guideline-Befragung
- **🔍 Semantische Suche** in Brand Guidelines mit OpenAI Embeddings
- **💬 Chat-Interface** für natürliche Sprachinteraktion mit Brand-Daten
- **🎨 Farb-Ähnlichkeits-Bewertung** mit HSV-basierten Algorithmen für intelligente Farb-Matching
- **📊 Brand-Compliance-Analyzer** für automatische Konformitätsbewertung
- **⚡ Streaming-Unterstützung** für Echtzeit-Antworten in n8n Workflows
- **🖼️ Bildanalyse** mit GPT-4o Vision für Icons, Logos und Grafiken
- **📐 SVG-Unterstützung** mit automatischer PNG-Konvertierung
- **🎯 Icon-Klassifizierung** mit detaillierter Beschreibung und Brand-Compliance

## Services

### n8n Service
- **Port**: 5680 (extern) -> 5678 (intern)
- **Login**: admin / brandchecker123
- **URL**: http://localhost:5680

### Python Service
- **Port**: 8000
- **Features**: PDF Text-Extraktion mit pdfminer.six
- **URL**: http://localhost:8000

### LLM API Service (NEU!)
- **Port**: 8001
- **Features**: KI-gestützte Brand-Guideline-Befragung mit GPT-5
- **URL**: http://localhost:8001
- **Endpoints**: `/api/ask`, `/api/search`, `/api/embeddings/generate`
- **Streaming**: Unterstützt Echtzeit-Antworten für n8n Integration
- **Farb-Ähnlichkeits**: HSV-basierte Farb-Matching-Algorithmen

### Image API Service (NEU!)
- **Port**: 8002
- **Features**: Bildanalyse mit GPT-4o Vision für Icons, Logos und Grafiken
- **URL**: http://localhost:8002
- **Endpoints**: `/api/analyze-image`
- **SVG-Support**: Automatische Konvertierung von SVG zu PNG
- **Brand Compliance**: Automatische Bewertung von Brand Guide Bildern (100/100)

### PostgreSQL mit pgvector
- **Port**: 5433
- **Features**: Vector Embeddings für semantische Suche
- **pgvector**: Für effiziente Ähnlichkeitssuche in Brand Guidelines

## Installation und Start

```bash
# 1. OpenAI API Key setzen (erforderlich für LLM-Features)
export OPENAI_API_KEY="your_openai_api_key_here"

# 2. Container starten
docker-compose up -d

# 3. Logs anzeigen
docker-compose logs -f

# 4. Container stoppen
docker-compose down
```

### 🔑 Erforderliche Umgebungsvariablen

Für die LLM-Funktionalität benötigen Sie einen OpenAI API Key:

```bash
# .env Datei erstellen oder Umgebungsvariable setzen
OPENAI_API_KEY=sk-proj-your-key-here
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

## 🧠 LLM API Endpoints (NEU!)

### Brand-Guideline-Befragung
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"question": "Welche Farben sind für Bosch erlaubt?", "brand_id": "brand-uuid"}' \
  http://localhost:8001/api/ask
```

### Semantische Suche
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "Bosch Farben", "brand_id": "brand-uuid"}' \
  http://localhost:8001/api/search
```

### Embeddings generieren
```bash
curl -X POST http://localhost:8001/api/embeddings/generate
```

### Brand-Informationen abrufen
```bash
curl http://localhost:8001/api/brands
curl http://localhost:8001/api/brands/{brand_id}/assets
curl http://localhost:8001/api/brands/{brand_id}/guidelines
```

### Streaming-Antworten (NEU!)
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"question": "Welche Farben sind für Bosch erlaubt?", "brand_id": "brand-uuid", "stream": true}' \
  http://localhost:8001/api/ask
```

## 🎨 Erweiterte Brand-Analyse Features (NEU!)

### Farb-Ähnlichkeits-Bewertung
Das System kann jetzt Farben basierend auf HSV-Ähnlichkeits-Algorithmen bewerten:

```python
# Beispiel: Ähnlichkeit zwischen Farben berechnen
similarity = analyzer.color_similarity("#007bc0", "#0088cc")  # 99.3% Ähnlichkeit
best_match = analyzer.find_best_color_match("#0088cc")  # Findet Bosch Blau 50
```

### Brand-Compliance-Analyzer
Automatische Konformitätsbewertung für PDF-Dokumente:

```python
from brand_compliance_analyzer import BrandComplianceAnalyzer

analyzer = BrandComplianceAnalyzer()
result = analyzer.analyze_compliance(analysis_data)

# Ergebnis enthält:
# - Farb-Compliance mit Ähnlichkeits-Bewertung
# - Font-Compliance
# - Gesamtbewertung (0-100 Punkte)
# - Konkrete Empfehlungen
```

### n8n Integration mit Streaming
Für n8n Workflows mit Echtzeit-Antworten:

```json
{
  "toolDescription": "Bosch Brand Guidelines mit Streaming",
  "method": "POST",
  "url": "http://brandchecker-llm-api:8001/api/ask",
  "bodyParameters": {
    "question": "{{ $json.question }}",
    "brand_id": "9a933c7f-bd87-400f-b13a-b3bce7c822d8",
    "stream": true
  }
}
```

## Verzeichnisstruktur

```
brandchecker/
├── docker-compose.yml
├── python_app/
│   ├── app.py
│   ├── llm_api.py              # LLM API Service
│   ├── embedding_service.py    # OpenAI Embedding Service
│   ├── brand_guidelines_importer.py
│   ├── optimize_indexes.py     # Vector Index Optimierung
│   ├── brand_compliance_analyzer.py  # Brand-Compliance-Analyzer (NEU!)
│   ├── optimize_brand_data.py  # Daten-Optimierung (NEU!)
│   ├── import_optimized_data.py  # Optimierte Daten-Import (NEU!)
│   ├── reindex_optimized_data.py  # Master-Reindexierung (NEU!)
│   └── simple_optimize.py    # Einfache Daten-Optimierung (NEU!)
├── postgres_init/
│   ├── 01_init_database.sql
│   └── 02_brand_guidelines_schema.sql
├── shared/
│   ├── JSON/
│   │   ├── graphql.json        # Brand Guidelines Daten
│   │   └── html.json
│   ├── images/
│   ├── logos/
│   └── reports/
├── test_llm_system.py          # LLM System Test
├── LLM_SETUP_GUIDE.md          # Setup Anleitung
├── requirements.txt
└── README.md
```

## Hinweise

- Der n8n Service läuft auf Port 5680 um Konflikte mit der bestehenden n8n Instanz auf Port 5678 zu vermeiden
- Alle Services teilen sich das `shared` Verzeichnis für Datenaustausch
- PDF-Dateien werden temporär verarbeitet und automatisch gelöscht
- **LLM-Features erfordern einen gültigen OpenAI API Key**
- Brand Guidelines werden automatisch in die Datenbank importiert und mit Embeddings versehen
- **Farb-Ähnlichkeits-Bewertung** nutzt HSV-Algorithmen für präzise Farb-Matching
- **Streaming-Unterstützung** ermöglicht Echtzeit-Antworten in n8n Workflows
- **Brand-Compliance-Analyzer** bietet automatische Konformitätsbewertung mit 0-100 Punkte-System
- Vector-Indexes werden automatisch optimiert für optimale Suchperformance

## ⚠️ WICHTIG für n8n Workflows:

**Verwende IMMER den Container-Namen statt localhost:**

**❌ Falsch:** `http://localhost:8000/extract-fonts`
**✅ Richtig:** `http://brandchecker-python:8000/extract-fonts`

**❌ Falsch:** `http://localhost:8001/api/ask`
**✅ Richtig:** `http://brandchecker-llm-api:8001/api/ask`

Siehe `N8N_SETUP_GUIDE.md` für detaillierte Anweisungen.

## 🏗️ Architektur

Das System besteht aus mehreren Microservices:

- **🐍 Python App** - Hauptanwendung mit KI-Analysen
- **🧠 LLM API Service** - KI-gestützte Brand-Guideline-Befragung mit GPT-4o
- **🎨 Color Profile Service** - Farbanalyse und -extraktion
- **🔤 Font Profile Service** - Font-Erkennung und -analyse
- **🖼️ Image Profile Service** - Bildverarbeitung und Logo-Detection
- **📄 PDF Measure Service** - PDF-Layout und -Messungen
- **🗄️ PostgreSQL mit pgvector** - Datenbank mit Vector Embeddings für semantische Suche
- **🔄 N8N** - Workflow-Automatisierung

## 📋 Voraussetzungen

- Docker & Docker Compose
- Python 3.9+
- PostgreSQL 15+ mit pgvector Extension
- OpenAI API Key (für LLM-Features)
- N8N (optional)

## 🚀 Quick Start

```bash
# Repository klonen
git clone https://github.com/CHBRDK/brandchecker.git
cd brandchecker

# OpenAI API Key setzen (ERFORDERLICH für LLM-Features)
export OPENAI_API_KEY="your_openai_api_key_here"

# Services starten
docker-compose up -d

# Status prüfen
docker-compose ps

# LLM-System testen
python3 test_llm_system.py
```

### 🔑 Umgebungsvariablen

Erstelle eine `.env` Datei oder setze die folgenden Variablen:

```bash
# OpenAI API Key (ERFORDERLICH für LLM-Features)
OPENAI_API_KEY=your_openai_api_key_here

# LLM Model Konfiguration (optional, Standardwerte vorhanden)
EMBEDDING_MODEL=text-embedding-3-large
LLM_MODEL=gpt-5
EMBEDDING_DIMENSIONS=3072
FALLBACK_EMBEDDING_MODEL=text-embedding-3-small
FALLBACK_LLM_MODEL=gpt-4o

# PostgreSQL Konfiguration (optional, Standardwerte vorhanden)
POSTGRES_DB=brandchecker
POSTGRES_USER=brandchecker_user
POSTGRES_PASSWORD=brandchecker_password
```

## 📚 Dokumentation

- **[LLM Setup Guide](LLM_SETUP_GUIDE.md)** - 🆕 Vollständige Anleitung für LLM-Integration
- [N8N Setup Guide](N8N_SETUP_GUIDE.md) - N8N Integration
- [Knowledge Database Integration](KNOWLEDGE_DATABASE_INTEGRATION.md) - KI-Datenbank
- [PostgreSQL Integration](POSTGRES_INTEGRATION.md) - Datenbank Setup
- [N8N Workflow Tutorial](N8N_WORKFLOW_TUTORIAL.md) - Workflow-Erstellung

### 🧠 LLM-Features im Detail

Das System bietet jetzt erweiterte KI-Funktionalitäten:

1. **Semantische Suche** - Finde relevante Brand Guidelines mit natürlicher Sprache
2. **Intelligente Befragung** - Stelle Fragen zu Brand Guidelines und erhalte kontextuelle Antworten
3. **Vector Embeddings** - Effiziente Ähnlichkeitssuche in großen Textmengen
4. **Automatische Compliance-Checks** - Überprüfe Dokumente gegen Brand Guidelines
5. **N8N Integration** - Nutze LLM-Features in Workflows

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