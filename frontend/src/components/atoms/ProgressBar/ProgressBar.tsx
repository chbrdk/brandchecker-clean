import React from 'react';
import { Typography } from '../Typography';
import './ProgressBar.css';

/**
 * Progress Bar Variant
 */
export type ProgressBarVariant = 'linear' | 'circular';

/**
 * Progress Bar Props
 */
export interface ProgressBarProps {
  /** Progress value (0-100) */
  value: number;
  /** Maximum value (default: 100) */
  max?: number;
  /** Progress bar variant */
  variant?: ProgressBarVariant;
  /** Size */
  size?: 'sm' | 'md' | 'lg';
  /** Show percentage label */
  showPercentage?: boolean;
  /** Custom label */
  label?: string;
  /** Show label */
  showLabel?: boolean;
  /** Color variant */
  color?: 'primary' | 'success' | 'warning' | 'error';
  /** Custom color */
  customColor?: string;
  /** Additional CSS class */
  className?: string;
}

/**
 * Progress Bar Component
 * 
 * Displays progress with linear or circular variants.
 * Supports different colors, sizes, and optional labels.
 * 
 * Features:
 * - Linear and circular variants
 * - Multiple sizes and colors
 * - Optional percentage and custom labels
 * - Smooth animations
 * - Responsive design
 * 
 * @param props - ProgressBarProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * // Basic linear progress
 * <ProgressBar value={75} />
 * 
 * // Circular progress with label
 * <ProgressBar value={60} variant="circular" label="Loading..." showPercentage />
 * 
 * // Custom color
 * <ProgressBar value={85} color="success" customColor="#10b981" />
 * ```
 */
export const ProgressBar = ({
  value,
  max = 100,
  variant = 'linear',
  size = 'md',
  showPercentage = false,
  label,
  showLabel = true,
  color = 'primary',
  customColor,
  className = ''
}: ProgressBarProps) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);
  
  const classes = [
    'progress-bar',
    `progress-bar--${variant}`,
    `progress-bar--${size}`,
    `progress-bar--${color}`,
    className
  ].filter(Boolean).join(' ');

  const getProgressColor = () => {
    if (customColor) return customColor;
    
    switch (color) {
      case 'success': return 'var(--color-status-success)';
      case 'warning': return 'var(--color-status-warning)';
      case 'error': return 'var(--color-status-error)';
      default: return 'var(--color-primary-500)';
    }
  };

  const renderLinearProgress = () => (
    <div className="progress-bar__container">
      <div className="progress-bar__track">
        <div 
          className="progress-bar__fill"
          style={{ 
            width: `${percentage}%`,
            backgroundColor: getProgressColor()
          }}
        />
      </div>
      
      {(showPercentage || label) && (
        <div className="progress-bar__labels">
          {showPercentage && (
            <Typography 
              variant="caption" 
              size={size === 'sm' ? 'xs' : 'sm'}
              color="secondary"
            >
              {Math.round(percentage)}%
            </Typography>
          )}
          {showLabel && label && (
            <Typography 
              variant="caption" 
              size={size === 'sm' ? 'xs' : 'sm'}
              color="primary"
            >
              {label}
            </Typography>
          )}
        </div>
      )}
    </div>
  );

  const renderCircularProgress = () => {
    const radius = size === 'sm' ? 20 : size === 'lg' ? 40 : 30;
    const strokeWidth = size === 'sm' ? 3 : size === 'lg' ? 6 : 4;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (percentage / 100) * circumference;

    return (
      <div className="progress-bar__circular-container">
        <svg 
          className="progress-bar__circular-svg"
          width={radius * 2 + strokeWidth * 2} 
          height={radius * 2 + strokeWidth * 2}
        >
          <circle
            className="progress-bar__circular-track"
            cx={radius + strokeWidth}
            cy={radius + strokeWidth}
            r={radius}
            strokeWidth={strokeWidth}
          />
          <circle
            className="progress-bar__circular-fill"
            cx={radius + strokeWidth}
            cy={radius + strokeWidth}
            r={radius}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            style={{ stroke: getProgressColor() }}
          />
        </svg>
        
        {(showPercentage || label) && (
          <div className="progress-bar__circular-content">
            {showPercentage && (
              <Typography 
                variant="caption" 
                size={size === 'sm' ? 'xs' : size === 'lg' ? 'sm' : 'xs'}
                weight="semibold"
                color="primary"
              >
                {Math.round(percentage)}%
              </Typography>
            )}
            {showLabel && label && (
              <Typography 
                variant="caption" 
                size="xs"
                color="secondary"
              >
                {label}
              </Typography>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className={classes}>
      {variant === 'linear' ? renderLinearProgress() : renderCircularProgress()}
    </div>
  );
};

ProgressBar.displayName = 'ProgressBar';
