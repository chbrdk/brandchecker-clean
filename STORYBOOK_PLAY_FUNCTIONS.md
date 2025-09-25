# Storybook Play Functions Integration für BrandChecker

## 🎯 Warum Play Functions?

Die [Storybook Play Functions](https://storybook.js.org/docs/writing-stories/play-function?renderer=react#writing-stories-with-the-play-function) sind eine revolutionäre Funktion in Storybook 9, die es ermöglicht, **interaktive Tests und Benutzer-Workflows** direkt in Storybook zu implementieren.

## 🚀 Vorteile für BrandChecker

### 1. **Automatisierte Brand-Analyse Workflows**
```typescript
export const PDFUploadWorkflow: Story = {
  play: async ({ canvas, userEvent }) => {
    // PDF-Datei hochladen
    const fileInput = canvas.getByLabelText('Upload PDF');
    const file = new File(['pdf content'], 'test.pdf', { type: 'application/pdf' });
    await userEvent.upload(fileInput, file);
    
    // Analyse starten
    const analyzeButton = canvas.getByRole('button', { name: 'Analyze PDF' });
    await userEvent.click(analyzeButton);
    
    // Ergebnisse validieren
    await expect(canvas.getByText('Color Analysis')).toBeVisible();
    await expect(canvas.getByText('Font Analysis')).toBeVisible();
  },
};
```

### 2. **Form-Validierung testen**
```typescript
export const FormValidation: Story = {
  play: async ({ canvas, userEvent }) => {
    const emailInput = canvas.getByLabelText('Email Address');
    
    // Ungültige E-Mail eingeben
    await userEvent.type(emailInput, 'invalid-email');
    await userEvent.tab(); // Trigger validation
    
    // Fehler-Message prüfen
    await expect(canvas.getByText('Please enter a valid email address')).toBeVisible();
    
    // Korrekte E-Mail eingeben
    await userEvent.clear(emailInput);
    await userEvent.type(emailInput, 'user@example.com');
    
    // Success-State prüfen
    await expect(canvas.getByText('Email address is valid')).toBeVisible();
  },
};
```

### 3. **Brand-Compliance-Checker testen**
```typescript
export const BrandComplianceCheck: Story = {
  play: async ({ canvas, userEvent }) => {
    // Brand-Guidelines laden
    const loadGuidelinesButton = canvas.getByRole('button', { name: 'Load Brand Guidelines' });
    await userEvent.click(loadGuidelinesButton);
    
    // PDF hochladen
    const fileInput = canvas.getByLabelText('Upload Document');
    await userEvent.upload(fileInput, new File(['content'], 'document.pdf'));
    
    // Compliance-Check starten
    const checkButton = canvas.getByRole('button', { name: 'Check Compliance' });
    await userEvent.click(checkButton);
    
    // Ergebnisse validieren
    await expect(canvas.getByText('Compliance Score: 85%')).toBeVisible();
    await expect(canvas.getByText('Issues Found: 3')).toBeVisible();
  },
};
```

## 🛠️ Implementierung

### Schritt 1: Dependencies installieren
```bash
npm install --save-dev @storybook/test
```

### Schritt 2: Play Functions zu Stories hinzufügen
```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { expect } from '@storybook/test';
import { MyComponent } from './MyComponent';

export const InteractiveStory: Story = {
  play: async ({ canvas, userEvent }) => {
    // Interaktionen hier implementieren
    const button = canvas.getByRole('button');
    await userEvent.click(button);
    
    // Assertions hier hinzufügen
    await expect(canvas.getByText('Success!')).toBeVisible();
  },
};
```

### Schritt 3: Test-IDs zu Komponenten hinzufügen
```typescript
// In der Komponente
<div data-testid="loading-skeleton">
  <div data-testid="skeleton-line"></div>
</div>
```

## 📋 Verfügbare APIs

### Canvas Object
- `canvas.getByRole()` - Elemente nach Rolle finden
- `canvas.getByLabelText()` - Elemente nach Label finden
- `canvas.getByTestId()` - Elemente nach Test-ID finden
- `canvas.getAllByRole()` - Alle Elemente einer Rolle finden

### UserEvent Object
- `userEvent.click()` - Klick-Simulation
- `userEvent.type()` - Tasteneingabe
- `userEvent.hover()` - Hover-Simulation
- `userEvent.tab()` - Tab-Navigation
- `userEvent.keyboard()` - Tastatur-Events
- `userEvent.upload()` - Datei-Upload

### Expect Object
- `expect().toBeVisible()` - Sichtbarkeit prüfen
- `expect().toHaveAttribute()` - Attribute prüfen
- `expect().toHaveValue()` - Werte prüfen
- `expect().toHaveFocus()` - Focus prüfen

## 🎨 BrandChecker-spezifische Anwendungen

### 1. **PDF-Upload Workflow**
```typescript
export const PDFAnalysisWorkflow: Story = {
  play: async ({ canvas, userEvent }) => {
    // PDF hochladen
    const fileInput = canvas.getByLabelText('Upload PDF');
    await userEvent.upload(fileInput, new File(['pdf'], 'brand-guidelines.pdf'));
    
    // Analyse starten
    await userEvent.click(canvas.getByRole('button', { name: 'Start Analysis' }));
    
    // Warten auf Ergebnisse
    await expect(canvas.getByText('Analysis Complete')).toBeVisible();
    
    // Ergebnisse prüfen
    await expect(canvas.getByText('Colors Found: 5')).toBeVisible();
    await expect(canvas.getByText('Fonts Found: 3')).toBeVisible();
  },
};
```

### 2. **Brand-Guidelines Navigation**
```typescript
export const BrandGuidelinesNavigation: Story = {
  play: async ({ canvas, userEvent }) => {
    // Navigation öffnen
    await userEvent.click(canvas.getByRole('button', { name: 'Open Guidelines' }));
    
    // Durch Kategorien navigieren
    await userEvent.click(canvas.getByRole('button', { name: 'Colors' }));
    await expect(canvas.getByText('Brand Colors')).toBeVisible();
    
    await userEvent.click(canvas.getByRole('button', { name: 'Typography' }));
    await expect(canvas.getByText('Brand Fonts')).toBeVisible();
  },
};
```

### 3. **Compliance-Check Workflow**
```typescript
export const ComplianceCheckWorkflow: Story = {
  play: async ({ canvas, userEvent }) => {
    // Dokument hochladen
    const fileInput = canvas.getByLabelText('Upload Document');
    await userEvent.upload(fileInput, new File(['content'], 'marketing-material.pdf'));
    
    // Compliance-Check starten
    await userEvent.click(canvas.getByRole('button', { name: 'Check Compliance' }));
    
    // Ergebnisse validieren
    await expect(canvas.getByText('Compliance Score: 92%')).toBeVisible();
    
    // Issues durchgehen
    const issues = canvas.getAllByTestId('compliance-issue');
    await expect(issues).toHaveLength(2);
    
    // Issue-Details öffnen
    await userEvent.click(issues[0]);
    await expect(canvas.getByText('Issue Details')).toBeVisible();
  },
};
```

## 🔧 Setup für BrandChecker

### 1. Package.json erweitern
```json
{
  "devDependencies": {
    "@storybook/test": "^9.1.8"
  }
}
```

### 2. Storybook-Konfiguration
```typescript
// .storybook/main.ts
export default {
  addons: [
    '@storybook/addon-interactions',
    '@storybook/addon-test-runner',
  ],
};
```

### 3. Test-Runner Setup
```bash
npm install --save-dev @storybook/test-runner
```

## 🎯 Nächste Schritte

1. **Dependencies installieren**: `@storybook/test` hinzufügen
2. **Interaktive Stories erstellen**: Für alle BrandChecker-Komponenten
3. **Test-Runner konfigurieren**: Automatische Tests in CI/CD
4. **Workflow-Tests**: Komplette Brand-Analyse-Workflows testen

## 💡 Best Practices

- **Test-IDs verwenden**: Für stabile Selektoren
- **Realistische Daten**: Echte PDF-Dateien für Tests
- **Fehler-Szenarien**: Auch negative Testfälle abdecken
- **Performance**: Lange Workflows in separate Stories aufteilen
- **Dokumentation**: Play Functions gut dokumentieren

Die Play Functions werden unser BrandChecker-Projekt erheblich verbessern, indem sie **automatisierte Tests** und **interaktive Dokumentation** in einem Tool kombinieren!
