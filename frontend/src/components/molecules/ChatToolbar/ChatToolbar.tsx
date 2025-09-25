import React, { useState } from 'react';
import { Input } from '../../atoms/Input';
import { Button } from '../../atoms/Button';
import { Icon } from '../../atoms/Icon';
import './ChatToolbar.css';

/**
 * ChatToolbar Component Props
 * 
 * Props for the chat toolbar component with input, send button, and file upload.
 * 
 * @interface ChatToolbarProps
 */
export interface ChatToolbarProps {
  /** Whether the toolbar is loading */
  loading?: boolean;
  /** Whether the toolbar is disabled */
  disabled?: boolean;
  /** Placeholder text for input */
  placeholder?: string;
  /** Callback when a message is sent */
  onMessageSend?: (message: string, files?: File[]) => void;
  /** Callback when files are uploaded */
  onFilesUpload?: (files: File[]) => void;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

/**
 * ChatToolbar Component
 * 
 * A clean, minimalist toolbar for chat input with text input, send button, and file upload.
 * Designed for practical use without unnecessary branding or marketing elements.
 * 
 * Features:
 * - Clean text input with placeholder
 * - Send button as icon button
 * - File upload integration
 * - Loading states
 * - Disabled states
 * - Keyboard shortcuts (Enter to send)
 * - Minimalist design
 * 
 * @param props - ChatToolbarProps
 * @returns JSX.Element
 * 
 * @example
 * ```tsx
 * <ChatToolbar 
 *   placeholder="Ask about your brand..."
 *   onMessageSend={(message, files) => console.log(message, files)}
 *   onFilesUpload={(files) => console.log(files)}
 * />
 * ```
 */
export const ChatToolbar = ({
  loading = false,
  disabled = false,
  placeholder = "Ask about your brand...",
  onMessageSend,
  onFilesUpload,
  className = '',
  ...props
}: ChatToolbarProps) => {
  const [message, setMessage] = useState('');
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);

  // Handle message input change
  const handleMessageChange = (value: string) => {
    setMessage(value);
  };

  // Handle file upload
  const handleFilesUpload = (files: File[]) => {
    setUploadedFiles(files);
    onFilesUpload?.(files);
  };

  // Handle send message
  const handleSendMessage = () => {
    if (message.trim() || uploadedFiles.length > 0) {
      onMessageSend?.(message, uploadedFiles);
      setMessage('');
      setUploadedFiles([]);
    }
  };

  // Handle key press
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Check if send button should be enabled
  const canSend = !disabled && !loading && (message.trim() || uploadedFiles.length > 0);

  return (
    <div className={`chat-toolbar ${className}`} {...props}>
      {/* File Upload Button */}
      <div className="chat-toolbar__upload">
        <Button
          variant="secondary"
          size="medium"
          onClick={() => {
            // Create a hidden file input
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.pdf';
            input.multiple = true;
            input.onchange = (e) => {
              const files = Array.from((e.target as HTMLInputElement).files || []);
              handleFilesUpload(files);
            };
            input.click();
          }}
          disabled={disabled || loading}
          iconName="upload"
          className="chat-toolbar__upload-button"
        />
      </div>

      {/* Input Field */}
      <div className="chat-toolbar__input">
        <Input
          type="text"
          placeholder={placeholder}
          value={message}
          onChange={handleMessageChange}
          onKeyPress={handleKeyPress}
          disabled={disabled || loading}
          className="chat-toolbar__text-input"
        />
      </div>

          {/* Send Button */}
          <div className="chat-toolbar__send">
            <Button
              variant="secondary"
              size="medium"
              onClick={handleSendMessage}
              disabled={!canSend}
              loading={loading}
              iconName="send"
              className="chat-toolbar__send-button"
            />
          </div>

      {/* Uploaded Files Display */}
      {uploadedFiles.length > 0 && (
        <div className="chat-toolbar__files">
          <div className="chat-toolbar__files-list">
            {uploadedFiles.map((file, index) => (
              <div key={index} className="chat-toolbar__file-item">
                <Icon name="file" size="sm" />
                <span className="chat-toolbar__file-name">{file.name}</span>
                <button
                  type="button"
                  className="chat-toolbar__file-remove"
                  onClick={() => {
                    const newFiles = uploadedFiles.filter((_, i) => i !== index);
                    setUploadedFiles(newFiles);
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
    </div>
  );
};
