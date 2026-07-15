"""
==============================================================================
GEETA AI Engine

File        : paths.py
Package     : config
Description : Centralized project path management.

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Final


###############################################################################
# ROOT PATHS
###############################################################################

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[2]

SRC_DIR: Final[Path] = PROJECT_ROOT / "src"

CONFIG_DIR: Final[Path] = SRC_DIR / "config"

CORE_DIR: Final[Path] = SRC_DIR / "core"

DATABASE_DIR: Final[Path] = SRC_DIR / "database"

PROVIDERS_DIR: Final[Path] = SRC_DIR / "providers"

LISTENERS_DIR: Final[Path] = SRC_DIR / "listeners"

COLLECTORS_DIR: Final[Path] = SRC_DIR / "collectors"

ANALYZERS_DIR: Final[Path] = SRC_DIR / "analyzers"

PATCHER_DIR: Final[Path] = SRC_DIR / "patcher"

MEMORY_DIR: Final[Path] = SRC_DIR / "memory"

SERVICES_DIR: Final[Path] = SRC_DIR / "services"

UTILS_DIR: Final[Path] = SRC_DIR / "utils"

API_DIR: Final[Path] = SRC_DIR / "api"

PLUGINS_DIR: Final[Path] = SRC_DIR / "plugins"

UI_DIR: Final[Path] = SRC_DIR / "ui"

INDEXER_DIR: Final[Path] = SRC_DIR / "indexer"

AGENTS_DIR: Final[Path] = SRC_DIR / "agents"

PROMPTS_DIR: Final[Path] = SRC_DIR / "prompts"

###############################################################################
# PROJECT DIRECTORIES
###############################################################################

ASSETS_DIR: Final[Path] = PROJECT_ROOT / "assets"

DOCS_DIR: Final[Path] = PROJECT_ROOT / "docs"

LOGS_DIR: Final[Path] = PROJECT_ROOT / "logs"

TESTS_DIR: Final[Path] = PROJECT_ROOT / "tests"

WORKSPACE_DIR: Final[Path] = PROJECT_ROOT / "workspace"

DATABASE_STORAGE_DIR: Final[Path] = PROJECT_ROOT / "database"

TEMP_DIR: Final[Path] = PROJECT_ROOT / "temp"

CACHE_DIR: Final[Path] = PROJECT_ROOT / "cache"

BACKUP_DIR: Final[Path] = PROJECT_ROOT / "backup"

EXPORT_DIR: Final[Path] = PROJECT_ROOT / "exports"

###############################################################################
# FILE PATHS
###############################################################################

ENV_FILE: Final[Path] = PROJECT_ROOT / ".env"

ENV_EXAMPLE_FILE: Final[Path] = PROJECT_ROOT / ".env.example"

README_FILE: Final[Path] = PROJECT_ROOT / "README.md"

CHANGELOG_FILE: Final[Path] = PROJECT_ROOT / "CHANGELOG.md"

LICENSE_FILE: Final[Path] = PROJECT_ROOT / "LICENSE"

EDITORCONFIG_FILE: Final[Path] = PROJECT_ROOT / ".editorconfig"

GITIGNORE_FILE: Final[Path] = PROJECT_ROOT / ".gitignore"

PYPROJECT_FILE: Final[Path] = PROJECT_ROOT / "pyproject.toml"

###############################################################################
# REQUIRED DIRECTORIES
###############################################################################

REQUIRED_DIRECTORIES: tuple[Path, ...] = (
    LOGS_DIR,
    DATABASE_STORAGE_DIR,
    WORKSPACE_DIR,
    CACHE_DIR,
    TEMP_DIR,
    BACKUP_DIR,
    EXPORT_DIR,
)

###############################################################################
# DIRECTORY HELPERS
###############################################################################


def create_required_directories() -> None:
    """
    Create all required project directories if they do not exist.
    """

    for directory in REQUIRED_DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)


def directory_exists(path: Path) -> bool:
    """
    Check whether a directory exists.

    Args:
        path:
            Directory path.

    Returns:
        True if directory exists.
    """

    return path.exists() and path.is_dir()


def file_exists(path: Path) -> bool:
    """
    Check whether a file exists.

    Args:
        path:
            File path.

    Returns:
        True if file exists.
    """

    return path.exists() and path.is_file()


###############################################################################
# VALIDATION
###############################################################################


def validate_project_structure() -> list[str]:
    """
    Validate the minimum project structure.

    Returns:
        List of missing directories.
    """

    missing: list[str] = []

    required = (
        SRC_DIR,
        CONFIG_DIR,
        CORE_DIR,
    )

    for directory in required:
        if not directory.exists():
            missing.append(str(directory))

    return missing


###############################################################################
# INITIALIZATION
###############################################################################

create_required_directories()

###############################################################################
# EXPORTS
###############################################################################

__all__ = [
    "PROJECT_ROOT",
    "SRC_DIR",
    "CONFIG_DIR",
    "CORE_DIR",
    "DATABASE_DIR",
    "PROVIDERS_DIR",
    "LISTENERS_DIR",
    "COLLECTORS_DIR",
    "ANALYZERS_DIR",
    "PATCHER_DIR",
    "MEMORY_DIR",
    "SERVICES_DIR",
    "UTILS_DIR",
    "API_DIR",
    "PLUGINS_DIR",
    "UI_DIR",
    "INDEXER_DIR",
    "AGENTS_DIR",
    "PROMPTS_DIR",
    "ASSETS_DIR",
    "DOCS_DIR",
    "LOGS_DIR",
    "TESTS_DIR",
    "WORKSPACE_DIR",
    "DATABASE_STORAGE_DIR",
    "TEMP_DIR",
    "CACHE_DIR",
    "BACKUP_DIR",
    "EXPORT_DIR",
    "ENV_FILE",
    "ENV_EXAMPLE_FILE",
    "README_FILE",
    "CHANGELOG_FILE",
    "LICENSE_FILE",
    "EDITORCONFIG_FILE",
    "GITIGNORE_FILE",
    "PYPROJECT_FILE",
    "REQUIRED_DIRECTORIES",
    "create_required_directories",
    "directory_exists",
    "file_exists",
    "validate_project_structure",
]