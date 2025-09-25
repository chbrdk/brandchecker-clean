import React from 'react';
import { Icon } from '../Icon';
import type { IconName } from '../Icon';
import './Chip.css';

export interface ChipProps {
  /** Chip content */
  children: React.ReactNode;
  /** Chip variant */
  variant?: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info';
  /** Chip size */
  size?: 'small' | 'medium' | 'large';
  /** Whether the chip is removable */
  removable?: boolean;
  /** Whether the chip is disabled */
  disabled?: boolean;
  /** Whether the chip is selected */
  selected?: boolean;
  /** Whether the chip is clickable */
  clickable?: boolean;
  /** Icon to display */
  icon?: IconName;
  /** Icon position */
  iconPosition?: 'left' | 'right';
  /** Avatar to display */
  avatar?: React.ReactNode;
  /** Click handler */
  onClick?: () => void;
  /** Remove handler */
  onRemove?: () => void;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

/** Chip/Tag Component */
export const Chip = ({
  children,
  variant = 'default',
  size = 'medium',
  removable = false,
  disabled = false,
  selected = false,
  clickable = false,
  icon,
  iconPosition = 'left',
  avatar,
  onClick,
  onRemove,
  className = '',
  ...props
}: ChipProps) => {
  const isInteractive = clickable || removable;
  
  const classes = [
    'chip',
    `chip--${variant}`,
    `chip--${size}`,
    removable && 'chip--removable',
    disabled && 'chip--disabled',
    selected && 'chip--selected',
    clickable && 'chip--clickable',
    isInteractive && 'chip--interactive',
    className
  ].filter(Boolean).join(' ');

  const handleClick = () => {
    if (disabled) return;
    onClick?.();
  };

  const handleRemove = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (disabled) return;
    onRemove?.();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (disabled) return;
    
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    } else if (e.key === 'Delete' || e.key === 'Backspace') {
      e.preventDefault();
      onRemove?.();
    }
  };

  const content = (
    <>
      {avatar && (
        <span className="chip__avatar" aria-hidden="true">
          {avatar}
        </span>
      )}
      
      {icon && iconPosition === 'left' && (
        <span className="chip__icon chip__icon--left" aria-hidden="true">
          <Icon name={icon} size="xs" />
        </span>
      )}
      
      <span className="chip__text">{children}</span>
      
      {icon && iconPosition === 'right' && (
        <span className="chip__icon chip__icon--right" aria-hidden="true">
          <Icon name={icon} size="xs" />
        </span>
      )}
      
      {removable && (
        <button
          type="button"
          className="chip__remove"
          onClick={handleRemove}
          disabled={disabled}
          aria-label={`Remove ${children}`}
        >
          <Icon name="x" size="xs" />
        </button>
      )}
    </>
  );

  if (clickable) {
    return (
      <button
        type="button"
        className={classes}
        onClick={handleClick}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        aria-pressed={selected}
        {...props}
      >
        {content}
      </button>
    );
  }

  return (
    <span
      className={classes}
      role={isInteractive ? 'button' : undefined}
      tabIndex={isInteractive && !disabled ? 0 : undefined}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      aria-pressed={selected}
      {...props}
    >
      {content}
    </span>
  );
};

/** Chip Group Component */
export interface ChipGroupProps {
  /** Chip group children */
  children: React.ReactNode;
  /** Chip group alignment */
  align?: 'left' | 'center' | 'right';
  /** Chip group spacing */
  spacing?: 'none' | 'small' | 'medium' | 'large';
  /** Whether chips wrap to new lines */
  wrap?: boolean;
  /** Additional CSS class */
  className?: string;
}

export const ChipGroup = ({
  children,
  align = 'left',
  spacing = 'medium',
  wrap = true,
  className = '',
  ...props
}: ChipGroupProps) => {
  const classes = [
    'chip-group',
    `chip-group--align-${align}`,
    `chip-group--spacing-${spacing}`,
    wrap && 'chip-group--wrap',
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={classes} {...props}>
      {children}
    </div>
  );
};
