-- ============================================================================
-- GEETA AI Engine
-- Database Schema
-- Version : 1.0.0-alpha.1
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ============================================================================
-- Projects
-- ============================================================================

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT NOT NULL UNIQUE,
    language TEXT,
    framework TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_projects_name
ON projects(name);

CREATE INDEX IF NOT EXISTS idx_projects_path
ON projects(path);

-- ============================================================================
-- Source Files
-- ============================================================================

CREATE TABLE IF NOT EXISTS source_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    extension TEXT,
    checksum TEXT,
    size INTEGER,
    last_modified TIMESTAMP,
    indexed INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_source_files_project
ON source_files(project_id);

CREATE INDEX IF NOT EXISTS idx_source_files_path
ON source_files(file_path);

-- ============================================================================
-- Symbols
-- ============================================================================

CREATE TABLE IF NOT EXISTS symbols (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    symbol_name TEXT NOT NULL,
    symbol_type TEXT NOT NULL,
    line_number INTEGER,
    column_number INTEGER,
    parent_symbol TEXT,
    FOREIGN KEY(file_id)
        REFERENCES source_files(id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_symbols_name
ON symbols(symbol_name);

CREATE INDEX IF NOT EXISTS idx_symbols_file
ON symbols(file_id);

-- ============================================================================
-- Dependencies
-- ============================================================================

CREATE TABLE IF NOT EXISTS dependencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    dependency TEXT NOT NULL,
    dependency_type TEXT,
    FOREIGN KEY(file_id)
        REFERENCES source_files(id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_dependencies_file
ON dependencies(file_id);

-- ============================================================================
-- Errors
-- ============================================================================

CREATE TABLE IF NOT EXISTS errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    file_path TEXT,
    error_type TEXT,
    error_message TEXT,
    traceback TEXT,
    severity TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_errors_project
ON errors(project_id);

-- ============================================================================
-- AI Memory
-- ============================================================================

CREATE TABLE IF NOT EXISTS ai_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    memory_key TEXT NOT NULL,
    memory_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_memory_key
ON ai_memory(memory_key);

-- ============================================================================
-- Sessions
-- ============================================================================

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE,
    project_id INTEGER,
    provider TEXT,
    model TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    FOREIGN KEY(project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sessions_project
ON sessions(project_id);

-- ============================================================================
-- Patch History
-- ============================================================================

CREATE TABLE IF NOT EXISTS patches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    file_path TEXT,
    patch_type TEXT,
    diff TEXT,
    applied INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_patches_project
ON patches(project_id);

-- ============================================================================
-- Settings
-- ============================================================================

CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key TEXT UNIQUE,
    setting_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);