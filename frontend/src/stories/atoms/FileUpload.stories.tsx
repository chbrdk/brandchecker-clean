import type { Meta, StoryObj } from '@storybook/react';
import { FileUpload } from '../../components/atoms/FileUpload/FileUpload';

const meta: Meta<typeof FileUpload> = {
  title: 'Atoms/FileUpload',
  component: FileUpload,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A comprehensive file upload component with drag & drop functionality, file validation, and progress tracking. Perfect for PDF uploads in BrandChecker.',
      },
    },
  },
  argTypes: {
    accept: {
      control: 'text',
      description: 'Accepted file types (e.g., ".pdf", ".pdf,.doc,.docx")',
    },
    maxSize: {
      control: 'number',
      description: 'Maximum file size in bytes',
    },
    maxFiles: {
      control: 'number',
      description: 'Maximum number of files',
    },
    multiple: {
      control: 'boolean',
      description: 'Whether to allow multiple files',
    },
    disabled: {
      control: 'boolean',
      description: 'Whether the upload is disabled',
    },
    buttonText: {
      control: 'text',
      description: 'Upload button text',
    },
    dragText: {
      control: 'text',
      description: 'Drag & drop text',
    },
    fileTypeDescription: {
      control: 'text',
      description: 'File type description',
    },
    iconName: {
      control: 'select',
      options: ['upload', 'file', 'folder', 'plus'],
      description: 'Icon for upload button',
    },
    onFilesSelect: {
      action: 'files selected',
      description: 'Callback when files are selected',
    },
    onFilesDrop: {
      action: 'files dropped',
      description: 'Callback when files are dropped',
    },
    onUploadStart: {
      action: 'upload started',
      description: 'Callback when upload starts',
    },
    onUploadComplete: {
      action: 'upload completed',
      description: 'Callback when upload completes',
    },
    onUploadError: {
      action: 'upload error',
      description: 'Callback when upload fails',
    },
  },
};

export default meta;
type Story = StoryObj<typeof FileUpload>;

export const Default: Story = {
  args: {
    accept: '.pdf',
    maxSize: 10 * 1024 * 1024, // 10MB
    maxFiles: 5,
    multiple: false,
    disabled: false,
    buttonText: 'Choose Files',
    dragText: 'Drag & drop files here or click to browse',
    fileTypeDescription: 'PDF files up to 10MB',
    iconName: 'upload',
  },
};

export const MultipleFiles: Story = {
  args: {
    accept: '.pdf,.doc,.docx',
    maxSize: 5 * 1024 * 1024, // 5MB
    maxFiles: 3,
    multiple: true,
    buttonText: 'Upload Documents',
    dragText: 'Drop your documents here',
    fileTypeDescription: 'PDF, DOC, DOCX files up to 5MB',
    iconName: 'folder',
  },
};

export const LargeFiles: Story = {
  args: {
    accept: '.pdf',
    maxSize: 50 * 1024 * 1024, // 50MB
    maxFiles: 1,
    multiple: false,
    buttonText: 'Upload Large PDF',
    dragText: 'Drop your large PDF here',
    fileTypeDescription: 'PDF files up to 50MB',
    iconName: 'file',
  },
};

export const Disabled: Story = {
  args: {
    accept: '.pdf',
    maxSize: 10 * 1024 * 1024,
    maxFiles: 5,
    multiple: false,
    disabled: true,
    buttonText: 'Choose Files',
    dragText: 'Drag & drop files here or click to browse',
    fileTypeDescription: 'PDF files up to 10MB',
    iconName: 'upload',
  },
};

export const CustomStyling: Story = {
  args: {
    accept: '.pdf,.png,.jpg,.jpeg',
    maxSize: 20 * 1024 * 1024, // 20MB
    maxFiles: 10,
    multiple: true,
    buttonText: 'Upload Brand Assets',
    dragText: 'Drop your brand assets here',
    fileTypeDescription: 'PDF, PNG, JPG, JPEG files up to 20MB',
    iconName: 'plus',
    className: 'custom-file-upload',
  },
};

export const BrandCheckerPDF: Story = {
  args: {
    accept: '.pdf',
    maxSize: 10 * 1024 * 1024, // 10MB
    maxFiles: 3,
    multiple: true,
    buttonText: 'Upload PDF',
    dragText: 'Drag & drop your brand documents here',
    fileTypeDescription: 'PDF files up to 10MB',
    iconName: 'upload',
  },
};

export const WithErrorHandling: Story = {
  args: {
    accept: '.pdf',
    maxSize: 1024 * 1024, // 1MB (small for testing)
    maxFiles: 1,
    multiple: false,
    buttonText: 'Choose File',
    dragText: 'Drop a PDF here (max 1MB)',
    fileTypeDescription: 'PDF files up to 1MB',
    iconName: 'upload',
    onUploadError: (error) => {
      console.error('Upload error:', error);
    },
  },
};

export const AllFileTypes: Story = {
  args: {
    accept: '.pdf,.doc,.docx,.txt,.rtf,.odt',
    maxSize: 15 * 1024 * 1024, // 15MB
    maxFiles: 5,
    multiple: true,
    buttonText: 'Upload Documents',
    dragText: 'Drop your documents here',
    fileTypeDescription: 'PDF, DOC, DOCX, TXT, RTF, ODT files up to 15MB',
    iconName: 'folder',
  },
};
