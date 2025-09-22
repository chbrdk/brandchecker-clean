# 🧠 Knowledge Database Integration - GPT Embeddings & Vector Search

## 🎉 Erfolgreich implementiert!

### ✅ Knowledge Database mit GPT Embeddings
- **Vector Extensions**: PostgreSQL mit pgvector für Embeddings
- **GPT Integration**: OpenAI Embeddings und GPT-4o für Queries
- **Automatische Chunking**: Intelligente Textaufteilung
- **Vector Search**: Ähnlichkeitssuche in der Knowledge Base

## 🏗️ Knowledge Database Schema

### 📊 Haupttabellen

#### 1️⃣ `knowledge_chunks`
```sql
- id (UUID, Primary Key)
- pdf_document_id (UUID, Foreign Key)
- chunk_type (VARCHAR) -- 'text', 'color_analysis', 'font_analysis', 'layout_analysis', 'image_analysis', 'vector_analysis'
- chunk_index (INTEGER)
- content (TEXT)
- metadata (JSONB)
- embedding (vector(1536)) -- OpenAI embedding vector
- embedding_model (VARCHAR)
- embedding_created_at (TIMESTAMP)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

#### 2️⃣ `knowledge_queries`
```sql
- id (UUID, Primary Key)
- query_text (TEXT)
- query_embedding (vector(1536))
- response_text (TEXT)
- response_sources (JSONB)
- response_metadata (JSONB)
- processing_time (REAL)
- model_used (VARCHAR)
- created_at (TIMESTAMP)
```

#### 3️⃣ `knowledge_search_history`
```sql
- id (UUID, Primary Key)
- query_id (UUID, Foreign Key)
- chunk_id (UUID, Foreign Key)
- similarity_score (REAL)
- rank_position (INTEGER)
- created_at (TIMESTAMP)
```

#### 4️⃣ `knowledge_categories`
```sql
- id (UUID, Primary Key)
- name (VARCHAR)
- description (TEXT)
- parent_category_id (UUID, Foreign Key)
- created_at (TIMESTAMP)
```

## 🎯 Neue API-Endpunkte

### 📊 Knowledge Database Endpunkte

#### 1️⃣ `GET /knowledge/stats`
```bash
curl http://localhost:8000/knowledge/stats
```
**Antwort:**
```json
{
  "success": true,
  "knowledge_stats": {
    "total_chunks": 2,
    "total_queries": 0,
    "chunks_by_type": {
      "color_analysis": 2
    },
    "recent_chunks_24h": 2
  }
}
```

#### 2️⃣ `POST /knowledge/search`
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "red colors", "limit": 5, "similarity_threshold": 0.1}' \
  http://localhost:8000/knowledge/search
```
**Antwort:**
```json
{
  "success": true,
  "query": "red colors",
  "results": [
    {
      "id": "chunk-uuid",
      "chunk_type": "color_analysis",
      "content": "Design Color: Red - Hex: #ed1c24 - Corrected: #e41617 - Distance: 16.91",
      "metadata": {
        "color_hex": "#ed1c24",
        "corrected_hex": "#e41617",
        "correction_distance": 16.91
      },
      "filename": "color.pdf",
      "filepath": "/shared/color.pdf",
      "similarity_score": 0.8
    }
  ],
  "total": 2
}
```

#### 3️⃣ `POST /knowledge/query`
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "What colors are in this PDF?"}' \
  http://localhost:8000/knowledge/query
```
**Antwort:**
```json
{
  "success": true,
  "query_text": "What colors are in this PDF?",
  "response_text": "Based on the PDF analysis, this document contains several red color variants...",
  "sources": [...],
  "query_id": "query-uuid",
  "total_sources": 2
}
```

#### 4️⃣ `GET /knowledge/chunks`
```bash
curl "http://localhost:8000/knowledge/chunks?chunk_type=color_analysis&limit=10"
```
**Antwort:**
```json
{
  "success": true,
  "chunks": [
    {
      "id": "chunk-uuid",
      "chunk_type": "color_analysis",
      "chunk_index": 0,
      "content": "Design Color: Red - Hex: #ed1c24 - Corrected: #e41617 - Distance: 16.91",
      "metadata": {...},
      "filename": "color.pdf",
      "filepath": "/shared/color.pdf"
    }
  ],
  "total": 2
}
```

#### 5️⃣ `POST /knowledge/embed`
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"pdf_id": "pdf-uuid", "analysis_data": {...}}' \
  http://localhost:8000/knowledge/embed
```
**Antwort:**
```json
{
  "success": true,
  "chunks_extracted": 2,
  "chunks_saved": 2,
  "chunk_ids": ["chunk-uuid-1", "chunk-uuid-2"]
}
```

## 🔄 Automatische Knowledge Integration

### ✅ Integrierte Speicherung
Alle Analysen werden automatisch in die Knowledge Database eingebettet:

#### 📊 `extract-all-path` Endpunkt
```json
{
  "success": true,
  "filename": "color.pdf",
  "filepath": "/shared/color.pdf",
  "database_id": "pdf-uuid",
  "complete_analysis": { ... },
  "summary": {
    "total_colors": 24,
    "total_design_colors": 3,
    "processing_time": 59.13
  }
}
```

**Automatisch erstellt:**
- ✅ Knowledge Chunks aus Farbanalyse
- ✅ Knowledge Chunks aus Design-Farben
- ✅ Knowledge Chunks aus Font-Analyse
- ✅ Knowledge Chunks aus Layout-Analyse
- ✅ Knowledge Chunks aus Image-Analyse
- ✅ Knowledge Chunks aus Vector-Analyse

## 🎨 Knowledge Chunk Extraction

### 📊 Extrahierte Informationen

#### 🎨 Color Analysis Chunks
```
Content: "Color: Red - Hex: #ed1c24 - RGB: [237, 28, 36] - Usage: 1 times"
Metadata: {
  "color_hex": "#ed1c24",
  "color_rgb": [237, 28, 36],
  "usage_count": 1,
  "color_space": "rgb"
}
```

#### 🎨 Design Color Chunks
```
Content: "Design Color: Red - Hex: #ed1c24 - Corrected: #e41617 - Distance: 16.91"
Metadata: {
  "color_hex": "#ed1c24",
  "corrected_hex": "#e41617",
  "correction_distance": 16.91,
  "color_space": "rgb"
}
```

#### 🔤 Font Analysis Chunks
```
Content: "Font: Arial - Size: 12pt - Style: bold - Usage: 5 times"
Metadata: {
  "font_name": "Arial",
  "font_size": "12pt",
  "font_style": "bold",
  "usage_count": 5
}
```

#### 📐 Layout Analysis Chunks
```
Content: "Layout: 1 pages - Width: 595.276 - Height: 841.890 - Aspect Ratio: 0.707"
Metadata: {
  "total_pages": 1,
  "avg_width": 595.276,
  "avg_height": 841.890,
  "avg_aspect_ratio": 0.707
}
```

## 🔍 Vector Search & GPT Integration

### 🎯 Ähnlichkeitssuche
- **Cosine Similarity**: Vector-basierte Ähnlichkeitssuche
- **Threshold-basiert**: Konfigurierbare Ähnlichkeitsschwelle
- **Ranking**: Sortierung nach Ähnlichkeitsscore

### 🤖 GPT-Integration
- **Context-Aware**: Verwendet relevante Chunks als Kontext
- **Structured Responses**: Formatierte Antworten basierend auf PDF-Analyse
- **Source Tracking**: Verfolgung der verwendeten Quellen

### 📊 Beispiel GPT Query
```bash
# Query: "What colors are in this PDF?"
# Response: "Based on the PDF analysis, this document contains several red color variants:
# - Primary red: #ed1c24 (RGB: 237, 28, 36)
# - Corrected red: #e41617 (with correction distance: 16.91)
# These colors are used in design elements and appear to be brand colors."
```

## 🚀 Vorteile der Knowledge Database

### ✅ Vorteile:
1. **Intelligente Suche**: Vector-basierte Ähnlichkeitssuche
2. **GPT-Integration**: KI-gestützte Fragen und Antworten
3. **Automatische Chunking**: Intelligente Textaufteilung
4. **Persistente Speicherung**: Dauerhafte Knowledge Base
5. **Erweiterte Abfragen**: Natürlichsprachige Fragen
6. **Source Tracking**: Verfolgung der Informationsquellen

### 🔧 Technische Features:
- **Vector Extensions**: PostgreSQL pgvector für Embeddings
- **OpenAI Integration**: Embeddings und GPT-4o
- **Automatic Chunking**: Intelligente Textaufteilung
- **Similarity Search**: Cosine-basierte Ähnlichkeitssuche
- **Context-Aware**: Kontextbewusste GPT-Antworten
- **Metadata Storage**: Flexible JSONB-Metadaten

## 📈 Monitoring und Statistiken

### 📊 Verfügbare Statistiken
- **Gesamte Chunks**: Anzahl aller Knowledge Chunks
- **Gesamte Queries**: Anzahl aller GPT-Queries
- **Chunks nach Typ**: Verteilung nach Chunk-Typen
- **24h Aktivität**: Neue Chunks in den letzten 24 Stunden

### 🔍 Abfragen
```bash
# Knowledge Stats
curl http://localhost:8000/knowledge/stats

# Knowledge Search
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "red colors", "limit": 5}' \
  http://localhost:8000/knowledge/search

# GPT Query
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "What colors are in this PDF?"}' \
  http://localhost:8000/knowledge/query
```

## 🎯 N8N Integration

### 🔧 Knowledge Database Endpunkte in n8n
```javascript
// Knowledge Stats
{
  "url": "http://brandchecker-python:8000/knowledge/stats",
  "method": "GET"
}

// Knowledge Search
{
  "url": "http://brandchecker-python:8000/knowledge/search",
  "method": "POST",
  "contentType": "application/json",
  "body": {
    "query": "red colors",
    "limit": 5,
    "similarity_threshold": 0.1
  }
}

// GPT Query
{
  "url": "http://brandchecker-python:8000/knowledge/query",
  "method": "POST",
  "contentType": "application/json",
  "body": {
    "query": "What colors are in this PDF?"
  }
}
```

## 🔄 Migration und Backup

### 📁 Knowledge Database Backup
```bash
# Backup erstellen
docker-compose exec brandchecker-postgres pg_dump -U brandchecker_user brandchecker > backup_with_knowledge.sql

# Backup wiederherstellen
docker-compose exec -T brandchecker-postgres psql -U brandchecker_user brandchecker < backup_with_knowledge.sql
```

### 🔄 Volume-Persistenz
```yaml
volumes:
  brandchecker_postgres_data:
    driver: local
```

## 🎉 Fazit

Die **Knowledge Database Integration** ist vollständig implementiert und funktionsfähig!

**Schlüssel-Features:**
- ✅ Vector-basierte Ähnlichkeitssuche
- ✅ GPT-Integration für intelligente Queries
- ✅ Automatische Knowledge Chunk Extraction
- ✅ Persistente Knowledge Base
- ✅ Erweiterte Suchfunktionen
- ✅ N8N-Integration bereit
- ✅ Backup und Monitoring

**Perfekt für intelligente PDF-Analysen!** 🧠🎨
