# BrandChecker Frontend Komponenten-Architektur

## Übersicht
Das BrandChecker-System benötigt eine umfassende Frontend-Architektur für die Darstellung und Interaktion mit Brand-Analyse-Daten. Diese Dokumentation definiert alle benötigten Komponenten basierend auf den Backend-Services und der Storybook-Philosophie.

## Backend-Services Integration
- **Python Service** (Port 8000): PDF-Analyse, Text/Font/Farb-Extraktion
- **LLM API Service** (Port 8001): KI-gestützte Brand-Guideline-Befragung
- **Image API Service** (Port 8002): Bildanalyse mit GPT-4o Vision
- **Color Profile Service** (Port 8082): Farbanalyse
- **Font Profile Service**: Font-Erkennung
- **Logo Profile Service**: Logo-Detection
- **Image Profile Service** (Port 8085): Bildverarbeitung
- **PDF Measure Service** (Port 8086): PDF-Layout-Messungen

## Komponenten-Kategorien

### 1. 🎨 Design System Foundation

#### 1.1 Basis-Komponenten
- **Button** ✅ (erweitert mit Icon-Library)
  - Varianten: primary, secondary, danger, success, ghost, link
  - Größen: small, medium, large
  - Zustände: loading, disabled, active
  - Icons: Icon-Library Integration (iconName, iconPosition)
  - Features: Loading-Icon automatisch, Click-Support

- **Input** ✅ (erweitert mit Icon-Library)
  - Typen: text, email, password, number, file, search
  - Zustände: error, success, disabled
  - Validierung: real-time feedback
  - Labels: floating, inline, placeholder
  - Icons: Icon-Library Integration (iconName, iconPosition)

- **Select/Dropdown** ✅ (erweitert mit Icon-Button)
  - Single/Multi-Select
  - Search-Funktionalität
  - Gruppierung von Optionen
  - Custom Option Rendering
  - Icon-Button für Chevrons (bessere UX)

- **Card** ✅ (bereits vorhanden)
  - Basis-Card mit Header/Body/Footer
  - Varianten: elevated, outlined, filled
  - Interaktive Cards (hover, click)

- **Modal/Dialog** ✅ (bereits vorhanden)
  - Modal mit Overlay
  - Confirmation Dialogs
  - Fullscreen Modals
  - Drawer/Sidebar Varianten

- **Accordion** ✅ (NEU implementiert)
  - Collapsible Sections
  - Single/Multiple Open
  - Custom Icons (Icon-Library)
  - Varianten: default, flush, outlined
  - Accessibility Support

- **Chip/Tag** ✅ (NEU implementiert)
  - Status Indicators
  - Category Labels
  - Removable Chips
  - Clickable Chips
  - Icon Support (Icon-Library)
  - Varianten: default, primary, secondary, success, warning, error, info
  - Größen: small, medium, large
  - ChipGroup für Gruppierung

#### 1.2 Layout-Komponenten
- **Container** ✅ (bereits vorhanden)
  - Responsive Container
  - Max-Width Varianten
  - Padding/Margin Utilities

- **Grid** ✅ (vereinfacht implementiert)
  - CSS Grid System
  - Responsive Breakpoints
  - Auto-Layout Features
  - Einfache Gaps und Columns

- **Spacer** ✅ (bereits vorhanden)
  - Margin/Padding Utilities
  - Responsive Spacing
  - Mobile-First Approach

- **Icon-Library** ✅ (NEU implementiert)
  - 60+ SVG Icons
  - 9 Kategorien (Navigation, Actions, Status, Files, Brand, User, Communication, System)
  - TypeScript Support
  - Flexible Größen (xs, sm, md, lg, xl)
  - Custom Colors
  - Click Support
  - Accessibility

### 2. 📊 Data Display Komponenten

#### 2.1 Tabellen
- **Table** ✅ (erweitert mit Chip-Integration)
  - Sortierung (asc/desc)
  - Filterung pro Spalte
  - Pagination
  - Row Selection
  - Responsive Design
  - Export-Funktionen
  - Icon-Library Integration bereit
  - Chip-Integration für Status und Tags

- **DataTable** (NEU)
  - Erweiterte Table mit:
  - Server-side Pagination
  - Advanced Filtering
  - Column Resizing
  - Row Grouping
  - Virtual Scrolling

#### 2.2 Listen
- **List** (NEU)
  - Simple List
  - Nested Lists
  - Action Items
  - Drag & Drop

- **VirtualList** (NEU)
  - Performance-optimierte Listen
  - Infinite Scrolling
  - Dynamic Heights

#### 2.3 Charts & Visualisierungen
- **Chart** (NEU)
  - Bar Charts
  - Line Charts
  - Pie Charts
  - Scatter Plots
  - Integration mit Chart.js/D3

- **ProgressBar** (NEU)
  - Linear Progress
  - Circular Progress
  - Multi-step Progress
  - Custom Labels

- **Badge** (NEU)
  - Status Badges
  - Count Badges
  - Color Variants
  - Size Variants

### 3. 🎯 Brand-Analyse spezifische Komponenten

#### 3.1 PDF-Upload & Verarbeitung
- **FileUpload** (NEU)
  - Drag & Drop Interface
  - Multiple File Support
  - File Type Validation
  - Progress Tracking
  - Preview Functionality

- **PDFPreview** (NEU)
  - PDF Thumbnail
  - Page Navigation
  - Zoom Controls
  - Annotation Support

- **ProcessingStatus** (NEU)
  - Real-time Processing Updates
  - Step-by-step Progress
  - Error Handling
  - Retry Functionality

#### 3.2 Brand-Analyse Ergebnisse
- **AnalysisResults** (NEU)
  - Tabbed Interface für verschiedene Analysen
  - Expandable Sections
  - Export Options
  - Comparison Views

- **ColorAnalysis** (NEU)
  - Color Palette Display
  - Color Swatches
  - HSV/RGB/HEX Values
  - Similarity Scores
  - Brand Compliance Check

- **FontAnalysis** (NEU)
  - Font Family Display
  - Font Size Analysis
  - Font Weight Distribution
  - Brand Font Compliance

- **LogoAnalysis** (NEU)
  - Logo Detection Results
  - Similarity Matching
  - Brand Logo Compliance
  - Logo Variations

- **LayoutAnalysis** (NEU)
  - Layout Structure Visualization
  - Element Positioning
  - Spacing Analysis
  - Brand Guideline Compliance

#### 3.3 Brand Guidelines Integration
- **BrandGuidelines** (NEU)
  - Interactive Brand Guide Viewer
  - Search Functionality
  - Category Navigation
  - Download Options

- **ComplianceChecker** (NEU)
  - Real-time Compliance Scoring
  - Issue Highlighting
  - Recommendations
  - Fix Suggestions

- **BrandChat** (NEU)
  - Chat Interface für LLM-Integration
  - Natural Language Queries
  - Context-aware Responses
  - Conversation History

### 4. 🔍 Search & Filter Komponenten

#### 4.1 Suchfunktionalität
- **SearchBox** (NEU)
  - Real-time Search
  - Search Suggestions
  - Search History
  - Advanced Search Options

- **FilterPanel** (NEU)
  - Multi-criteria Filtering
  - Date Range Filters
  - Category Filters
  - Custom Filter Logic

- **SortControls** (NEU)
  - Multi-column Sorting
  - Sort Direction Indicators
  - Custom Sort Functions

### 5. 📱 Navigation & Routing

#### 5.1 Navigation
- **Header** ✅ (erweitert mit Icon-Library)
  - Brand Logo Integration
  - Navigation Menu
  - User Profile
  - Notifications
  - Search Integration
  - Icon-Library Integration (NavItem)

- **Sidebar** ✅ (erweitert mit Icon-Library)
  - Collapsible Sidebar
  - Navigation Groups
  - Active State Management
  - Responsive Behavior
  - Icon-Library Integration (SidebarItem)

- **Breadcrumbs** (NEU)
  - Hierarchical Navigation
  - Clickable Paths
  - Custom Separators

- **Pagination** (NEU)
  - Page Navigation
  - Page Size Selection
  - Jump to Page
  - Total Count Display

#### 5.2 Tabs & Accordions
- **Tabs** (NEU)
  - Horizontal/Vertical Tabs
  - Scrollable Tabs
  - Tab Content Management
  - Dynamic Tab Creation

- **Accordion** ✅ (NEU implementiert)
  - Collapsible Sections
  - Single/Multiple Open
  - Custom Headers
  - Animation Support
  - Icon-Library Integration
  - Accessibility Support

### 6. 🎨 Brand-spezifische UI-Komponenten

#### 6.1 Brand Identity
- **BrandLogo** (NEU)
  - Dynamic Logo Loading
  - Logo Variations
  - Responsive Sizing
  - Brand Color Integration

- **BrandColors** (NEU)
  - Brand Color Palette
  - Color Usage Guidelines
  - Accessibility Information
  - Color Picker Integration

- **BrandTypography** (NEU)
  - Brand Font Display
  - Typography Scale
  - Usage Examples
  - Font Loading States

#### 6.2 Brand Compliance
- **ComplianceScore** (NEU)
  - Visual Score Display
  - Score Breakdown
  - Improvement Suggestions
  - Historical Tracking

- **IssueTracker** (NEU)
  - Compliance Issues List
  - Issue Severity
  - Fix Recommendations
  - Issue Resolution Tracking

### 7. 🔧 Utility Komponenten

#### 7.1 Feedback & States
- **Alert** (NEU)
  - Success/Error/Warning/Info
  - Dismissible Alerts
  - Action Buttons
  - Custom Icons

- **Toast** (NEU)
  - Notification System
  - Auto-dismiss
  - Stack Management
  - Custom Positioning

- **Loading** (NEU)
  - Spinner Variants
  - Skeleton Screens
  - Progress Indicators
  - Custom Loading States

- **EmptyState** (NEU)
  - No Data States
  - Error States
  - Custom Illustrations
  - Action Prompts

#### 7.2 Form Utilities
- **FormField** (NEU)
  - Label Management
  - Error Display
  - Help Text
  - Required Indicators

- **FormGroup** (NEU)
  - Field Grouping
  - Validation Management
  - Layout Control
  - Accessibility Support

- **ValidationMessage** (NEU)
  - Error Messages
  - Success Messages
  - Warning Messages
  - Custom Validation

### 8. 📊 Dashboard & Reporting

#### 8.1 Dashboard Komponenten
- **Dashboard** (NEU)
  - Widget-based Layout
  - Drag & Drop Widgets
  - Customizable Views
  - Real-time Updates

- **Widget** (NEU)
  - Chart Widgets
  - Metric Widgets
  - List Widgets
  - Custom Widgets

- **MetricCard** (NEU)
  - KPI Display
  - Trend Indicators
  - Comparison Values
  - Click Actions

#### 8.2 Reporting
- **ReportGenerator** (NEU)
  - Report Templates
  - Custom Report Builder
  - Export Options
  - Scheduled Reports

- **ReportViewer** (NEU)
  - PDF Viewer
  - Interactive Reports
  - Annotation Support
  - Sharing Options

### 9. 🔐 Authentication & User Management

#### 9.1 Auth Komponenten
- **LoginForm** (NEU)
  - Username/Password
  - Social Login
  - Remember Me
  - Forgot Password

- **UserProfile** (NEU)
  - Profile Information
  - Avatar Upload
  - Settings Management
  - Activity History

- **PermissionGate** (NEU)
  - Role-based Access
  - Permission Checking
  - Conditional Rendering
  - Access Denied States

### 10. 🎛️ Settings & Configuration

#### 10.1 Settings
- **SettingsPanel** (NEU)
  - Tabbed Settings
  - Form Validation
  - Save States
  - Reset Options

- **ThemeSelector** (NEU)
  - Light/Dark Mode
  - Custom Themes
  - Brand Theme Integration
  - Preview Functionality

- **LanguageSelector** (NEU)
  - Multi-language Support
  - RTL Support
  - Locale Settings
  - Translation Management

## Implementierungsreihenfolge

### Phase 1: Foundation (Woche 1-2)
1. **Design System Setup**
   - Button erweitern ✅
   - Input, Select, Checkbox
   - Card, Modal
   - Container, Grid, Spacer

2. **Layout Komponenten**
   - Header erweitern ✅
   - Sidebar, Breadcrumbs
   - Tabs, Accordion

### Phase 2: Data Display (Woche 3-4)
1. **Tabellen & Listen**
   - Table, DataTable
   - List, VirtualList
   - SearchBox, FilterPanel

2. **Charts & Visualisierungen**
   - Chart, ProgressBar
   - Badge, Alert

### Phase 3: Brand-spezifisch (Woche 5-6)
1. **PDF & Upload**
   - FileUpload, PDFPreview
   - ProcessingStatus

2. **Analyse Ergebnisse**
   - AnalysisResults
   - ColorAnalysis, FontAnalysis
   - LogoAnalysis, LayoutAnalysis

### Phase 4: Advanced Features (Woche 7-8)
1. **Brand Guidelines**
   - BrandGuidelines
   - ComplianceChecker
   - BrandChat

2. **Dashboard & Reporting**
   - Dashboard, Widget
   - MetricCard, ReportGenerator

### Phase 5: Polish & Integration (Woche 9-10)
1. **Authentication**
   - LoginForm, UserProfile
   - PermissionGate

2. **Settings & Configuration**
   - SettingsPanel
   - ThemeSelector, LanguageSelector

## Atomic Design Struktur

### **Korrekte Atomic Design Hierarchie:**

```
src/
├── components/
│   ├── atoms/           # Basis-Komponenten (kleinste Einheiten)
│   │   ├── Button/      ✅
│   │   ├── Input/       ✅
│   │   ├── Select/      ✅
│   │   ├── Card/        ✅
│   │   ├── Container/   ✅
│   │   ├── Grid/        ✅
│   │   ├── Spacer/      ✅
│   │   ├── Icon/        ✅
│   │   └── Chip/        ✅
│   ├── molecules/       # Zusammengesetzte Komponenten
│   │   ├── Modal/       ✅ (verschoben)
│   │   ├── Accordion/   ✅ (verschoben)
│   │   ├── SearchBox/   🔄 (geplant)
│   │   ├── FormField/   🔄 (geplant)
│   │   └── ...
│   ├── organisms/       # Komplexe UI-Komponenten
│   │   ├── Header/      ✅ (verschoben)
│   │   ├── Sidebar/     ✅ (verschoben)
│   │   ├── Table/       ✅ (verschoben)
│   │   ├── DataTable/   🔄 (geplant)
│   │   └── ...
│   └── templates/       # Layout-Templates
│       ├── Dashboard/   🔄 (geplant)
│       ├── AnalysisPage/ 🔄 (geplant)
│       └── ...
├── stories/
│   ├── atoms/           # Atom Stories
│   ├── molecules/       # Molecule Stories
│   ├── organisms/       # Organism Stories
│   └── templates/       # Template Stories
└── styles/
    ├── tokens/          # Design Tokens
    ├── base/            # Basis-Styles
    └── components/      # Komponenten-Styles
```

### **Atomic Design Prinzipien:**

#### **🔬 Atoms (Basis-Komponenten):**
- **Kleinste Einheiten** des Design-Systems
- **Nicht weiter zerlegbar** ohne Verlust der Funktionalität
- **Wiederverwendbar** in verschiedenen Kontexten
- **Beispiele**: Button, Input, Icon, Chip, Spacer

#### **🧬 Molecules (Zusammengesetzte Komponenten):**
- **Kombinationen von Atoms** mit spezifischer Funktionalität
- **Eigenständige Komponenten** mit klarem Zweck
- **Beispiele**: Modal, Accordion, SearchBox, FormField

#### **🦠 Organisms (Komplexe Komponenten):**
- **Komplexe UI-Bereiche** mit mehreren Molecules/Atoms
- **Funktionale Einheiten** mit eigenem Verhalten
- **Beispiele**: Header, Sidebar, Table, DataTable

#### **📄 Templates (Layout-Templates):**
- **Seiten-Layouts** mit Platzhaltern für Content
- **Struktur** ohne spezifischen Content
- **Beispiele**: Dashboard, AnalysisPage, LoginPage

## Design Tokens

### Farben
- Primary: Brand-spezifische Hauptfarben
- Secondary: Unterstützende Farben
- Success: Grün-Töne für Erfolg
- Warning: Orange-Töne für Warnungen
- Error: Rot-Töne für Fehler
- Neutral: Grau-Töne für Text und Hintergründe

### Typography
- Font Families: Brand-spezifische Schriftarten
- Font Sizes: Responsive Größen-Scale
- Font Weights: Light, Regular, Medium, Bold
- Line Heights: Optimiert für Lesbarkeit

### Spacing
- Base Unit: 8px
- Scale: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px
- Responsive: Mobile, Tablet, Desktop

### Breakpoints
- Mobile: 320px - 767px
- Tablet: 768px - 1023px
- Desktop: 1024px+

## Nächste Schritte

1. **Design System Setup** - Design Tokens definieren
2. **Komponenten-Implementierung** - Phase 1 starten
3. **Storybook Stories** - Für jede Komponente
4. **Testing Setup** - Unit Tests für Komponenten
5. **Documentation** - Komponenten-Dokumentation
6. **Integration** - Backend-Services Integration
7. **Performance** - Optimierung und Monitoring
8. **Accessibility** - WCAG Compliance
9. **Internationalization** - Multi-language Support
10. **Deployment** - Production Setup
