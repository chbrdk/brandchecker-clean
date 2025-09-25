import type { Meta, StoryObj } from '@storybook/react';
import { Input } from '../../components/atoms/Input';

const meta: Meta<typeof Input> = {
  title: 'Atoms/Input',
  component: Input,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A versatile input component with multiple variants, sizes, and validation states.',
      },
    },
  },
  argTypes: {
    type: {
      control: 'select',
      options: ['text', 'email', 'password', 'number', 'file', 'search'],
      description: 'Input type',
    },
    size: {
      control: 'select',
      options: ['small', 'medium', 'large'],
      description: 'Input size',
    },
    variant: {
      control: 'select',
      options: ['outlined', 'filled', 'underlined'],
      description: 'Input variant style',
    },
    disabled: {
      control: 'boolean',
      description: 'Disable the input',
    },
    required: {
      control: 'boolean',
      description: 'Mark as required field',
    },
    label: {
      control: 'text',
      description: 'Input label',
    },
    placeholder: {
      control: 'text',
      description: 'Placeholder text',
    },
    error: {
      control: 'text',
      description: 'Error message',
    },
    success: {
      control: 'text',
      description: 'Success message',
    },
    helpText: {
      control: 'text',
      description: 'Help text',
    },
    iconPosition: {
      control: 'select',
      options: ['left', 'right'],
      description: 'Position of the icon',
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

// Default story
export const Default: Story = {
  args: {
    placeholder: 'Enter text...',
  },
};

// With label
export const WithLabel: Story = {
  args: {
    label: 'Email Address',
    placeholder: 'Enter your email',
    type: 'email',
  },
};

// Required field
export const Required: Story = {
  args: {
    label: 'Required Field',
    placeholder: 'This field is required',
    required: true,
  },
};

// Error state
export const WithError: Story = {
  args: {
    label: 'Email Address',
    placeholder: 'Enter your email',
    type: 'email',
    error: 'Please enter a valid email address',
    defaultValue: 'invalid-email',
  },
};

// Success state
export const WithSuccess: Story = {
  args: {
    label: 'Email Address',
    placeholder: 'Enter your email',
    type: 'email',
    success: 'Email address is valid',
    defaultValue: 'user@example.com',
  },
};

// With help text
export const WithHelpText: Story = {
  args: {
    label: 'Password',
    placeholder: 'Enter your password',
    type: 'password',
    helpText: 'Password must be at least 8 characters long',
  },
};

// Disabled
export const Disabled: Story = {
  args: {
    label: 'Disabled Input',
    placeholder: 'This input is disabled',
    disabled: true,
    defaultValue: 'Disabled value',
  },
};

// Sizes
export const Small: Story = {
  args: {
    label: 'Small Input',
    placeholder: 'Small size',
    size: 'small',
  },
};

export const Medium: Story = {
  args: {
    label: 'Medium Input',
    placeholder: 'Medium size',
    size: 'medium',
  },
};

export const Large: Story = {
  args: {
    label: 'Large Input',
    placeholder: 'Large size',
    size: 'large',
  },
};

// Variants
export const Outlined: Story = {
  args: {
    label: 'Outlined Input',
    placeholder: 'Outlined variant',
    variant: 'outlined',
  },
};

export const Filled: Story = {
  args: {
    label: 'Filled Input',
    placeholder: 'Filled variant',
    variant: 'filled',
  },
};

export const Underlined: Story = {
  args: {
    label: 'Underlined Input',
    placeholder: 'Underlined variant',
    variant: 'underlined',
  },
};

// With icons
export const WithIconLeft: Story = {
  args: {
    label: 'Search',
    placeholder: 'Search...',
    type: 'search',
    icon: (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"/>
        <path d="m21 21-4.35-4.35"/>
      </svg>
    ),
    iconPosition: 'left',
  },
};

export const WithIconRight: Story = {
  args: {
    label: 'Password',
    placeholder: 'Enter password',
    type: 'password',
    icon: (
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
        <circle cx="12" cy="16" r="1"/>
        <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
      </svg>
    ),
    iconPosition: 'right',
  },
};

// File input
export const FileInput: Story = {
  args: {
    label: 'Upload File',
    type: 'file',
    helpText: 'Select a file to upload',
  },
};

// Number input
export const NumberInput: Story = {
  args: {
    label: 'Age',
    type: 'number',
    placeholder: 'Enter your age',
    min: 0,
    max: 120,
  },
};

// Interactive validation test
export const InteractiveValidation: Story = {
  args: {
    label: 'Email Address',
    placeholder: 'Enter your email',
    type: 'email',
    required: true,
  },
};

// Interactive form workflow
export const FormWorkflow: Story = {
  args: {
    label: 'Password',
    placeholder: 'Enter password',
    type: 'password',
    helpText: 'Password must be at least 8 characters',
  },
};

// All variants showcase
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', width: '400px' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h3>Variants</h3>
        <Input variant="outlined" placeholder="Outlined" />
        <Input variant="filled" placeholder="Filled" />
        <Input variant="underlined" placeholder="Underlined" />
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h3>Sizes</h3>
        <Input size="small" placeholder="Small" />
        <Input size="medium" placeholder="Medium" />
        <Input size="large" placeholder="Large" />
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h3>States</h3>
        <Input placeholder="Normal" />
        <Input placeholder="With Error" error="This field has an error" />
        <Input placeholder="With Success" success="This field is valid" />
        <Input placeholder="Disabled" disabled />
        <Input placeholder="Required" required />
      </div>
    </div>
  ),
  parameters: {
    layout: 'padded',
  },
};
