import type { Meta, StoryObj } from '@storybook/react';
import { Carousel } from './Carousel';
import { ColorSwatch } from '../ColorSwatch';
import { Typography } from '../Typography';
import { Button } from '../Button';
import { Card } from '../Card';

const meta: Meta<typeof Carousel> = {
  title: 'Atoms/Carousel',
  component: Carousel,
  tags: ['autodocs'],
  argTypes: {
    children: {
      control: false,
      description: 'Content to be displayed in the carousel',
    },
    itemsPerView: {
      control: { type: 'number', min: 1, max: 5 },
      description: 'Number of items visible at once',
    },
    showArrows: {
      control: 'boolean',
      description: 'Whether to show navigation arrows',
    },
    showDots: {
      control: 'boolean',
      description: 'Whether to show pagination dots',
    },
    autoPlay: {
      control: 'boolean',
      description: 'Whether to automatically advance slides',
    },
    autoPlayInterval: {
      control: { type: 'number', min: 1000, max: 10000, step: 500 },
      description: 'Interval between auto-play transitions in milliseconds',
    },
    loop: {
      control: 'boolean',
      description: 'Whether to loop back to the beginning after the last slide',
    },
    onSlideChange: {
      action: 'slide changed',
      description: 'Callback function when slide changes',
    },
  },
};

export default meta;
type Story = StoryObj<typeof Carousel>;

// Sample color data for ColorSwatch examples
const sampleColors = [
  { hex: '#FF0000', name: 'Red', usage_percentage: 25.5, usage_count: 45 },
  { hex: '#00FF00', name: 'Green', usage_percentage: 20.3, usage_count: 36 },
  { hex: '#0000FF', name: 'Blue', usage_percentage: 18.7, usage_count: 33 },
  { hex: '#FFFF00', name: 'Yellow', usage_percentage: 15.2, usage_count: 27 },
  { hex: '#FF00FF', name: 'Magenta', usage_percentage: 12.1, usage_count: 21 },
  { hex: '#00FFFF', name: 'Cyan', usage_percentage: 8.2, usage_count: 14 },
];

// Sample content for different carousel types
const colorSwatchItems = sampleColors.map((color, index) => (
  <ColorSwatch
    key={index}
    color={color}
    size="md"
    showName={true}
    showPercentage={true}
    showCount={true}
    onClick={(color) => console.log('Color clicked:', color)}
  />
));

const textItems = Array.from({ length: 6 }, (_, index) => (
  <div key={index} style={{ textAlign: 'center', padding: 'var(--space-4)' }}>
    <Typography variant="h3" size="lg" weight="bold">
      Slide {index + 1}
    </Typography>
    <Typography variant="body" size="md" color="secondary" style={{ marginTop: 'var(--space-2)' }}>
      This is slide content number {index + 1}
    </Typography>
  </div>
));

const cardItems = Array.from({ length: 5 }, (_, index) => (
  <Card
    key={index}
    variant="elevated"
    size="md"
    style={{ margin: 'var(--space-2)' }}
  >
    <Typography variant="h4" size="md" weight="semibold">
      Card {index + 1}
    </Typography>
    <Typography variant="body" size="sm" color="secondary" style={{ marginTop: 'var(--space-2)' }}>
      This is a sample card content for slide {index + 1}.
    </Typography>
    <Button
      variant="primary"
      size="sm"
      style={{ marginTop: 'var(--space-3)' }}
      onClick={() => console.log(`Card ${index + 1} clicked`)}
    >
      Action
    </Button>
  </Card>
));

export const Default: Story = {
  args: {
    itemsPerView: 1,
    showArrows: true,
    showDots: true,
    autoPlay: false,
    loop: true,
  },
  render: (args) => (
    <div style={{ maxWidth: '600px', margin: '0 auto' }}>
      <Carousel {...args}>
        {textItems}
      </Carousel>
    </div>
  ),
};

export const MultipleItems: Story = {
  args: {
    itemsPerView: 3,
    showArrows: true,
    showDots: true,
    autoPlay: false,
    loop: true,
  },
  render: (args) => (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <Carousel {...args}>
        {textItems}
      </Carousel>
    </div>
  ),
};

export const ColorSwatchCarousel: Story = {
  args: {
    itemsPerView: 4,
    showArrows: true,
    showDots: true,
    autoPlay: false,
    loop: true,
  },
  render: (args) => (
    <div style={{ maxWidth: '600px', margin: '0 auto' }}>
      <Typography variant="h4" size="md" weight="semibold" style={{ marginBottom: 'var(--space-4)', textAlign: 'center' }}>
        Color Palette
      </Typography>
      <Carousel {...args}>
        {colorSwatchItems}
      </Carousel>
    </div>
  ),
};

export const CardCarousel: Story = {
  args: {
    itemsPerView: 2,
    showArrows: true,
    showDots: true,
    autoPlay: false,
    loop: true,
  },
  render: (args) => (
    <div style={{ maxWidth: '700px', margin: '0 auto' }}>
      <Carousel {...args}>
        {cardItems}
      </Carousel>
    </div>
  ),
};

export const AutoPlay: Story = {
  args: {
    itemsPerView: 2,
    showArrows: true,
    showDots: true,
    autoPlay: true,
    autoPlayInterval: 2000,
    loop: true,
  },
  render: (args) => (
    <div style={{ maxWidth: '600px', margin: '0 auto' }}>
      <Typography variant="body" size="sm" color="secondary" style={{ marginBottom: 'var(--space-3)', textAlign: 'center' }}>
        Auto-playing every 2 seconds
      </Typography>
      <Carousel {...args}>
        {textItems}
      </Carousel>
    </div>
  ),
};

export const NoArrows: Story = {
  args: {
    itemsPerView: 3,
    showArrows: false,
    showDots: true,
    autoPlay: false,
    loop: true,
  },
  render: (args) => (
    <div style={{ maxWidth: '600px', margin: '0 auto' }}>
      <Carousel {...args}>
        {textItems}
      </Carousel>
    </div>
  ),
};

export const NoDots: Story = {
  args: {
    itemsPerView: 2,
    showArrows: true,
    showDots: false,
    autoPlay: false,
    loop: true,
  },
  render: (args) => (
    <div style={{ maxWidth: '600px', margin: '0 auto' }}>
      <Carousel {...args}>
        {textItems}
      </Carousel>
    </div>
  ),
};

export const NoLoop: Story = {
  args: {
    itemsPerView: 2,
    showArrows: true,
    showDots: true,
    autoPlay: false,
    loop: false,
  },
  render: (args) => (
    <div style={{ maxWidth: '600px', margin: '0 auto' }}>
      <Typography variant="body" size="sm" color="secondary" style={{ marginBottom: 'var(--space-3)', textAlign: 'center' }}>
        No looping - arrows disabled at ends
      </Typography>
      <Carousel {...args}>
        {textItems}
      </Carousel>
    </div>
  ),
};

export const Responsive: Story = {
  args: {
    itemsPerView: 1,
    showArrows: true,
    showDots: true,
    autoPlay: false,
    loop: true,
  },
  render: (args) => (
    <div style={{ maxWidth: '100%', margin: '0 auto' }}>
      <Typography variant="body" size="sm" color="secondary" style={{ marginBottom: 'var(--space-3)', textAlign: 'center' }}>
        Responsive carousel - adjust window size to see changes
      </Typography>
      <Carousel {...args}>
        {colorSwatchItems}
      </Carousel>
    </div>
  ),
};

export const SingleItem: Story = {
  args: {
    itemsPerView: 1,
    showArrows: false,
    showDots: false,
    autoPlay: true,
    autoPlayInterval: 3000,
    loop: true,
  },
  render: (args) => (
    <div style={{ maxWidth: '400px', margin: '0 auto' }}>
      <Carousel {...args}>
        {textItems.slice(0, 3)}
      </Carousel>
    </div>
  ),
};

export const Interactive: Story = {
  args: {
    itemsPerView: 2,
    showArrows: true,
    showDots: true,
    autoPlay: false,
    loop: true,
  },
  render: (args) => (
    <div style={{ maxWidth: '600px', margin: '0 auto' }}>
      <Typography variant="body" size="sm" color="secondary" style={{ marginBottom: 'var(--space-3)', textAlign: 'center' }}>
        Click dots or arrows to navigate
      </Typography>
      <Carousel {...args}>
        {cardItems}
      </Carousel>
    </div>
  ),
};
