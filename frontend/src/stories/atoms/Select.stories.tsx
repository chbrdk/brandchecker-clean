import type { Meta, StoryObj } from '@storybook/react';
import { Select } from '../../components/atoms/Select';

const meta: Meta<typeof Select> = {
  title: 'Atoms/Select',
  component: Select,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A versatile select component with multiple selection, search, and grouping capabilities.',
      },
    },
  },
  argTypes: {
    size: {
      control: 'select',
      options: ['small', 'medium', 'large'],
      description: 'Select size',
    },
    variant: {
      control: 'select',
      options: ['outlined', 'filled'],
      description: 'Select variant style',
    },
    disabled: {
      control: 'boolean',
      description: 'Disable the select',
    },
    required: {
      control: 'boolean',
      description: 'Mark as required field',
    },
    multiple: {
      control: 'boolean',
      description: 'Allow multiple selection',
    },
    searchable: {
      control: 'boolean',
      description: 'Enable search functionality',
    },
    clearable: {
      control: 'boolean',
      description: 'Allow clearing selection',
    },
    label: {
      control: 'text',
      description: 'Select label',
    },
    placeholder: {
      control: 'text',
      description: 'Placeholder text',
    },
    error: {
      control: 'text',
      description: 'Error message',
    },
    helpText: {
      control: 'text',
      description: 'Help text',
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

// Sample options
const basicOptions = [
  { value: 'option1', label: 'Option 1' },
  { value: 'option2', label: 'Option 2' },
  { value: 'option3', label: 'Option 3' },
  { value: 'option4', label: 'Option 4' },
  { value: 'option5', label: 'Option 5' },
];

const groupedOptions = [
  { value: 'apple', label: 'Apple', group: 'Fruits' },
  { value: 'banana', label: 'Banana', group: 'Fruits' },
  { value: 'orange', label: 'Orange', group: 'Fruits' },
  { value: 'carrot', label: 'Carrot', group: 'Vegetables' },
  { value: 'broccoli', label: 'Broccoli', group: 'Vegetables' },
  { value: 'spinach', label: 'Spinach', group: 'Vegetables' },
];

const manyOptions = Array.from({ length: 50 }, (_, i) => ({
  value: `option${i + 1}`,
  label: `Option ${i + 1}`,
}));

// Default story
export const Default: Story = {
  args: {
    options: basicOptions,
    placeholder: 'Select an option...',
  },
};

// With label
export const WithLabel: Story = {
  args: {
    options: basicOptions,
    label: 'Choose an option',
    placeholder: 'Select an option...',
  },
};

// Required field
export const Required: Story = {
  args: {
    options: basicOptions,
    label: 'Required Field',
    placeholder: 'This field is required',
    required: true,
  },
};

// Error state
export const WithError: Story = {
  args: {
    options: basicOptions,
    label: 'Select Option',
    placeholder: 'Select an option...',
    error: 'Please select a valid option',
  },
};

// With help text
export const WithHelpText: Story = {
  args: {
    options: basicOptions,
    label: 'Select Option',
    placeholder: 'Select an option...',
    helpText: 'Choose the best option for your needs',
  },
};

// Disabled
export const Disabled: Story = {
  args: {
    options: basicOptions,
    label: 'Disabled Select',
    placeholder: 'This select is disabled',
    disabled: true,
    value: 'option1',
  },
};

// Sizes
export const Small: Story = {
  args: {
    options: basicOptions,
    label: 'Small Select',
    placeholder: 'Small size',
    size: 'small',
  },
};

export const Medium: Story = {
  args: {
    options: basicOptions,
    label: 'Medium Select',
    placeholder: 'Medium size',
    size: 'medium',
  },
};

export const Large: Story = {
  args: {
    options: basicOptions,
    label: 'Large Select',
    placeholder: 'Large size',
    size: 'large',
  },
};

// Variants
export const Outlined: Story = {
  args: {
    options: basicOptions,
    label: 'Outlined Select',
    placeholder: 'Outlined variant',
    variant: 'outlined',
  },
};

export const Filled: Story = {
  args: {
    options: basicOptions,
    label: 'Filled Select',
    placeholder: 'Filled variant',
    variant: 'filled',
  },
};

// Multiple selection
export const Multiple: Story = {
  args: {
    options: basicOptions,
    label: 'Multiple Selection',
    placeholder: 'Select multiple options...',
    multiple: true,
  },
};

// Searchable
export const Searchable: Story = {
  args: {
    options: manyOptions,
    label: 'Searchable Select',
    placeholder: 'Search and select...',
    searchable: true,
  },
};

// Clearable
export const Clearable: Story = {
  args: {
    options: basicOptions,
    label: 'Clearable Select',
    placeholder: 'Select an option...',
    clearable: true,
    value: 'option1',
  },
};

// With groups
export const WithGroups: Story = {
  args: {
    options: groupedOptions,
    label: 'Grouped Options',
    placeholder: 'Select from groups...',
  },
};

// Multiple with groups
export const MultipleWithGroups: Story = {
  args: {
    options: groupedOptions,
    label: 'Multiple Selection with Groups',
    placeholder: 'Select multiple items...',
    multiple: true,
  },
};

// Searchable with groups
export const SearchableWithGroups: Story = {
  args: {
    options: groupedOptions,
    label: 'Searchable with Groups',
    placeholder: 'Search within groups...',
    searchable: true,
  },
};

// All features combined
export const AllFeatures: Story = {
  args: {
    options: groupedOptions,
    label: 'All Features',
    placeholder: 'Search, select multiple, clear...',
    multiple: true,
    searchable: true,
    clearable: true,
    helpText: 'This select has all features enabled',
  },
};

// Interactive example
export const Interactive: Story = {
  args: {
    options: basicOptions,
    label: 'Interactive Select',
    placeholder: 'Click to interact',
    onChange: (value) => console.log('Selected:', value),
  },
};

// All variants showcase
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', width: '400px' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h3>Variants</h3>
        <Select options={basicOptions} variant="outlined" placeholder="Outlined" />
        <Select options={basicOptions} variant="filled" placeholder="Filled" />
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h3>Sizes</h3>
        <Select options={basicOptions} size="small" placeholder="Small" />
        <Select options={basicOptions} size="medium" placeholder="Medium" />
        <Select options={basicOptions} size="large" placeholder="Large" />
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h3>Features</h3>
        <Select options={basicOptions} placeholder="Basic" />
        <Select options={basicOptions} multiple placeholder="Multiple" />
        <Select options={basicOptions} searchable placeholder="Searchable" />
        <Select options={basicOptions} clearable placeholder="Clearable" />
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <h3>States</h3>
        <Select options={basicOptions} placeholder="Normal" />
        <Select options={basicOptions} placeholder="With Error" error="This field has an error" />
        <Select options={basicOptions} placeholder="Disabled" disabled />
        <Select options={basicOptions} placeholder="Required" required />
      </div>
    </div>
  ),
  parameters: {
    layout: 'padded',
  },
};
