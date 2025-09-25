import React from 'react';
import './Color.css';

/**
 * Color Component Props
 * 
 * Provides comprehensive color system control with swatches, palettes, pickers, and brand colors.
 * Supports all color variants including primary, secondary, success, warning, error, info, neutral, brand, grey, black, and white.
 * 
 * @interface ColorProps
 */
export interface ColorProps {
  /** Color variant */
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info' | 'neutral' | 'brand' | 'grey' | 'black' | 'white';
  /** Color shade */
  shade?: '50' | '100' | '200' | '300' | '400' | '500' | '600' | '700' | '800' | '900';
  /** Color type */
  type?: 'background' | 'text' | 'border' | 'accent';
  /** Whether to show color name */
  showName?: boolean;
  /** Whether to show color value */
  showValue?: boolean;
  /** Whether to show color code */
  showCode?: boolean;
  /** Custom color value */
  customColor?: string;
  /** Additional CSS class */
  className?: string;
  /** Children content */
  children?: React.ReactNode;
  /** Additional props */
  [key: string]: any;
}

/**
 * ColorSwatch Component
 * 
 * Displays a single color swatch with optional details like name, value, and CSS code.
 * Supports all color variants and shades from the design system.
 * 
 * Features:
 * - All color variants (primary, secondary, success, warning, error, info, neutral, brand, grey, black, white)
 * - All color shades (50-900)
 * - Optional color information display (name, value, CSS code)
 * - Custom color support
 * - Responsive design
 * - Accessibility-friendly
 * 
 * @param props - ColorProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * // Basic color swatch
 * <ColorSwatch variant="primary" shade="500" />
 * 
 * // With details
 * <ColorSwatch variant="success" shade="600" showName showValue showCode />
 * 
 * // Custom color
 * <ColorSwatch customColor="#ff6b6b" showName showValue />
 * ```
 */
export const ColorSwatch = ({
  variant = 'primary',
  shade = '500',
  type = 'background',
  showName = false,
  showValue = false,
  showCode = false,
  customColor,
  className = '',
  children,
  ...props
}: ColorProps) => {
  const classes = [
    'color-swatch',
    `color-swatch--${variant}`,
    `color-swatch--${shade}`,
    `color-swatch--${type}`,
    className
  ].filter(Boolean).join(' ');

  const getColorValue = () => {
    if (customColor) return customColor;
    return `var(--color-${variant}-${shade})`;
  };

  const getColorName = () => {
    if (customColor) return 'Custom';
    return `${variant.charAt(0).toUpperCase() + variant.slice(1)} ${shade}`;
  };

  const getColorCode = () => {
    if (customColor) return customColor;
    return `--color-${variant}-${shade}`;
  };

  return (
    <div className={classes} {...props}>
      <div 
        className="color-swatch__preview"
        style={{ backgroundColor: getColorValue() }}
      />
      {(showName || showValue || showCode || children) && (
        <div className="color-swatch__info">
          {showName && (
            <div className="color-swatch__name">{getColorName()}</div>
          )}
          {showValue && (
            <div className="color-swatch__value">{getColorValue()}</div>
          )}
          {showCode && (
            <div className="color-swatch__code">{getColorCode()}</div>
          )}
          {children}
        </div>
      )}
    </div>
  );
};

/** Color Palette Component */
/**
 * Color Palette Props
 * 
 * Props for displaying a complete color palette with all shades of a specific color variant.
 * 
 * @interface ColorPaletteProps
 */
export interface ColorPaletteProps {
  /** Color variant */
  variant: 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info' | 'neutral' | 'grey' | 'black' | 'white';
  /** Whether to show color names */
  showNames?: boolean;
  /** Whether to show color values */
  showValues?: boolean;
  /** Whether to show color codes */
  showCodes?: boolean;
  /** Additional CSS class */
  className?: string;
}

/**
 * ColorPalette Component
 * 
 * Displays a complete color palette with all shades (50-900) of a specific color variant.
 * Useful for showcasing the full range of a color in the design system.
 * 
 * Features:
 * - Complete color shade range (50-900)
 * - Configurable information display
 * - Responsive grid layout
 * - Consistent styling
 * 
 * @param props - ColorPaletteProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * <ColorPalette variant="primary" showNames showValues />
 * <ColorPalette variant="grey" showNames />
 * ```
 */
export const ColorPalette = ({
  variant,
  showNames = true,
  showValues = false,
  showCodes = false,
  className = '',
  ...props
}: ColorPaletteProps) => {
  const shades = ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'];
  
  const classes = [
    'color-palette',
    `color-palette--${variant}`,
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={classes} {...props}>
      <div className="color-palette__header">
        <h3 className="color-palette__title">
          {variant.charAt(0).toUpperCase() + variant.slice(1)} Colors
        </h3>
      </div>
      <div className="color-palette__swatches">
        {shades.map(shade => (
          <ColorSwatch
            key={shade}
            variant={variant}
            shade={shade as any}
            showName={showNames}
            showValue={showValues}
            showCode={showCodes}
          />
        ))}
      </div>
    </div>
  );
};

/** Color Picker Component */
export interface ColorPickerProps {
  /** Selected color */
  value?: string;
  /** Color change handler */
  onChange?: (color: string) => void;
  /** Available colors */
  colors?: string[];
  /** Whether to show custom color input */
  showCustom?: boolean;
  /** Additional CSS class */
  className?: string;
}

export const ColorPicker = ({
  value = '#000000',
  onChange,
  colors = [
    '#ef4444', '#f97316', '#f59e0b', '#eab308', '#84cc16',
    '#22c55e', '#10b981', '#14b8a6', '#06b6d4', '#0ea5e9',
    '#3b82f6', '#6366f1', '#8b5cf6', '#a855f7', '#d946ef',
    '#ec4899', '#f43f5e', '#64748b', '#6b7280', '#374151'
  ],
  showCustom = true,
  className = '',
  ...props
}: ColorPickerProps) => {
  const classes = [
    'color-picker',
    className
  ].filter(Boolean).join(' ');

  const handleColorClick = (color: string) => {
    onChange?.(color);
  };

  const handleCustomChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange?.(e.target.value);
  };

  return (
    <div className={classes} {...props}>
      <div className="color-picker__grid">
        {colors.map(color => (
          <button
            key={color}
            type="button"
            className={`color-picker__swatch ${value === color ? 'color-picker__swatch--selected' : ''}`}
            style={{ backgroundColor: color }}
            onClick={() => handleColorClick(color)}
            aria-label={`Select color ${color}`}
          />
        ))}
      </div>
      {showCustom && (
        <div className="color-picker__custom">
          <label className="color-picker__label">Custom Color:</label>
          <input
            type="color"
            value={value}
            onChange={handleCustomChange}
            className="color-picker__input"
          />
        </div>
      )}
    </div>
  );
};

/** Brand Color Component */
export interface BrandColorProps {
  /** Brand color type */
  type?: 'primary' | 'secondary' | 'accent' | 'neutral';
  /** Whether to show color information */
  showInfo?: boolean;
  /** Additional CSS class */
  className?: string;
}

export const BrandColor = ({
  type = 'primary',
  showInfo = true,
  className = '',
  ...props
}: BrandColorProps) => {
  const classes = [
    'brand-color',
    `brand-color--${type}`,
    className
  ].filter(Boolean).join(' ');

  const getBrandColor = () => {
    switch (type) {
      case 'primary': return 'var(--color-brand-primary)';
      case 'secondary': return 'var(--color-brand-secondary)';
      case 'accent': return 'var(--color-brand-accent)';
      case 'neutral': return 'var(--color-brand-neutral)';
      default: return 'var(--color-brand-primary)';
    }
  };

  const getBrandColorName = () => {
    switch (type) {
      case 'primary': return 'Primary Brand Color';
      case 'secondary': return 'Secondary Brand Color';
      case 'accent': return 'Accent Brand Color';
      case 'neutral': return 'Neutral Brand Color';
      default: return 'Primary Brand Color';
    }
  };

  return (
    <div className={classes} {...props}>
      <div 
        className="brand-color__preview"
        style={{ backgroundColor: getBrandColor() }}
      />
      {showInfo && (
        <div className="brand-color__info">
          <div className="brand-color__name">{getBrandColorName()}</div>
          <div className="brand-color__value">{getBrandColor()}</div>
        </div>
      )}
    </div>
  );
};
