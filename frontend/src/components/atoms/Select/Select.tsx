import React, { useState, useRef, useEffect } from 'react';
import { Icon } from '../Icon';
import './Select.css';

export interface SelectOption {
  value: string | number;
  label: string;
  disabled?: boolean;
}

export interface SelectProps {
  options: SelectOption[];
  value?: string | number;
  placeholder?: string;
  label?: string;
  disabled?: boolean;
  required?: boolean;
  error?: string;
  helpText?: string;
  size?: 'small' | 'medium' | 'large';
  variant?: 'outlined' | 'filled';
  onChange?: (value: string | number) => void;
  className?: string;
  id?: string;
  name?: string;
}

export const Select = ({
  options = [],
  value,
  placeholder = 'Select an option...',
  label,
  disabled = false,
  required = false,
  error,
  helpText,
  size = 'medium',
  variant = 'outlined',
  onChange,
  className = '',
  id,
  name,
  ...props
}: SelectProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const selectRef = useRef<HTMLDivElement>(null);

  const selectId = id || `select-${Math.random().toString(36).substr(2, 9)}`;
  const hasError = !!error;
  const hasValue = value !== undefined && value !== '';

  const handleToggle = () => {
    if (disabled) return;
    setIsOpen(!isOpen);
  };

  const handleSelect = (option: SelectOption) => {
    if (option.disabled) return;
    onChange?.(option.value);
    setIsOpen(false);
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (selectRef.current && !selectRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const getDisplayValue = () => {
    const option = options.find(opt => opt.value === value);
    return option?.label || placeholder;
  };

  const selectClasses = [
    'select',
    `select--${variant}`,
    `select--${size}`,
    hasError && 'select--error',
    isOpen && 'select--open',
    disabled && 'select--disabled',
    className
  ].filter(Boolean).join(' ');

  return (
    <div className="select-wrapper">
      {label && (
        <label htmlFor={selectId} className="select__label">
          {label}
          {required && <span className="select__required">*</span>}
        </label>
      )}
      
      <div
        ref={selectRef}
        className={selectClasses}
        tabIndex={disabled ? -1 : 0}
        onClick={handleToggle}
        role="combobox"
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        aria-invalid={hasError}
        {...props}
      >
        <div className="select__trigger">
          <span className="select__value">
            {getDisplayValue()}
          </span>
          <button
            type="button"
            className="select__arrow-button"
            onClick={(e) => {
              e.stopPropagation();
              handleToggle();
            }}
            aria-label={isOpen ? 'Close dropdown' : 'Open dropdown'}
            disabled={disabled}
          >
            <Icon name={isOpen ? 'chevron-up' : 'chevron-down'} size="sm" />
          </button>
        </div>
        
        {isOpen && (
          <div className="select__dropdown">
            <ul className="select__list" role="listbox">
              {options.length === 0 ? (
                <li className="select__option select__option--empty">
                  No options available
                </li>
              ) : (
                options.map((option) => (
                  <li
                    key={option.value}
                    className={[
                      'select__option',
                      value === option.value && 'select__option--selected',
                      option.disabled && 'select__option--disabled'
                    ].filter(Boolean).join(' ')}
                    onClick={() => handleSelect(option)}
                    role="option"
                    aria-selected={value === option.value}
                  >
                    {option.label}
                  </li>
                ))
              )}
            </ul>
          </div>
        )}
      </div>
      
      {(helpText || error) && (
        <div className={`select__message ${error ? 'select__message--error' : 'select__message--help'}`}>
          {error || helpText}
        </div>
      )}
    </div>
  );
};