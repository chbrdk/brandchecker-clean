import type { Meta, StoryObj } from '@storybook/react';
import { BrandCheckerPage } from '../../components/templates/BrandCheckerPage';

const meta: Meta<typeof BrandCheckerPage> = {
  title: 'Templates/BrandCheckerPage',
  component: BrandCheckerPage,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Main template for the BrandChecker application with different stages and sticky toolbar.'
      }
    }
  },
  argTypes: {
    stage: {
      control: 'select',
      options: ['initial', 'uploading', 'processing', 'chat', 'results'],
      description: 'Current stage of the application'
    },
    onStageChange: {
      action: 'stage changed',
      description: 'Stage change handler'
    },
    onFileUpload: {
      action: 'files uploaded',
      description: 'File upload handler'
    },
    onSendMessage: {
      action: 'message sent',
      description: 'Message send handler'
    }
  },
  tags: ['autodocs']
};

export default meta;
type Story = StoryObj<typeof BrandCheckerPage>;

export const Initial: Story = {
  args: {
    stage: 'initial'
  }
};

export const Uploading: Story = {
  args: {
    stage: 'uploading'
  }
};

export const Processing: Story = {
  args: {
    stage: 'processing'
  }
};
