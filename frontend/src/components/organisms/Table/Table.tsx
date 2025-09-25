import React, { useState, useMemo } from 'react';
import { Icon } from '../../atoms/Icon';
import type { IconName } from '../../atoms/Icon';
import './Table.css';

export interface TableColumn<T = any> {
  /** Unique column key */
  key: string;
  /** Column header title */
  title: string;
  /** Column width */
  width?: string | number;
  /** Column alignment */
  align?: 'left' | 'center' | 'right';
  /** Is column sortable */
  sortable?: boolean;
  /** Is column resizable */
  resizable?: boolean;
  /** Custom render function */
  render?: (value: any, record: T, index: number) => React.ReactNode;
  /** Column data accessor */
  dataIndex?: string;
  /** Fixed column position */
  fixed?: 'left' | 'right';
  /** Column is hidden on mobile */
  hideOnMobile?: boolean;
  /** Custom CSS class */
  className?: string;
}

export interface TableProps<T = any> {
  /** Table data */
  data: T[];
  /** Table columns */
  columns: TableColumn<T>[];
  /** Table size */
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  /** Table variant */
  variant?: 'default' | 'striped' | 'bordered' | 'compact';
  /** Enable row selection */
  rowSelection?: {
    type: 'checkbox' | 'radio';
    selectedRowKeys?: React.Key[];
    onSelect?: (record: T, selected: boolean, selectedRows: T[]) => void;
    onSelectAll?: (selected: boolean, selectedRows: T[], changeRows: T[]) => void;
  };
  /** Enable sorting */
  sortable?: boolean;
  /** Sort configuration */
  sortConfig?: {
    key: string;
    direction: 'asc' | 'desc';
  };
  /** Sort change handler */
  onSortChange?: (key: string, direction: 'asc' | 'desc') => void;
  /** Row click handler */
  onRowClick?: (record: T, index: number) => void;
  /** Row hover handler */
  onRowHover?: (record: T, index: number) => void;
  /** Loading state */
  loading?: boolean;
  /** Empty state */
  empty?: React.ReactNode;
  /** Pagination */
  pagination?: {
    current: number;
    pageSize: number;
    total: number;
    onChange: (page: number, pageSize: number) => void;
  };
  /** Table caption */
  caption?: string;
  /** Sticky header */
  stickyHeader?: boolean;
  /** Max height for scrollable table */
  maxHeight?: string | number;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

export interface TableCellProps {
  /** Cell content */
  children: React.ReactNode;
  /** Cell alignment */
  align?: 'left' | 'center' | 'right';
  /** Column span */
  colSpan?: number;
  /** Row span */
  rowSpan?: number;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

export interface TableRowProps {
  /** Row content */
  children: React.ReactNode;
  /** Row is selected */
  selected?: boolean;
  /** Row is hoverable */
  hoverable?: boolean;
  /** Row click handler */
  onClick?: () => void;
  /** Additional CSS class */
  className?: string;
  /** Additional props */
  [key: string]: any;
}

/** Responsive Table Component */
export const Table = <T extends Record<string, any>>({
  data,
  columns,
  size = 'md',
  variant = 'default',
  rowSelection,
  sortable = false,
  sortConfig,
  onSortChange,
  onRowClick,
  onRowHover,
  loading = false,
  empty,
  pagination,
  caption,
  stickyHeader = false,
  maxHeight,
  className = '',
  ...props
}: TableProps<T>) => {
  const [internalSortConfig, setInternalSortConfig] = useState<{
    key: string;
    direction: 'asc' | 'desc';
  } | null>(sortConfig || null);
  
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>(
    rowSelection?.selectedRowKeys || []
  );

  const currentSortConfig = sortConfig || internalSortConfig;

  // Sort data
  const sortedData = useMemo(() => {
    if (!currentSortConfig || !sortable) return data;

    return [...data].sort((a, b) => {
      const aValue = a[currentSortConfig.key];
      const bValue = b[currentSortConfig.key];
      
      if (aValue === bValue) return 0;
      
      const comparison = aValue < bValue ? -1 : 1;
      return currentSortConfig.direction === 'asc' ? comparison : -comparison;
    });
  }, [data, currentSortConfig, sortable]);

  const handleSort = (key: string) => {
    if (!sortable) return;

    const direction = 
      currentSortConfig?.key === key && currentSortConfig?.direction === 'asc' 
        ? 'desc' 
        : 'asc';

    const newSortConfig = { key, direction };

    if (!sortConfig) {
      setInternalSortConfig(newSortConfig);
    }

    onSortChange?.(key, direction);
  };

  const handleRowSelect = (record: T, index: number, selected: boolean) => {
    const key = record.key || index;
    let newSelectedKeys = [...selectedRowKeys];

    if (rowSelection?.type === 'radio') {
      newSelectedKeys = selected ? [key] : [];
    } else {
      if (selected) {
        newSelectedKeys.push(key);
      } else {
        newSelectedKeys = newSelectedKeys.filter(k => k !== key);
      }
    }

    setSelectedRowKeys(newSelectedKeys);
    
    const selectedRows = sortedData.filter((item, idx) => 
      newSelectedKeys.includes(item.key || idx)
    );

    rowSelection?.onSelect?.(record, selected, selectedRows);
  };

  const handleSelectAll = (selected: boolean) => {
    const allKeys = sortedData.map((item, index) => item.key || index);
    const newSelectedKeys = selected ? allKeys : [];
    
    setSelectedRowKeys(newSelectedKeys);
    
    const selectedRows = selected ? sortedData : [];
    const changeRows = selected ? sortedData : [];

    rowSelection?.onSelectAll?.(selected, selectedRows, changeRows);
  };

  const classes = [
    'table-container',
    `table-container--${size}`,
    `table-container--${variant}`,
    stickyHeader ? 'table-container--sticky-header' : '',
    loading ? 'table-container--loading' : '',
    className
  ].filter(Boolean).join(' ');

  const tableClasses = [
    'table',
    `table--${size}`,
    `table--${variant}`,
  ].filter(Boolean).join(' ');

  const containerStyle: React.CSSProperties = {
    maxHeight: maxHeight || undefined,
    overflow: maxHeight ? 'auto' : undefined,
  };

  const visibleColumns = columns.filter(col => !col.hideOnMobile);

  if (loading) {
    return (
      <div className={classes} style={containerStyle} {...props}>
        <div className="table__loading">
          <div className="table__loading-spinner"></div>
          <span>Loading...</span>
        </div>
      </div>
    );
  }

  if (!data.length) {
    return (
      <div className={classes} {...props}>
        <div className="table__empty">
          {empty || (
            <>
              <div className="table__empty-icon">📄</div>
              <div className="table__empty-text">No data available</div>
            </>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className={classes} style={containerStyle} {...props}>
      {caption && <div className="table__caption">{caption}</div>}
      
      <table className={tableClasses}>
        <thead className="table__header">
          <tr>
            {rowSelection && (
              <th className="table__cell table__cell--selection">
                {rowSelection.type === 'checkbox' && (
                  <input
                    type="checkbox"
                    checked={selectedRowKeys.length === sortedData.length && sortedData.length > 0}
                    onChange={(e) => handleSelectAll(e.target.checked)}
                    className="table__checkbox"
                  />
                )}
              </th>
            )}
            
            {visibleColumns.map((column) => (
              <th
                key={column.key}
                className={[
                  'table__cell',
                  'table__header-cell',
                  column.align ? `table__cell--${column.align}` : '',
                  column.sortable && sortable ? 'table__header-cell--sortable' : '',
                  currentSortConfig?.key === column.key ? 'table__header-cell--sorted' : '',
                  column.className
                ].filter(Boolean).join(' ')}
                style={{ width: column.width }}
                onClick={() => column.sortable && sortable && handleSort(column.key)}
              >
                <div className="table__header-content">
                  <span className="table__header-title">{column.title}</span>
                  {column.sortable && sortable && (
                    <span className="table__sort-indicator">
                      {currentSortConfig?.key === column.key ? (
                        currentSortConfig.direction === 'asc' ? '↑' : '↓'
                      ) : '↕'}
                    </span>
                  )}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        
        <tbody className="table__body">
          {sortedData.map((record, index) => {
            const key = record.key || index;
            const isSelected = selectedRowKeys.includes(key);
            
            return (
              <TableRow
                key={key}
                selected={isSelected}
                hoverable={!!onRowClick || !!onRowHover}
                onClick={() => onRowClick?.(record, index)}
                onMouseEnter={() => onRowHover?.(record, index)}
              >
                {rowSelection && (
                  <TableCell className="table__cell--selection">
                    <input
                      type={rowSelection.type}
                      name={rowSelection.type === 'radio' ? 'table-row-selection' : undefined}
                      checked={isSelected}
                      onChange={(e) => handleRowSelect(record, index, e.target.checked)}
                      className={`table__${rowSelection.type}`}
                    />
                  </TableCell>
                )}
                
                {visibleColumns.map((column) => {
                  const value = column.dataIndex ? record[column.dataIndex] : record[column.key];
                  const cellContent = column.render 
                    ? column.render(value, record, index)
                    : value;

                  return (
                    <TableCell
                      key={column.key}
                      align={column.align}
                      className={column.className}
                    >
                      {cellContent}
                    </TableCell>
                  );
                })}
              </TableRow>
            );
          })}
        </tbody>
      </table>
      
      {pagination && (
        <div className="table__pagination">
          <TablePagination {...pagination} />
        </div>
      )}
    </div>
  );
};

/** Table Row Component */
export const TableRow = ({
  children,
  selected = false,
  hoverable = false,
  onClick,
  className = '',
  ...props
}: TableRowProps) => {
  const classes = [
    'table__row',
    selected ? 'table__row--selected' : '',
    hoverable ? 'table__row--hoverable' : '',
    className
  ].filter(Boolean).join(' ');

  return (
    <tr 
      className={classes} 
      onClick={onClick}
      {...props}
    >
      {children}
    </tr>
  );
};

/** Table Cell Component */
export const TableCell = ({
  children,
  align = 'left',
  colSpan,
  rowSpan,
  className = '',
  ...props
}: TableCellProps) => {
  const classes = [
    'table__cell',
    `table__cell--${align}`,
    className
  ].filter(Boolean).join(' ');

  return (
    <td 
      className={classes}
      colSpan={colSpan}
      rowSpan={rowSpan}
      {...props}
    >
      {children}
    </td>
  );
};

/** Simple Pagination Component */
interface TablePaginationProps {
  current: number;
  pageSize: number;
  total: number;
  onChange: (page: number, pageSize: number) => void;
}

const TablePagination = ({ current, pageSize, total, onChange }: TablePaginationProps) => {
  const totalPages = Math.ceil(total / pageSize);
  const startItem = (current - 1) * pageSize + 1;
  const endItem = Math.min(current * pageSize, total);

  const handlePrevious = () => {
    if (current > 1) {
      onChange(current - 1, pageSize);
    }
  };

  const handleNext = () => {
    if (current < totalPages) {
      onChange(current + 1, pageSize);
    }
  };

  return (
    <div className="table-pagination">
      <div className="table-pagination__info">
        Showing {startItem}-{endItem} of {total} items
      </div>
      
      <div className="table-pagination__controls">
        <button
          className="table-pagination__button"
          onClick={handlePrevious}
          disabled={current <= 1}
        >
          Previous
        </button>
        
        <span className="table-pagination__current">
          Page {current} of {totalPages}
        </span>
        
        <button
          className="table-pagination__button"
          onClick={handleNext}
          disabled={current >= totalPages}
        >
          Next
        </button>
      </div>
    </div>
  );
};
