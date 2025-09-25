import React, { forwardRef } from 'react';
import { Icon } from '../Icon';
import type { IconName } from '../Icon';
import { Typography } from '../Typography';
import './Input.css';

/**
 * Input Component Props
 * 
 * Comprehensive input component with multiple types, states, validation, and icon support.
 * Integrates with the Icon library and Typography system for consistent styling.
 * 
 * @interface InputProps
 */
export interface InputProps {
  /** Input type */
  type?: 'text' | 'email' | 'password' | 'number' | 'file' | 'search';
  /** Input label */
  label?: string;
  /** Placeholder text */
  placeholder?: string;
  /** Input value */
  value?: string;
  /** Default value */
  defaultValue?: string;
  /** Disabled state */
  disabled?: boolean;
  /** Required field */
  required?: boolean;
  /** Error message */
  error?: string;
  /** Success message */
  success?: string;
  /** Help text */
  helpText?: string;
  /** Input size */
  size?: 'small' | 'medium' | 'large';
  /** Input variant */
  variant?: 'outlined' | 'filled' | 'underlined';
  /** Icon element */
  icon?: React.ReactNode;
  /** Icon name from icon library */
  iconName?: IconName;
  /** Icon position */
  iconPosition?: 'left' | 'right';
  /** Change handler */
  onChange?: (value: string) => void;
  /** Focus handler */
  onFocus?: () => void;
  /** Blur handler */
  onBlur?: () => void;
  /** Additional CSS class */
  className?: string;
  /** Input ID */
  id?: string;
  /** Input name */
  name?: string;
  /** Auto complete */
  autoComplete?: string;
  /** Max length */
  maxLength?: number;
  /** Min length */
  minLength?: number;
  /** Pattern */
  pattern?: string;
  /** Additional props */
  [key: string]: any;
}

/**
 * Input Component
 * 
 * A comprehensive input component with multiple types, states, validation, and icon support.
 * Integrates with the Icon library and Typography system for consistent styling across the application.
 * 
 * Features:
 * - Multiple input types (text, email, password, number, file, search)
 * - Three sizes (small, medium, large)
 * - Three variants (outlined, filled, underlined)
 * - Validation states (error, success)
 * - Icon support (left/right positioning)
 * - Typography system integration for labels and messages
 * - Accessibility features
 * - Help text and error messages
 * - Required field indicators
 * 
 * @param props - InputProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * // Basic input
 * <Input type="text" label="Name" placeholder="Enter your name" />
 * 
 * // With icon
 * <Input type="email" label="Email" iconName="mail" iconPosition="left" />
 * 
 * // With validation
 * <Input type="password" label="Password" error="Password is required" />
 * 
 * // With help text
 * <Input type="number" label="Age" helpText="Must be between 18 and 100" />
 * ```
 */
export const Input = forwardRef<HTMLInputElement, InputProps>(({
  type = 'text',
  label,
  placeholder,
  value,
  defaultValue,
  disabled = false,
  required = false,
  error,
  success,
  helpText,
  size = 'medium',
  variant = 'outlined',
  icon,
  iconName,
  iconPosition = 'left',
  onChange,
  onFocus,
  onBlur,
  className = '',
  id,
  name,
  autoComplete,
  maxLength,
  minLength,
  pattern,
  ...props
}, ref) => {
  // Generate unique ID for input if not provided
  const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
  
  // Determine input states
  const hasError = !!error;
  const hasSuccess = !!success;
  const hasIcon = !!icon;
  
  // Build CSS classes for input styling
  const inputClasses = [
    'input',
    `input--${variant}`,
    `input--${size}`,
    hasError && 'input--error',
    hasSuccess && 'input--success',
    hasIcon && `input--with-icon`,
    hasIcon && `input--icon-${iconPosition}`,
    disabled && 'input--disabled',
    className
  ].filter(Boolean).join(' ');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange?.(e.target.value);
  };

  // Render icon element (from icon library or custom icon)
  const renderIcon = () => {
    // Use iconName from icon library if provided
    const iconElement = iconName ? (
      <Icon name={iconName} size="sm" />
    ) : icon;

    if (!iconElement) return null;
    
    return (
      <span className={`input__icon input__icon--${iconPosition}`} aria-hidden="true">
        {iconElement}
      </span>
    );
  };

  // Render label with Typography system and required indicator
  const renderLabel = () => {
    if (!label) return null;
    
    return (
      <label htmlFor={inputId} className="input__label">
        <Typography variant="caption" weight="medium">{label}</Typography>
        {required && <span className="input__required" aria-label="required">*</span>}
      </label>
    );
  };

  // Render help text, error, or success messages with Typography system
  const renderHelpText = () => {
    if (!helpText && !error && !success) return null;
    
    const message = error || success || helpText;
    const type = error ? 'error' : success ? 'success' : 'help';
    
    return (
      <div className={`input__message input__message--${type}`} role={error ? 'alert' : undefined}>
        <Typography variant="small" color={error ? 'error' : success ? 'success' : 'secondary'}>
          {message}
        </Typography>
      </div>
    );
  };

  return (
    <div className="input-wrapper">
      {renderLabel()}
      <div className="input-container">
        {renderIcon()}
        <input
          ref={ref}
          id={inputId}
          name={name}
          type={type}
          value={value}
          defaultValue={defaultValue}
          placeholder={placeholder}
          disabled={disabled}
          required={required}
          autoComplete={autoComplete}
          maxLength={maxLength}
          minLength={minLength}
          pattern={pattern}
          className={inputClasses}
          onChange={handleChange}
          onFocus={onFocus}
          onBlur={onBlur}
          aria-invalid={hasError}
          aria-describedby={helpText || error || success ? `${inputId}-message` : undefined}
          {...props}
        />
      </div>
      {renderHelpText()}
    </div>
  );
});

Input.displayName = 'Input';
