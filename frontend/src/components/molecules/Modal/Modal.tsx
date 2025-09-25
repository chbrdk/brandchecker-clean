import React, { useEffect, useRef } from 'react';
import './Modal.css';

export interface ModalProps {
  /** Modal open state */
  isOpen: boolean;
  /** Close handler */
  onClose: () => void;
  /** Modal title */
  title?: string;
  /** Modal content */
  children: React.ReactNode;
  /** Modal size */
  size?: 'small' | 'medium' | 'large' | 'fullscreen';
  /** Modal variant */
  variant?: 'default' | 'confirmation' | 'alert';
  /** Show close button */
  showCloseButton?: boolean;
  /** Close on overlay click */
  closeOnOverlayClick?: boolean;
  /** Close on escape key */
  closeOnEscape?: boolean;
  /** Modal footer */
  footer?: React.ReactNode;
  /** Additional CSS class */
  className?: string;
  /** Overlay CSS class */
  overlayClassName?: string;
  /** Additional props */
  [key: string]: any;
}

/** Enhanced Modal component with multiple variants and sizes */
export const Modal = ({
  isOpen,
  onClose,
  title,
  children,
  size = 'medium',
  variant = 'default',
  showCloseButton = true,
  closeOnOverlayClick = true,
  closeOnEscape = true,
  footer,
  className = '',
  overlayClassName = '',
  ...props
}: ModalProps) => {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousActiveElement = useRef<HTMLElement | null>(null);

  // Handle escape key
  useEffect(() => {
    if (!isOpen || !closeOnEscape) return;

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, closeOnEscape, onClose]);

  // Handle focus management
  useEffect(() => {
    if (isOpen) {
      // Store the currently focused element
      previousActiveElement.current = document.activeElement as HTMLElement;
      
      // Focus the modal
      setTimeout(() => {
        modalRef.current?.focus();
      }, 0);
    } else {
      // Restore focus to the previously focused element
      if (previousActiveElement.current) {
        previousActiveElement.current.focus();
      }
    }
  }, [isOpen]);

  // Handle body scroll lock
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  // Handle overlay click
  const handleOverlayClick = (e: React.MouseEvent) => {
    if (closeOnOverlayClick && e.target === e.currentTarget) {
      onClose();
    }
  };

  if (!isOpen) return null;

  const modalClasses = [
    'modal',
    `modal--${size}`,
    `modal--${variant}`,
    className
  ].filter(Boolean).join(' ');

  const overlayClasses = [
    'modal__overlay',
    overlayClassName
  ].filter(Boolean).join(' ');

  const renderHeader = () => {
    if (!title && !showCloseButton) return null;
    
    return (
      <div className="modal__header">
        {title && <h2 className="modal__title">{title}</h2>}
        {showCloseButton && (
          <button
            type="button"
            className="modal__close"
            onClick={onClose}
            aria-label="Close modal"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        )}
      </div>
    );
  };

  const renderFooter = () => {
    if (!footer) return null;
    
    return <div className="modal__footer">{footer}</div>;
  };

  return (
    <div className={overlayClasses} onClick={handleOverlayClick}>
      <div
        ref={modalRef}
        className={modalClasses}
        role="dialog"
        aria-modal="true"
        aria-labelledby={title ? 'modal-title' : undefined}
        tabIndex={-1}
        {...props}
      >
        {renderHeader()}
        <div className="modal__content">
          {children}
        </div>
        {renderFooter()}
      </div>
    </div>
  );
};
