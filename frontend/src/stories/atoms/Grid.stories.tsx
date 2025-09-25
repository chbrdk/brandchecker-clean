import type { Meta, StoryObj } from '@storybook/react';
import { Grid, GridItem } from '../../components/atoms/Grid';
import { Card } from '../../components/atoms/Card';

const meta: Meta<typeof Grid> = {
  title: 'Atoms/Grid',
  component: Grid,
  parameters: {
    layout: 'padded',
  },
  argTypes: {
    columns: {
      control: { type: 'select' },
      options: [1, 2, 3, 4, 6, 12],
    },
    gap: {
      control: { type: 'select' },
      options: ['none', 'sm', 'md', 'lg'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof Grid>;

// Helper component for demo content
const DemoCard = ({ children, color = 'blue' }: { children: React.ReactNode; color?: string }) => (
  <Card style={{ backgroundColor: `var(--color-${color}-50)`, border: `1px solid var(--color-${color}-200)` }}>
    <div style={{ padding: '16px', textAlign: 'center' }}>
      {children}
    </div>
  </Card>
);

export const Default: Story = {
  args: {
    columns: 12,
    gap: 'md',
  },
  render: (args) => (
    <Grid {...args}>
      <GridItem span={6}>
        <DemoCard color="blue">Item 1 (50%)</DemoCard>
      </GridItem>
      <GridItem span={6}>
        <DemoCard color="green">Item 2 (50%)</DemoCard>
      </GridItem>
    </Grid>
  ),
};

export const TwoColumns: Story = {
  args: {
    columns: 2,
    gap: 'md',
  },
  render: (args) => (
    <Grid {...args}>
      <GridItem span={1}>
        <DemoCard color="blue">Left</DemoCard>
      </GridItem>
      <GridItem span={1}>
        <DemoCard color="green">Right</DemoCard>
      </GridItem>
    </Grid>
  ),
};

export const ThreeColumns: Story = {
  args: {
    columns: 3,
    gap: 'lg',
  },
  render: (args) => (
    <Grid {...args}>
      <GridItem span={1}>
        <DemoCard color="blue">Column 1</DemoCard>
      </GridItem>
      <GridItem span={1}>
        <DemoCard color="green">Column 2</DemoCard>
      </GridItem>
      <GridItem span={1}>
        <DemoCard color="purple">Column 3</DemoCard>
      </GridItem>
    </Grid>
  ),
};

export const FourColumns: Story = {
  args: {
    columns: 4,
    gap: 'sm',
  },
  render: (args) => (
    <Grid {...args}>
      <GridItem span={1}>
        <DemoCard color="blue">1</DemoCard>
      </GridItem>
      <GridItem span={1}>
        <DemoCard color="green">2</DemoCard>
      </GridItem>
      <GridItem span={1}>
        <DemoCard color="purple">3</DemoCard>
      </GridItem>
      <GridItem span={1}>
        <DemoCard color="orange">4</DemoCard>
      </GridItem>
    </Grid>
  ),
};

export const TwelveColumnSystem: Story = {
  args: {
    columns: 12,
    gap: 'md',
  },
  render: (args) => (
    <Grid {...args}>
      <GridItem span={12}>
        <DemoCard color="blue">Full Width (12/12)</DemoCard>
      </GridItem>
      <GridItem span={6}>
        <DemoCard color="green">Half Width (6/12)</DemoCard>
      </GridItem>
      <GridItem span={6}>
        <DemoCard color="purple">Half Width (6/12)</DemoCard>
      </GridItem>
      <GridItem span={4}>
        <DemoCard color="orange">Third Width (4/12)</DemoCard>
      </GridItem>
      <GridItem span={4}>
        <DemoCard color="red">Third Width (4/12)</DemoCard>
      </GridItem>
      <GridItem span={4}>
        <DemoCard color="yellow">Third Width (4/12)</DemoCard>
      </GridItem>
    </Grid>
  ),
};

export const DifferentGaps: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      <div>
        <h3>No Gap</h3>
        <Grid columns={3} gap="none">
          <GridItem span={1}><DemoCard color="blue">1</DemoCard></GridItem>
          <GridItem span={1}><DemoCard color="green">2</DemoCard></GridItem>
          <GridItem span={1}><DemoCard color="purple">3</DemoCard></GridItem>
        </Grid>
      </div>
      
      <div>
        <h3>Small Gap</h3>
        <Grid columns={3} gap="sm">
          <GridItem span={1}><DemoCard color="blue">1</DemoCard></GridItem>
          <GridItem span={1}><DemoCard color="green">2</DemoCard></GridItem>
          <GridItem span={1}><DemoCard color="purple">3</DemoCard></GridItem>
        </Grid>
      </div>
      
      <div>
        <h3>Medium Gap</h3>
        <Grid columns={3} gap="md">
          <GridItem span={1}><DemoCard color="blue">1</DemoCard></GridItem>
          <GridItem span={1}><DemoCard color="green">2</DemoCard></GridItem>
          <GridItem span={1}><DemoCard color="purple">3</DemoCard></GridItem>
        </Grid>
      </div>
      
      <div>
        <h3>Large Gap</h3>
        <Grid columns={3} gap="lg">
          <GridItem span={1}><DemoCard color="blue">1</DemoCard></GridItem>
          <GridItem span={1}><DemoCard color="green">2</DemoCard></GridItem>
          <GridItem span={1}><DemoCard color="purple">3</DemoCard></GridItem>
        </Grid>
      </div>
    </div>
  ),
};

export const MixedSpans: Story = {
  args: {
    columns: 12,
    gap: 'md',
  },
  render: (args) => (
    <Grid {...args}>
      <GridItem span={8}>
        <DemoCard color="blue">Main Content (8/12)</DemoCard>
      </GridItem>
      <GridItem span={4}>
        <DemoCard color="green">Sidebar (4/12)</DemoCard>
      </GridItem>
      <GridItem span={3}>
        <DemoCard color="purple">Quarter (3/12)</DemoCard>
      </GridItem>
      <GridItem span={9}>
        <DemoCard color="orange">Three Quarters (9/12)</DemoCard>
      </GridItem>
    </Grid>
  ),
};
