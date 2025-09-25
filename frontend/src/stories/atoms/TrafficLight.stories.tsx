import type { Meta, StoryObj } from '@storybook/react';
import { TrafficLight } from '../../components/atoms/TrafficLight';

const meta: Meta<typeof TrafficLight> = {
  title: 'Atoms/TrafficLight',
  component: TrafficLight,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Traffic light component for displaying status indicators with color coding.'
      }
    }
  },
  argTypes: {
    status: {
      control: 'select',
      options: ['error', 'warning', 'success'],
      description: 'Status type'
    },
    label: {
      control: 'text',
      description: 'Custom label text'
    },
    showLabel: {
      control: 'boolean',
      description: 'Show label'
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
      description: 'Size variant'
    },
    iconName: {
      control: 'select',
      options: ['alert-circle', 'info', 'check-circle', 'alert-triangle', 'x-circle'],
      description: 'Custom icon name'
    }
  },
  tags: ['autodocs']
};

export default meta;
type Story = StoryObj<typeof TrafficLight>;

export const Success: Story = {
  args: {
    status: 'success',
    label: 'All Good',
    size: 'md'
  }
};

export const Warning: Story = {
  args: {
    status: 'warning',
    label: 'Needs Attention',
    size: 'md'
  }
};

export const Error: Story = {
  args: {
    status: 'error',
    label: 'Critical Issue',
    size: 'md'
  }
};

export const WithoutLabel: Story = {
  args: {
    status: 'success',
    showLabel: false,
    size: 'md'
  }
};

export const CustomIcon: Story = {
  args: {
    status: 'warning',
    label: 'Custom Warning',
    iconName: 'alert-triangle',
    size: 'lg'
  }
};

export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <TrafficLight status="success" label="Small" size="sm" />
      <TrafficLight status="warning" label="Medium" size="md" />
      <TrafficLight status="error" label="Large" size="lg" />
    </div>
  )
};

export const AllStatuses: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <TrafficLight status="error" label="Error" size="md" />
      <TrafficLight status="warning" label="Warning" size="md" />
      <TrafficLight status="success" label="Success" size="md" />
    </div>
  )
};

export const DefaultLabels: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <TrafficLight status="error" size="md" />
      <TrafficLight status="warning" size="md" />
      <TrafficLight status="success" size="md" />
    </div>
  )
};
