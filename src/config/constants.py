"""
==============================================================================
GEETA AI Engine
Configuration Constants

File:
    src/config/constants.py

Description:
    Centralized application constants used throughout the GEETA AI Engine.

Author:
    GEETA AI Team

License:
    MIT License
==============================================================================
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path

###############################################################################
# Project Information
###############################################################################

PROJECT_NAME: str = "GEETA AI Engine"
PROJECT_SHORT_NAME: str = "GEETA"

PROJECT_VERSION: str = "1.0.0-alpha.1"

PROJECT_DESCRIPTION: str = (
    "Enterprise AI Coding & Debugging Engine"
)

PROJECT_AUTHOR: str = "Sadanand Vishwakarma"

COPYRIGHT_YEAR: str = "2026"

LICENSE_NAME: str = "MIT"

###############################################################################
# Application
###############################################################################

DEFAULT_ENCODING: str = "utf-8"

DEFAULT_TIMEZONE: str = "UTC"

MAX_LOG_FILE_SIZE_MB: int = 20

MAX_LOG_BACKUP_FILES: int = 10

###############################################################################
# Environment
###############################################################################

ENV_DEVELOPMENT: str = "development"

ENV_TESTING: str = "testing"

ENV_PRODUCTION: str = "production"

SUPPORTED_ENVIRONMENTS = (
    ENV_DEVELOPMENT,
    ENV_TESTING,
    ENV_PRODUCTION,
)

###############################################################################
# Log Levels
###############################################################################

LOG_DEBUG = "DEBUG"

LOG_INFO = "INFO"

LOG_WARNING = "WARNING"

LOG_ERROR = "ERROR"

LOG_CRITICAL = "CRITICAL"

SUPPORTED_LOG_LEVELS = (
    LOG_DEBUG,
    LOG_INFO,
    LOG_WARNING,
    LOG_ERROR,
    LOG_CRITICAL,
)

###############################################################################
# AI Providers
###############################################################################

PROVIDER_OPENAI = "openai"

PROVIDER_CLAUDE = "claude"

PROVIDER_GEMINI = "gemini"

PROVIDER_DEEPSEEK = "deepseek"

PROVIDER_OLLAMA = "ollama"

PROVIDER_OPENROUTER = "openrouter"

SUPPORTED_AI_PROVIDERS = (
    PROVIDER_OPENAI,
    PROVIDER_CLAUDE,
    PROVIDER_GEMINI,
    PROVIDER_DEEPSEEK,
    PROVIDER_OLLAMA,
    PROVIDER_OPENROUTER,
)

###############################################################################
# Default Models
###############################################################################

DEFAULT_OPENAI_MODEL = "gpt-5.5"

DEFAULT_CLAUDE_MODEL = "claude-sonnet-4"

DEFAULT_GEMINI_MODEL = "gemini-2.5-pro"

DEFAULT_DEEPSEEK_MODEL = "deepseek-chat"

DEFAULT_OLLAMA_MODEL = "llama3"

###############################################################################
# Database
###############################################################################

DATABASE_NAME = "geeta_ai_engine.db"

DATABASE_TIMEOUT = 30

DATABASE_POOL_SIZE = 10

DATABASE_FOREIGN_KEYS = True

###############################################################################
# Event Bus
###############################################################################

MAX_EVENT_QUEUE_SIZE = 10000

EVENT_TIMEOUT_SECONDS = 30

###############################################################################
# Workspace
###############################################################################

DEFAULT_WORKSPACE_NAME = "workspace"

DEFAULT_MEMORY_NAME = "memory"

DEFAULT_LOG_DIRECTORY = "logs"

DEFAULT_DATABASE_DIRECTORY = "database"

###############################################################################
# File Extensions
###############################################################################

PYTHON_EXTENSION = ".py"

JSON_EXTENSION = ".json"

YAML_EXTENSION = ".yaml"

YML_EXTENSION = ".yml"

MARKDOWN_EXTENSION = ".md"

TEXT_EXTENSION = ".txt"

SQL_EXTENSION = ".sql"

SUPPORTED_SOURCE_EXTENSIONS = (
    ".py",
)

###############################################################################
# Application Exit Codes
###############################################################################

EXIT_SUCCESS = 0

EXIT_FAILURE = 1

EXIT_CONFIGURATION_ERROR = 2

EXIT_DATABASE_ERROR = 3

EXIT_UNKNOWN_ERROR = 99

###############################################################################
# Enums
###############################################################################


class Environment(str, Enum):
    DEVELOPMENT = ENV_DEVELOPMENT
    TESTING = ENV_TESTING
    PRODUCTION = ENV_PRODUCTION


class AIProvider(str, Enum):
    OPENAI = PROVIDER_OPENAI
    CLAUDE = PROVIDER_CLAUDE
    GEMINI = PROVIDER_GEMINI
    DEEPSEEK = PROVIDER_DEEPSEEK
    OLLAMA = PROVIDER_OLLAMA
    OPENROUTER = PROVIDER_OPENROUTER

###############################################################################
# Directory Names
###############################################################################

CONFIG_DIRECTORY = "config"

CORE_DIRECTORY = "core"

DATABASE_DIRECTORY = "database"

LISTENERS_DIRECTORY = "listeners"

COLLECTORS_DIRECTORY = "collectors"

ANALYZERS_DIRECTORY = "analyzers"

INDEXER_DIRECTORY = "indexer"

AGENTS_DIRECTORY = "agents"

PROVIDERS_DIRECTORY = "providers"

PROMPTS_DIRECTORY = "prompts"

PATCHER_DIRECTORY = "patcher"

MEMORY_DIRECTORY = "memory"

SERVICES_DIRECTORY = "services"

API_DIRECTORY = "api"

UI_DIRECTORY = "ui"

PLUGINS_DIRECTORY = "plugins"

UTILS_DIRECTORY = "utils"

TESTS_DIRECTORY = "tests"

DOCS_DIRECTORY = "docs"

ASSETS_DIRECTORY = "assets"

###############################################################################
# Network Defaults
###############################################################################

DEFAULT_HOST = "127.0.0.1"

DEFAULT_HTTP_PORT = 8000

DEFAULT_WEBSOCKET_PORT = 8001

###############################################################################
# Thread Pool
###############################################################################

DEFAULT_MAX_WORKERS = 4

MIN_WORKERS = 1

MAX_WORKERS = 32

###############################################################################
# Cache
###############################################################################

DEFAULT_CACHE_SIZE = 512

DEFAULT_CACHE_TTL_SECONDS = 3600

###############################################################################
# File Watcher
###############################################################################

FILE_WATCH_DEBOUNCE_MS = 300

MAX_FILE_EVENTS = 10000

###############################################################################
# Memory
###############################################################################

DEFAULT_MEMORY_LIMIT_MB = 512

SESSION_MEMORY_NAME = "session"

PROJECT_MEMORY_NAME = "project"

ERROR_MEMORY_NAME = "errors"

###############################################################################
# API
###############################################################################

API_VERSION = "v1"

API_PREFIX = f"/api/{API_VERSION}"

###############################################################################
# Paths
###############################################################################

PROJECT_ROOT = Path.cwd()

SRC_PATH = PROJECT_ROOT / "src"

LOG_PATH = PROJECT_ROOT / "logs"

DATABASE_PATH = PROJECT_ROOT / "database"

WORKSPACE_PATH = PROJECT_ROOT / "workspace"

DOCS_PATH = PROJECT_ROOT / "docs"

ASSETS_PATH = PROJECT_ROOT / "assets"

###############################################################################
# Default Configuration
###############################################################################

DEFAULT_CONFIG = {
    "environment": ENV_DEVELOPMENT,
    "log_level": LOG_INFO,
    "provider": PROVIDER_OPENAI,
    "host": DEFAULT_HOST,
    "http_port": DEFAULT_HTTP_PORT,
    "websocket_port": DEFAULT_WEBSOCKET_PORT,
    "workers": DEFAULT_MAX_WORKERS,
    "cache_size": DEFAULT_CACHE_SIZE,
}

###############################################################################
# Export
###############################################################################

__all__ = [
    "PROJECT_NAME",
    "PROJECT_VERSION",
    "PROJECT_AUTHOR",
    "PROJECT_DESCRIPTION",
    "LICENSE_NAME",
    "Environment",
    "AIProvider",
    "DEFAULT_CONFIG",
]