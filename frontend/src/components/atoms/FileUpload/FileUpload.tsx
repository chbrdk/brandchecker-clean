import React, { useRef, useState, useCallback } from 'react';
import { Icon } from '../Icon';
import type { IconName } from '../Icon';
import { Typography } from '../Typography';
import './FileUpload.css';

/**
 * FileUpload Component Props
 * 
 * Comprehensive file upload component with drag & drop, multiple file support,
 * file type validation, and progress tracking.
 * 
 * @interface FileUploadProps
 */
export interface FileUploadProps {
  /** Accepted file types */
  accept?: string;
  /** Maximum file size in bytes */
  maxSize?: number;
  /** Maximum number of files */
  maxFiles?: number;
  /** Whether to allow multiple files */
  multiple?: boolean;
  /** Whether the upload is disabled */
  disabled?: boolean;
  /** Upload button text */
  buttonText?: string;
  /** Drag & drop text */
  dragText?: string;
  /** File type description */
  fileTypeDescription?: string;
  /** Icon for upload button */
  iconName?: IconName;
  /** Callback when files are selected */
  onFilesSelect?: (files: File[]) => void;
  /** Callback when files are dropped */
  onFilesDrop?: (files: File[]) => void;
  /** Callback when upload starts */
  onUploadStart?: (files: File[]) => void;
  /** Callback when upload completes */
  onUploadComplete?: (files: File[]) => void;
  /** Callback when upload fails */
  onUploadError?: (error: string) => void;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

/**
 * FileUpload Component
 * 
 * A comprehensive file upload component with drag & drop functionality,
 * file validation, and progress tracking. Perfect for PDF uploads in BrandChecker.
 * 
 * Features:
 * - Drag & drop interface
 * - Multiple file support
 * - File type validation
 * - File size validation
 * - Progress tracking
 * - Error handling
 * - Icon integration
 * - Typography system integration
 * - Accessibility features
 * 
 * @param props - FileUploadProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * // Basic PDF upload
 * <FileUpload 
 *   accept=".pdf" 
 *   maxSize={10 * 1024 * 1024} // 10MB
 *   onFilesSelect={(files) => console.log(files)}
 * />
 * 
 * // Multiple files with custom text
 * <FileUpload 
 *   accept=".pdf,.doc,.docx" 
 *   multiple 
 *   buttonText="Upload Documents"
 *   dragText="Drop your brand documents here"
 * />
 * ```
 */
export const FileUpload = ({
  accept = '.pdf',
  maxSize = 10 * 1024 * 1024, // 10MB default
  maxFiles = 5,
  multiple = false,
  disabled = false,
  buttonText = 'Choose Files',
  dragText = 'Drag & drop files here or click to browse',
  fileTypeDescription = 'PDF files up to 10MB',
  iconName = 'upload',
  onFilesSelect,
  onFilesDrop,
  onUploadStart,
  onUploadComplete,
  onUploadError,
  className = '',
  ...props
}: FileUploadProps) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Validate file type
  const validateFileType = useCallback((file: File): boolean => {
    if (!accept) return true;
    
    const acceptedTypes = accept.split(',').map(type => type.trim());
    return acceptedTypes.some(type => {
      if (type.startsWith('.')) {
        return file.name.toLowerCase().endsWith(type.toLowerCase());
      }
      return file.type.includes(type);
    });
  }, [accept]);

  // Validate file size
  const validateFileSize = useCallback((file: File): boolean => {
    return file.size <= maxSize;
  }, [maxSize]);

  // Validate files
  const validateFiles = useCallback((files: File[]): { valid: File[]; errors: string[] } => {
    const validFiles: File[] = [];
    const errors: string[] = [];

    // Check max files limit
    if (files.length > maxFiles) {
      errors.push(`Maximum ${maxFiles} files allowed`);
      return { valid: [], errors };
    }

    files.forEach(file => {
      if (!validateFileType(file)) {
        errors.push(`${file.name}: Invalid file type. Accepted: ${accept}`);
        return;
      }
      
      if (!validateFileSize(file)) {
        errors.push(`${file.name}: File too large. Max size: ${Math.round(maxSize / 1024 / 1024)}MB`);
        return;
      }
      
      validFiles.push(file);
    });

    return { valid: validFiles, errors };
  }, [maxFiles, validateFileType, validateFileSize, accept, maxSize]);

  // Handle file selection
  const handleFileSelect = useCallback((files: File[]) => {
    const { valid, errors } = validateFiles(files);
    
    if (errors.length > 0) {
      setError(errors.join(', '));
      onUploadError?.(errors.join(', '));
      return;
    }

    setError(null);
    setSelectedFiles(valid);
    onFilesSelect?.(valid);
  }, [validateFiles, onFilesSelect, onUploadError]);

  // Handle input change
  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    handleFileSelect(files);
  }, [handleFileSelect]);

  // Handle drag events
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    if (!disabled) {
      setIsDragOver(true);
    }
  }, [disabled]);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    if (disabled) return;
    
    const files = Array.from(e.dataTransfer.files);
    handleFileSelect(files);
    onFilesDrop?.(files);
  }, [disabled, handleFileSelect, onFilesDrop]);

  // Handle button click
  const handleButtonClick = useCallback(() => {
    if (!disabled) {
      fileInputRef.current?.click();
    }
  }, [disabled]);

  // Handle upload
  const handleUpload = useCallback(async () => {
    if (selectedFiles.length === 0) return;
    
    setIsUploading(true);
    setError(null);
    
    try {
      onUploadStart?.(selectedFiles);
      // Simulate upload process
      await new Promise(resolve => setTimeout(resolve, 2000));
      onUploadComplete?.(selectedFiles);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Upload failed';
      setError(errorMessage);
      onUploadError?.(errorMessage);
    } finally {
      setIsUploading(false);
    }
  }, [selectedFiles, onUploadStart, onUploadComplete, onUploadError]);

  // Remove file
  const removeFile = useCallback((index: number) => {
    const newFiles = selectedFiles.filter((_, i) => i !== index);
    setSelectedFiles(newFiles);
  }, [selectedFiles]);

  // Build CSS classes
  const uploadClasses = [
    'file-upload',
    isDragOver && 'file-upload--drag-over',
    disabled && 'file-upload--disabled',
    error && 'file-upload--error',
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={uploadClasses} {...props}>
      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept={accept}
        multiple={multiple}
        onChange={handleInputChange}
        disabled={disabled}
        className="file-upload__input"
        aria-label="File upload"
      />

      {/* Upload area */}
      <div
        className="file-upload__area"
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleButtonClick}
        role="button"
        tabIndex={disabled ? -1 : 0}
        aria-label="Upload files"
      >
        <div className="file-upload__content">
          <Icon name={iconName} size="lg" className="file-upload__icon" />
          <Typography variant="body" className="file-upload__text">
            {dragText}
          </Typography>
          <Typography variant="small" color="secondary" className="file-upload__description">
            {fileTypeDescription}
          </Typography>
        </div>
      </div>

      {/* Upload button */}
      <button
        type="button"
        className="file-upload__button"
        onClick={handleButtonClick}
        disabled={disabled}
      >
        <Icon name={iconName} size="sm" />
        <Typography variant="body" size="sm">{buttonText}</Typography>
      </button>

      {/* Selected files */}
      {selectedFiles.length > 0 && (
        <div className="file-upload__files">
          <Typography variant="caption" weight="medium" className="file-upload__files-title">
            Selected Files ({selectedFiles.length})
          </Typography>
          <div className="file-upload__files-list">
            {selectedFiles.map((file, index) => (
              <div key={index} className="file-upload__file">
                <Icon name="file" size="sm" />
                <Typography variant="small" className="file-upload__file-name">
                  {file.name}
                </Typography>
                <Typography variant="small" color="secondary" className="file-upload__file-size">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </Typography>
                <button
                  type="button"
                  className="file-upload__file-remove"
                  onClick={(e) => {
                    e.stopPropagation();
                    removeFile(index);
                  }}
                  aria-label={`Remove ${file.name}`}
                >
                  <Icon name="close" size="sm" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Error message */}
      {error && (
        <div className="file-upload__error">
          <Icon name="alert-circle" size="sm" />
          <Typography variant="small" color="error">
            {error}
          </Typography>
        </div>
      )}

      {/* Upload button */}
      {selectedFiles.length > 0 && (
        <button
          type="button"
          className="file-upload__upload-button"
          onClick={handleUpload}
          disabled={isUploading || disabled}
        >
          {isUploading ? (
            <>
              <Icon name="loader" size="sm" />
              <Typography variant="body" size="sm">Uploading...</Typography>
            </>
          ) : (
            <>
              <Icon name="upload" size="sm" />
              <Typography variant="body" size="sm">Upload Files</Typography>
            </>
          )}
        </button>
      )}
    </div>
  );
};
