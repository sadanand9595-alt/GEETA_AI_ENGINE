"""
==============================================================================
GEETA AI Engine

File        : exceptions.py
Package     : utils
Description : Custom Exception Definitions

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

###############################################################################
# Base Exception
###############################################################################


class GEETAError(Exception):
    """
    Base exception for the GEETA AI Engine.
    """

    def __init__(
        self,
        message: str = "GEETA AI Engine error.",
    ) -> None:

        super().__init__(message)


###############################################################################
# Configuration
###############################################################################


class ConfigurationError(GEETAError):
    """
    Raised when configuration is invalid.
    """


###############################################################################
# Database
###############################################################################


class DatabaseError(GEETAError):
    """
    Database related exception.
    """


class MigrationError(DatabaseError):
    """
    Database migration failed.
    """


###############################################################################
# File System
###############################################################################


class FileOperationError(GEETAError):
    """
    File operation failed.
    """


class FileNotFoundErrorGEETA(FileOperationError):
    """
    Project file not found.
    """


###############################################################################
# Plugin
###############################################################################


class PluginError(GEETAError):
    """
    Plugin related exception.
    """


class PluginRegistrationError(PluginError):
    """
    Plugin registration failed.
    """


class PluginInitializationError(PluginError):
    """
    Plugin initialization failed.
    """


###############################################################################
# Service Container
###############################################################################


class ServiceError(GEETAError):
    """
    Service container exception.
    """


class ServiceNotFoundError(ServiceError):
    """
    Requested service is not registered.
    """


###############################################################################
# Event Bus
###############################################################################


class EventError(GEETAError):
    """
    Event bus exception.
    """


###############################################################################
# AI Provider
###############################################################################


class AIProviderError(GEETAError):
    """
    AI provider error.
    """


class AIConnectionError(AIProviderError):
    """
    Failed to connect to AI provider.
    """


class AIAuthenticationError(AIProviderError):
    """
    Invalid API credentials.
    """
###############################################################################
# Validation
###############################################################################


class ValidationError(GEETAError):
    """
    Raised when validation fails.
    """


###############################################################################
# Project
###############################################################################


class ProjectError(GEETAError):
    """
    Project related exception.
    """


class ProjectNotFoundError(ProjectError):
    """
    Project could not be found.
    """


class ProjectIndexError(ProjectError):
    """
    Project indexing failed.
    """


###############################################################################
# Parser
###############################################################################


class ParserError(GEETAError):
    """
    Source parser exception.
    """


###############################################################################
# Memory
###############################################################################


class MemoryError(GEETAError):
    """
    AI memory exception.
    """


###############################################################################
# Debugger
###############################################################################


class DebuggerError(GEETAError):
    """
    AI debugger exception.
    """


###############################################################################
# Patch Engine
###############################################################################


class PatchError(GEETAError):
    """
    Patch engine exception.
    """


###############################################################################
# Workspace
###############################################################################


class WorkspaceError(GEETAError):
    """
    Workspace exception.
    """


###############################################################################
# Process
###############################################################################


class ProcessExecutionError(GEETAError):
    """
    External process execution failed.
    """


###############################################################################
# Network
###############################################################################


class NetworkError(GEETAError):
    """
    Network communication failed.
    """


###############################################################################
# Timeout
###############################################################################


class TimeoutErrorGEETA(GEETAError):
    """
    Operation timed out.
    """


###############################################################################
# Permission
###############################################################################


class PermissionDeniedError(GEETAError):
    """
    Permission denied.
    """


###############################################################################
# Internal
###############################################################################


class InternalError(GEETAError):
    """
    Unexpected internal application error.
    """


###############################################################################
# Exports
###############################################################################

__all__ = [
    "GEETAError",
    "ConfigurationError",
    "DatabaseError",
    "MigrationError",
    "FileOperationError",
    "FileNotFoundErrorGEETA",
    "PluginError",
    "PluginRegistrationError",
    "PluginInitializationError",
    "ServiceError",
    "ServiceNotFoundError",
    "EventError",
    "AIProviderError",
    "AIConnectionError",
    "AIAuthenticationError",
    "ValidationError",
    "ProjectError",
    "ProjectNotFoundError",
    "ProjectIndexError",
    "ParserError",
    "MemoryError",
    "DebuggerError",
    "PatchError",
    "WorkspaceError",
    "ProcessExecutionError",
    "NetworkError",
    "TimeoutErrorGEETA",
    "PermissionDeniedError",
    "InternalError",
]