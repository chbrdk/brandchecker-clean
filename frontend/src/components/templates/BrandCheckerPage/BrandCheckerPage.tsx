import React, { useState } from 'react';
import { Typography } from '../../atoms/Typography';
import { FileUpload } from '../../atoms/FileUpload';
import { ChatToolbar } from '../../molecules/ChatToolbar';
import './BrandCheckerPage.css';

/**
 * BrandChecker Page Props
 */
export interface BrandCheckerPageProps {
  /** Current stage */
  stage?: 'initial' | 'uploading' | 'processing' | 'chat' | 'results';
  /** Stage change handler */
  onStageChange?: (stage: 'initial' | 'uploading' | 'processing' | 'chat' | 'results') => void;
  /** File upload handler */
  onFileUpload?: (files: File[]) => void;
  /** Message send handler */
  onSendMessage?: (message: string) => void;
  /** Additional CSS class */
  className?: string;
}

/**
 * BrandChecker Page Component
 */
export const BrandCheckerPage = ({
  stage = 'initial',
  onStageChange,
  onFileUpload,
  onSendMessage,
  className = ''
}: BrandCheckerPageProps) => {
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileUpload = async (files: File[]) => {
    setIsUploading(true);
    setUploadedFiles(files);
    
    // Simulate upload process
    setTimeout(() => {
      setIsUploading(false);
      onStageChange?.('processing');
      onFileUpload?.(files);
    }, 2000);
  };

  const handleSendMessage = (message: string) => {
    onSendMessage?.(message);
  };
  const renderInitialStage = () => (
    <div className="brandchecker-initial">
      <div className="brandchecker-initial__title">
        <Typography variant="h1" size="xl" weight="bold" color="primary">
          BrandChecker
        </Typography>
      </div>
      
      <div className="brandchecker-initial__subtitle">
        <Typography variant="body" size="lg" color="secondary">
          Upload your brand files to get started with AI-powered brand analysis
        </Typography>
      </div>
      
      <div className="brandchecker-initial__upload">
        <FileUpload
          accept=".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png"
          multiple={true}
          onFilesChange={handleFileUpload}
          disabled={isUploading}
          loading={isUploading}
        />
      </div>
    </div>
  );

  const renderUploadingStage = () => (
    <div className="brandchecker-initial">
      <div className="brandchecker-initial__title">
        <Typography variant="h2" size="lg" weight="semibold">
          Uploading Files...
        </Typography>
      </div>
      
      <div className="brandchecker-initial__subtitle">
        <Typography variant="body" color="secondary">
          Please wait while we process your files
        </Typography>
      </div>
    </div>
  );

  const renderProcessingStage = () => (
    <div className="brandchecker-initial">
      <div className="brandchecker-initial__title">
        <Typography variant="h2" size="lg" weight="semibold">
          Analyzing Your Brand...
        </Typography>
      </div>
      
      <div className="brandchecker-initial__subtitle">
        <Typography variant="body" color="secondary">
          Our AI is examining your brand materials
        </Typography>
      </div>
    </div>
  );

  const renderStageContent = () => {
    switch (stage) {
      case 'initial':
        return renderInitialStage();
      case 'uploading':
        return renderUploadingStage();
      case 'processing':
        return renderProcessingStage();
      default:
        return renderInitialStage();
    }
  };

  return (
    <div className={`brandchecker-page ${className}`}>
      <div className="brandchecker-page__content">
        {renderStageContent()}
      </div>
      
      <div className="brandchecker-page__toolbar">
        <ChatToolbar
          placeholder="Ask about your brand..."
          onSendMessage={handleSendMessage}
          onFilesUpload={handleFileUpload}
          disabled={stage === 'uploading' || stage === 'processing'}
          loading={stage === 'uploading' || stage === 'processing'}
        />
      </div>
    </div>
  );
};

BrandCheckerPage.displayName = 'BrandCheckerPage';