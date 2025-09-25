import type { Meta, StoryObj } from '@storybook/react';
import { ChatToolbar } from '../../components/molecules/ChatToolbar/ChatToolbar';

const meta: Meta<typeof ChatToolbar> = {
  title: 'Molecules/ChatToolbar',
  component: ChatToolbar,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A clean, minimalist toolbar for chat input with text input, send button, and file upload. Designed for practical use without unnecessary branding or marketing elements.',
      },
    },
  },
  argTypes: {
    loading: {
      control: 'boolean',
      description: 'Whether the toolbar is loading',
    },
    disabled: {
      control: 'boolean',
      description: 'Whether the toolbar is disabled',
    },
    placeholder: {
      control: 'text',
      description: 'Placeholder text for input',
    },
    onMessageSend: {
      action: 'message sent',
      description: 'Callback when a message is sent',
    },
    onFilesUpload: {
      action: 'files uploaded',
      description: 'Callback when files are uploaded',
    },
  },
};

export default meta;
type Story = StoryObj<typeof ChatToolbar>;

export const Default: Story = {
  args: {
    loading: false,
    disabled: false,
    placeholder: 'Ask about your brand...',
  },
};

export const Loading: Story = {
  args: {
    loading: true,
    disabled: false,
    placeholder: 'Ask about your brand...',
  },
};

export const Disabled: Story = {
  args: {
    loading: false,
    disabled: true,
    placeholder: 'Ask about your brand...',
  },
};

export const WithInteraction: Story = {
  args: {
    loading: false,
    disabled: false,
    placeholder: 'Ask about your brand...',
    onMessageSend: (message, files) => {
      console.log('Message sent:', message);
      console.log('Files uploaded:', files);
    },
    onFilesUpload: (files) => {
      console.log('Files uploaded:', files);
    },
  },
};

export const InteractiveDemo: Story = {
  args: {
    loading: false,
    disabled: false,
    placeholder: 'Ask about your brand...',
    onMessageSend: (message, files) => {
      alert(`Message: "${message}"\nFiles: ${files?.length || 0} files uploaded`);
    },
    onFilesUpload: (files) => {
      alert(`${files.length} files uploaded:\n${files.map(f => f.name).join('\n')}`);
    },
  },
};

export const CustomPlaceholder: Story = {
  args: {
    loading: false,
    disabled: false,
    placeholder: 'Type your question here...',
  },
};
