import React from 'react';
import { Typography } from '../Typography';
import { Score } from '../Score';
import { TrafficLight } from '../TrafficLight';
import { ProgressBar } from '../ProgressBar';
import { Icon } from '../Icon';
import type { IconName } from '../Icon';
import './MetricCard.css';

/**
 * Metric Card Type
 */
export type MetricCardType = 'score' | 'traffic-light' | 'progress' | 'custom';

/**
 * Metric Card Props
 */
export interface MetricCardProps {
  /** Metric type */
  type: MetricCardType;
  /** Metric title */
  title: string;
  /** Metric description */
  description?: string;
  /** Metric value */
  value: number;
  /** Maximum value (for score/progress) */
  max?: number;
  /** Traffic light status */
  status?: 'success' | 'warning' | 'error';
  /** Progress bar variant */
  progressVariant?: 'linear' | 'circular';
  /** Show percentage */
  showPercentage?: boolean;
  /** Custom label */
  label?: string;
  /** Icon name */
  iconName?: IconName;
  /** Size */
  size?: 'sm' | 'md' | 'lg';
  /** Color variant */
  color?: 'primary' | 'success' | 'warning' | 'error';
  /** Custom color */
  customColor?: string;
  /** Additional CSS class */
  className?: string;
  /** Click handler */
  onClick?: () => void;
  /** Children content */
  children?: React.ReactNode;
}

/**
 * Metric Card Component
 * 
 * Displays metrics in a card format with different visualization types.
 * Combines Score, TrafficLight, and ProgressBar components for unified metric display.
 * 
 * Features:
 * - Multiple metric types (score, traffic-light, progress, custom)
 * - Consistent card layout with title and description
 * - Icon support
 * - Click interaction
 * - Responsive design
 * - Design token integration
 * 
 * @param props - MetricCardProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * // Score metric
 * <MetricCard 
 *   type="score" 
 *   title="Brand Consistency" 
 *   value={85} 
 *   description="Overall brand adherence score" 
 * />
 * 
 * // Traffic light metric
 * <MetricCard 
 *   type="traffic-light" 
 *   title="Color Usage" 
 *   status="warning" 
 *   description="Needs attention" 
 * />
 * 
 * // Progress metric
 * <MetricCard 
 *   type="progress" 
 *   title="Analysis Progress" 
 *   value={60} 
 *   progressVariant="circular" 
 *   showPercentage 
 * />
 * ```
 */
export const MetricCard = ({
  type,
  title,
  description,
  value,
  max = 100,
  status,
  progressVariant = 'linear',
  showPercentage = false,
  label,
  iconName,
  size = 'md',
  color = 'primary',
  customColor,
  className = '',
  onClick,
  children
}: MetricCardProps) => {
  const classes = [
    'metric-card',
    `metric-card--${type}`,
    `metric-card--${size}`,
    `metric-card--${color}`,
    onClick && 'metric-card--clickable',
    className
  ].filter(Boolean).join(' ');

  const renderMetric = () => {
    switch (type) {
      case 'score':
        return (
          <Score
            value={value}
            max={max}
            label={label}
            size={size}
            showPercentage={showPercentage}
            iconName={iconName}
            className="metric-card__metric"
          />
        );
      
      case 'traffic-light':
        return (
          <TrafficLight
            status={status || 'success'}
            label={label}
            size={size}
            iconName={iconName}
            className="metric-card__metric"
          />
        );
      
      case 'progress':
        return (
          <ProgressBar
            value={value}
            max={max}
            variant={progressVariant}
            size={size}
            showPercentage={showPercentage}
            label={label}
            color={color}
            customColor={customColor}
            className="metric-card__metric"
          />
        );
      
      case 'custom':
        return (
          <div className="metric-card__custom">
            {children}
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div
      className={classes}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      aria-label={`${title}: ${description || ''}`}
    >
      <div className="metric-card__header">
        {iconName && (
          <div className="metric-card__icon">
            <Icon name={iconName} size={size === 'sm' ? 'sm' : 'md'} />
          </div>
        )}
        <div className="metric-card__title">
          <Typography 
            variant="h3" 
            size={size === 'sm' ? 'sm' : size === 'lg' ? 'lg' : 'md'} 
            weight="semibold"
            color="primary"
          >
            {title}
          </Typography>
        </div>
      </div>
      
      {description && (
        <div className="metric-card__description">
          <Typography 
            variant="body" 
            size={size === 'sm' ? 'xs' : 'sm'} 
            color="secondary"
          >
            {description}
          </Typography>
        </div>
      )}
      
      <div className="metric-card__content">
        {renderMetric()}
      </div>
    </div>
  );
};

MetricCard.displayName = 'MetricCard';
