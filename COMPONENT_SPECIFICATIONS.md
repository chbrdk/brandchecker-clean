# BrandChecker Komponenten-Spezifikationen

## Phase 1: Foundation Komponenten

### 1. Input Komponente

#### Props Interface
```typescript
interface InputProps {
  type?: 'text' | 'email' | 'password' | 'number' | 'file' | 'search';
  label?: string;
  placeholder?: string;
  value?: string;
  defaultValue?: string;
  disabled?: boolean;
  required?: boolean;
  error?: string;
  success?: string;
  helpText?: string;
  size?: 'small' | 'medium' | 'large';
  variant?: 'outlined' | 'filled' | 'underlined';
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  onChange?: (value: string) => void;
  onFocus?: () => void;
  onBlur?: () => void;
  className?: string;
  id?: string;
  name?: string;
  autoComplete?: string;
  maxLength?: number;
  minLength?: number;
  pattern?: string;
}
```

#### Features
- **Validierung**: Real-time validation mit error/success states
- **Icons**: Support für Links/Rechts Icons
- **Größen**: Small (32px), Medium (40px), Large (48px)
- **Varianten**: Outlined (Standard), Filled, Underlined
- **Accessibility**: ARIA labels, error announcements
- **File Upload**: Spezielle Behandlung für file type

#### Storybook Stories
- Default
- With Label
- With Error
- With Success
- With Help Text
- With Icon
- Disabled
- Required
- File Upload
- Different Sizes
- Different Variants

### 2. Select/Dropdown Komponente

#### Props Interface
```typescript
interface SelectProps {
  options: Array<{
    value: string | number;
    label: string;
    disabled?: boolean;
    group?: string;
  }>;
  value?: string | number | Array<string | number>;
  placeholder?: string;
  label?: string;
  disabled?: boolean;
  required?: boolean;
  error?: string;
  helpText?: string;
  size?: 'small' | 'medium' | 'large';
  variant?: 'outlined' | 'filled';
  multiple?: boolean;
  searchable?: boolean;
  clearable?: boolean;
  maxHeight?: number;
  onChange?: (value: string | number | Array<string | number>) => void;
  onSearch?: (query: string) => void;
  className?: string;
  id?: string;
  name?: string;
}
```

#### Features
- **Multi-Select**: Unterstützung für mehrere Auswahlen
- **Search**: Suchfunktionalität in Optionen
- **Gruppierung**: Optionen in Gruppen organisieren
- **Custom Rendering**: Custom Option Templates
- **Keyboard Navigation**: Arrow keys, Enter, Escape
- **Accessibility**: Screen reader support

#### Storybook Stories
- Default
- With Label
- Multiple Selection
- Searchable
- With Groups
- With Error
- Disabled
- Clearable
- Custom Options
- Different Sizes

### 3. Card Komponente

#### Props Interface
```typescript
interface CardProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  header?: React.ReactNode;
  footer?: React.ReactNode;
  variant?: 'elevated' | 'outlined' | 'filled';
  padding?: 'none' | 'small' | 'medium' | 'large';
  hoverable?: boolean;
  clickable?: boolean;
  loading?: boolean;
  className?: string;
  onClick?: () => void;
}
```

#### Features
- **Varianten**: Elevated (Shadow), Outlined (Border), Filled (Background)
- **Interaktiv**: Hover effects, click handlers
- **Flexible Content**: Header, Body, Footer sections
- **Loading State**: Skeleton loading
- **Responsive**: Automatische Anpassung

#### Storybook Stories
- Default
- With Title
- With Header and Footer
- Elevated Variant
- Outlined Variant
- Filled Variant
- Hoverable
- Clickable
- Loading State
- Different Padding

### 4. Modal/Dialog Komponente

#### Props Interface
```typescript
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: 'small' | 'medium' | 'large' | 'fullscreen';
  variant?: 'default' | 'confirmation' | 'alert';
  showCloseButton?: boolean;
  closeOnOverlayClick?: boolean;
  closeOnEscape?: boolean;
  footer?: React.ReactNode;
  className?: string;
  overlayClassName?: string;
}
```

#### Features
- **Größen**: Small (400px), Medium (600px), Large (800px), Fullscreen
- **Varianten**: Default, Confirmation, Alert
- **Keyboard Support**: Escape to close
- **Focus Management**: Auto-focus, trap focus
- **Animation**: Smooth open/close transitions
- **Accessibility**: ARIA attributes, focus management

#### Storybook Stories
- Default
- With Title
- Small Size
- Large Size
- Fullscreen
- Confirmation Dialog
- Alert Dialog
- Without Close Button
- Custom Footer
- Long Content

### 5. Button Erweiterungen

#### Erweiterte Props Interface
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger' | 'success' | 'ghost' | 'link';
  size?: 'small' | 'medium' | 'large';
  loading?: boolean;
  disabled?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  fullWidth?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  className?: string;
}
```

#### Neue Features
- **Loading State**: Spinner während Aktionen
- **Icon Support**: Links/Rechts Icons
- **Varianten**: Danger (Rot), Success (Grün), Ghost, Link
- **Full Width**: Button nimmt gesamte Breite ein
- **Accessibility**: ARIA states, keyboard support

### 6. Container Komponente

#### Props Interface
```typescript
interface ContainerProps {
  children: React.ReactNode;
  maxWidth?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'full';
  padding?: 'none' | 'small' | 'medium' | 'large';
  center?: boolean;
  fluid?: boolean;
  className?: string;
}
```

#### Features
- **Max Width**: Responsive Container-Größen
- **Padding**: Konfigurierbare Innenabstände
- **Centering**: Automatische Zentrierung
- **Fluid**: Volle Breite ohne Max-Width
- **Responsive**: Automatische Anpassung

### 7. Grid System

#### Props Interface
```typescript
interface GridProps {
  children: React.ReactNode;
  columns?: number | { xs?: number; sm?: number; md?: number; lg?: number; xl?: number };
  gap?: 'none' | 'small' | 'medium' | 'large';
  className?: string;
}

interface GridItemProps {
  children: React.ReactNode;
  span?: number | { xs?: number; sm?: number; md?: number; lg?: number; xl?: number };
  offset?: number | { xs?: number; sm?: number; md?: number; lg?: number; xl?: number };
  className?: string;
}
```

#### Features
- **Responsive Columns**: Breakpoint-spezifische Spalten
- **Gap Control**: Abstände zwischen Grid-Items
- **Span/Offset**: Flexible Item-Positionierung
- **CSS Grid**: Moderne Grid-Implementierung

## Design Tokens

### Farben
```typescript
const colors = {
  primary: {
    50: '#f0f9ff',
    100: '#e0f2fe',
    500: '#0ea5e9',
    600: '#0284c7',
    700: '#0369a1',
    900: '#0c4a6e',
  },
  secondary: {
    50: '#f8fafc',
    100: '#f1f5f9',
    500: '#64748b',
    600: '#475569',
    700: '#334155',
    900: '#0f172a',
  },
  success: {
    50: '#f0fdf4',
    100: '#dcfce7',
    500: '#22c55e',
    600: '#16a34a',
    700: '#15803d',
    900: '#14532d',
  },
  warning: {
    50: '#fffbeb',
    100: '#fef3c7',
    500: '#f59e0b',
    600: '#d97706',
    700: '#b45309',
    900: '#92400e',
  },
  error: {
    50: '#fef2f2',
    100: '#fee2e2',
    500: '#ef4444',
    600: '#dc2626',
    700: '#b91c1c',
    900: '#991b1b',
  },
};
```

### Typography
```typescript
const typography = {
  fontFamily: {
    sans: ['Inter', 'system-ui', 'sans-serif'],
    mono: ['JetBrains Mono', 'monospace'],
  },
  fontSize: {
    xs: '0.75rem',    // 12px
    sm: '0.875rem',   // 14px
    base: '1rem',     // 16px
    lg: '1.125rem',   // 18px
    xl: '1.25rem',    // 20px
    '2xl': '1.5rem',  // 24px
    '3xl': '1.875rem', // 30px
    '4xl': '2.25rem', // 36px
  },
  fontWeight: {
    light: 300,
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
  lineHeight: {
    tight: 1.25,
    normal: 1.5,
    relaxed: 1.75,
  },
};
```

### Spacing
```typescript
const spacing = {
  0: '0',
  1: '0.25rem',  // 4px
  2: '0.5rem',   // 8px
  3: '0.75rem',  // 12px
  4: '1rem',     // 16px
  5: '1.25rem',  // 20px
  6: '1.5rem',   // 24px
  8: '2rem',     // 32px
  10: '2.5rem',  // 40px
  12: '3rem',    // 48px
  16: '4rem',    // 64px
  20: '5rem',    // 80px
  24: '6rem',    // 96px
};
```

### Breakpoints
```typescript
const breakpoints = {
  xs: '320px',
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
};
```

## Implementierungsplan

### Woche 1: Basis-Komponenten
- [ ] Input Komponente
- [ ] Button Erweiterungen
- [ ] Card Komponente
- [ ] Container Komponente

### Woche 2: Erweiterte Komponenten
- [ ] Select/Dropdown Komponente
- [ ] Modal/Dialog Komponente
- [ ] Grid System
- [ ] Spacer Utilities

### Woche 3: Storybook Integration
- [ ] Stories für alle Komponenten
- [ ] Controls und Actions
- [ ] Documentation
- [ ] Accessibility Testing

### Woche 4: Testing & Polish
- [ ] Unit Tests
- [ ] Visual Regression Tests
- [ ] Performance Testing
- [ ] Documentation Updates

## Nächste Schritte

1. **Design Tokens Setup** - CSS Custom Properties
2. **Komponenten-Implementierung** - TypeScript + CSS Modules
3. **Storybook Stories** - Comprehensive Story Coverage
4. **Testing Setup** - Jest + React Testing Library
5. **Documentation** - Komponenten-Dokumentation
6. **Integration** - Backend-Services Integration
7. **Performance** - Bundle Size Optimization
8. **Accessibility** - WCAG 2.1 AA Compliance
