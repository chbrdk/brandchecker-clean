import type { Meta, StoryObj } from '@storybook/react';
import { Table } from '../../components/organisms';
import type { TableColumn } from '../../components/organisms';
import { Button } from '../../components/atoms/Button';
import { Chip } from '../../components/atoms/Chip';
import { useState } from 'react';

const meta: Meta<typeof Table> = {
  title: 'Organisms/Table',
  component: Table,
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component: 'Responsive table component with mobile-first design, sorting, selection, and pagination features.',
      },
    },
  },
  argTypes: {
    size: {
      control: 'select',
      options: ['xs', 'sm', 'md', 'lg', 'xl'],
      description: 'Table size',
    },
    variant: {
      control: 'select',
      options: ['default', 'striped', 'bordered', 'compact'],
      description: 'Table variant style',
    },
    sortable: {
      control: 'boolean',
      description: 'Enable sorting functionality',
    },
    stickyHeader: {
      control: 'boolean',
      description: 'Enable sticky header',
    },
    loading: {
      control: 'boolean',
      description: 'Show loading state',
    },
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

// Sample data for BrandChecker
interface BrandAnalysisData {
  key: string;
  id: string;
  brandName: string;
  documentType: string;
  colorCompliance: number;
  fontCompliance: number;
  logoCompliance: number;
  overallScore: number;
  status: 'completed' | 'processing' | 'failed';
  createdAt: string;
  fileSize: string;
}

const brandAnalysisData: BrandAnalysisData[] = [
  {
    key: '1',
    id: 'BA-2024-001',
    brandName: 'Nike',
    documentType: 'Brand Guidelines PDF',
    colorCompliance: 95,
    fontCompliance: 88,
    logoCompliance: 92,
    overallScore: 91.7,
    status: 'completed',
    createdAt: '2024-01-15',
    fileSize: '2.4 MB',
  },
  {
    key: '2',
    id: 'BA-2024-002',
    brandName: 'Coca Cola',
    documentType: 'Marketing Presentation',
    colorCompliance: 87,
    fontCompliance: 95,
    logoCompliance: 89,
    overallScore: 90.3,
    status: 'completed',
    createdAt: '2024-01-14',
    fileSize: '1.8 MB',
  },
  {
    key: '3',
    id: 'BA-2024-003',
    brandName: 'Apple',
    documentType: 'Product Brochure',
    colorCompliance: 98,
    fontCompliance: 97,
    logoCompliance: 96,
    overallScore: 97.0,
    status: 'completed',
    createdAt: '2024-01-13',
    fileSize: '3.2 MB',
  },
  {
    key: '4',
    id: 'BA-2024-004',
    brandName: 'Microsoft',
    documentType: 'Annual Report',
    colorCompliance: 82,
    fontCompliance: 79,
    logoCompliance: 85,
    overallScore: 82.0,
    status: 'processing',
    createdAt: '2024-01-12',
    fileSize: '5.1 MB',
  },
  {
    key: '5',
    id: 'BA-2024-005',
    brandName: 'Google',
    documentType: 'Brand Guidelines PDF',
    colorCompliance: 0,
    fontCompliance: 0,
    logoCompliance: 0,
    overallScore: 0,
    status: 'failed',
    createdAt: '2024-01-11',
    fileSize: '1.2 MB',
  },
];

const getStatusChip = (status: string) => {
  const statusConfig = {
    completed: { variant: 'success' as const, text: 'Completed' },
    processing: { variant: 'warning' as const, text: 'Processing' },
    failed: { variant: 'error' as const, text: 'Failed' },
  };
  
  const config = statusConfig[status as keyof typeof statusConfig];
  
  return (
    <Chip variant={config.variant} size="small">
      {config.text}
    </Chip>
  );
};

const getComplianceScore = (score: number) => {
  const color = score >= 90 ? '#10b981' : score >= 70 ? '#f59e0b' : '#ef4444';
  return (
    <span style={{ color, fontWeight: '600' }}>
      {score > 0 ? `${score}%` : '-'}
    </span>
  );
};

const brandAnalysisColumns: TableColumn<BrandAnalysisData>[] = [
  {
    key: 'id',
    title: 'Analysis ID',
    dataIndex: 'id',
    width: 120,
    sortable: true,
  },
  {
    key: 'brandName',
    title: 'Brand Name',
    dataIndex: 'brandName',
    sortable: true,
    render: (value, record) => (
      <div style={{ fontWeight: '600', color: '#1f2937' }}>
        {value}
      </div>
    ),
  },
  {
    key: 'documentType',
    title: 'Document Type',
    dataIndex: 'documentType',
    hideOnMobile: true,
  },
  {
    key: 'colorCompliance',
    title: 'Color',
    dataIndex: 'colorCompliance',
    align: 'center',
    sortable: true,
    render: (value) => getComplianceScore(value),
  },
  {
    key: 'fontCompliance',
    title: 'Font',
    dataIndex: 'fontCompliance',
    align: 'center',
    sortable: true,
    hideOnMobile: true,
    render: (value) => getComplianceScore(value),
  },
  {
    key: 'logoCompliance',
    title: 'Logo',
    dataIndex: 'logoCompliance',
    align: 'center',
    sortable: true,
    hideOnMobile: true,
    render: (value) => getComplianceScore(value),
  },
  {
    key: 'overallScore',
    title: 'Overall Score',
    dataIndex: 'overallScore',
    align: 'center',
    sortable: true,
    render: (value) => (
      <div style={{ 
        fontWeight: '700', 
        fontSize: '16px',
        color: value >= 90 ? '#10b981' : value >= 70 ? '#f59e0b' : '#ef4444'
      }}>
        {value > 0 ? `${value}%` : '-'}
      </div>
    ),
  },
  {
    key: 'status',
    title: 'Status',
    dataIndex: 'status',
    align: 'center',
    render: (value) => getStatusChip(value),
  },
  {
    key: 'actions',
    title: 'Actions',
    align: 'center',
    render: (_, record) => (
      <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
        <Button size="small" variant="ghost">View</Button>
        {record.status === 'completed' && (
          <Button size="small" variant="ghost">Download</Button>
        )}
      </div>
    ),
  },
];

// Basic Table
export const Default: Story = {
  render: () => (
    <Table
      data={brandAnalysisData}
      columns={brandAnalysisColumns}
      caption="Brand Analysis Results"
    />
  ),
};

// BrandChecker Analysis Table
export const BrandCheckerAnalysis: Story = {
  render: () => (
    <div style={{ backgroundColor: '#f9fafb', padding: '24px', borderRadius: '8px' }}>
      <h2 style={{ marginBottom: '16px', color: '#1f2937' }}>Brand Compliance Analysis</h2>
      <Table
        data={brandAnalysisData}
        columns={brandAnalysisColumns}
        size="md"
        variant="striped"
        sortable
        stickyHeader
        maxHeight="400px"
        onRowClick={(record) => console.log('Clicked:', record)}
      />
    </div>
  ),
};

// With Row Selection
export const WithRowSelection: Story = {
  render: () => {
    const [selectedRows, setSelectedRows] = useState<string[]>([]);
    
    return (
      <div>
        <div style={{ marginBottom: '16px', padding: '12px', backgroundColor: '#f3f4f6', borderRadius: '6px' }}>
          <strong>Selected: {selectedRows.length} items</strong>
          {selectedRows.length > 0 && (
            <div style={{ marginTop: '8px', display: 'flex', gap: '8px' }}>
              <Button size="small" variant="primary">Bulk Export</Button>
              <Button size="small" variant="secondary">Bulk Delete</Button>
            </div>
          )}
        </div>
        
        <Table
          data={brandAnalysisData}
          columns={brandAnalysisColumns}
          rowSelection={{
            type: 'checkbox',
            selectedRowKeys: selectedRows,
            onSelect: (record, selected, selectedRows) => {
              console.log('Selected:', record, selected, selectedRows);
            },
            onSelectAll: (selected, selectedRows) => {
              setSelectedRows(selected ? selectedRows.map(r => r.key) : []);
            },
          }}
          sortable
        />
      </div>
    );
  },
};

// With Pagination
export const WithPagination: Story = {
  render: () => {
    const [currentPage, setCurrentPage] = useState(1);
    const pageSize = 3;
    const startIndex = (currentPage - 1) * pageSize;
    const paginatedData = brandAnalysisData.slice(startIndex, startIndex + pageSize);
    
    return (
      <Table
        data={paginatedData}
        columns={brandAnalysisColumns}
        pagination={{
          current: currentPage,
          pageSize: pageSize,
          total: brandAnalysisData.length,
          onChange: (page) => setCurrentPage(page),
        }}
        sortable
      />
    );
  },
};

// Sortable Table
export const Sortable: Story = {
  render: () => {
    const [sortConfig, setSortConfig] = useState<{
      key: string;
      direction: 'asc' | 'desc';
    } | null>(null);
    
    return (
      <Table
        data={brandAnalysisData}
        columns={brandAnalysisColumns}
        sortable
        sortConfig={sortConfig || undefined}
        onSortChange={(key, direction) => {
          setSortConfig({ key, direction });
          console.log('Sort changed:', key, direction);
        }}
      />
    );
  },
};

// Different Variants
export const DifferentVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      <div>
        <h3 style={{ marginBottom: '12px' }}>Default</h3>
        <Table
          data={brandAnalysisData.slice(0, 3)}
          columns={brandAnalysisColumns.slice(0, 5)}
          variant="default"
        />
      </div>
      
      <div>
        <h3 style={{ marginBottom: '12px' }}>Striped</h3>
        <Table
          data={brandAnalysisData.slice(0, 3)}
          columns={brandAnalysisColumns.slice(0, 5)}
          variant="striped"
        />
      </div>
      
      <div>
        <h3 style={{ marginBottom: '12px' }}>Bordered</h3>
        <Table
          data={brandAnalysisData.slice(0, 3)}
          columns={brandAnalysisColumns.slice(0, 5)}
          variant="bordered"
        />
      </div>
      
      <div>
        <h3 style={{ marginBottom: '12px' }}>Compact</h3>
        <Table
          data={brandAnalysisData.slice(0, 3)}
          columns={brandAnalysisColumns.slice(0, 5)}
          variant="compact"
        />
      </div>
    </div>
  ),
};

// Different Sizes
export const DifferentSizes: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      <div>
        <h3 style={{ marginBottom: '12px' }}>Extra Small (XS)</h3>
        <Table
          data={brandAnalysisData.slice(0, 2)}
          columns={brandAnalysisColumns.slice(0, 4)}
          size="xs"
        />
      </div>
      
      <div>
        <h3 style={{ marginBottom: '12px' }}>Small (SM)</h3>
        <Table
          data={brandAnalysisData.slice(0, 2)}
          columns={brandAnalysisColumns.slice(0, 4)}
          size="sm"
        />
      </div>
      
      <div>
        <h3 style={{ marginBottom: '12px' }}>Medium (MD) - Default</h3>
        <Table
          data={brandAnalysisData.slice(0, 2)}
          columns={brandAnalysisColumns.slice(0, 4)}
          size="md"
        />
      </div>
      
      <div>
        <h3 style={{ marginBottom: '12px' }}>Large (LG)</h3>
        <Table
          data={brandAnalysisData.slice(0, 2)}
          columns={brandAnalysisColumns.slice(0, 4)}
          size="lg"
        />
      </div>
      
      <div>
        <h3 style={{ marginBottom: '12px' }}>Extra Large (XL)</h3>
        <Table
          data={brandAnalysisData.slice(0, 2)}
          columns={brandAnalysisColumns.slice(0, 4)}
          size="xl"
        />
      </div>
    </div>
  ),
};

// Loading State
export const Loading: Story = {
  render: () => (
    <Table
      data={[]}
      columns={brandAnalysisColumns}
      loading={true}
    />
  ),
};

// Empty State
export const Empty: Story = {
  render: () => (
    <Table
      data={[]}
      columns={brandAnalysisColumns}
      empty={
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <div style={{ fontSize: '48px', marginBottom: '16px' }}>🔍</div>
          <h3 style={{ margin: '0 0 8px 0', color: '#1f2937' }}>No Analysis Found</h3>
          <p style={{ margin: '0 0 16px 0', color: '#6b7280' }}>
            Start by uploading your brand documents to see analysis results here.
          </p>
          <Button variant="primary">Upload Documents</Button>
        </div>
      }
    />
  ),
};

// Mobile Responsive
export const MobileResponsive: Story = {
  render: () => (
    <Table
      data={brandAnalysisData}
      columns={brandAnalysisColumns}
      size="sm"
      variant="striped"
    />
  ),
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
};

// Sticky Header with Scroll
export const StickyHeaderWithScroll: Story = {
  render: () => (
    <div style={{ height: '300px' }}>
      <Table
        data={[...brandAnalysisData, ...brandAnalysisData, ...brandAnalysisData]}
        columns={brandAnalysisColumns}
        stickyHeader
        maxHeight="300px"
        caption="Scrollable Table with Sticky Header"
      />
    </div>
  ),
};

// Complex BrandChecker Dashboard Table
export const ComplexDashboardTable: Story = {
  render: () => {
    const [selectedRows, setSelectedRows] = useState<string[]>([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [sortConfig, setSortConfig] = useState<{
      key: string;
      direction: 'asc' | 'desc';
    }>({ key: 'overallScore', direction: 'desc' });
    
    const pageSize = 10;
    const startIndex = (currentPage - 1) * pageSize;
    const extendedData = [...brandAnalysisData, ...brandAnalysisData, ...brandAnalysisData];
    const paginatedData = extendedData.slice(startIndex, startIndex + pageSize);
    
    return (
      <div style={{ backgroundColor: '#f9fafb', padding: '24px', borderRadius: '12px' }}>
        <div style={{ marginBottom: '24px' }}>
          <h2 style={{ margin: '0 0 8px 0', color: '#1f2937' }}>Brand Compliance Dashboard</h2>
          <p style={{ margin: '0 0 16px 0', color: '#6b7280' }}>
            Monitor and analyze brand compliance across all your documents
          </p>
          
          {selectedRows.length > 0 && (
            <div style={{ 
              padding: '12px 16px', 
              backgroundColor: '#dbeafe', 
              border: '1px solid #93c5fd',
              borderRadius: '8px',
              marginBottom: '16px'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ color: '#1e40af', fontWeight: '500' }}>
                  {selectedRows.length} analysis selected
                </span>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <Button size="small" variant="primary">Export Selected</Button>
                  <Button size="small" variant="secondary">Compare</Button>
                  <Button size="small" variant="danger">Delete</Button>
                </div>
              </div>
            </div>
          )}
        </div>
        
        <Table
          data={paginatedData}
          columns={brandAnalysisColumns}
          size="md"
          variant="striped"
          sortable
          sortConfig={sortConfig}
          onSortChange={(key, direction) => {
            setSortConfig({ key, direction });
          }}
          rowSelection={{
            type: 'checkbox',
            selectedRowKeys: selectedRows,
            onSelect: (record, selected, selectedRows) => {
              const newSelectedRows = selected 
                ? [...selectedRows.map(r => r.key)]
                : selectedRows.filter(r => r.key !== record.key).map(r => r.key);
              setSelectedRows(newSelectedRows);
            },
            onSelectAll: (selected, selectedRows) => {
              setSelectedRows(selected ? selectedRows.map(r => r.key) : []);
            },
          }}
          pagination={{
            current: currentPage,
            pageSize: pageSize,
            total: extendedData.length,
            onChange: (page) => setCurrentPage(page),
          }}
          onRowClick={(record) => {
            console.log('View analysis details:', record);
          }}
          stickyHeader
          maxHeight="500px"
          caption="Brand Analysis Results - Real-time Data"
        />
      </div>
    );
  },
};

// Playground
export const Playground: Story = {
  args: {
    size: 'md',
    variant: 'default',
    sortable: false,
    stickyHeader: false,
    loading: false,
  },
  render: (args) => (
    <Table
      {...args}
      data={brandAnalysisData}
      columns={brandAnalysisColumns}
    />
  ),
};

// Chips in Table
export const WithChips: Story = {
  render: () => {
    const chipData = [
      {
        key: '1',
        name: 'Brand Guidelines',
        category: 'Documentation',
        tags: ['Design', 'Brand', 'Guidelines'],
        status: 'completed',
        compliance: 95,
      },
      {
        key: '2',
        name: 'Marketing Materials',
        category: 'Marketing',
        tags: ['Print', 'Digital', 'Social'],
        status: 'processing',
        compliance: 78,
      },
      {
        key: '3',
        name: 'Product Packaging',
        category: 'Product',
        tags: ['Packaging', 'Label', 'Design'],
        status: 'failed',
        compliance: 45,
      },
    ];

    const chipColumns: TableColumn<typeof chipData[0]>[] = [
      {
        key: 'name',
        title: 'Name',
        dataIndex: 'name',
      },
      {
        key: 'category',
        title: 'Category',
        dataIndex: 'category',
        render: (value) => (
          <Chip variant="secondary" size="small">
            {value}
          </Chip>
        ),
      },
      {
        key: 'tags',
        title: 'Tags',
        dataIndex: 'tags',
        render: (tags: string[]) => (
          <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
            {tags.map(tag => (
              <Chip key={tag} variant="default" size="small">
                {tag}
              </Chip>
            ))}
          </div>
        ),
      },
      {
        key: 'status',
        title: 'Status',
        dataIndex: 'status',
        align: 'center',
        render: (value) => getStatusChip(value),
      },
      {
        key: 'compliance',
        title: 'Compliance',
        dataIndex: 'compliance',
        align: 'center',
        render: (value) => (
          <Chip 
            variant={value >= 90 ? 'success' : value >= 70 ? 'warning' : 'error'}
            size="small"
          >
            {value}%
          </Chip>
        ),
      },
    ];

    return (
      <Table
        data={chipData}
        columns={chipColumns}
        size="md"
        variant="default"
      />
    );
  },
};
