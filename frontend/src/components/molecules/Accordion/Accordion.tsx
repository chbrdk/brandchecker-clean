import React, { useState, useRef, useEffect } from 'react';
import { Icon } from '../../atoms/Icon';
import type { IconName } from '../../atoms/Icon';
import './Accordion.css';

export interface AccordionItemProps {
  /** Accordion item title */
  title: React.ReactNode;
  /** Accordion item content */
  children: React.ReactNode;
  /** Whether the item is expanded by default */
  defaultExpanded?: boolean;
  /** Whether the item is disabled */
  disabled?: boolean;
  /** Custom icon for the expand/collapse button */
  icon?: IconName;
  /** Custom icon position */
  iconPosition?: 'left' | 'right';
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

export interface AccordionProps {
  /** Accordion items */
  children: React.ReactNode;
  /** Whether multiple items can be open at once */
  allowMultiple?: boolean;
  /** Whether to show borders between items */
  bordered?: boolean;
  /** Accordion variant */
  variant?: 'default' | 'flush' | 'outlined';
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

/** Individual Accordion Item Component */
export const AccordionItem = ({
  title,
  children,
  defaultExpanded = false,
  disabled = false,
  icon = 'chevron-down',
  iconPosition = 'right',
  className = '',
  ...props
}: AccordionItemProps) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  const contentRef = useRef<HTMLDivElement>(null);

  const toggleExpanded = () => {
    if (!disabled) {
      setIsExpanded(prev => !prev);
    }
  };

  const classes = [
    'accordion-item',
    isExpanded && 'accordion-item--expanded',
    disabled && 'accordion-item--disabled',
    className
  ].filter(Boolean).join(' ');

  const headerClasses = [
    'accordion-item__header',
    isExpanded && 'accordion-item__header--expanded',
    disabled && 'accordion-item__header--disabled'
  ].filter(Boolean).join(' ');

  return (
    <div className={classes} {...props}>
      <button
        type="button"
        className={headerClasses}
        onClick={toggleExpanded}
        disabled={disabled}
        aria-expanded={isExpanded}
        aria-disabled={disabled}
      >
        {iconPosition === 'left' && (
          <span className="accordion-item__icon accordion-item__icon--left">
            <Icon 
              name={icon} 
              size="sm" 
              style={{ 
                transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)',
                transition: 'transform 0.2s ease-in-out'
              }} 
            />
          </span>
        )}
        <span className="accordion-item__title">{title}</span>
        {iconPosition === 'right' && (
          <span className="accordion-item__icon accordion-item__icon--right">
            <Icon 
              name={icon} 
              size="sm" 
              style={{ 
                transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)',
                transition: 'transform 0.2s ease-in-out'
              }} 
            />
          </span>
        )}
      </button>
      <div
        ref={contentRef}
        className="accordion-item__content"
        style={{
          maxHeight: isExpanded ? (contentRef.current?.scrollHeight || 'auto') : '0px',
          overflow: 'hidden',
          transition: 'max-height 0.3s ease-out, padding 0.3s ease-out',
          padding: isExpanded ? 'var(--space-4)' : '0 var(--space-4)',
        }}
        aria-hidden={!isExpanded}
      >
        <div className="accordion-item__body">
          {children}
        </div>
      </div>
    </div>
  );
};

/** Main Accordion Component */
export const Accordion = ({
  children,
  allowMultiple = false,
  bordered = true,
  variant = 'default',
  className = '',
  ...props
}: AccordionProps) => {
  const [expandedItems, setExpandedItems] = useState<Set<number>>(new Set());

  const handleItemToggle = (index: number) => {
    setExpandedItems(prev => {
      const newSet = new Set(prev);
      if (newSet.has(index)) {
        newSet.delete(index);
      } else {
        if (!allowMultiple) {
          newSet.clear();
        }
        newSet.add(index);
      }
      return newSet;
    });
  };

  const classes = [
    'accordion',
    `accordion--${variant}`,
    bordered && 'accordion--bordered',
    className
  ].filter(Boolean).join(' ');

  // Clone children and add controlled state
  const accordionItems = React.Children.map(children, (child, index) => {
    if (React.isValidElement<AccordionItemProps>(child)) {
      return React.cloneElement(child, {
        isExpanded: expandedItems.has(index),
        onToggle: () => handleItemToggle(index),
        key: index,
      });
    }
    return child;
  });

  return (
    <div className={classes} {...props}>
      {accordionItems}
    </div>
  );
};
