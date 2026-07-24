-- Database initialization script
-- Run once when PostgreSQL container starts first time

CREATE TABLE IF NOT EXISTS scans (
    id SERIAL PRIMARY KEY,
    target VARCHAR(500) NOT NULL,
    overall_score INTEGER DEFAULT 0,
    scan_type VARCHAR(50) DEFAULT 'website',
    scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS findings (
    id SERIAL PRIMARY KEY,
    scan_id INTEGER REFERENCES scans(id) ON DELETE CASCADE,
    check_id VARCHAR(200),
    name VARCHAR(500),
    status VARCHAR(50),
    severity VARCHAR(50),
    risk_score INTEGER DEFAULT 0,
    priority VARCHAR(50),
    description TEXT,
    evidence TEXT,
    category VARCHAR(200),
    target_type VARCHAR(100),
    target_asset VARCHAR(500),
    scanner_name VARCHAR(200),
    remediation TEXT,
    recommendation TEXT,
    business_impact TEXT,
    mapped_controls TEXT[],
    raw_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS compliance_scores (
    id SERIAL PRIMARY KEY,
    scan_id INTEGER REFERENCES scans(id) ON DELETE CASCADE,
    framework VARCHAR(50),
    score INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    scan_id INTEGER REFERENCES scans(id) ON DELETE CASCADE,
    type VARCHAR(50),
    path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cloud credentials table (encrypted)
CREATE TABLE IF NOT EXISTS cloud_credentials (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    provider VARCHAR(50) NOT NULL,  -- aws, azure, gcp, dockerhub
    encrypted_data TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Upgrade databases created by older releases without replacing data.
ALTER TABLE scans ADD COLUMN IF NOT EXISTS scan_type VARCHAR(50) DEFAULT 'website';
ALTER TABLE scans ADD COLUMN IF NOT EXISTS scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE findings ADD COLUMN IF NOT EXISTS status VARCHAR(50);
ALTER TABLE findings ADD COLUMN IF NOT EXISTS severity VARCHAR(50);
ALTER TABLE findings ADD COLUMN IF NOT EXISTS risk_score INTEGER DEFAULT 0;
ALTER TABLE findings ADD COLUMN IF NOT EXISTS priority VARCHAR(50);
ALTER TABLE findings ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE findings ADD COLUMN IF NOT EXISTS evidence TEXT;
ALTER TABLE findings ADD COLUMN IF NOT EXISTS category VARCHAR(200);
ALTER TABLE findings ADD COLUMN IF NOT EXISTS target_type VARCHAR(100);
ALTER TABLE findings ADD COLUMN IF NOT EXISTS target_asset VARCHAR(500);
ALTER TABLE findings ADD COLUMN IF NOT EXISTS scanner_name VARCHAR(200);
ALTER TABLE findings ADD COLUMN IF NOT EXISTS remediation TEXT;
ALTER TABLE findings ADD COLUMN IF NOT EXISTS recommendation TEXT;
ALTER TABLE findings ADD COLUMN IF NOT EXISTS business_impact TEXT;
ALTER TABLE findings ADD COLUMN IF NOT EXISTS mapped_controls TEXT[];
ALTER TABLE findings ADD COLUMN IF NOT EXISTS raw_data JSONB;
ALTER TABLE findings ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE reports ADD COLUMN IF NOT EXISTS type VARCHAR(50);
ALTER TABLE reports ADD COLUMN IF NOT EXISTS path VARCHAR(500);
ALTER TABLE reports ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE cloud_credentials ADD COLUMN IF NOT EXISTS name VARCHAR(200);
ALTER TABLE cloud_credentials ADD COLUMN IF NOT EXISTS provider VARCHAR(50);
ALTER TABLE cloud_credentials ADD COLUMN IF NOT EXISTS encrypted_data TEXT;
ALTER TABLE cloud_credentials ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE cloud_credentials ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE INDEX IF NOT EXISTS idx_findings_scan_id ON findings(scan_id);
CREATE INDEX IF NOT EXISTS idx_findings_severity ON findings(severity);
CREATE INDEX IF NOT EXISTS idx_compliance_scan_id ON compliance_scores(scan_id);
