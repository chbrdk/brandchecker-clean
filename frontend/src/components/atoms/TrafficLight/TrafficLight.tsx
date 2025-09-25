import React from 'react';
import { Typography } from '../Typography';
import { Icon } from '../Icon';
import type { IconName } from '../Icon';
import './TrafficLight.css';

/**
 * Traffic Light Status
 */
export type TrafficLightStatus = 'error' | 'warning' | 'success';

/**
 * Traffic Light Props
 */
export interface TrafficLightProps {
  /** Status type */
  status: TrafficLightStatus;
  /** Status label */
  label?: string;
  /** Show label */
  showLabel?: boolean;
  /** Size */
  size?: 'sm' | 'md' | 'lg';
  /** Icon name (overrides default) */
  iconName?: IconName;
  /** Additional CSS class */
  className?: string;
}

/**
 * Traffic Light Component
 * 
 * Displays a status indicator with color coding and optional label.
 * Uses red/yellow/green color scheme for error/warning/success states.
 * 
 * Features:
 * - Three status types (error, warning, success)
 * - Color-coded indicators
 * - Optional labels and icons
 * - Multiple sizes
 * - Responsive design
 * 
 * @param props - TrafficLightProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * // Basic status
 * <TrafficLight status="success" label="All Good" />
 * 
 * // Warning with custom icon
 * <TrafficLight status="warning" iconName="alert-triangle" />
 * 
 * // Error without label
 * <TrafficLight status="error" showLabel={false} />
 * ```
 */
export const TrafficLight = ({
  status,
  label,
  showLabel = true,
  size = 'md',
  iconName,
  className = ''
}: TrafficLightProps) => {
  const classes = [
    'traffic-light',
    `traffic-light--${status}`,
    `traffic-light--${size}`,
    className
  ].filter(Boolean).join(' ');

  const getStatusConfig = () => {
    switch (status) {
      case 'error':
        return {
          color: 'var(--color-status-error)',
          bgColor: 'var(--color-status-error-bg)',
          borderColor: 'var(--color-status-error-border)',
          defaultIcon: 'alert-circle' as IconName,
          defaultLabel: 'Kritisch'
        };
      case 'warning':
        return {
          color: 'var(--color-status-warning)',
          bgColor: 'var(--color-status-warning-bg)',
          borderColor: 'var(--color-status-warning-border)',
          defaultIcon: 'info' as IconName,
          defaultLabel: 'Verbesserung'
        };
      case 'success':
        return {
          color: 'var(--color-status-success)',
          bgColor: 'var(--color-status-success-bg)',
          borderColor: 'var(--color-status-success-border)',
          defaultIcon: 'check-circle' as IconName,
          defaultLabel: 'Gut'
        };
    }
  };

  const config = getStatusConfig();
  const displayLabel = label || config.defaultLabel;
  const displayIcon = iconName || config.defaultIcon;

  const getIconSize = () => {
    switch (size) {
      case 'sm': return 'xs';
      case 'lg': return 'sm';
      default: return 'xs';
    }
  };

  return (
    <div 
      className={classes}
      style={{
        '--traffic-light-color': config.color,
        '--traffic-light-bg': config.bgColor,
        '--traffic-light-border': config.borderColor
      } as React.CSSProperties}
    >
      <div className="traffic-light__indicator">
        <Icon 
          name={displayIcon} 
          size={getIconSize()}
        />
      </div>
      
      {showLabel && displayLabel && (
        <div className="traffic-light__label">
          <Typography 
            variant="caption" 
            size={size === 'sm' ? 'xs' : 'sm'}
            weight="medium"
          >
            {displayLabel}
          </Typography>
        </div>
      )}
    </div>
  );
};

TrafficLight.displayName = 'TrafficLight';
