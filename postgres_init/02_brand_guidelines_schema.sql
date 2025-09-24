-- Brand Guidelines Database Schema Extension
-- This script extends the existing schema to handle brand guideline data

-- ============================================================================
-- BRAND GUIDELINES TABLES
-- ============================================================================

-- Table for brands
CREATE TABLE IF NOT EXISTS brands (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    external_id VARCHAR(255) UNIQUE, -- Original brand ID from GraphQL
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE,
    description TEXT,
    primary_color_hex VARCHAR(7),
    primary_color_rgb INTEGER[],
    avatar_url TEXT,
    brand_guide_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for asset libraries
CREATE TABLE IF NOT EXISTS asset_libraries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
    external_id VARCHAR(255), -- Original library ID from GraphQL
    name VARCHAR(255) NOT NULL,
    asset_count INTEGER DEFAULT 0,
    asset_types TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(brand_id, external_id)
);

-- Table for brand assets
CREATE TABLE IF NOT EXISTS brand_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    library_id UUID REFERENCES asset_libraries(id) ON DELETE CASCADE,
    external_id VARCHAR(255), -- Original asset ID from GraphQL
    title VARCHAR(500) NOT NULL,
    asset_type VARCHAR(50) NOT NULL, -- svg, gif, png, etc.
    download_url TEXT,
    preview_url TEXT,
    width INTEGER,
    height INTEGER,
    size_bytes BIGINT,
    file_extension VARCHAR(10),
    modified_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(library_id, external_id)
);

-- Table for guideline pages
CREATE TABLE IF NOT EXISTS guideline_pages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
    page_path VARCHAR(500) NOT NULL, -- e.g., "/document/7158"
    title TEXT NOT NULL,
    url TEXT,
    page_order INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(brand_id, page_path)
);

-- Table for page sections (headings)
CREATE TABLE IF NOT EXISTS page_sections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    page_id UUID REFERENCES guideline_pages(id) ON DELETE CASCADE,
    heading_level VARCHAR(10) NOT NULL, -- h1, h2, h3, etc.
    text TEXT NOT NULL,
    section_order INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(page_id, section_order)
);

-- Table for page content
CREATE TABLE IF NOT EXISTS page_content (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    page_id UUID REFERENCES guideline_pages(id) ON DELETE CASCADE,
    content_type VARCHAR(50) NOT NULL, -- paragraph, list_item, navigation
    content TEXT NOT NULL,
    content_order INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(page_id, content_order)
);

-- ============================================================================
-- BRAND GUIDELINE KNOWLEDGE CHUNKS
-- ============================================================================

-- Extended knowledge chunks table for brand guidelines
CREATE TABLE IF NOT EXISTS brand_knowledge_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
    chunk_type VARCHAR(50) NOT NULL, -- 'asset_description', 'guideline_text', 'brand_rule', 'color_guideline', 'typography_rule'
    source_type VARCHAR(50) NOT NULL, -- 'graphql_asset', 'html_page', 'pdf_analysis'
    source_id VARCHAR(255), -- Reference to original source
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB, -- Additional metadata (asset type, page section, etc.)
    embedding vector(1536), -- OpenAI embedding vector (1536 dimensions for text-embedding-3-small)
    embedding_model VARCHAR(50) DEFAULT 'text-embedding-3-small',
    embedding_created_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for brand compliance checks
CREATE TABLE IF NOT EXISTS brand_compliance_checks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pdf_document_id UUID REFERENCES pdf_documents(id) ON DELETE CASCADE,
    brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
    check_type VARCHAR(50) NOT NULL, -- 'color_compliance', 'font_compliance', 'logo_compliance', 'layout_compliance'
    compliance_score REAL, -- 0.0 to 1.0
    violations JSONB, -- Details about violations found
    recommendations JSONB, -- AI-generated recommendations
    check_data JSONB, -- Raw check results
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- BRAND-SPECIFIC ANALYSIS TABLES
-- ============================================================================

-- Table for brand color standards
CREATE TABLE IF NOT EXISTS brand_colors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
    color_name VARCHAR(100) NOT NULL,
    hex_code VARCHAR(7) NOT NULL,
    rgb_values INTEGER[] NOT NULL,
    cmyk_values REAL[],
    color_usage VARCHAR(100), -- 'primary', 'secondary', 'accent', 'background'
    color_category VARCHAR(50), -- 'corporate', 'functional', 'emotional'
    is_allowed BOOLEAN DEFAULT true,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for brand font standards
CREATE TABLE IF NOT EXISTS brand_fonts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    brand_id UUID REFERENCES brands(id) ON DELETE CASCADE,
    font_name VARCHAR(200) NOT NULL,
    font_family VARCHAR(200),
    font_weight VARCHAR(50), -- 'light', 'regular', 'bold', etc.
    usage_purpose VARCHAR(100), -- 'headings', 'body', 'captions', 'logos'
    is_allowed BOOLEAN DEFAULT true,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Brand tables indexes
CREATE INDEX IF NOT EXISTS idx_brands_external_id ON brands(external_id);
CREATE INDEX IF NOT EXISTS idx_brands_slug ON brands(slug);
CREATE INDEX IF NOT EXISTS idx_brands_name ON brands(name);

CREATE INDEX IF NOT EXISTS idx_asset_libraries_brand_id ON asset_libraries(brand_id);
CREATE INDEX IF NOT EXISTS idx_asset_libraries_external_id ON asset_libraries(external_id);

CREATE INDEX IF NOT EXISTS idx_brand_assets_library_id ON brand_assets(library_id);
CREATE INDEX IF NOT EXISTS idx_brand_assets_external_id ON brand_assets(external_id);
CREATE INDEX IF NOT EXISTS idx_brand_assets_type ON brand_assets(asset_type);
CREATE INDEX IF NOT EXISTS idx_brand_assets_title ON brand_assets(title);

CREATE INDEX IF NOT EXISTS idx_guideline_pages_brand_id ON guideline_pages(brand_id);
CREATE INDEX IF NOT EXISTS idx_guideline_pages_path ON guideline_pages(page_path);

CREATE INDEX IF NOT EXISTS idx_page_sections_page_id ON page_sections(page_id);
CREATE INDEX IF NOT EXISTS idx_page_content_page_id ON page_content(page_id);

-- Brand knowledge chunks indexes
CREATE INDEX IF NOT EXISTS idx_brand_knowledge_chunks_brand_id ON brand_knowledge_chunks(brand_id);
CREATE INDEX IF NOT EXISTS idx_brand_knowledge_chunks_type ON brand_knowledge_chunks(chunk_type);
CREATE INDEX IF NOT EXISTS idx_brand_knowledge_chunks_source_type ON brand_knowledge_chunks(source_type);
CREATE INDEX IF NOT EXISTS idx_brand_knowledge_chunks_embedding ON brand_knowledge_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Compliance check indexes
CREATE INDEX IF NOT EXISTS idx_brand_compliance_checks_pdf_id ON brand_compliance_checks(pdf_document_id);
CREATE INDEX IF NOT EXISTS idx_brand_compliance_checks_brand_id ON brand_compliance_checks(brand_id);
CREATE INDEX IF NOT EXISTS idx_brand_compliance_checks_type ON brand_compliance_checks(check_type);
CREATE INDEX IF NOT EXISTS idx_brand_compliance_checks_score ON brand_compliance_checks(compliance_score);

-- Brand standards indexes
CREATE INDEX IF NOT EXISTS idx_brand_colors_brand_id ON brand_colors(brand_id);
CREATE INDEX IF NOT EXISTS idx_brand_colors_hex ON brand_colors(hex_code);
CREATE INDEX IF NOT EXISTS idx_brand_colors_usage ON brand_colors(color_usage);

CREATE INDEX IF NOT EXISTS idx_brand_fonts_brand_id ON brand_fonts(brand_id);
CREATE INDEX IF NOT EXISTS idx_brand_fonts_name ON brand_fonts(font_name);
CREATE INDEX IF NOT EXISTS idx_brand_fonts_purpose ON brand_fonts(usage_purpose);

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Update triggers for updated_at
CREATE TRIGGER update_brands_updated_at 
    BEFORE UPDATE ON brands 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_asset_libraries_updated_at 
    BEFORE UPDATE ON asset_libraries 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_brand_assets_updated_at 
    BEFORE UPDATE ON brand_assets 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_guideline_pages_updated_at 
    BEFORE UPDATE ON guideline_pages 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_brand_knowledge_chunks_updated_at 
    BEFORE UPDATE ON brand_knowledge_chunks 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_brand_colors_updated_at 
    BEFORE UPDATE ON brand_colors 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_brand_fonts_updated_at 
    BEFORE UPDATE ON brand_fonts 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View for brand overview with asset counts
CREATE OR REPLACE VIEW brand_overview AS
SELECT 
    b.id,
    b.name,
    b.slug,
    b.primary_color_hex,
    COUNT(DISTINCT al.id) as library_count,
    COUNT(DISTINCT ba.id) as asset_count,
    COUNT(DISTINCT gp.id) as guideline_page_count,
    b.created_at
FROM brands b
LEFT JOIN asset_libraries al ON b.id = al.brand_id
LEFT JOIN brand_assets ba ON al.id = ba.library_id
LEFT JOIN guideline_pages gp ON b.id = gp.brand_id
GROUP BY b.id, b.name, b.slug, b.primary_color_hex, b.created_at;

-- View for compliance summary
CREATE OR REPLACE VIEW compliance_summary AS
SELECT 
    pd.filename,
    b.name as brand_name,
    AVG(bcc.compliance_score) as avg_compliance_score,
    COUNT(bcc.id) as check_count,
    MAX(bcc.created_at) as last_check
FROM pdf_documents pd
JOIN brand_compliance_checks bcc ON pd.id = bcc.pdf_document_id
JOIN brands b ON bcc.brand_id = b.id
GROUP BY pd.filename, b.name;

-- ============================================================================
-- INITIAL DATA INSERTION
-- ============================================================================

-- Insert Bosch brand data
INSERT INTO brands (external_id, name, slug, primary_color_hex, primary_color_rgb, brand_guide_url) VALUES
('eyJpZGVudGlmaWVyIjoxMDcsInR5cGUiOiJicmFuZCJ9', 'Bosch Corporate - Test', 'bosch-corporate-test', '#825FFF', ARRAY[130, 95, 255], 'https://brandguide-bosch-test.frontify.com')
ON CONFLICT (external_id) DO UPDATE SET
    name = EXCLUDED.name,
    primary_color_hex = EXCLUDED.primary_color_hex,
    primary_color_rgb = EXCLUDED.primary_color_rgb,
    updated_at = CURRENT_TIMESTAMP;

-- Insert brand categories for knowledge chunks
INSERT INTO knowledge_categories (name, description) VALUES
('Asset Guidelines', 'Information about brand assets, logos, and visual elements'),
('Brand Rules', 'Brand usage rules and compliance guidelines'),
('Design Standards', 'Design principles and standards'),
('Color Guidelines', 'Brand color usage and specifications'),
('Typography Guidelines', 'Font and typography specifications')
ON CONFLICT (name) DO NOTHING;
