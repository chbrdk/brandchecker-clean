import React from 'react';
import { Typography } from '../Typography';
import './ColorSwatch.css';

/**
 * Color Data Interface
 */
export interface ColorData {
  hex: string;
  name?: string;
  usage_percentage?: number;
  usage_count?: number;
  rgb?: [number, number, number];
  description?: string;
}

/**
 * ColorSwatch Props
 */
export interface ColorSwatchProps {
  /** Color data */
  color: ColorData;
  /** Size variant */
  size?: 'sm' | 'md' | 'lg';
  /** Show color name */
  showName?: boolean;
  /** Show usage percentage */
  showPercentage?: boolean;
  /** Show usage count */
  showCount?: boolean;
  /** Show RGB values */
  showRgb?: boolean;
  /** Show description */
  showDescription?: boolean;
  /** Click handler */
  onClick?: (color: ColorData) => void;
  /** Additional CSS class */
  className?: string;
}

/**
 * ColorSwatch Component
 * 
 * Displays a single color swatch with detailed information from PDF extraction.
 * Shows hex color, name, usage statistics, and RGB values.
 * 
 * Features:
 * - Multiple sizes (sm, md, lg)
 * - Configurable information display
 * - Click interaction
 * - Usage statistics
 * - RGB color information
 * - Responsive design
 * - Design token integration
 * 
 * @param props - ColorSwatchProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * // Basic color swatch
 * <ColorSwatch 
 *   color={{ hex: '#ff6b6b', name: 'Red', usage_percentage: 24.5 }} 
 * />
 * 
 * // With all details
 * <ColorSwatch 
 *   color={colorData}
 *   size="lg"
 *   showName
 *   showPercentage
 *   showCount
 *   showRgb
 *   onClick={handleColorClick}
 * />
 * ```
 */
export const ColorSwatch = ({
  color,
  size = 'md',
  showName = true,
  showPercentage = true,
  showCount = false,
  showRgb = false,
  showDescription = false,
  onClick,
  className = ''
}: ColorSwatchProps) => {
  const classes = [
    'color-swatch',
    `color-swatch--${size}`,
    onClick && 'color-swatch--clickable',
    className
  ].filter(Boolean).join(' ');

  const handleClick = () => {
    onClick?.(color);
  };

  const formatRgb = (rgb: [number, number, number]) => {
    return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
  };

  const getContrastColor = (hex: string) => {
    // Simple contrast calculation
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    const brightness = (r * 299 + g * 587 + b * 114) / 1000;
    return brightness > 128 ? '#000000' : '#ffffff';
  };

  return (
    <div
      className={classes}
      onClick={handleClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      style={{
        '--color-swatch-bg': color.hex,
        '--color-swatch-text': getContrastColor(color.hex)
      } as React.CSSProperties}
    >
      <div className="color-swatch__preview">
        <div 
          className="color-swatch__color"
          style={{ backgroundColor: color.hex }}
        />
      </div>
      
      <div className="color-swatch__info">
        {showName && color.name && (
          <Typography 
            variant="body" 
            size={size === 'sm' ? 'xs' : size === 'lg' ? 'sm' : 'xs'} 
            weight="medium"
            className="color-swatch__name"
          >
            {color.name}
          </Typography>
        )}
        
        <Typography 
          variant="body" 
          size={size === 'sm' ? 'xs' : size === 'lg' ? 'sm' : 'xs'} 
          weight="semibold"
          className="color-swatch__hex"
        >
          {color.hex.toUpperCase()}
        </Typography>
        
        {showPercentage && color.usage_percentage !== undefined && (
          <Typography 
            variant="caption" 
            size="xs" 
            color="secondary"
            className="color-swatch__percentage"
          >
            {color.usage_percentage.toFixed(1)}%
          </Typography>
        )}
        
        {showCount && color.usage_count !== undefined && (
          <Typography 
            variant="caption" 
            size="xs" 
            color="secondary"
            className="color-swatch__count"
          >
            {color.usage_count.toLocaleString()}x
          </Typography>
        )}
        
        {showRgb && color.rgb && (
          <Typography 
            variant="caption" 
            size="xs" 
            color="secondary"
            className="color-swatch__rgb"
          >
            {formatRgb(color.rgb)}
          </Typography>
        )}
        
        {showDescription && color.description && (
          <Typography 
            variant="caption" 
            size="xs" 
            color="secondary"
            className="color-swatch__description"
          >
            {color.description}
          </Typography>
        )}
      </div>
    </div>
  );
};

ColorSwatch.displayName = 'ColorSwatch';
