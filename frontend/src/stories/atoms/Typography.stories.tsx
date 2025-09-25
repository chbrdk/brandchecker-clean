import type { Meta, StoryObj } from '@storybook/react';
import { 
  Typography, 
  Heading1, 
  Heading2, 
  Heading3, 
  Heading4, 
  Heading5, 
  Heading6,
  Body,
  Caption,
  Small,
  Lead,
  Subtitle,
  BrandTypography
} from '../../components/atoms/Typography';

const meta: Meta<typeof Typography> = {
  title: 'Atoms/Typography',
  component: Typography,
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component: 'A comprehensive typography system with consistent font sizes, weights, colors, and text modifiers.',
      },
    },
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'body', 'caption', 'small', 'lead', 'subtitle'],
      description: 'Typography variant',
    },
    size: {
      control: 'select',
      options: ['xs', 'sm', 'base', 'lg', 'xl', '2xl', '3xl', '4xl', '5xl', '6xl'],
      description: 'Typography size override',
    },
    weight: {
      control: 'select',
      options: ['light', 'normal', 'medium', 'semibold', 'bold', 'extrabold'],
      description: 'Typography weight',
    },
    color: {
      control: 'select',
      options: ['primary', 'secondary', 'tertiary', 'success', 'warning', 'error', 'info', 'muted'],
      description: 'Typography color',
    },
    align: {
      control: 'select',
      options: ['left', 'center', 'right', 'justify'],
      description: 'Text alignment',
    },
    truncate: {
      control: 'boolean',
      description: 'Whether text should be truncated',
    },
    uppercase: {
      control: 'boolean',
      description: 'Whether text should be uppercase',
    },
    lowercase: {
      control: 'boolean',
      description: 'Whether text should be lowercase',
    },
    capitalize: {
      control: 'boolean',
      description: 'Whether text should be capitalized',
    },
    italic: {
      control: 'boolean',
      description: 'Whether text should be italic',
    },
    underline: {
      control: 'boolean',
      description: 'Whether text should be underlined',
    },
    strikethrough: {
      control: 'boolean',
      description: 'Whether text should be strikethrough',
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Typography>;

export const Default: Story = {
  args: {
    children: 'Typography Text',
  },
};

export const Headings: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <Heading1>Heading 1 - Main Title</Heading1>
      <Heading2>Heading 2 - Section Title</Heading2>
      <Heading3>Heading 3 - Subsection Title</Heading3>
      <Heading4>Heading 4 - Component Title</Heading4>
      <Heading5>Heading 5 - Small Title</Heading5>
      <Heading6>Heading 6 - Smallest Title</Heading6>
    </div>
  ),
};

export const TextVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <Lead>Lead text - This is a lead paragraph that stands out from regular body text.</Lead>
      <Body>Body text - This is regular body text used for most content.</Body>
      <Subtitle>Subtitle text - This is subtitle text used for secondary information.</Subtitle>
      <Caption>Caption text - This is caption text used for small details.</Caption>
      <Small>Small text - This is small text used for fine print.</Small>
    </div>
  ),
};

export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      <Typography size="xs">Extra Small Text (xs)</Typography>
      <Typography size="sm">Small Text (sm)</Typography>
      <Typography size="base">Base Text (base)</Typography>
      <Typography size="lg">Large Text (lg)</Typography>
      <Typography size="xl">Extra Large Text (xl)</Typography>
      <Typography size="2xl">2X Large Text (2xl)</Typography>
      <Typography size="3xl">3X Large Text (3xl)</Typography>
      <Typography size="4xl">4X Large Text (4xl)</Typography>
    </div>
  ),
};

export const Weights: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      <Typography weight="light">Light Weight Text</Typography>
      <Typography weight="normal">Normal Weight Text</Typography>
      <Typography weight="medium">Medium Weight Text</Typography>
      <Typography weight="semibold">Semibold Weight Text</Typography>
      <Typography weight="bold">Bold Weight Text</Typography>
      <Typography weight="extrabold">Extra Bold Weight Text</Typography>
    </div>
  ),
};

export const Colors: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      <Typography color="primary">Primary Color Text</Typography>
      <Typography color="secondary">Secondary Color Text</Typography>
      <Typography color="tertiary">Tertiary Color Text</Typography>
      <Typography color="success">Success Color Text</Typography>
      <Typography color="warning">Warning Color Text</Typography>
      <Typography color="error">Error Color Text</Typography>
      <Typography color="info">Info Color Text</Typography>
      <Typography color="muted">Muted Color Text</Typography>
    </div>
  ),
};

export const Alignment: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <Typography align="left">Left aligned text - This text is aligned to the left.</Typography>
      <Typography align="center">Center aligned text - This text is centered.</Typography>
      <Typography align="right">Right aligned text - This text is aligned to the right.</Typography>
      <Typography align="justify">
        Justified text - This text is justified, meaning it spreads across the full width 
        of the container with even spacing between words. This creates a clean, 
        uniform appearance for longer paragraphs.
      </Typography>
    </div>
  ),
};

export const TextModifiers: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      <Typography uppercase>Uppercase Text</Typography>
      <Typography lowercase>Lowercase Text</Typography>
      <Typography capitalize>capitalized text</Typography>
      <Typography italic>Italic Text</Typography>
      <Typography underline>Underlined Text</Typography>
      <Typography strikethrough>Strikethrough Text</Typography>
    </div>
  ),
};

export const Truncate: Story = {
  render: () => (
    <div style={{ width: '200px' }}>
      <Typography truncate>
        This is a very long text that will be truncated with ellipsis when it exceeds the container width.
      </Typography>
    </div>
  ),
};

export const BrandTypographyStory: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <BrandTypography type="brand-name">BrandChecker</BrandTypography>
      <BrandTypography type="brand-tagline">Your Brand Analysis Platform</BrandTypography>
      <BrandTypography type="brand-description">
        BrandChecker helps you analyze and maintain brand consistency across all your materials.
      </BrandTypography>
      <BrandTypography type="brand-heading">Brand Analysis Dashboard</BrandTypography>
    </div>
  ),
};

export const InteractiveExample: Story = {
  render: () => {
    const [text, setText] = React.useState('Interactive Typography');
    const [variant, setVariant] = React.useState<'h1' | 'h2' | 'h3' | 'body'>('body');
    const [color, setColor] = React.useState<'primary' | 'secondary' | 'success' | 'error'>('primary');
    const [weight, setWeight] = React.useState<'normal' | 'medium' | 'bold'>('normal');

    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <div>
          <h3>Controls</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <input
              type="text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter text..."
              style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
            />
            <select
              value={variant}
              onChange={(e) => setVariant(e.target.value as any)}
              style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
            >
              <option value="h1">Heading 1</option>
              <option value="h2">Heading 2</option>
              <option value="h3">Heading 3</option>
              <option value="body">Body</option>
            </select>
            <select
              value={color}
              onChange={(e) => setColor(e.target.value as any)}
              style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
            >
              <option value="primary">Primary</option>
              <option value="secondary">Secondary</option>
              <option value="success">Success</option>
              <option value="error">Error</option>
            </select>
            <select
              value={weight}
              onChange={(e) => setWeight(e.target.value as any)}
              style={{ padding: '8px', border: '1px solid #ccc', borderRadius: '4px' }}
            >
              <option value="normal">Normal</option>
              <option value="medium">Medium</option>
              <option value="bold">Bold</option>
            </select>
          </div>
        </div>

        <div>
          <h3>Result</h3>
          <Typography variant={variant} color={color} weight={weight}>
            {text}
          </Typography>
        </div>
      </div>
    );
  },
};

export const TypographyScale: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div>
        <h3>Heading Scale</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <Heading1>Heading 1 (4xl)</Heading1>
          <Heading2>Heading 2 (3xl)</Heading2>
          <Heading3>Heading 3 (2xl)</Heading3>
          <Heading4>Heading 4 (xl)</Heading4>
          <Heading5>Heading 5 (lg)</Heading5>
          <Heading6>Heading 6 (base)</Heading6>
        </div>
      </div>

      <div>
        <h3>Text Scale</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <Lead>Lead Text (lg)</Lead>
          <Body>Body Text (base)</Body>
          <Subtitle>Subtitle Text (sm)</Subtitle>
          <Caption>Caption Text (sm)</Caption>
          <Small>Small Text (xs)</Small>
        </div>
      </div>
    </div>
  ),
};
