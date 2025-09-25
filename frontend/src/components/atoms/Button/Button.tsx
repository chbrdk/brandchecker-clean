import React from 'react';
import { Icon } from '../Icon';
import type { IconName } from '../Icon';
import { Typography } from '../Typography';
import './Button.css';

/**
 * Button Component Props
 * 
 * Comprehensive button component with multiple variants, sizes, states, and icon support.
 * Integrates with the Icon library and Typography system for consistent styling.
 * 
 * @interface ButtonProps
 */
export interface ButtonProps {
  /** Button variant */
  variant?: 'primary' | 'secondary' | 'danger' | 'success' | 'ghost' | 'link';
  /** Button size */
  size?: 'small' | 'medium' | 'large';
  /** Loading state */
  loading?: boolean;
  /** Disabled state */
  disabled?: boolean;
  /** Icon element */
  icon?: React.ReactNode;
  /** Icon name from icon library */
  iconName?: IconName;
  /** Icon position */
  iconPosition?: 'left' | 'right';
  /** Full width button */
  fullWidth?: boolean;
  /** Button content */
  children?: React.ReactNode;
  /** Click handler */
  onClick?: () => void;
  /** Button type */
  type?: 'button' | 'submit' | 'reset';
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

/**
 * Button Component
 * 
 * A comprehensive button component with multiple variants, sizes, states, and icon support.
 * Integrates with the Icon library and Typography system for consistent styling across the application.
 * 
 * Features:
 * - Multiple variants (primary, secondary, danger, success, ghost, link)
 * - Three sizes (small, medium, large)
 * - Loading state with spinner
 * - Icon support (left/right positioning)
 * - Typography system integration
 * - Accessibility features
 * - Full width option
 * - Disabled state
 * 
 * @param props - ButtonProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * // Basic button
 * <Button variant="primary" size="medium">Click me</Button>
 * 
 * // With icon
 * <Button variant="secondary" iconName="plus" iconPosition="left">Add Item</Button>
 * 
 * // Loading state
 * <Button variant="primary" loading>Processing...</Button>
 * 
 * // Full width
 * <Button variant="success" fullWidth>Save Changes</Button>
 * ```
 */
export const Button = ({
  variant = 'primary',
  size = 'medium',
  loading = false,
  disabled = false,
  icon,
  iconName,
  iconPosition = 'left',
  fullWidth = false,
  children,
  onClick,
  type = 'button',
  className = '',
  ...props
}: ButtonProps) => {
  // Determine if button should be disabled (either explicitly disabled or loading)
  const isDisabled = disabled || loading;
  
  // Check if this is an icon-only button (no text content)
  const isIconOnly = (iconName || icon) && (!children || children === '');
  
  // Build CSS classes for button styling
  const buttonClasses = [
    'btn',
    `btn--${variant}`,
    `btn--${size}`,
    fullWidth && 'btn--full-width',
    loading && 'btn--loading',
    isDisabled && 'btn--disabled',
    isIconOnly && 'btn--icon-only',
    className
  ].filter(Boolean).join(' ');

  // Handle click events (prevent clicks when disabled or loading)
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    if (isDisabled) {
      e.preventDefault();
      return;
    }
    onClick?.(e);
  };

  const renderContent = () => {
    if (loading) {
      return (
        <>
          <Icon name="loading" size="sm" className="btn__spinner-icon" />
          <span className="btn__text">Loading...</span>
        </>
      );
    }

    // Use iconName from icon library if provided
    const iconElement = iconName ? (
      <Icon name={iconName} size="sm" />
    ) : icon;

    if (iconElement) {
      // If this is an icon-only button, just render the icon
      if (isIconOnly) {
        return (
          <span className="btn__icon" aria-hidden="true">
            {iconElement}
          </span>
        );
      }
      
      // Otherwise render icon with text
      return (
        <>
          {iconPosition === 'left' && (
            <span className="btn__icon btn__icon--left" aria-hidden="true">
              {iconElement}
            </span>
          )}
          <Typography variant="body" size="sm" className="btn__text">{children || ''}</Typography>
          {iconPosition === 'right' && (
            <span className="btn__icon btn__icon--right" aria-hidden="true">
              {iconElement}
            </span>
          )}
        </>
      );
    }

    return <Typography variant="body" size="sm" className="btn__text">{children || ''}</Typography>;
  };

  return (
    <button
      type={type}
      className={buttonClasses}
      onClick={handleClick}
      disabled={isDisabled}
      aria-disabled={isDisabled}
      {...props}
    >
      {renderContent()}
    </button>
  );
};
