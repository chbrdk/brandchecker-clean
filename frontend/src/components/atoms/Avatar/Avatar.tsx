import React from 'react';
import './Avatar.css';

/**
 * Avatar Component Props
 */
export interface AvatarProps {
  /** Avatar image source */
  src?: string;
  /** Alt text for image */
  alt?: string;
  /** User initials to display when no image */
  initials?: string;
  /** Avatar size */
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  /** Avatar shape */
  shape?: 'circle' | 'square' | 'rounded';
  /** Status indicator */
  status?: 'online' | 'offline' | 'away' | 'busy';
  /** Background color for initials */
  backgroundColor?: string;
  /** Text color for initials */
  textColor?: string;
  /** Click handler */
  onClick?: () => void;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

/**
 * Avatar Component
 */
export const Avatar = ({
  src,
  alt = 'Avatar',
  initials,
  size = 'md',
  shape = 'circle',
  status,
  backgroundColor,
  textColor = 'white',
  onClick,
  className = '',
  ...props
}: AvatarProps) => {
  const classes = [
    'avatar',
    `avatar--${size}`,
    `avatar--${shape}`,
    status && `avatar--${status}`,
    onClick && 'avatar--clickable',
    className
  ].filter(Boolean).join(' ');

  const handleClick = () => {
    if (onClick) {
      onClick();
    }
  };

  const renderContent = () => {
    if (src) {
      return (
        <img
          src={src}
          alt={alt}
          className="avatar__image"
          onError={(e) => {
            (e.target as HTMLImageElement).style.display = 'none';
          }}
        />
      );
    }

    if (initials) {
      return (
        <div className="avatar__initials">
          {initials}
        </div>
      );
    }

    // Default fallback
    return (
      <div className="avatar__fallback">
        <svg className="avatar__icon-svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
        </svg>
      </div>
    );
  };

  return (
    <div
      className={classes}
      onClick={handleClick}
      tabIndex={onClick ? 0 : undefined}
      role={onClick ? 'button' : undefined}
      aria-label={onClick ? alt : undefined}
      style={{
        backgroundColor: backgroundColor || undefined,
        color: textColor || undefined
      }}
      {...props}
    >
      {renderContent()}
      {status && <div className={`avatar__status avatar__status--${status}`} />}
    </div>
  );
};

Avatar.displayName = 'Avatar';