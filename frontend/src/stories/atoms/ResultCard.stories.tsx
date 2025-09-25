import type { Meta, StoryObj } from '@storybook/react';
import { ResultCard } from '../../components/atoms/ResultCard';
import type { AnalysisResult, ChartDataPoint, RecommendationItem } from '../../components/atoms/ResultCard';

const meta: Meta<typeof ResultCard> = {
  title: 'Atoms/ResultCard',
  component: ResultCard,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Result card component for displaying BrandChecker analysis results in various formats.'
      }
    }
  },
  argTypes: {
    type: {
      control: 'select',
      options: ['score', 'analysis', 'comparison', 'trend', 'recommendations', 'summary'],
      description: 'Result card type'
    },
    variant: {
      control: 'select',
      options: ['default', 'compact', 'detailed', 'interactive'],
      description: 'Card variant'
    },
    title: {
      control: 'text',
      description: 'Card title'
    },
    description: {
      control: 'text',
      description: 'Card description'
    },
    score: {
      control: { type: 'range', min: 0, max: 100, step: 1 },
      description: 'Main score value'
    },
    status: {
      control: 'select',
      options: ['success', 'warning', 'error'],
      description: 'Overall status'
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
      description: 'Card size'
    },
    showScore: {
      control: 'boolean',
      description: 'Show score'
    },
    showStatus: {
      control: 'boolean',
      description: 'Show status'
    },
    showChart: {
      control: 'boolean',
      description: 'Show chart'
    },
    showRecommendations: {
      control: 'boolean',
      description: 'Show recommendations'
    },
    showDetails: {
      control: 'boolean',
      description: 'Show details'
    },
    onClick: {
      action: 'clicked',
      description: 'Click handler'
    },
    onExpand: {
      action: 'expanded',
      description: 'Expand handler'
    }
  },
  tags: ['autodocs']
};

export default meta;
type Story = StoryObj<typeof ResultCard>;

const sampleAnalysisResults: AnalysisResult[] = [
  {
    category: 'Logo Usage',
    score: 85,
    status: 'success',
    details: 'Logo placement and sizing follow brand guidelines correctly.'
  },
  {
    category: 'Color Compliance',
    score: 92,
    status: 'success',
    details: 'All colors match the approved brand palette.'
  },
  {
    category: 'Typography',
    score: 78,
    status: 'warning',
    details: 'Some text uses non-brand fonts. Consider updating to brand fonts.'
  },
  {
    category: 'Spacing',
    score: 88,
    status: 'success',
    details: 'Layout spacing follows brand guidelines consistently.'
  }
];

const sampleChartData: ChartDataPoint[] = [
  { label: 'Logo', value: 85 },
  { label: 'Colors', value: 92 },
  { label: 'Typography', value: 78 },
  { label: 'Spacing', value: 88 },
  { label: 'Imagery', value: 75 }
];

const sampleRecommendations: RecommendationItem[] = [
  {
    id: '1',
    title: 'Update Typography Guidelines',
    description: 'Review and update typography usage across all materials.',
    priority: 'medium',
    status: 'pending',
    category: 'Typography',
    tags: ['typography', 'guidelines'],
    estimatedTime: '2-3 hours',
    impact: 'medium',
    createdAt: new Date('2024-01-15')
  },
  {
    id: '2',
    title: 'Improve Image Quality',
    description: 'Update low-resolution images with high-quality alternatives.',
    priority: 'low',
    status: 'pending',
    category: 'Visual Assets',
    tags: ['images', 'quality'],
    estimatedTime: '1-2 hours',
    impact: 'low',
    createdAt: new Date('2024-01-16')
  }
];

export const ScoreCard: Story = {
  args: {
    type: 'score',
    title: 'Brand Consistency Score',
    description: 'Overall brand adherence across all materials',
    score: 85,
    status: 'success',
    iconName: 'star',
    showScore: true,
    showStatus: true,
    size: 'md'
  }
};

export const AnalysisCard: Story = {
  args: {
    type: 'analysis',
    title: 'Brand Analysis Results',
    description: 'Detailed analysis of brand elements',
    score: 85,
    status: 'success',
    analysisResults: sampleAnalysisResults,
    iconName: 'target',
    showScore: true,
    showStatus: true,
    size: 'md'
  }
};

export const ComparisonCard: Story = {
  args: {
    type: 'comparison',
    title: 'Brand Element Comparison',
    description: 'Comparison of different brand elements',
    chartData: sampleChartData,
    iconName: 'bar-chart',
    showChart: true,
    size: 'md'
  }
};

export const TrendCard: Story = {
  args: {
    type: 'trend',
    title: 'Brand Consistency Trend',
    description: 'Brand consistency improvement over time',
    chartData: [
      { label: 'Q1', value: 65 },
      { label: 'Q2', value: 72 },
      { label: 'Q3', value: 78 },
      { label: 'Q4', value: 85 }
    ],
    iconName: 'trending-up',
    showChart: true,
    size: 'md'
  }
};

export const RecommendationsCard: Story = {
  args: {
    type: 'recommendations',
    title: 'Improvement Recommendations',
    description: 'Actionable recommendations for brand improvement',
    recommendations: sampleRecommendations,
    iconName: 'list',
    showRecommendations: true,
    size: 'md'
  }
};

export const SummaryCard: Story = {
  args: {
    type: 'summary',
    title: 'Brand Analysis Summary',
    description: 'Complete brand analysis overview',
    score: 85,
    status: 'success',
    analysisResults: sampleAnalysisResults.slice(0, 2),
    chartData: sampleChartData,
    recommendations: sampleRecommendations.slice(0, 2),
    iconName: 'file-text',
    showScore: true,
    showStatus: true,
    showChart: true,
    showRecommendations: true,
    showDetails: true,
    category: 'Brand Analysis',
    tags: ['brand', 'consistency', 'analysis'],
    timestamp: new Date(),
    size: 'lg'
  }
};

export const FullWidthSummaryCard: Story = {
  args: {
    type: 'summary',
    variant: 'full-width',
    title: 'Comprehensive Brand Analysis Dashboard',
    description: 'Complete overview of your brand consistency analysis with detailed insights',
    score: 85,
    status: 'success',
    analysisResults: sampleAnalysisResults,
    chartData: sampleChartData,
    recommendations: sampleRecommendations,
    iconName: 'target',
    showScore: true,
    showStatus: true,
    showChart: true,
    showRecommendations: true,
    showDetails: true,
    category: 'Brand Analysis',
    tags: ['brand', 'consistency', 'analysis', 'dashboard'],
    timestamp: new Date(),
    size: 'lg'
  }
};

export const CompactCard: Story = {
  args: {
    type: 'score',
    variant: 'compact',
    title: 'Quick Score',
    score: 85,
    status: 'success',
    showScore: true,
    showStatus: true,
    size: 'sm'
  }
};

export const DetailedCard: Story = {
  args: {
    type: 'analysis',
    variant: 'detailed',
    title: 'Detailed Analysis',
    description: 'Comprehensive brand analysis with all details',
    score: 85,
    status: 'success',
    analysisResults: sampleAnalysisResults,
    chartData: sampleChartData,
    recommendations: sampleRecommendations,
    iconName: 'target',
    showScore: true,
    showStatus: true,
    showChart: true,
    showRecommendations: true,
    showDetails: true,
    category: 'Brand Analysis',
    tags: ['brand', 'consistency', 'analysis', 'detailed'],
    timestamp: new Date(),
    size: 'lg'
  }
};

export const InteractiveCard: Story = {
  args: {
    type: 'analysis',
    variant: 'interactive',
    title: 'Interactive Analysis',
    description: 'Click to view detailed results',
    score: 85,
    status: 'success',
    analysisResults: sampleAnalysisResults,
    iconName: 'target',
    showScore: true,
    showStatus: true,
    showDetails: true,
    category: 'Brand Analysis',
    tags: ['interactive', 'analysis'],
    onClick: () => console.log('Card clicked!'),
    onExpand: () => console.log('Card expanded!'),
    size: 'md'
  }
};

export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', width: '100%', maxWidth: '500px' }}>
      <ResultCard 
        type="score" 
        title="Small Card" 
        score={85} 
        status="success" 
        size="sm" 
        showScore 
        showStatus 
      />
      <ResultCard 
        type="score" 
        title="Medium Card" 
        score={85} 
        status="success" 
        size="md" 
        showScore 
        showStatus 
      />
      <ResultCard 
        type="score" 
        title="Large Card" 
        score={85} 
        status="success" 
        size="lg" 
        showScore 
        showStatus 
      />
    </div>
  )
};

export const Types: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', width: '800px' }}>
      <ResultCard 
        type="score" 
        title="Score" 
        score={85} 
        status="success" 
        showScore 
        showStatus 
        size="sm"
      />
      <ResultCard 
        type="analysis" 
        title="Analysis" 
        analysisResults={sampleAnalysisResults.slice(0, 2)} 
        size="sm"
      />
      <ResultCard 
        type="comparison" 
        title="Comparison" 
        chartData={sampleChartData.slice(0, 3)} 
        showChart 
        size="sm"
      />
      <ResultCard 
        type="recommendations" 
        title="Recommendations" 
        recommendations={sampleRecommendations.slice(0, 2)} 
        showRecommendations 
        size="sm"
      />
    </div>
  )
};

export const StatusVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', width: '100%', maxWidth: '500px' }}>
      <ResultCard 
        type="score" 
        title="Success Status" 
        score={95} 
        status="success" 
        showScore 
        showStatus 
        size="md"
      />
      <ResultCard 
        type="score" 
        title="Warning Status" 
        score={65} 
        status="warning" 
        showScore 
        showStatus 
        size="md"
      />
      <ResultCard 
        type="score" 
        title="Error Status" 
        score={35} 
        status="error" 
        showScore 
        showStatus 
        size="md"
      />
    </div>
  )
};

export const BrandCheckerDashboard: Story = {
  render: () => (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', width: '900px' }}>
      <ResultCard 
        type="score" 
        title="Overall Brand Score" 
        score={85} 
        status="success" 
        iconName="star"
        showScore 
        showStatus 
        size="md"
      />
      <ResultCard 
        type="analysis" 
        title="Element Analysis" 
        analysisResults={sampleAnalysisResults.slice(0, 3)} 
        iconName="target"
        size="md"
      />
      <ResultCard 
        type="comparison" 
        title="Element Comparison" 
        chartData={sampleChartData} 
        iconName="bar-chart"
        showChart 
        size="md"
      />
      <ResultCard 
        type="recommendations" 
        title="Action Items" 
        recommendations={sampleRecommendations} 
        iconName="list"
        showRecommendations 
        size="md"
      />
    </div>
  )
};
