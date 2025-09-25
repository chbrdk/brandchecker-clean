import React, { useState, useRef, useEffect } from 'react';
import { Icon } from '../../atoms/Icon';
import type { IconName } from '../../atoms/Icon';
import { Badge } from '../../atoms/Badge';
import './Sidebar.css';

export interface SidebarProps {
  /** Sidebar content */
  children: React.ReactNode;
  /** Sidebar variant */
  variant?: 'default' | 'compact' | 'floating';
  /** Sidebar width */
  width?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  /** Collapsible sidebar */
  collapsible?: boolean;
  /** Default collapsed state */
  defaultCollapsed?: boolean;
  /** Controlled collapsed state */
  collapsed?: boolean;
  /** Collapse handler */
  onCollapse?: (collapsed: boolean) => void;
  /** Fixed sidebar */
  fixed?: boolean;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

export interface SidebarNavigationProps {
  /** Navigation items */
  children: React.ReactNode;
  /** Navigation title */
  title?: string;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

export interface SidebarItemProps {
  /** Navigation link */
  href?: string;
  /** Active state */
  active?: boolean;
  /** Disabled state */
  disabled?: boolean;
  /** Icon */
  icon?: React.ReactNode;
  /** Icon name from icon library */
  iconName?: IconName;
  /** Badge */
  badge?: string | number;
  /** Badge variant */
  badgeVariant?: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info' | 'neutral';
  /** Badge type */
  badgeType?: 'count' | 'status' | 'notification' | 'dot';
  /** Children */
  children: React.ReactNode;
  /** Click handler */
  onClick?: () => void;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

export interface SidebarGroupProps {
  /** Group title */
  title: string;
  /** Group items */
  children: React.ReactNode;
  /** Collapsible group */
  collapsible?: boolean;
  /** Default expanded state */
  defaultExpanded?: boolean;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

export interface SidebarFooterProps {
  /** Footer content */
  children: React.ReactNode;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

/** Responsive Sidebar Component */
export const Sidebar = ({
  children,
  variant = 'default',
  width = 'md',
  collapsible = false,
  defaultCollapsed = false,
  collapsed: controlledCollapsed,
  onCollapse,
  fixed = false,
  className = '',
  ...props
}: SidebarProps) => {
  const [internalCollapsed, setInternalCollapsed] = useState(defaultCollapsed);
  const isControlled = controlledCollapsed !== undefined;
  const collapsed = isControlled ? controlledCollapsed : internalCollapsed;

  const classes = [
    'sidebar',
    `sidebar--${variant}`,
    `sidebar--${width}`,
    collapsible ? 'sidebar--collapsible' : '',
    collapsed ? 'sidebar--collapsed' : '',
    fixed ? 'sidebar--fixed' : '',
    className
  ].filter(Boolean).join(' ');

  const handleCollapse = () => {
    const newCollapsed = !collapsed;
    if (!isControlled) {
      setInternalCollapsed(newCollapsed);
    }
    onCollapse?.(newCollapsed);
  };

  return (
    <aside className={classes} {...props}>
      {collapsible && (
        <button
          className="sidebar__toggle"
          onClick={handleCollapse}
          aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          <span className="sidebar__toggle-icon">
            {collapsed ? '→' : '←'}
          </span>
        </button>
      )}
      <div className="sidebar__content">
        {children}
      </div>
    </aside>
  );
};

/** Sidebar Navigation Component */
export const SidebarNavigation = ({
  children,
  title,
  className = '',
  ...props
}: SidebarNavigationProps) => {
  const classes = [
    'sidebar-nav',
    className
  ].filter(Boolean).join(' ');

  return (
    <nav className={classes} {...props}>
      {title && <h3 className="sidebar-nav__title">{title}</h3>}
      <ul className="sidebar-nav__list">
        {children}
      </ul>
    </nav>
  );
};

/** Sidebar Item Component */
export const SidebarItem = ({
  href,
  active = false,
  disabled = false,
  icon,
  iconName,
  badge,
  badgeVariant = 'primary',
  badgeType = 'count',
  children,
  onClick,
  className = '',
  ...props
}: SidebarItemProps) => {
  const classes = [
    'sidebar-item',
    active ? 'sidebar-item--active' : '',
    disabled ? 'sidebar-item--disabled' : '',
    className
  ].filter(Boolean).join(' ');

      const content = (
        <>
          {(icon || iconName) && (
            <span className="sidebar-item__icon">
              {iconName ? <Icon name={iconName} size="sm" /> : icon}
            </span>
          )}
          <span className="sidebar-item__text">{children}</span>
          {badge && (
            <Badge 
              variant={badgeVariant} 
              type={badgeType} 
              size="small"
            >
              {badge}
            </Badge>
          )}
        </>
      );

  if (href && !disabled) {
    return (
      <li className="sidebar-item__wrapper">
        <a href={href} className={classes} {...props}>
          {content}
        </a>
      </li>
    );
  }

  return (
    <li className="sidebar-item__wrapper">
      <button
        className={classes}
        onClick={disabled ? undefined : onClick}
        disabled={disabled}
        {...props}
      >
        {content}
      </button>
    </li>
  );
};

/** Sidebar Group Component */
export const SidebarGroup = ({
  title,
  children,
  collapsible = false,
  defaultExpanded = true,
  className = '',
  ...props
}: SidebarGroupProps) => {
  const [expanded, setExpanded] = useState(defaultExpanded);

  const classes = [
    'sidebar-group',
    className
  ].filter(Boolean).join(' ');

  const handleToggle = () => {
    if (collapsible) {
      setExpanded(!expanded);
    }
  };

  return (
    <div className={classes} {...props}>
      <div 
        className={`sidebar-group__header ${collapsible ? 'sidebar-group__header--clickable' : ''}`}
        onClick={collapsible ? handleToggle : undefined}
      >
        <h4 className="sidebar-group__title">{title}</h4>
        {collapsible && (
          <span className="sidebar-group__toggle">
            {expanded ? '▼' : '▶'}
          </span>
        )}
      </div>
      {expanded && (
        <div className="sidebar-group__content">
          {children}
        </div>
      )}
    </div>
  );
};

/** Sidebar Footer Component */
export const SidebarFooter = ({
  children,
  className = '',
  ...props
}: SidebarFooterProps) => {
  const classes = [
    'sidebar-footer',
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={classes} {...props}>
      {children}
    </div>
  );
};
