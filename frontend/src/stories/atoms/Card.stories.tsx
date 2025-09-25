import type { Meta, StoryObj } from '@storybook/react';
import { Card } from '../../components/atoms/Card';

const meta: Meta<typeof Card> = {
  title: 'Atoms/Card',
  component: Card,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A flexible card component with multiple variants, padding options, and interactive states.',
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['elevated', 'outlined', 'filled'],
      description: 'Card variant style',
    },
    padding: {
      control: 'select',
      options: ['none', 'small', 'medium', 'large'],
      description: 'Card padding size',
    },
    hoverable: {
      control: 'boolean',
      description: 'Enable hover effects',
    },
    clickable: {
      control: 'boolean',
      description: 'Make card clickable',
    },
    loading: {
      control: 'boolean',
      description: 'Show loading skeleton',
    },
    title: {
      control: 'text',
      description: 'Card title',
    },
    subtitle: {
      control: 'text',
      description: 'Card subtitle',
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

// Default story
export const Default: Story = {
  args: {
    children: 'This is a basic card with some content.',
  },
};

// With title
export const WithTitle: Story = {
  args: {
    title: 'Card Title',
    children: 'This card has a title and some content below it.',
  },
};

// With title and subtitle
export const WithTitleAndSubtitle: Story = {
  args: {
    title: 'Card Title',
    subtitle: 'This is a subtitle',
    children: 'This card has both a title and subtitle.',
  },
};

// Variants
export const Elevated: Story = {
  args: {
    title: 'Elevated Card',
    children: 'This card has an elevated shadow effect.',
    variant: 'elevated',
  },
};

export const Outlined: Story = {
  args: {
    title: 'Outlined Card',
    children: 'This card has a border outline.',
    variant: 'outlined',
  },
};

export const Filled: Story = {
  args: {
    title: 'Filled Card',
    children: 'This card has a filled background.',
    variant: 'filled',
  },
};

// Padding variants
export const NoPadding: Story = {
  args: {
    title: 'No Padding',
    children: 'This card has no padding.',
    padding: 'none',
  },
};

export const SmallPadding: Story = {
  args: {
    title: 'Small Padding',
    children: 'This card has small padding.',
    padding: 'small',
  },
};

export const MediumPadding: Story = {
  args: {
    title: 'Medium Padding',
    children: 'This card has medium padding.',
    padding: 'medium',
  },
};

export const LargePadding: Story = {
  args: {
    title: 'Large Padding',
    children: 'This card has large padding.',
    padding: 'large',
  },
};

// Interactive states
export const Hoverable: Story = {
  args: {
    title: 'Hoverable Card',
    children: 'Hover over this card to see the effect.',
    hoverable: true,
  },
};

export const Clickable: Story = {
  args: {
    title: 'Clickable Card',
    children: 'Click this card to see the interaction.',
    clickable: true,
    onClick: () => alert('Card clicked!'),
  },
};

export const Loading: Story = {
  args: {
    title: 'Loading Card',
    children: 'This content will be replaced with a loading skeleton.',
    loading: true,
  },
};

// With custom header
export const CustomHeader: Story = {
  args: {
    title: 'Custom Header',
    children: 'This card has a custom header with an action button.',
  },
};

// With custom footer
export const CustomFooter: Story = {
  args: {
    title: 'Card with Footer',
    children: 'This card has a custom footer.',
  },
};

// Interactive clickable card
export const ClickableInteraction: Story = {
  args: {
    title: 'Clickable Card',
    children: 'Click this card to interact.',
    clickable: true,
    onClick: () => alert('Card clicked!'),
  },
};

// Loading state interaction
export const LoadingInteraction: Story = {
  args: {
    title: 'Loading Card',
    children: 'This content will be replaced with a loading skeleton.',
    loading: true,
  },
};

// All variants showcase
export const AllVariants: Story = {
  render: () => (
    <div>
      <Card variant="elevated" title="Elevated Card">This is an elevated card with shadow.</Card>
      <Card variant="outlined" title="Outlined Card">This is an outlined card with border.</Card>
      <Card variant="filled" title="Filled Card">This is a filled card with background.</Card>
    </div>
  ),
  parameters: {
    layout: 'padded',
  },
};
