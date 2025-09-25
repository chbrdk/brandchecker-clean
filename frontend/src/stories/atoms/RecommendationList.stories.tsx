import type { Meta, StoryObj } from '@storybook/react';
import { RecommendationList } from '../../components/atoms/RecommendationList';
import type { RecommendationItem } from '../../components/atoms/RecommendationList';

const meta: Meta<typeof RecommendationList> = {
  title: 'Atoms/RecommendationList',
  component: RecommendationList,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Recommendation list component for displaying actionable recommendations with priority, status, and metadata.'
      }
    }
  },
  argTypes: {
    title: {
      control: 'text',
      description: 'List title'
    },
    description: {
      control: 'text',
      description: 'List description'
    },
    recommendations: {
      control: 'object',
      description: 'Recommendations data'
    },
    showPriority: {
      control: 'boolean',
      description: 'Show priority indicators'
    },
    showStatus: {
      control: 'boolean',
      description: 'Show status indicators'
    },
    showCategory: {
      control: 'boolean',
      description: 'Show category'
    },
    showTags: {
      control: 'boolean',
      description: 'Show tags'
    },
    showEstimatedTime: {
      control: 'boolean',
      description: 'Show estimated time'
    },
    showImpact: {
      control: 'boolean',
      description: 'Show impact level'
    },
    showTimestamps: {
      control: 'boolean',
      description: 'Show timestamps'
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
      description: 'List size'
    },
    maxItems: {
      control: { type: 'number', min: 1, max: 10 },
      description: 'Maximum items to show'
    },
    showMoreButton: {
      control: 'boolean',
      description: 'Show more button'
    },
    onRecommendationClick: {
      action: 'recommendation clicked',
      description: 'Recommendation click handler'
    },
    onStatusChange: {
      action: 'status changed',
      description: 'Status change handler'
    },
    onDismiss: {
      action: 'dismissed',
      description: 'Dismiss handler'
    }
  },
  tags: ['autodocs']
};

export default meta;
type Story = StoryObj<typeof RecommendationList>;

const brandRecommendations: RecommendationItem[] = [
  {
    id: '1',
    title: 'Update Logo Usage Guidelines',
    description: 'The current logo usage in marketing materials doesn\'t follow the brand guidelines. Update the logo placement and sizing rules.',
    priority: 'high',
    status: 'pending',
    category: 'Brand Identity',
    tags: ['logo', 'guidelines', 'marketing'],
    iconName: 'target',
    estimatedTime: '2-3 hours',
    impact: 'high',
    createdAt: new Date('2024-01-15')
  },
  {
    id: '2',
    title: 'Fix Color Inconsistencies',
    description: 'Several documents use outdated color values. Update all materials to use the current brand color palette.',
    priority: 'critical',
    status: 'in-progress',
    category: 'Visual Identity',
    tags: ['colors', 'palette', 'consistency'],
    iconName: 'alert-circle',
    estimatedTime: '4-6 hours',
    impact: 'high',
    createdAt: new Date('2024-01-14')
  },
  {
    id: '3',
    title: 'Improve Typography Spacing',
    description: 'Text spacing in presentations needs adjustment to match brand standards. Review and update spacing rules.',
    priority: 'medium',
    status: 'pending',
    category: 'Typography',
    tags: ['typography', 'spacing', 'presentations'],
    iconName: 'info',
    estimatedTime: '1-2 hours',
    impact: 'medium',
    createdAt: new Date('2024-01-16')
  },
  {
    id: '4',
    title: 'Update Social Media Templates',
    description: 'Social media templates need to be refreshed with current brand elements and messaging.',
    priority: 'low',
    status: 'completed',
    category: 'Digital Assets',
    tags: ['social media', 'templates', 'digital'],
    iconName: 'check',
    estimatedTime: '3-4 hours',
    impact: 'medium',
    createdAt: new Date('2024-01-10'),
    completedAt: new Date('2024-01-12')
  },
  {
    id: '5',
    title: 'Review Brand Voice Guidelines',
    description: 'Brand voice documentation needs updating to reflect current company values and tone.',
    priority: 'medium',
    status: 'pending',
    category: 'Brand Voice',
    tags: ['voice', 'tone', 'messaging'],
    iconName: 'info',
    estimatedTime: '2-3 hours',
    impact: 'medium',
    createdAt: new Date('2024-01-17')
  }
];

export const Default: Story = {
  args: {
    title: 'Brand Improvement Recommendations',
    description: 'Actionable recommendations to improve brand consistency',
    recommendations: brandRecommendations,
    showPriority: true,
    showStatus: true,
    showTags: true,
    size: 'md'
  }
};

export const WithAllFeatures: Story = {
  args: {
    title: 'Complete Recommendation List',
    description: 'All features enabled for comprehensive recommendation display',
    recommendations: brandRecommendations,
    showPriority: true,
    showStatus: true,
    showCategory: true,
    showTags: true,
    showEstimatedTime: true,
    showImpact: true,
    showTimestamps: true,
    size: 'md'
  }
};

export const CompactView: Story = {
  args: {
    title: 'Quick Actions',
    description: 'Compact view for quick reference',
    recommendations: brandRecommendations.slice(0, 3),
    showPriority: true,
    showStatus: true,
    showTags: false,
    showEstimatedTime: false,
    showImpact: false,
    size: 'sm'
  }
};

export const InteractiveList: Story = {
  args: {
    title: 'Interactive Recommendations',
    description: 'Click on recommendations to view details',
    recommendations: brandRecommendations,
    showPriority: true,
    showStatus: true,
    showTags: true,
    showEstimatedTime: true,
    showImpact: true,
    size: 'md',
    onRecommendationClick: (recommendation) => {
      console.log('Clicked recommendation:', recommendation.title);
    },
    onStatusChange: (id, status) => {
      console.log('Status changed:', id, status);
    },
    onDismiss: (id) => {
      console.log('Dismissed:', id);
    }
  }
};

export const LimitedItems: Story = {
  args: {
    title: 'Top Priority Items',
    description: 'Showing only the most critical recommendations',
    recommendations: brandRecommendations,
    showPriority: true,
    showStatus: true,
    showTags: true,
    maxItems: 3,
    showMoreButton: true,
    size: 'md'
  }
};

export const Sizes: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', width: '100%', maxWidth: '600px' }}>
      <RecommendationList 
        title="Small List" 
        recommendations={brandRecommendations.slice(0, 2)} 
        size="sm" 
        showPriority 
        showStatus 
      />
      <RecommendationList 
        title="Medium List" 
        recommendations={brandRecommendations.slice(0, 2)} 
        size="md" 
        showPriority 
        showStatus 
      />
      <RecommendationList 
        title="Large List" 
        recommendations={brandRecommendations.slice(0, 2)} 
        size="lg" 
        showPriority 
        showStatus 
      />
    </div>
  )
};

export const PriorityLevels: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', width: '100%', maxWidth: '600px' }}>
      <RecommendationList 
        title="Critical Priority" 
        recommendations={brandRecommendations.filter(r => r.priority === 'critical')} 
        showPriority 
        showStatus 
        size="md"
      />
      <RecommendationList 
        title="High Priority" 
        recommendations={brandRecommendations.filter(r => r.priority === 'high')} 
        showPriority 
        showStatus 
        size="md"
      />
      <RecommendationList 
        title="Medium Priority" 
        recommendations={brandRecommendations.filter(r => r.priority === 'medium')} 
        showPriority 
        showStatus 
        size="md"
      />
      <RecommendationList 
        title="Low Priority" 
        recommendations={brandRecommendations.filter(r => r.priority === 'low')} 
        showPriority 
        showStatus 
        size="md"
      />
    </div>
  )
};

export const StatusTypes: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', width: '100%', maxWidth: '600px' }}>
      <RecommendationList 
        title="Pending Items" 
        recommendations={brandRecommendations.filter(r => r.status === 'pending')} 
        showPriority 
        showStatus 
        size="md"
      />
      <RecommendationList 
        title="In Progress" 
        recommendations={brandRecommendations.filter(r => r.status === 'in-progress')} 
        showPriority 
        showStatus 
        size="md"
      />
      <RecommendationList 
        title="Completed" 
        recommendations={brandRecommendations.filter(r => r.status === 'completed')} 
        showPriority 
        showStatus 
        showTimestamps
        size="md"
      />
    </div>
  )
};

export const EmptyState: Story = {
  args: {
    title: 'No Recommendations',
    description: 'All recommendations have been addressed',
    recommendations: [],
    showPriority: true,
    showStatus: true,
    size: 'md'
  }
};
