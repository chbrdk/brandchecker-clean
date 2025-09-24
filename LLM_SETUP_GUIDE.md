# 🧠 Brand Guidelines LLM Integration Setup Guide

## 🎯 Übersicht

Dieses System integriert die neuesten OpenAI-Modelle (GPT-5, text-embedding-3-large) für semantische Suche und automatische Compliance-Prüfung von Brand Guidelines.

## 🚀 Schnellstart

### 1. OpenAI API Key einrichten

```bash
# API Key setzen
export OPENAI_API_KEY="your-openai-api-key-here"

# Oder in .env Datei (falls erstellt)
echo "OPENAI_API_KEY=your-openai-api-key-here" >> .env
```

### 2. Services starten

```bash
# Alle Services starten
docker-compose up -d

# Status überprüfen
docker-compose ps
```

### 3. Datenbank-Schema aktualisieren

```bash
# Neues Schema mit 3072-dimensionalen Embeddings
docker-compose exec brandchecker-postgres psql -U brandchecker_user -d brandchecker -f /docker-entrypoint-initdb.d/02_brand_guidelines_schema.sql
```

### 4. Brand Guidelines importieren

```bash
# JSON-Daten importieren
docker-compose exec brandchecker-python python /app/brand_guidelines_importer.py
```

### 5. Embeddings generieren

```bash
# OpenAI Embeddings erstellen (kann einige Minuten dauern)
docker-compose exec llm-api-service python /app/embedding_service.py
```

### 6. Indexes optimieren

```bash
# Vector-Indexes für beste Performance optimieren
docker-compose exec brandchecker-python python /app/optimize_indexes.py
```

### 7. System testen

```bash
# Vollständigen Test durchführen
python test_llm_system.py
```

## 📊 Modelle & Konfiguration

### Aktuelle Modelle (neueste verfügbare)

| Komponente | Primäres Modell | Fallback-Modell | Dimensionen |
|------------|----------------|-----------------|-------------|
| **Embeddings** | `text-embedding-3-large` | `text-embedding-3-small` | 3072 |
| **LLM** | `gpt-5` | `gpt-4o` | - |

### Warum diese Modelle?

- **text-embedding-3-large**: Beste Performance für semantische Suche, bis zu 3072 Dimensionen
- **gpt-5**: Neuestes und leistungsstärkstes Modell (August 2025), 400k Token Kontext
- **Fallback-System**: Automatische Nutzung älterer Modelle falls neue nicht verfügbar

## 🔧 API Endpoints

### LLM API Service (Port 8001)

| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/health` | GET | Service-Status |
| `/api/brands` | GET | Alle verfügbaren Brands |
| `/api/search` | POST | Semantische Suche |
| `/api/ask` | POST | LLM-Fragen & Antworten |
| `/api/compliance/check` | POST | Compliance-Prüfung |
| `/api/embeddings/status` | GET | Embedding-Status |
| `/api/embeddings/generate` | POST | Embeddings generieren |

### Beispiel-Requests

#### Semantische Suche
```bash
curl -X POST http://localhost:8001/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Welche Farben sind für Bosch Corporate erlaubt?",
    "brand_id": "8a9239a4-18f6-4aca-b9fe-08426bd01825",
    "limit": 5
  }'
```

#### LLM-Frage
```bash
curl -X POST http://localhost:8001/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Welche Schriftarten darf ich für Bosch verwenden?",
    "brand_id": "8a9239a4-18f6-4aca-b9fe-08426bd01825"
  }'
```

#### Compliance-Prüfung
```bash
curl -X POST http://localhost:8001/api/compliance/check \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Ich verwende die Farbe #FF0000 für mein Bosch-Logo.",
    "brand_id": "8a9239a4-18f6-4aca-b9fe-08426bd01825",
    "check_type": "colors"
  }'
```

## 🗄️ Datenbankstruktur

### Optimierte Vector-Indexes

- **ivfflat Index**: Für schnelle Cosine-Similarity-Suche
- **Optimierte Parameter**: Automatische Berechnung basierend auf Datenmenge
- **Composite Indexes**: Für brand-spezifische Abfragen
- **Materialized Views**: Für Performance-Optimierung

### Embedding-Tabellen

```sql
-- Brand Knowledge Chunks (3072 Dimensionen)
brand_knowledge_chunks (
    id UUID,
    brand_id UUID,
    chunk_type VARCHAR(50),
    content TEXT,
    embedding vector(3072),
    embedding_model VARCHAR(50),
    metadata JSONB
)

-- Knowledge Queries
knowledge_queries (
    id UUID,
    query_text TEXT,
    query_embedding vector(3072),
    response_text TEXT
)
```

## 🔍 Use Cases

### 1. Semantische Suche
- **Frage**: "Welche Farben sind für Bosch erlaubt?"
- **System**: Findet relevante Brand-Guidelines automatisch
- **Antwort**: Konkrete Farbangaben mit HEX-Codes und Verwendungsregeln

### 2. Compliance-Checking
- **Input**: PDF-Dokument oder Text-Inhalt
- **System**: Prüft automatisch gegen Brand-Standards
- **Output**: Compliance-Score und spezifische Empfehlungen

### 3. Asset-Empfehlungen
- **Kontext**: "Ich brauche ein Logo für Social Media"
- **System**: Empfiehlt passende Assets basierend auf Guidelines
- **Output**: Spezifische Asset-URLs und Verwendungsregeln

### 4. Brand-Guideline Q&A
- **Frage**: "Darf ich das Bosch-Logo in schwarz-weiß verwenden?"
- **System**: Durchsucht Guidelines und gibt präzise Antwort
- **Output**: Ja/Nein mit Begründung und Verweisen

## ⚡ Performance-Optimierungen

### Vector-Index-Optimierung
```bash
# Indexes mit optimalen Parametern erstellen
python optimize_indexes.py
```

### Automatische Fallbacks
- **GPT-5 nicht verfügbar** → Automatischer Wechsel zu GPT-4o
- **text-embedding-3-large nicht verfügbar** → Fallback zu text-embedding-3-small
- **Rate-Limiting** → Automatische Verzögerungen und Batch-Verarbeitung

### Caching-Strategien
- **Embedding-Cache**: Bereits generierte Embeddings werden wiederverwendet
- **Materialized Views**: Häufige Abfragen werden vorberechnet
- **Connection Pooling**: Optimierte Datenbankverbindungen

## 🔧 Troubleshooting

### Häufige Probleme

#### 1. OpenAI API Key nicht gesetzt
```bash
# Fehler: "OPENAI_API_KEY environment variable is required"
export OPENAI_API_KEY="your-key-here"
docker-compose restart llm-api-service
```

#### 2. GPT-5 nicht verfügbar
```bash
# System nutzt automatisch GPT-4o als Fallback
# Logs zeigen: "Model gpt-5 not available, trying fallback..."
```

#### 3. Embeddings nicht generiert
```bash
# Embeddings manuell generieren
docker-compose exec llm-api-service python /app/embedding_service.py
```

#### 4. Langsame Performance
```bash
# Indexes optimieren
docker-compose exec brandchecker-python python /app/optimize_indexes.py
```

### Logs überprüfen

```bash
# LLM API Service Logs
docker-compose logs llm-api-service

# Embedding Service Logs
docker-compose logs brandchecker-python

# PostgreSQL Logs
docker-compose logs brandchecker-postgres
```

## 📈 Monitoring

### Embedding-Status überprüfen
```bash
curl http://localhost:8001/api/embeddings/status
```

### Performance-Metriken
- **Embedding-Coverage**: Prozentsatz der indexierten Inhalte
- **Search-Latency**: Zeit für semantische Suche
- **LLM-Response-Time**: Zeit für AI-Antworten
- **Index-Performance**: Vector-Index-Effizienz

## 🚀 Nächste Schritte

1. **n8n Integration**: LLM-API in n8n-Workflows einbinden
2. **PDF-Integration**: Automatische Compliance-Prüfung von PDF-Dokumenten
3. **Real-time Updates**: Automatische Embedding-Updates bei neuen Guidelines
4. **Multi-Brand Support**: Erweiterung für mehrere Brand-Guidelines
5. **Advanced Analytics**: Detaillierte Compliance-Reports und Trends

## 💡 Tipps

- **Batch-Processing**: Embeddings in kleinen Batches generieren für bessere Stabilität
- **Rate-Limiting**: OpenAI API-Limits beachten (60 Requests/Minute für Embeddings)
- **Backup**: Regelmäßige Backups der Embedding-Daten
- **Updates**: System regelmäßig auf neue Modelle aktualisieren

---

**🎉 Ihr Brand Guidelines LLM-System ist jetzt bereit für den produktiven Einsatz!**
