-- Brandchecker Database Initialization
-- This script creates the initial database schema for the Brandchecker application

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Create tables for PDF analysis results

-- Table for PDF documents
CREATE TABLE IF NOT EXISTS pdf_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(500) NOT NULL,
    file_size BIGINT,
    page_count INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    analysis_status VARCHAR(50) DEFAULT 'pending',
    analysis_completed_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(filepath)
);

-- Table for color analysis results
CREATE TABLE IF NOT EXISTS color_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pdf_document_id UUID REFERENCES pdf_documents(id) ON DELETE CASCADE,
    analysis_type VARCHAR(50) NOT NULL, -- 'all_colors', 'design_colors', 'intelligent_colors'
    total_colors INTEGER,
    primary_color_space VARCHAR(50),
    color_management_strategy VARCHAR(100),
    analysis_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(pdf_document_id, analysis_type)
);

-- Table for individual colors
CREATE TABLE IF NOT EXISTS colors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    color_analysis_id UUID REFERENCES color_analysis(id) ON DELETE CASCADE,
    name VARCHAR(100),
    hex_code VARCHAR(7),
    rgb_values INTEGER[],
    rgb_precise REAL[],
    cmyk_values REAL[],
    color_space VARCHAR(50),
    usage_count INTEGER DEFAULT 0,
    usage_percentage REAL,
    sources TEXT[],
    corrected_hex VARCHAR(7),
    corrected_rgb INTEGER[],
    correction_distance REAL,
    original_values REAL[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for font analysis results
CREATE TABLE IF NOT EXISTS font_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pdf_document_id UUID REFERENCES pdf_documents(id) ON DELETE CASCADE,
    total_fonts INTEGER,
    total_usage INTEGER,
    analysis_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(pdf_document_id)
);

-- Table for layout analysis results
CREATE TABLE IF NOT EXISTS layout_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pdf_document_id UUID REFERENCES pdf_documents(id) ON DELETE CASCADE,
    total_pages INTEGER,
    page_dimensions JSONB,
    layout_type VARCHAR(50),
    analysis_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(pdf_document_id)
);

-- Table for image analysis results
CREATE TABLE IF NOT EXISTS image_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pdf_document_id UUID REFERENCES pdf_documents(id) ON DELETE CASCADE,
    total_images INTEGER,
    total_image_area REAL,
    image_types JSONB,
    analysis_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(pdf_document_id)
);

-- Table for vector analysis results
CREATE TABLE IF NOT EXISTS vector_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pdf_document_id UUID REFERENCES pdf_documents(id) ON DELETE CASCADE,
    total_vectors INTEGER,
    vector_types JSONB,
    analysis_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(pdf_document_id)
);

-- Table for complete analysis results
CREATE TABLE IF NOT EXISTS complete_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pdf_document_id UUID REFERENCES pdf_documents(id) ON DELETE CASCADE,
    analysis_summary JSONB,
    complete_data JSONB,
    processing_time REAL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(pdf_document_id)
);

-- ============================================================================
-- KNOWLEDGE DATABASE TABLES FOR GPT EMBEDDINGS
-- ============================================================================

-- Table for knowledge chunks (text segments from PDFs)
CREATE TABLE IF NOT EXISTS knowledge_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pdf_document_id UUID REFERENCES pdf_documents(id) ON DELETE CASCADE,
    chunk_type VARCHAR(50) NOT NULL, -- 'text', 'color_analysis', 'font_analysis', 'layout_analysis', 'image_analysis', 'vector_analysis'
    chunk_index INTEGER NOT NULL, -- Order within the document
    content TEXT NOT NULL, -- The actual text content
    metadata JSONB, -- Additional metadata (page number, position, etc.)
    embedding vector(1536), -- OpenAI embedding vector (1536 dimensions)
    embedding_model VARCHAR(50) DEFAULT 'text-embedding-3-small', -- Model used for embedding
    embedding_created_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for knowledge queries and responses
CREATE TABLE IF NOT EXISTS knowledge_queries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    query_text TEXT NOT NULL,
    query_embedding vector(1536), -- Query embedding for similarity search
    response_text TEXT,
    response_sources JSONB, -- Sources used for the response (chunk IDs, etc.)
    response_metadata JSONB, -- Additional response metadata
    processing_time REAL,
    model_used VARCHAR(50) DEFAULT 'gpt-4o',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for knowledge search history
CREATE TABLE IF NOT EXISTS knowledge_search_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    query_id UUID REFERENCES knowledge_queries(id) ON DELETE CASCADE,
    chunk_id UUID REFERENCES knowledge_chunks(id) ON DELETE CASCADE,
    similarity_score REAL, -- Cosine similarity score
    rank_position INTEGER, -- Position in search results
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for knowledge categories and tags
CREATE TABLE IF NOT EXISTS knowledge_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    parent_category_id UUID REFERENCES knowledge_categories(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for chunk categorization
CREATE TABLE IF NOT EXISTS chunk_categories (
    chunk_id UUID REFERENCES knowledge_chunks(id) ON DELETE CASCADE,
    category_id UUID REFERENCES knowledge_categories(id) ON DELETE CASCADE,
    confidence_score REAL DEFAULT 1.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (chunk_id, category_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_pdf_documents_filename ON pdf_documents(filename);
CREATE INDEX IF NOT EXISTS idx_pdf_documents_filepath ON pdf_documents(filepath);
CREATE INDEX IF NOT EXISTS idx_pdf_documents_created_at ON pdf_documents(created_at);
CREATE INDEX IF NOT EXISTS idx_pdf_documents_analysis_status ON pdf_documents(analysis_status);

CREATE INDEX IF NOT EXISTS idx_colors_hex_code ON colors(hex_code);
CREATE INDEX IF NOT EXISTS idx_colors_color_space ON colors(color_space);
CREATE INDEX IF NOT EXISTS idx_colors_usage_count ON colors(usage_count);

CREATE INDEX IF NOT EXISTS idx_color_analysis_type ON color_analysis(analysis_type);
CREATE INDEX IF NOT EXISTS idx_color_analysis_created_at ON color_analysis(created_at);

-- Knowledge database indexes
CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_pdf_id ON knowledge_chunks(pdf_document_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_type ON knowledge_chunks(chunk_type);
CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_embedding ON knowledge_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_created_at ON knowledge_chunks(created_at);

CREATE INDEX IF NOT EXISTS idx_knowledge_queries_created_at ON knowledge_queries(created_at);
CREATE INDEX IF NOT EXISTS idx_knowledge_queries_embedding ON knowledge_queries USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_knowledge_search_history_query_id ON knowledge_search_history(query_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_search_history_chunk_id ON knowledge_search_history(chunk_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_search_history_similarity ON knowledge_search_history(similarity_score);

CREATE INDEX IF NOT EXISTS idx_chunk_categories_chunk_id ON chunk_categories(chunk_id);
CREATE INDEX IF NOT EXISTS idx_chunk_categories_category_id ON chunk_categories(category_id);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_pdf_documents_updated_at 
    BEFORE UPDATE ON pdf_documents 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_knowledge_chunks_updated_at 
    BEFORE UPDATE ON knowledge_chunks 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create a view for recent analyses
CREATE OR REPLACE VIEW recent_analyses AS
SELECT 
    pd.id,
    pd.filename,
    pd.filepath,
    pd.analysis_status,
    pd.created_at,
    pd.analysis_completed_at,
    ca.total_colors,
    fa.total_fonts,
    la.total_pages,
    ia.total_images,
    va.total_vectors
FROM pdf_documents pd
LEFT JOIN color_analysis ca ON pd.id = ca.pdf_document_id AND ca.analysis_type = 'all_colors'
LEFT JOIN font_analysis fa ON pd.id = fa.pdf_document_id
LEFT JOIN layout_analysis la ON pd.id = la.pdf_document_id
LEFT JOIN image_analysis ia ON pd.id = ia.pdf_document_id
LEFT JOIN vector_analysis va ON pd.id = va.pdf_document_id
ORDER BY pd.created_at DESC;

-- Create a view for knowledge search results
CREATE OR REPLACE VIEW knowledge_search_results AS
SELECT 
    kc.id as chunk_id,
    kc.chunk_type,
    kc.content,
    kc.metadata,
    kc.similarity_score,
    kc.rank_position,
    pd.filename,
    pd.filepath,
    kq.query_text,
    kq.created_at as query_created_at
FROM knowledge_chunks kc
JOIN pdf_documents pd ON kc.pdf_document_id = pd.id
JOIN knowledge_search_history ksh ON kc.id = ksh.chunk_id
JOIN knowledge_queries kq ON ksh.query_id = kq.id
ORDER BY ksh.similarity_score DESC;

-- Insert initial knowledge categories
INSERT INTO knowledge_categories (name, description) VALUES
('Color Analysis', 'Information about colors, color spaces, and color management'),
('Font Analysis', 'Information about fonts, typography, and text styling'),
('Layout Analysis', 'Information about page layout, structure, and design'),
('Image Analysis', 'Information about images, graphics, and visual elements'),
('Vector Analysis', 'Information about vector graphics and illustrations'),
('Brand Analysis', 'Information about branding, logos, and brand elements'),
('Technical Analysis', 'Technical details about PDF structure and metadata')
ON CONFLICT (name) DO NOTHING;

-- Grant permissions (if using a different user)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO brandchecker_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO brandchecker_user;
