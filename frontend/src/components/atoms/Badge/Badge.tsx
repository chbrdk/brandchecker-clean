import React from 'react';
import { Icon } from '../Icon';
import type { IconName } from '../Icon';
import './Badge.css';

export interface BadgeProps {
  /** Badge content */
  children?: React.ReactNode;
  /** Badge variant */
  variant?: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info' | 'neutral';
  /** Badge size */
  size?: 'small' | 'medium' | 'large';
  /** Badge type */
  type?: 'count' | 'status' | 'notification' | 'dot';
  /** Whether the badge is visible */
  visible?: boolean;
  /** Maximum count to display */
  maxCount?: number;
  /** Icon to display */
  icon?: IconName;
  /** Whether the badge is clickable */
  clickable?: boolean;
  /** Click handler */
  onClick?: () => void;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

/** Badge Component */
export const Badge = ({
  children,
  variant = 'default',
  size = 'medium',
  type = 'count',
  visible = true,
  maxCount = 99,
  icon,
  clickable = false,
  onClick,
  className = '',
  ...props
}: BadgeProps) => {
  if (!visible) return null;

  const classes = [
    'badge',
    `badge--${variant}`,
    `badge--${size}`,
    `badge--${type}`,
    clickable && 'badge--clickable',
    className
  ].filter(Boolean).join(' ');

  const handleClick = () => {
    if (clickable) {
      onClick?.();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (clickable && (e.key === 'Enter' || e.key === ' ')) {
      e.preventDefault();
      handleClick();
    }
  };

  const renderContent = () => {
    if (type === 'dot') {
      return null; // Dot badges don't have content
    }

    if (type === 'count' && typeof children === 'number') {
      const count = children > maxCount ? `${maxCount}+` : children.toString();
      return <span className="badge__count">{count}</span>;
    }

    if (icon) {
      return (
        <>
          <Icon name={icon} size="xs" />
          {children && <span className="badge__text">{children}</span>}
        </>
      );
    }

    return <span className="badge__text">{children}</span>;
  };

  const content = (
    <>
      {renderContent()}
    </>
  );

  if (clickable) {
    return (
      <button
        type="button"
        className={classes}
        onClick={handleClick}
        onKeyDown={handleKeyDown}
        aria-label={typeof children === 'string' ? children : 'Badge'}
        {...props}
      >
        {content}
      </button>
    );
  }

  return (
    <span
      className={classes}
      role={type === 'notification' ? 'alert' : undefined}
      aria-label={typeof children === 'string' ? children : 'Badge'}
      {...props}
    >
      {content}
    </span>
  );
};

/** Notification Badge Component */
export interface NotificationBadgeProps {
  /** Number of notifications */
  count?: number;
  /** Maximum count to display */
  maxCount?: number;
  /** Whether the badge is visible */
  visible?: boolean;
  /** Click handler */
  onClick?: () => void;
  /** Additional CSS class */
  className?: string;
}

export const NotificationBadge = ({
  count = 0,
  maxCount = 99,
  visible = true,
  onClick,
  className = '',
  ...props
}: NotificationBadgeProps) => {
  return (
    <Badge
      type="notification"
      variant={count > 0 ? 'error' : 'neutral'}
      size="small"
      visible={visible && count > 0}
      clickable={!!onClick}
      onClick={onClick}
      className={className}
      {...props}
    >
      {count}
    </Badge>
  );
};

/** Status Badge Component */
export interface StatusBadgeProps {
  /** Status text */
  status: string;
  /** Status variant */
  variant?: 'success' | 'warning' | 'error' | 'info' | 'neutral';
  /** Status icon */
  icon?: IconName;
  /** Additional CSS class */
  className?: string;
}

export const StatusBadge = ({
  status,
  variant = 'neutral',
  icon,
  className = '',
  ...props
}: StatusBadgeProps) => {
  return (
    <Badge
      type="status"
      variant={variant}
      size="small"
      icon={icon}
      className={className}
      {...props}
    >
      {status}
    </Badge>
  );
};
