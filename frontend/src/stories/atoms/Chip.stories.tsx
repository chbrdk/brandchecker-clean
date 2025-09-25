import type { Meta, StoryObj } from '@storybook/react';
import { Chip, ChipGroup } from '../../components/atoms/Chip';

const meta: Meta<typeof Chip> = {
  title: 'Atoms/Chip',
  component: Chip,
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component: 'A versatile chip/tag component for displaying labels, categories, and interactive elements with various variants and states.',
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'primary', 'secondary', 'success', 'warning', 'error', 'info'],
      description: 'Chip visual variant',
    },
    size: {
      control: 'select',
      options: ['small', 'medium', 'large'],
      description: 'Chip size',
    },
    removable: {
      control: 'boolean',
      description: 'Whether the chip can be removed',
    },
    disabled: {
      control: 'boolean',
      description: 'Whether the chip is disabled',
    },
    selected: {
      control: 'boolean',
      description: 'Whether the chip is selected',
    },
    clickable: {
      control: 'boolean',
      description: 'Whether the chip is clickable',
    },
    icon: {
      control: 'select',
      options: [
        'check', 'x', 'info', 'warning', 'error', 'success',
        'eye', 'color-palette', 'type', 'logo', 'analytics',
        'user', 'settings', 'star', 'heart', 'bookmark'
      ],
      description: 'Icon to display',
    },
    iconPosition: {
      control: 'select',
      options: ['left', 'right'],
      description: 'Icon position',
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Chip>;

export const Default: Story = {
  args: {
    children: 'Default Chip',
  },
};

export const Variants: Story = {
  render: () => (
    <ChipGroup spacing="medium">
      <Chip variant="default">Default</Chip>
      <Chip variant="primary">Primary</Chip>
      <Chip variant="secondary">Secondary</Chip>
      <Chip variant="success">Success</Chip>
      <Chip variant="warning">Warning</Chip>
      <Chip variant="error">Error</Chip>
      <Chip variant="info">Info</Chip>
    </ChipGroup>
  ),
};

export const Sizes: Story = {
  render: () => (
    <ChipGroup spacing="medium">
      <Chip size="small">Small</Chip>
      <Chip size="medium">Medium</Chip>
      <Chip size="large">Large</Chip>
    </ChipGroup>
  ),
};

export const WithIcons: Story = {
  render: () => (
    <ChipGroup spacing="medium">
      <Chip icon="check" iconPosition="left">Success</Chip>
      <Chip icon="warning" iconPosition="left">Warning</Chip>
      <Chip icon="error" iconPosition="left">Error</Chip>
      <Chip icon="info" iconPosition="left">Info</Chip>
      <Chip icon="star" iconPosition="right">Favorite</Chip>
      <Chip icon="heart" iconPosition="right">Liked</Chip>
    </ChipGroup>
  ),
};

export const Removable: Story = {
  render: () => (
    <ChipGroup spacing="medium">
      <Chip removable onRemove={() => alert('Removed!')}>Removable</Chip>
      <Chip variant="primary" removable onRemove={() => alert('Removed!')}>Primary Removable</Chip>
      <Chip variant="success" removable onRemove={() => alert('Removed!')}>Success Removable</Chip>
      <Chip variant="warning" removable onRemove={() => alert('Removed!')}>Warning Removable</Chip>
    </ChipGroup>
  ),
};

export const Clickable: Story = {
  render: () => (
    <ChipGroup spacing="medium">
      <Chip clickable onClick={() => alert('Clicked!')}>Clickable</Chip>
      <Chip variant="primary" clickable onClick={() => alert('Clicked!')}>Primary Clickable</Chip>
      <Chip variant="secondary" clickable onClick={() => alert('Clicked!')}>Secondary Clickable</Chip>
    </ChipGroup>
  ),
};

export const Selected: Story = {
  render: () => (
    <ChipGroup spacing="medium">
      <Chip selected>Selected</Chip>
      <Chip variant="primary" selected>Primary Selected</Chip>
      <Chip variant="success" selected>Success Selected</Chip>
      <Chip variant="warning" selected>Warning Selected</Chip>
    </ChipGroup>
  ),
};

export const Disabled: Story = {
  render: () => (
    <ChipGroup spacing="medium">
      <Chip disabled>Disabled</Chip>
      <Chip variant="primary" disabled>Primary Disabled</Chip>
      <Chip variant="success" disabled>Success Disabled</Chip>
      <Chip removable disabled onRemove={() => alert('Removed!')}>Removable Disabled</Chip>
    </ChipGroup>
  ),
};

export const BrandAnalysis: Story = {
  render: () => (
    <ChipGroup spacing="medium">
      <Chip variant="success" icon="check">Compliant</Chip>
      <Chip variant="error" icon="x">Non-Compliant</Chip>
      <Chip variant="warning" icon="warning">Warning</Chip>
      <Chip variant="info" icon="info">Pending</Chip>
      <Chip icon="eye">Analysis Complete</Chip>
      <Chip icon="color-palette">Color Analysis</Chip>
      <Chip icon="type">Typography</Chip>
      <Chip icon="logo">Logo Detection</Chip>
    </ChipGroup>
  ),
};

export const StatusTags: Story = {
  render: () => (
    <ChipGroup spacing="medium">
      <Chip variant="success" icon="check">Approved</Chip>
      <Chip variant="error" icon="x">Rejected</Chip>
      <Chip variant="warning" icon="warning">Review Required</Chip>
      <Chip variant="info" icon="info">In Progress</Chip>
      <Chip variant="default" icon="clock">Scheduled</Chip>
      <Chip variant="secondary" icon="user">Assigned</Chip>
    </ChipGroup>
  ),
};

export const CategoryTags: Story = {
  render: () => (
    <ChipGroup spacing="medium">
      <Chip variant="primary" icon="color-palette">Colors</Chip>
      <Chip variant="primary" icon="type">Typography</Chip>
      <Chip variant="primary" icon="logo">Logo</Chip>
      <Chip variant="primary" icon="layout">Layout</Chip>
      <Chip variant="primary" icon="analytics">Analytics</Chip>
      <Chip variant="primary" icon="brand">Brand Guidelines</Chip>
    </ChipGroup>
  ),
};

export const InteractiveExample: Story = {
  render: () => {
    const [selectedChips, setSelectedChips] = React.useState<string[]>([]);
    const [removableChips, setRemovableChips] = React.useState(['Tag 1', 'Tag 2', 'Tag 3']);

    const handleChipClick = (chip: string) => {
      setSelectedChips(prev => 
        prev.includes(chip) 
          ? prev.filter(c => c !== chip)
          : [...prev, chip]
      );
    };

    const handleChipRemove = (chip: string) => {
      setRemovableChips(prev => prev.filter(c => c !== chip));
    };

    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <div>
          <h4>Selectable Chips</h4>
          <ChipGroup spacing="medium">
            {['Design', 'Development', 'Marketing', 'Sales'].map(chip => (
              <Chip
                key={chip}
                clickable
                selected={selectedChips.includes(chip)}
                onClick={() => handleChipClick(chip)}
              >
                {chip}
              </Chip>
            ))}
          </ChipGroup>
          <p style={{ marginTop: '8px', fontSize: '14px', color: '#666' }}>
            Selected: {selectedChips.join(', ') || 'None'}
          </p>
        </div>

        <div>
          <h4>Removable Chips</h4>
          <ChipGroup spacing="medium">
            {removableChips.map(chip => (
              <Chip
                key={chip}
                removable
                variant="primary"
                onRemove={() => handleChipRemove(chip)}
              >
                {chip}
              </Chip>
            ))}
          </ChipGroup>
        </div>
      </div>
    );
  },
};

export const ChipGroupVariations: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h4>Left Aligned</h4>
        <ChipGroup align="left" spacing="medium">
          <Chip variant="primary">Primary</Chip>
          <Chip variant="secondary">Secondary</Chip>
          <Chip variant="success">Success</Chip>
        </ChipGroup>
      </div>

      <div>
        <h4>Center Aligned</h4>
        <ChipGroup align="center" spacing="medium">
          <Chip variant="primary">Primary</Chip>
          <Chip variant="secondary">Secondary</Chip>
          <Chip variant="success">Success</Chip>
        </ChipGroup>
      </div>

      <div>
        <h4>Right Aligned</h4>
        <ChipGroup align="right" spacing="medium">
          <Chip variant="primary">Primary</Chip>
          <Chip variant="secondary">Secondary</Chip>
          <Chip variant="success">Success</Chip>
        </ChipGroup>
      </div>

      <div>
        <h4>Different Spacing</h4>
        <ChipGroup spacing="small">
          <Chip variant="primary">Small</Chip>
          <Chip variant="secondary">Spacing</Chip>
          <Chip variant="success">Group</Chip>
        </ChipGroup>
        <ChipGroup spacing="large" style={{ marginTop: '16px' }}>
          <Chip variant="primary">Large</Chip>
          <Chip variant="secondary">Spacing</Chip>
          <Chip variant="success">Group</Chip>
        </ChipGroup>
      </div>
    </div>
  ),
};
