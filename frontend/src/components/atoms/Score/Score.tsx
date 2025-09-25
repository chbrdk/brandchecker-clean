import React from 'react';
import { Typography } from '../Typography';
import { Icon } from '../Icon';
import type { IconName } from '../Icon';
import './Score.css';

/**
 * Score Component Props
 */
export interface ScoreProps {
  /** Score value (0-100) */
  value: number;
  /** Maximum score (default: 100) */
  max?: number;
  /** Score label */
  label?: string;
  /** Score size */
  size?: 'sm' | 'md' | 'lg' | 'xl';
  /** Show label */
  showLabel?: boolean;
  /** Show percentage */
  showPercentage?: boolean;
  /** Icon name */
  iconName?: IconName;
  /** Custom color */
  color?: string;
  /** Additional CSS class */
  className?: string;
}

/**
 * Score Component
 * 
 * Displays a score value with color coding, label, and optional icon.
 * Automatically determines color based on score percentage (red < 50%, yellow 50-80%, green > 80%).
 * 
 * Features:
 * - Color-coded scoring (red/yellow/green)
 * - Multiple sizes (sm, md, lg, xl)
 * - Optional label and percentage display
 * - Icon support
 * - Custom color override
 * - Responsive design
 * 
 * @param props - ScoreProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * // Basic score
 * <Score value={85} label="Brand Consistency" />
 * 
 * // Large score with icon
 * <Score value={72} size="lg" iconName="star" showPercentage />
 * 
 * // Custom color
 * <Score value={95} color="#8b5cf6" />
 * ```
 */
export const Score = ({
  value,
  max = 100,
  label,
  size = 'md',
  showLabel = true,
  showPercentage = false,
  iconName,
  color,
  className = ''
}: ScoreProps) => {
  const percentage = Math.round((value / max) * 100);
  
  const classes = [
    'score',
    `score--${size}`,
    className
  ].filter(Boolean).join(' ');

  // Determine color based on percentage
  const getScoreColor = () => {
    if (color) return color;
    if (percentage < 50) return 'var(--color-status-error)';
    if (percentage < 80) return 'var(--color-status-warning)';
    return 'var(--color-status-success)';
  };

  const getScoreStatus = () => {
    if (percentage < 50) return 'poor';
    if (percentage < 80) return 'fair';
    return 'excellent';
  };

  const getScoreIcon = (): IconName => {
    if (iconName) return iconName;
    if (percentage < 50) return 'alert-circle';
    if (percentage < 80) return 'info';
    return 'check-circle';
  };

  const renderScoreValue = () => {
    const displayValue = showPercentage ? `${percentage}%` : value.toString();
    
    return (
      <div className="score__value" style={{ color: getScoreColor() }}>
        <Typography 
          variant="h1" 
          size={size === 'sm' ? 'sm' : size === 'lg' ? 'lg' : size === 'xl' ? 'xl' : 'md'}
          weight="bold"
        >
          {displayValue}
        </Typography>
      </div>
    );
  };

  const renderIcon = () => {
    if (!iconName && !showLabel) return null;
    
    const iconSize = size === 'sm' ? 'xs' : size === 'lg' ? 'sm' : size === 'xl' ? 'md' : 'xs';
    
    return (
      <div className="score__icon" style={{ color: getScoreColor() }}>
        <Icon name={getScoreIcon()} size={iconSize} />
      </div>
    );
  };

  const renderLabel = () => {
    if (!showLabel || !label) return null;
    
    return (
      <div className="score__label">
        <Typography 
          variant="caption" 
          size={size === 'sm' ? 'xs' : 'sm'}
          color="secondary"
        >
          {label}
        </Typography>
      </div>
    );
  };

  return (
    <div className={classes} data-status={getScoreStatus()}>
      <div className="score__content">
        {renderIcon()}
        {renderScoreValue()}
      </div>
      {renderLabel()}
    </div>
  );
};

Score.displayName = 'Score';
