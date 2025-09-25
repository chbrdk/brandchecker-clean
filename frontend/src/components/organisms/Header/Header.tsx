import React, { useState, useRef, useEffect } from 'react';
import { Icon } from '../../atoms/Icon';
import type { IconName } from '../../atoms/Icon';
import { Badge } from '../../atoms/Badge';
import './Header.css';

export interface HeaderProps {
  /** Header content */
  children: React.ReactNode;
  /** Header variant */
  variant?: 'default' | 'transparent' | 'elevated';
  /** Fixed header */
  fixed?: boolean;
  /** Header height */
  height?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

export interface HeaderBrandProps {
  /** Brand logo */
  logo?: React.ReactNode;
  /** Brand title */
  title?: string;
  /** Brand subtitle */
  subtitle?: string;
  /** Brand link */
  href?: string;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

export interface HeaderNavigationProps {
  /** Navigation items */
  children: React.ReactNode;
  /** Navigation alignment */
  align?: 'left' | 'center' | 'right';
  /** Mobile menu behavior */
  mobileMenu?: 'dropdown' | 'overlay' | 'none';
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

export interface HeaderActionsProps {
  /** Action items */
  children: React.ReactNode;
  /** Actions alignment */
  align?: 'left' | 'center' | 'right';
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

export interface NavItemProps {
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

export interface BreadcrumbProps {
  /** Breadcrumb items */
  items: Array<{
    label: string;
    href?: string;
    active?: boolean;
  }>;
  /** Separator */
  separator?: string;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

/** Responsive Header Component */
export const Header = ({
  children,
  variant = 'default',
  fixed = false,
  height = 'md',
  className = '',
  ...props
}: HeaderProps) => {
  const classes = [
    'header',
    `header--${variant}`,
    `header--${height}`,
    fixed ? 'header--fixed' : '',
    className
  ].filter(Boolean).join(' ');

  return (
    <header className={classes} {...props}>
      <div className="header__container">
        {children}
      </div>
    </header>
  );
};

/** Header Brand Component */
export const HeaderBrand = ({
  logo,
  title,
  subtitle,
  href,
  className = '',
  ...props
}: HeaderBrandProps) => {
  const classes = [
    'header-brand',
    className
  ].filter(Boolean).join(' ');

  const content = (
    <>
      {logo && <div className="header-brand__logo">{logo}</div>}
      <div className="header-brand__content">
        {title && <div className="header-brand__title">{title}</div>}
        {subtitle && <div className="header-brand__subtitle">{subtitle}</div>}
      </div>
    </>
  );

  if (href) {
    return (
      <a href={href} className={classes} {...props}>
        {content}
      </a>
    );
  }

  return (
    <div className={classes} {...props}>
      {content}
    </div>
  );
};

/** Header Navigation Component */
export const HeaderNavigation = ({
  children,
  align = 'left',
  mobileMenu = 'dropdown',
  className = '',
  ...props
}: HeaderNavigationProps) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const mobileMenuRef = useRef<HTMLDivElement>(null);

  const classes = [
    'header-nav',
    `header-nav--${align}`,
    mobileMenu !== 'none' ? 'header-nav--mobile' : '',
    isMobileMenuOpen ? 'header-nav--mobile-open' : '',
    className
  ].filter(Boolean).join(' ');

  const handleMobileMenuToggle = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const handleMobileMenuClose = () => {
    setIsMobileMenuOpen(false);
  };

  // Close mobile menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (mobileMenuRef.current && !mobileMenuRef.current.contains(event.target as Node)) {
        setIsMobileMenuOpen(false);
      }
    };

    if (isMobileMenuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isMobileMenuOpen]);

  return (
    <nav className={classes} ref={mobileMenuRef} {...props}>
      {/* Desktop Navigation */}
      <div className="header-nav__desktop">
        {children}
      </div>

      {/* Mobile Menu Button */}
      {mobileMenu !== 'none' && (
        <button
          className="header-nav__mobile-toggle"
          onClick={handleMobileMenuToggle}
          aria-label="Toggle mobile menu"
          aria-expanded={isMobileMenuOpen}
        >
          <span className="header-nav__hamburger">
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>
      )}

      {/* Mobile Navigation */}
      {mobileMenu !== 'none' && (
        <div className="header-nav__mobile">
          <div className="header-nav__mobile-content">
            {children}
          </div>
          <div className="header-nav__mobile-overlay" onClick={handleMobileMenuClose} />
        </div>
      )}
    </nav>
  );
};

/** Header Actions Component */
export const HeaderActions = ({
  children,
  align = 'right',
  className = '',
  ...props
}: HeaderActionsProps) => {
  const classes = [
    'header-actions',
    `header-actions--${align}`,
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={classes} {...props}>
      {children}
    </div>
  );
};

/** Navigation Item Component */
export const NavItem = ({
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
}: NavItemProps) => {
  const classes = [
    'nav-item',
    active ? 'nav-item--active' : '',
    disabled ? 'nav-item--disabled' : '',
    className
  ].filter(Boolean).join(' ');

      const content = (
        <>
          {(icon || iconName) && (
            <span className="nav-item__icon">
              {iconName ? <Icon name={iconName} size="sm" /> : icon}
            </span>
          )}
          <span className="nav-item__text">{children}</span>
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
      <a href={href} className={classes} {...props}>
        {content}
      </a>
    );
  }

  return (
    <button
      className={classes}
      onClick={disabled ? undefined : onClick}
      disabled={disabled}
      {...props}
    >
      {content}
    </button>
  );
};

/** Breadcrumb Component */
export const Breadcrumb = ({
  items,
  separator = '›',
  className = '',
  ...props
}: BreadcrumbProps) => {
  const classes = [
    'breadcrumb',
    className
  ].filter(Boolean).join(' ');

  return (
    <nav className={classes} aria-label="Breadcrumb" {...props}>
      <ol className="breadcrumb__list">
        {items.map((item, index) => (
          <li key={index} className="breadcrumb__item">
            {item.href && !item.active ? (
              <a href={item.href} className="breadcrumb__link">
                {item.label}
              </a>
            ) : (
              <span className={`breadcrumb__text ${item.active ? 'breadcrumb__text--active' : ''}`}>
                {item.label}
              </span>
            )}
            {index < items.length - 1 && (
              <span className="breadcrumb__separator" aria-hidden="true">
                {separator}
              </span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
};
