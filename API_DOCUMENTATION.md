# 🚀 Brandchecker API Dokumentation

## 📋 Übersicht

Das Brandchecker-System bietet drei Hauptservices mit verschiedenen Endpunkten für PDF-Analyse, Brand-Compliance und LLM-Integration.

### Services
- **PDF-Analyzer**: Port 8000 - Vollständige PDF-Analyse und Logo-Erkennung
- **LLM-API**: Port 8001 - Semantische Suche und Brand-Compliance
- **Image-API**: Port 8002 - Bildanalyse mit GPT-4o Vision
- **PostgreSQL**: Port 5433 - Datenbank mit pgvector für Embeddings

---

## 🔍 PDF-Analyzer Service (Port 8000)

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "brandchecker-pdf-analyzer",
  "timestamp": "2025-09-24T09:30:00Z"
}
```

---

### Vollständige PDF-Analyse

#### Upload-basierte Analyse
```http
POST /extract-all
Content-Type: multipart/form-data
```

**Request Body:**
- `file`: PDF-Datei (multipart/form-data)

**Response:**
```json
{
  "success": true,
  "filename": "document.pdf",
  "complete_analysis": {
    "colors": [
      {
        "hex": "#007bc0",
        "rgb": "RGB(0, 123, 192)",
        "cmyk": "CMYK(100, 36, 0, 25)",
        "name": "Bosch Blau 50",
        "usage_percentage": 45.2
      }
    ],
    "fonts": [
      {
        "name": "BoschSans-Regular",
        "usage_percentage": 47.17
      }
    ],
    "layout": {
      "pages": 1,
      "regions": ["header", "content", "footer"]
    },
    "images": [
      {
        "type": "logo",
        "confidence": 0.95,
        "position": "top-left"
      }
    ],
    "vectors": []
  },
  "summary": {
    "total_colors": 5,
    "total_fonts": 3,
    "logo_detected": true,
    "brand_compliance_score": 85
  }
}
```

#### Pfad-basierte Analyse (für n8n)
```http
POST /extract-all-path
Content-Type: application/json
```

**Request Body:**
```json
{
  "filepath": "/shared/testfile1.pdf"
}
```

**Response:** Identisch mit `/extract-all`

---

### Einzelne Analysen

#### Farb-Analyse
```http
POST /extract-colors
Content-Type: multipart/form-data
```

**Request Body:**
- `file`: PDF-Datei

**Response:**
```json
{
  "success": true,
  "colors": [
    {
      "hex": "#007bc0",
      "rgb": "RGB(0, 123, 192)",
      "cmyk": "CMYK(100, 36, 0, 25)",
      "name": "Bosch Blau 50",
      "usage_percentage": 45.2,
      "pages": [1, 2, 3]
    }
  ],
  "summary": {
    "total_colors": 5,
    "bosch_colors_found": 3,
    "compliance_score": 85
  }
}
```

#### Font-Analyse
```http
POST /extract-fonts
Content-Type: multipart/form-data
```

**Response:**
```json
{
  "success": true,
  "fonts": [
    {
      "name": "BoschSans-Regular",
      "usage_percentage": 47.17,
      "size_range": "12-24pt",
      "pages": [1, 2]
    }
  ],
  "summary": {
    "total_fonts": 3,
    "bosch_fonts_found": 2,
    "compliance_score": 90
  }
}
```

#### Layout-Analyse
```http
POST /extract-layout
Content-Type: multipart/form-data
```

**Response:**
```json
{
  "success": true,
  "layout": {
    "pages": 1,
    "regions": [
      {
        "type": "header",
        "bbox": [0, 0, 595, 100],
        "confidence": 0.95
      }
    ],
    "structure": "single-column"
  }
}
```

#### Bild-Analyse
```http
POST /extract-images
Content-Type: multipart/form-data
```

**Response:**
```json
{
  "success": true,
  "images": [
    {
      "type": "logo",
      "confidence": 0.95,
      "position": "top-left",
      "bbox": [50, 50, 150, 100],
      "file_size": 1024
    }
  ],
  "summary": {
    "total_images": 3,
    "logos_detected": 1,
    "compliance_score": 85
  }
}
```

#### Vector-Analyse
```http
POST /extract-vectors
Content-Type: multipart/form-data
```

**Response:**
```json
{
  "success": true,
  "vectors": [
    {
      "type": "path",
      "complexity": "medium",
      "elements": 15
    }
  ]
}
```

---

### Logo-Erkennung

#### Custom Logo Detection
```http
POST /custom-logo-detection
Content-Type: multipart/form-data
```

**Request Body:**
- `file`: PDF-Datei
- `logo_template`: (optional) Logo-Template

**Response:**
```json
{
  "success": true,
  "logos_detected": [
    {
      "type": "bosch_logo",
      "confidence": 0.95,
      "position": "top-left",
      "bbox": [50, 50, 150, 100],
      "quality": "high"
    }
  ],
  "summary": {
    "total_logos": 1,
    "brand_compliance": true
  }
}
```

#### Intelligent Logo Detection
```http
POST /intelligent-logo-detection
Content-Type: multipart/form-data
```

**Response:** Erweiterte Logo-Erkennung mit AI

#### Global Graphic Detection
```http
POST /global-graphic-detection
Content-Type: multipart/form-data
```

**Response:** Globale Grafik-Erkennung

---

### Berichte generieren

#### Visual Report
```http
POST /generate-visual-report
Content-Type: multipart/form-data
```

**Response:**
```json
{
  "success": true,
  "report_url": "/download-report/visual_report_20250924_093000.pdf",
  "filename": "visual_report_20250924_093000.pdf"
}
```

#### Detailed Report
```http
POST /generate-detailed-report
Content-Type: multipart/form-data
```

**Response:**
```json
{
  "success": true,
  "report_url": "/download-report/detailed_report_20250924_093000.pdf",
  "filename": "detailed_report_20250924_093000.pdf"
}
```

#### AI Visual Report
```http
POST /generate-ai-visual-report
Content-Type: multipart/form-data
```

**Response:** AI-generierter visueller Bericht

---

## 🖼️ Image-API Service (Port 8002)

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "image-api-service",
  "timestamp": "2025-09-24T09:30:00Z"
}
```

---

### Bildanalyse mit GPT-4o Vision

#### Einzelbild-Analyse
```http
POST /api/analyze-image
Content-Type: application/json
```

**Request Body:**
```json
{
  "image_url": "https://example.com/image.jpg",
  "brand_id": "9a933c7f-bd87-400f-b13a-b3bce7c822d8"
}
```

**Response:**
```json
{
  "analysis": {
    "detailed_description": {
      "objects": ["Icon", "Arrow", "Text"],
      "text": ["Search", "Find"],
      "visual_elements": ["Bosch logo", "Color blocks"]
    },
    "brand_elements": {
      "logo_detection": {
        "present": true,
        "type": "Bosch wordmark",
        "color": "Red",
        "position": "Top left"
      },
      "colors_used": ["#007bc0", "#ed0007", "#71767c"],
      "typography": {
        "font_family": "Bosch Sans",
        "sizes": "Medium to Large",
        "styles": "Bold, Regular"
      }
    },
    "asset_type": "Icon",
    "brand_compliance_score": 100,
    "technical_analysis": {
      "quality": "High",
      "style": "Modern and clean",
      "professional_appearance": "Yes"
    }
  },
  "compliance_score": 100,
  "logo_detected": true,
  "model_used": "gpt-4o",
  "status": "success",
  "timestamp": "2025-09-24T09:30:00Z"
}
```

**Features:**
- **GPT-4o Vision**: Detaillierte Bildanalyse mit Logo-Erkennung
- **Brand Compliance**: Automatische Bewertung (0-100)
- **SVG-Unterstützung**: Automatische Konvertierung zu PNG
- **Farb-Extraktion**: HEX-Werte aus Bildern
- **Icon-Klassifizierung**: Automatische Kategorisierung

---

## 🧠 LLM-API Service (Port 8001)

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "llm-api-service",
  "timestamp": "2025-09-24T09:30:00Z"
}
```

---

### Semantische Suche
```http
POST /api/search
Content-Type: application/json
```

**Request Body:**
```json
{
  "query": "Bosch Farben",
  "brand_id": "9a933c7f-bd87-400f-b13a-b3bce7c822d8",
  "limit": 5
}
```

**Response:**
```json
{
  "query": "Bosch Farben",
  "results": [
    {
      "content": "Die offiziellen Bosch-Farben sind...",
      "similarity": 0.95,
      "source": "brand_guidelines",
      "metadata": {
        "section": "Farben",
        "page": 12
      }
    }
  ],
  "total_results": 5,
  "timestamp": "2025-09-24T09:30:00Z"
}
```

---

### Fragen beantworten
```http
POST /api/ask
Content-Type: application/json
```

**Request Body:**
```json
{
  "question": "Welche Farben sind für Bosch erlaubt?",
  "brand_id": "9a933c7f-bd87-400f-b13a-b3bce7c822d8",
  "limit": 5,
  "stream": false
}
```

**Response:**
```json
{
  "question": "Welche Farben sind für Bosch erlaubt?",
  "answer": "Die offiziellen Bosch-Farben sind:\n1. Bosch Blau 50 (#007bc0)\n2. Bosch Rot (#ed0007)\n3. Bosch Grau 50 (#71767c)\n4. Schwarz (#000000)\n5. Weiß (#ffffff)",
  "sources": [
    {
      "content": "Bosch Brand Guidelines - Farben",
      "similarity": 0.98
    }
  ],
  "source_count": 3,
  "timestamp": "2025-09-24T09:30:00Z"
}
```

---

### Brand-Compliance prüfen
```http
POST /api/compliance/check
Content-Type: application/json
```

**Request Body:**
```json
{
  "analysis_data": {
    "colors": [
      {
        "hex": "#007bc0",
        "usage_percentage": 45.2
      }
    ],
    "fonts": [
      {
        "name": "BoschSans-Regular",
        "usage_percentage": 47.17
      }
    ],
    "logo_detected": true
  },
  "brand_id": "9a933c7f-bd87-400f-b13a-b3bce7c822d8"
}
```

**Response:**
```json
{
  "brand_compliance_assessment": {
    "overall_score": 85,
    "compliance_status": "mostly_compliant",
    "assessment_date": "2025-09-24T09:30:00Z",
    "document_info": {
      "filename": "document.pdf",
      "total_pages": 1,
      "analysis_confidence": "high"
    },
    "color_compliance": {
      "score": 90,
      "status": "compliant",
      "approved_colors": [
        {
          "hex": "#007bc0",
          "name": "Bosch Blau 50",
          "usage_percentage": 45.2,
          "compliance": "approved"
        }
      ],
      "similar_colors": [],
      "non_compliant_colors": []
    },
    "font_compliance": {
      "score": 85,
      "status": "mostly_compliant",
      "approved_fonts": [
        {
          "name": "BoschSans-Regular",
          "usage_percentage": 47.17,
          "compliance": "approved"
        }
      ],
      "non_compliant_fonts": []
    },
    "logo_compliance": {
      "score": 100,
      "status": "compliant",
      "logo_detected": true
    },
    "overall_recommendations": [
      "Dokument entspricht größtenteils den Bosch Brand Guidelines"
    ]
  }
}
```

---

### Brand-Daten abrufen

#### Alle Brands
```http
GET /api/brands
```

**Response:**
```json
{
  "brands": [
    {
      "id": "9a933c7f-bd87-400f-b13a-b3bce7c822d8",
      "name": "Bosch Corporate",
      "description": "Hauptmarke Bosch",
      "created_at": "2025-09-24T09:30:00Z"
    }
  ],
  "total": 1
}
```

#### Brand Assets
```http
GET /api/brand/{brand_id}/assets
```

**Response:**
```json
{
  "brand_id": "9a933c7f-bd87-400f-b13a-b3bce7c822d8",
  "assets": [
    {
      "type": "logo",
      "name": "Bosch Logo",
      "url": "https://example.com/logo.png",
      "category": "primary"
    }
  ],
  "total": 1
}
```

#### Brand Guidelines
```http
GET /api/brand/{brand_id}/guidelines
```

**Response:**
```json
{
  "brand_id": "9a933c7f-bd87-400f-b13a-b3bce7c822d8",
  "guidelines": [
    {
      "section": "Farben",
      "content": "Die offiziellen Bosch-Farben sind...",
      "last_updated": "2025-09-24T09:30:00Z"
    }
  ],
  "total": 5
}
```

---

### Embeddings verwalten

#### Embeddings Status
```http
GET /api/embeddings/status
```

**Response:**
```json
{
  "total_chunks": 1250,
  "total_brands": 1,
  "last_updated": "2025-09-24T09:30:00Z",
  "embedding_model": "text-embedding-3-large",
  "dimensions": 3072
}
```

#### Embeddings generieren
```http
POST /api/embeddings/generate
Content-Type: application/json
```

**Request Body:**
```json
{
  "brand_id": "9a933c7f-bd87-400f-b13a-b3bce7c822d8",
  "force_regenerate": false
}
```

**Response:**
```json
{
  "status": "completed",
  "chunks_processed": 1250,
  "chunks_created": 0,
  "chunks_updated": 1250,
  "duration_seconds": 45.2,
  "timestamp": "2025-09-24T09:30:00Z"
}
```

---

## 🎨 Image-Analyzer (Standalone)

### Bild-URLs extrahieren
```bash
docker exec brandchecker-python python3 /app/python_app/extract_image_links.py
```

**Output:**
- `shared/JSON/extracted/image_urls.json` - Liste aller Bild-URLs
- `shared/JSON/extracted/image_extraction_stats.json` - Statistiken

### Bildanalyse ausführen
```bash
docker exec brandchecker-python python3 /app/python_app/image_analysis_service.py
```

**Input:**
- `shared/JSON/extracted/image_urls.json`

**Output:**
- `shared/JSON/analyzed/image_analysis_TIMESTAMP.json` - Analyseergebnisse
- `shared/JSON/analyzed/image_analysis_stats_TIMESTAMP.json` - Statistiken

**Analyseergebnis:**
```json
{
  "url": "https://example.com/image.png",
  "content_type": "image",
  "model_used": "gpt-4o",
  "analysis": {
    "detailed_description": {
      "objects": ["Logo", "Text", "Grafik"],
      "composition": "Zentriert mit Logo oben"
    },
    "brand_elements": {
      "logo": {
        "present": true,
        "type": "Bosch Logo",
        "color": "Rot",
        "position": "oben-links"
      },
      "colors": ["#007bc0", "#ed0007"],
      "typography": {
        "font_family": "BoschSans",
        "sizes": ["12pt", "18pt"]
      }
    },
    "asset_typ": "Logo",
    "brand_compliance": 95,
    "technical_analysis": {
      "quality": "hoch",
      "style": "professionell"
    }
  },
  "logo_detected": true,
  "tokens_used": 1250,
  "status": "success",
  "timestamp": "2025-09-24T09:30:00Z"
}
```

---

## 🔧 Fehlerbehandlung

### Standard-Fehler-Response
```json
{
  "error": "Fehlerbeschreibung",
  "status": "error",
  "timestamp": "2025-09-24T09:30:00Z"
}
```

### Häufige HTTP-Status-Codes
- `200`: Erfolgreich
- `400`: Ungültige Anfrage
- `404`: Nicht gefunden
- `500`: Interner Server-Fehler

---

## 📝 Beispiel-Workflows

### 1. Vollständige PDF-Analyse mit Brand-Compliance
```bash
# 1. PDF analysieren
curl -X POST http://localhost:7011/extract-all-path \
  -H "Content-Type: application/json" \
  -d '{"filepath": "/shared/testfile1.pdf"}'

# 2. Brand-Compliance prüfen
curl -X POST http://localhost:8001/api/compliance/check \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_data": {...},
    "brand_id": "9a933c7f-bd87-400f-b13a-b3bce7c822d8"
  }'
```

### 2. Semantische Suche nach Brand-Guidelines
```bash
curl -X POST http://localhost:8001/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Welche Schriftarten sind für Bosch erlaubt?",
    "brand_id": "9a933c7f-bd87-400f-b13a-b3bce7c822d8"
  }'
```

### 3. Bildanalyse aller Brand-Assets
```bash
# URLs extrahieren
docker exec brandchecker-python python3 /app/python_app/extract_image_links.py

# Bilder analysieren
docker exec brandchecker-python python3 /app/python_app/image_analysis_service.py
```

---

## 🚀 n8n Integration

### PDF-Analyse in n8n
```json
{
  "method": "POST",
  "url": "http://brandchecker-python:7011/extract-all-path",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "filepath": "{{ $json.filepath }}"
  }
}
```

### LLM-Integration in n8n
```json
{
  "method": "POST",
  "url": "http://brandchecker-llm-api:8001/api/ask",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "question": "{{ $json.question }}",
    "brand_id": "9a933c7f-bd87-400f-b13a-b3bce7c822d8",
    "stream": false
  }
}
```

---

## 📊 Performance-Metriken

### PDF-Analyzer
- **Durchschnittliche Verarbeitungszeit**: 2-5 Sekunden pro PDF
- **Unterstützte Formate**: PDF (alle Versionen)
- **Maximale Dateigröße**: 50MB
- **Gleichzeitige Anfragen**: 10

### LLM-API
- **Semantische Suche**: < 1 Sekunde
- **LLM-Antworten**: 2-5 Sekunden
- **Embedding-Generierung**: 45 Sekunden für 1250 Chunks
- **Gleichzeitige Anfragen**: 5

### Image-Analyzer
- **Bildanalyse**: 5-10 Sekunden pro Bild
- **SVG-Konvertierung**: Automatisch zu PNG
- **Unterstützte Formate**: PNG, JPEG, WebP, SVG
- **Batch-Verarbeitung**: 2 Bilder parallel

---

## 🔐 Authentifizierung

Aktuell ist keine Authentifizierung implementiert. Alle Endpunkte sind öffentlich zugänglich.

---

## 📞 Support

Bei Fragen oder Problemen:
1. Prüfe die Container-Logs: `docker logs brandchecker-python`
2. Teste Health-Checks: `curl http://localhost:7011/health`
3. Überprüfe die API-Dokumentation

---

*Letzte Aktualisierung: 2025-09-24*
