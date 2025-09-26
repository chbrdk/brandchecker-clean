# BrandChecker

Ein modernes Frontend für Markenanalyse mit ChatGPT-ähnlicher Benutzeroberfläche, entwickelt mit React, TypeScript und Docker.

## 🚀 Features

### Chat-Interface
- **ChatGPT-ähnliche UI** mit Avatar-basierten Nachrichten
- **File Upload** mit Drag & Drop Unterstützung
- **Preview-Generierung** für PDF und Bilder
- **Responsive Design** mit Mobile-First Ansatz
- **Markdown-Rendering** für formatierte Nachrichten

### Design System
- **Atomic Design** Struktur (Atoms, Molecules, Organisms, Templates)
- **Design Tokens** für konsistente Typography, Colors, Spacing
- **Component Library** mit Storybook Integration
- **Accessibility** Features und Keyboard Navigation

### Backend Integration
- **Secure File Upload** API mit Validierung
- **PDF Preview** Generierung mit `pdf2image`
- **Base64 Encoding** für Browser-Transfer
- **CORS** konfiguriert für Cross-Origin Requests

## 🏗️ Architektur

### Frontend Stack
- **React 18** mit TypeScript
- **Vite** als Build Tool
- **CSS Modules** für Styling
- **React Markdown** für Text-Rendering
- **Docker** Containerisierung

### Backend Stack
- **Flask** Python Web Framework
- **PyPDF2** & **pdf2image** für PDF-Verarbeitung
- **Pillow** für Bildverarbeitung
- **Flask-CORS** für Cross-Origin Support

### Development Tools
- **Storybook** für Component Development
- **Docker Compose** für Multi-Container Setup
- **Hot Module Replacement** für schnelle Entwicklung

## 📁 Projektstruktur

```
brandchecker/
├── frontend/                    # React Frontend
│   ├── src/
│   │   ├── app/                # Standalone App
│   │   ├── components/         # Component Library
│   │   │   ├── atoms/          # Atomic Components
│   │   │   ├── molecules/      # Molecule Components
│   │   │   ├── organisms/      # Organism Components
│   │   │   └── templates/      # Template Components
│   │   ├── styles/             # Design Tokens & Styles
│   │   └── stories/            # Storybook Stories
│   ├── Dockerfile.app          # App Container
│   └── vite.app.config.ts      # Vite Configuration
├── upload-service/              # Python Backend
│   ├── app.py                  # Flask Application
│   ├── requirements.txt        # Python Dependencies
│   └── Dockerfile.upload       # Upload Service Container
├── shared/                     # Shared Storage
│   └── uploads/               # Upload Directory
├── docker-compose.yml          # Multi-Container Setup
└── README.md                   # Diese Datei
```

## 🎨 Design System

### Typography
- **Font Sizes**: `xs` (12px), `sm` (14px), `base` (16px), `lg` (18px), `xl` (20px)
- **Font Weights**: `light`, `normal`, `medium`, `semibold`, `bold`
- **Line Heights**: `tight` (1.25), `normal` (1.5), `relaxed` (1.625)

### Colors
- **Primary**: Brand-spezifische Farben
- **Secondary**: Grau-Töne für UI-Elemente
- **Status**: Success, Warning, Error, Info
- **Text**: Primary, Secondary, Tertiary

### Spacing
- **Scale**: `1` (4px), `2` (8px), `3` (12px), `4` (16px), `6` (24px)
- **Responsive**: Mobile-First Breakpoints
- **Grid**: CSS Grid mit flexiblen Spalten

## 🚀 Installation & Setup

### Voraussetzungen
- Docker & Docker Compose
- Node.js 20+ (für lokale Entwicklung)
- Python 3.9+ (für Backend-Entwicklung)

### Docker Setup (Empfohlen)
```bash
# Repository klonen
git clone <repository-url>
cd brandchecker

# Container starten
docker-compose up -d

# Services prüfen
docker-compose ps
```

### Lokale Entwicklung
```bash
# Frontend
cd frontend
npm install
npm run app:dev

# Backend
cd upload-service
pip install -r requirements.txt
python app.py
```

## 🌐 Services & Ports

| Service | Port | Beschreibung |
|---------|------|--------------|
| **Frontend App** | 8005 | React Application |
| **Storybook** | 8004 | Component Library |
| **Upload Service** | 8006 | File Upload API |

## 📱 Verwendung

### File Upload
1. **Datei auswählen** über Drag & Drop oder File Picker
2. **Send klicken** um Upload zu starten
3. **Preview anzeigen** in der Chat-Card
4. **Dateieigenschaften** unter dem Preview-Bild

### Chat Interface
- **User Messages** erscheinen links mit Avatar
- **Agent Messages** erscheinen rechts mit AI-Avatar
- **Markdown Support** für formatierte Nachrichten
- **Responsive Layout** für alle Bildschirmgrößen

## 🔧 Development

### Component Development
```bash
# Storybook starten
cd frontend
npm run storybook

# Storybook im Docker
docker-compose up brandchecker-storybook
```

### Testing
```bash
# Frontend Tests
cd frontend
npm test

# Backend Tests
cd upload-service
python -m pytest
```

### Build
```bash
# Frontend Build
cd frontend
npm run build

# Docker Build
docker-compose build
```

## 📊 API Endpoints

### Upload Service
- **POST** `/upload` - File Upload mit Preview-Generierung
- **GET** `/health` - Service Health Check

### Request/Response Format
```json
{
  "success": true,
  "file_id": "uuid",
  "original_filename": "document.pdf",
  "file_type": "pdf",
  "file_size_mb": 4.39,
  "preview": {
    "available": true,
    "base64": "data:image/png;base64,...",
    "dimensions": [212, 300]
  }
}
```

## 🎯 Roadmap

### Geplant
- [ ] **Backend API Integration** - HTTP Client, Error Handling
- [ ] **Hauptseiten** - Dashboard, Chat, Upload, Results
- [ ] **React Router** - Navigation, Route Guards
- [ ] **State Management** - Context/Redux für Chat States
- [ ] **Error Handling** - Global Error Boundary, Toast Notifications
- [ ] **Testing** - Unit Tests, Integration Tests, E2E Tests

### In Entwicklung
- [x] **Component Library** - Atomic Design Struktur
- [x] **Design Tokens** - Typography, Colors, Spacing
- [x] **File Upload** - Secure Upload mit Preview
- [x] **Chat Interface** - ChatGPT-ähnliche UI
- [x] **Docker Setup** - Multi-Container Environment

## 🤝 Contributing

### Code Style
- **TypeScript** für Type Safety
- **ESLint** & **Prettier** für Code Formatting
- **Atomic Design** für Component Struktur
- **Design Tokens** für konsistente Styles

### Git Workflow
1. **Feature Branch** erstellen
2. **Changes** committen
3. **Pull Request** erstellen
4. **Code Review** durchführen
5. **Merge** nach Approval

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

## 🆘 Support

Bei Fragen oder Problemen:
1. **Issues** im Repository erstellen
2. **Documentation** prüfen
3. **Community** um Hilfe bitten

---

**BrandChecker** - Moderne Markenanalyse mit KI-Unterstützung 🚀