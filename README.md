<p align="center">
  <img src="assets/logo.png" width="180">
</p>
<h1 align="center">
# GEETA AI Engine
</h1>

<p align="center">

### Enterprise AI Coding & Debugging Engine
</p>

<p aling="center">

> Understand • Analyze • Debug • Patch • Automate
</p>

> Building the next generation AI Software Engineering Platform.
> Designed for developers. Built for the future.
---

## Introduction

GEETA AI Engine is an enterprise-grade AI software engineering engine designed to understand complete software projects, monitor execution, analyze runtime and static errors, generate intelligent fixes, and provide a modular foundation for modern AI-powered development environments.

It is designed as a standalone engine that can integrate with VS Code, custom IDEs, command-line tools, and future plugins.

The long-term goal is to evolve from an AI debugging engine into a complete autonomous software engineering platform.

## Vision

The vision of GEETA AI Engine is to redefine AI-assisted software development by creating an intelligent engine that understands complete software projects rather than isolated files.

Our goal is to build a modular, scalable, and extensible AI platform capable of analyzing source code, understanding project architecture, detecting errors, identifying root causes, generating intelligent patches, and assisting developers throughout the complete software development lifecycle.

GEETA AI Engine is designed to evolve from an advanced AI debugging engine into a fully autonomous software engineering platform capable of collaborating with developers, automating repetitive tasks, and accelerating software development without compromising code quality, maintainability, or security.

## Key Features

GEETA AI Engine provides a comprehensive set of enterprise-grade AI capabilities designed for modern software engineering.

### Project Intelligence

- Complete project understanding
- Workspace indexing
- AST (Abstract Syntax Tree) analysis
- Symbol indexing
- Dependency graph generation
- Cross-file context awareness

### Intelligent Error Detection

- Live file monitoring
- Python traceback analysis
- Runtime exception detection
- VS Code diagnostics integration
- Terminal output monitoring
- Log analysis

### AI-Powered Debugging

- Root cause analysis
- Intelligent error explanation
- Context-aware debugging
- Automatic solution generation
- Multi-file debugging support
- AI-assisted troubleshooting

### Intelligent Patch Engine

- Unified diff generation
- Patch validation
- One-click patch application
- Rollback support
- Safe code modification
- Preview before applying changes

### Multi-Provider AI Support

- OpenAI GPT
- Claude
- Gemini
- DeepSeek
- Ollama
- OpenRouter
- Future provider support

### Memory Engine

- Error history
- Project memory
- Session memory
- Context persistence
- Learning from previous fixes

### Plugin-Based Architecture

- Modular design
- Dynamic plugin loading
- Custom integrations
- Language extensions
- IDE extensions

### Developer Productivity

- AI Coding Assistant
- AI Debug Assistant
- AI Code Review
- AI Refactoring
- AI Documentation
- AI Test Generation

### VS Code Integration

- Live diagnostics
- Error highlighting
- AI Chat
- One-click fixes
- Terminal integration
- Workspace synchronization

### Enterprise Architecture

- Event-driven system
- Service container
- Plugin manager
- Scalable architecture
- Clean architecture principles
- SOLID design principles

### Future Capabilities

- Autonomous coding agents
- Security analysis
- Performance optimization
- DevOps automation
- Cloud integration
- Multi-language support

## Architecture

GEETA AI Engine follows a modular, event-driven, and plugin-based architecture designed for scalability, maintainability, and future extensibility.

The engine is organized into independent components that communicate through a centralized Event Bus, allowing each module to operate independently while remaining fully integrated.

```text
                           +----------------------+
                           |      Developer       |
                           +----------+-----------+
                                      |
                                      |
                           VS Code Extension
                                      |
                           WebSocket / REST API
                                      |
                                      ▼
+-----------------------------------------------------------------------+
|                           GEETA AI ENGINE                             |
|-----------------------------------------------------------------------|
|                                                                       |
|  Core Layer                                                           |
|  ├── Application                                                      |
|  ├── Event Bus                                                        |
|  ├── Service Container                                                |
|  ├── Plugin Manager                                                   |
|                                                                       |
|-----------------------------------------------------------------------|
|                                                                       |
|  Monitoring Layer                                                     |
|  ├── File Listener                                                    |
|  ├── Terminal Listener                                                |
|  ├── Traceback Listener                                               |
|  ├── VS Code Diagnostics                                              |
|                                                                       |
|-----------------------------------------------------------------------|
|                                                                       |
|  Intelligence Layer                                                   |
|  ├── Project Indexer                                                  |
|  ├── AST Parser                                                       |
|  ├── Symbol Index                                                     |
|  ├── Dependency Graph                                                 |
|  ├── Context Builder                                                  |
|                                                                       |
|-----------------------------------------------------------------------|
|                                                                       |
|  AI Layer                                                             |
|  ├── Prompt Engine                                                    |
|  ├── Provider Manager                                                 |
|  ├── GPT                                                              |
|  ├── Claude                                                           |
|  ├── Gemini                                                           |
|  ├── DeepSeek                                                         |
|  ├── Ollama                                                           |
|                                                                       |
|-----------------------------------------------------------------------|
|                                                                       |
|  Patch Engine                                                         |
|  ├── Diff Generator                                                   |
|  ├── Patch Validator                                                  |
|  ├── Patch Generator                                                  |
|  ├── Patch Applier                                                    |
|  ├── Rollback Engine                                                  |
|                                                                       |
|-----------------------------------------------------------------------|
|                                                                       |
|  Memory Layer                                                        |
|  ├── Session Memory                                                   |
|  ├── Error Memory                                                     |
|  ├── Project Memory                                                   |
|  ├── Embedding Memory                                                 |
|                                                                       |
|-----------------------------------------------------------------------|
|                                                                       |
|  Database Layer                                                       |
|  ├── SQLite                                                           |
|  ├── Repositories                                                     |
|  ├── Migrations                                                       |
|                                                                       |
+-----------------------------------------------------------------------+
                                      |
                                      ▼
                             Target Project

## System Workflow

The following workflow illustrates how GEETA AI Engine continuously monitors the development environment, understands project context, analyzes errors, and assists developers with intelligent solutions.

```text
                     Developer
                         │
                         ▼
                  Write / Edit Code
                         │
                         ▼
                     Save File
                         │
                         ▼
                 File Listener Detects Change
                         │
         ┌───────────────┼────────────────┐
         │               │                │
         ▼               ▼                ▼
   File Scanner   Terminal Listener   VS Code Diagnostics
         │               │                │
         └───────────────┼────────────────┘
                         ▼
                 Error & Context Collector
                         │
                         ▼
                 Project Intelligence Engine
                         │
         ┌───────────────┼────────────────┐
         │               │                │
         ▼               ▼                ▼
      AST Parser    Symbol Index    Dependency Graph
         │               │                │
         └───────────────┼────────────────┘
                         ▼
                  Context Builder
                         │
                         ▼
                 AI Provider Manager
                         │
     ┌──────────┬────────┼────────┬─────────┐
     │          │        │        │         │
     ▼          ▼        ▼        ▼         ▼
   GPT       Claude   Gemini  DeepSeek   Ollama
                         │
                         ▼
               Root Cause Analysis
                         │
                         ▼
                 Intelligent Patch Engine
                         │
         ┌───────────────┼────────────────┐
         │               │                │
         ▼               ▼                ▼
    Generate Diff   Validate Patch   Preview Changes
         │               │                │
         └───────────────┼────────────────┘
                         ▼
                  Apply Patch
                         │
                         ▼
                  Execute Tests
                         │
                         ▼
                 Update AI Memory
                         │
                         ▼
               Developer Receives Result
```

### Workflow Summary

1. Developer edits or creates source code.
2. File listeners detect project changes.
3. Runtime logs, terminal output, and IDE diagnostics are collected.
4. The Project Intelligence Engine builds complete project context.
5. The AI Provider analyzes the collected information.
6. Root cause analysis identifies the actual issue.
7. A safe patch is generated and validated.
8. The developer previews and applies the patch.
9. Tests are executed to verify the solution.
10. The successful fix is stored in the Memory Engine for future reuse.

## Project Structure

The project is organized into modular components following Clean Architecture principles. Each module has a single responsibility and communicates through well-defined interfaces.

```text
GEETA_AI_ENGINE/
│
├── assets/                     # Logos, banners, icons, images
│
├── docs/                       # Project documentation
│   ├── architecture/
│   ├── api/
│   ├── database/
│   ├── plugins/
│   └── user_guide/
│
├── examples/                   # Sample projects and examples
│
├── logs/                       # Runtime log files
│
├── scripts/                    # Utility and automation scripts
│
├── tests/                      # Test suite
│   ├── unit/
│   ├── integration/
│   ├── performance/
│   └── fixtures/
│
├── src/
│   │
│   ├── config/                 # Configuration management
│   │
│   ├── core/                   # Core framework components
│   │
│   ├── database/               # Database layer
│   │
│   ├── listeners/              # File, terminal and diagnostics listeners
│   │
│   ├── collectors/             # Runtime information collectors
│   │
│   ├── analyzers/              # Error and project analysis
│   │
│   ├── indexer/                # Project indexing engine
│   │
│   ├── agents/                 # AI software engineering agents
│   │
│   ├── providers/              # AI provider implementations
│   │
│   ├── prompts/                # Prompt templates
│   │
│   ├── patcher/                # Patch generation engine
│   │
│   ├── memory/                 # AI memory system
│   │
│   ├── services/               # Business logic services
│   │
│   ├── api/                    # REST & WebSocket APIs
│   │
│   ├── ui/                     # Desktop UI components
│   │
│   ├── plugins/                # IDE integrations
│   │
│   ├── utils/                  # Shared utility functions
│   │
│   └── main.py                 # Application entry point
│
├── .env.example
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
└── CHANGELOG.md
```

### Directory Overview

| Directory | Purpose |
|------------|---------|
| `src/` | Main application source code |
| `config/` | Application configuration |
| `core/` | Core architecture and framework |
| `database/` | Database layer and repositories |
| `listeners/` | File system, terminal and diagnostics monitoring |
| `collectors/` | Runtime information collection |
| `analyzers/` | Error and project analysis |
| `indexer/` | Project indexing and symbol management |
| `providers/` | AI provider integrations |
| `patcher/` | Patch generation and application |
| `memory/` | AI memory management |
| `services/` | Application services |
| `api/` | REST and WebSocket servers |
| `plugins/` | IDE integrations |
| `tests/` | Unit and integration tests |
| `docs/` | Project documentation |

## Installation

### System Requirements

Before installing GEETA AI Engine, ensure your development environment meets the following requirements.

| Requirement | Version |
|--------------|----------|
| Python | 3.12 or later |
| Git | Latest |
| Operating System | Windows, Linux, macOS |
| RAM | Minimum 8 GB (16 GB Recommended) |
| Storage | Minimum 2 GB Free Space |

---

## Clone the Repository

```bash
git clone https://github.com/<your-username>/GEETA_AI_ENGINE.git

cd GEETA_AI_ENGINE
```

---

## Create a Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install --upgrade pip

pip install -e .

# Install development dependencies

pip install -e ".[dev]"
```

---

## Configure Environment

Create a local environment file.

```bash
cp .env.example .env
```

Windows users can create a copy manually if the `cp` command is unavailable.

---

## Verify Installation

Run the following command to verify the installation.

```bash
python -m src.main
```

If the installation is successful, the application will initialize without errors and display the startup information in the console.

---

## Upgrade Dependencies

```bash
pip install --upgrade -e .
```

---

## Troubleshooting

### Python Version Error

Verify your Python version.

```bash
python --version
```

---

### Virtual Environment Not Activated

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

---

### Missing Dependencies

Reinstall all project dependencies.

```bash
pip install -e ".[dev]"
```
## Quick Start

This guide helps you get GEETA AI Engine up and running in just a few minutes.

---

### Step 1 — Launch the Engine

Start the application using:

```bash
python -m src.main
```

If everything is configured correctly, the engine will initialize its core services and display startup information in the terminal.

---

### Step 2 — Open Your Project

Open or connect the software project you want GEETA AI Engine to analyze.

Supported project types include:

- Python Projects
- Future support for JavaScript
- Future support for Java
- Future support for C#
- Future support for C++
- Future support for Rust

---

### Step 3 — Index the Project

The Project Intelligence Engine scans the workspace and builds:

- Project Index
- Symbol Index
- Dependency Graph
- Project Memory
- Context Database

This enables the AI to understand the project before providing suggestions.

---

### Step 4 — Start Monitoring

Once indexing is complete, GEETA AI Engine automatically begins monitoring:

- File changes
- Terminal output
- Runtime exceptions
- Python tracebacks
- IDE diagnostics
- Application logs

No manual configuration is required.

---

### Step 5 — Trigger an Error

Run your application normally.

Example:

```bash
python main.py
```

If an error occurs, GEETA AI Engine will automatically begin collecting diagnostic information.

---

### Step 6 — AI Analysis

The engine automatically gathers:

- Error details
- Stack trace
- Related source files
- Imports
- Dependencies
- Project context
- Previous fixes (if available)

The collected information is then sent to the configured AI provider.

---

### Step 7 — Review the Suggested Fix

GEETA AI Engine generates:

- Root Cause Analysis
- Error Explanation
- Suggested Fix
- Unified Diff
- Patch Preview

Review the generated solution before applying any changes.

---

### Step 8 — Apply the Patch

Apply the generated patch directly from the interface.

The Patch Engine performs validation before modifying project files.

---

### Step 9 — Verify the Result

After applying the patch, the engine:

- Re-runs validation
- Updates project memory
- Stores successful fixes
- Prepares context for future debugging sessions

---

## Expected Workflow

```text
Start Engine
      │
      ▼
Open Project
      │
      ▼
Index Workspace
      │
      ▼
Monitor Project
      │
      ▼
Detect Error
      │
      ▼
Collect Context
      │
      ▼
AI Analysis
      │
      ▼
Generate Patch
      │
      ▼
Review Changes
      │
      ▼
Apply Patch
      │
      ▼
Continue Development
```

---

## Next Steps

Once the engine is running successfully, continue with:

- Configuration
- AI Provider Setup
- Plugin Configuration
- Development Workflow

## Configuration

GEETA AI Engine uses environment variables and configuration files to manage application settings, AI providers, logging, database connections, and runtime behavior.

---

## Environment File

Copy the example environment file.

```bash
cp .env.example .env
```

Open the `.env` file and configure the required settings.

---

## Example Configuration

```env
# ======================================================
# GEETA AI Engine Configuration
# ======================================================

# Application
APP_NAME=GEETA AI Engine
APP_ENV=development
APP_DEBUG=true

# Logging
LOG_LEVEL=INFO

# Database
DATABASE_URL=sqlite:///database/geeta.db

# Default AI Provider
DEFAULT_PROVIDER=openai

# OpenAI
OPENAI_API_KEY=

# Claude
ANTHROPIC_API_KEY=

# Gemini
GEMINI_API_KEY=

# OpenRouter
OPENROUTER_API_KEY=

# DeepSeek
DEEPSEEK_API_KEY=

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Server
HOST=127.0.0.1
PORT=8000
```

---

## Configuration Categories

### Application

Controls application behavior.

| Variable | Description |
|----------|-------------|
| APP_NAME | Application name |
| APP_ENV | development / production |
| APP_DEBUG | Enable debug mode |

---

### Logging

Controls runtime logging.

| Variable | Description |
|----------|-------------|
| LOG_LEVEL | DEBUG, INFO, WARNING, ERROR |

---

### Database

Defines the project database.

| Variable | Description |
|----------|-------------|
| DATABASE_URL | SQLite connection string |

---

### AI Provider

Select the default AI model.

Supported providers:

- OpenAI
- Claude
- Gemini
- DeepSeek
- Ollama
- OpenRouter

---

### Server

Server configuration.

| Variable | Description |
|----------|-------------|
| HOST | Server host |
| PORT | Server port |

---

## Best Practices

- Never commit your `.env` file.
- Keep API keys private.
- Use different configuration for development and production.
- Rotate API keys regularly.
- Store secrets securely.

---

## Configuration Loading

At startup, GEETA AI Engine loads configuration in the following order:

```text
Default Settings
        │
        ▼
Configuration File
        │
        ▼
Environment Variables
        │
        ▼
Runtime Overrides
```

Runtime values always take precedence over default values.

## AI Providers

GEETA AI Engine is designed with a provider-independent architecture, allowing developers to switch between multiple AI models without changing application code.

The Provider Manager acts as an abstraction layer between the engine and external AI services, ensuring a consistent interface regardless of the selected provider.

---

## Supported Providers

| Provider | Status | Purpose |
|-----------|--------|---------|
| OpenAI | ✅ Supported | General-purpose reasoning and coding |
| Claude | ✅ Supported | Long-context reasoning and architecture analysis |
| Gemini | ✅ Supported | Fast code understanding and generation |
| OpenRouter | ✅ Supported | Access to multiple AI models through one API |
| Ollama | ✅ Supported | Local offline AI models |
| DeepSeek | ✅ Supported | Cost-effective coding assistance |

---

## Provider Architecture

```text
                  GEETA AI ENGINE
                         │
                         ▼
                Provider Manager
                         │
     ┌───────────┬───────────┬───────────┬───────────┐
     │           │           │           │           │
     ▼           ▼           ▼           ▼           ▼
  OpenAI      Claude      Gemini     DeepSeek     Ollama
                         │
                         ▼
                  AI Response
                         │
                         ▼
                Context Processor
                         │
                         ▼
                  Patch Generator
```

---

## Provider Selection

The active provider is configured using the `.env` file.

```env
DEFAULT_PROVIDER=openai
```

Available values:

```text
openai
claude
gemini
deepseek
ollama
openrouter
```

---

## Provider Configuration

### OpenAI

```env
OPENAI_API_KEY=your_api_key
```

---

### Claude

```env
ANTHROPIC_API_KEY=your_api_key
```

---

### Gemini

```env
GEMINI_API_KEY=your_api_key
```

---

### DeepSeek

```env
DEEPSEEK_API_KEY=your_api_key
```

---

### OpenRouter

```env
OPENROUTER_API_KEY=your_api_key
```

---

### Ollama

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

---

## Provider Switching

Changing AI providers does not require any code modifications.

Simply update the configuration:

```env
DEFAULT_PROVIDER=claude
```

Restart the application and the new provider becomes active.

---

## Future Provider Support

The provider system is fully extensible.

Future integrations may include:

- Azure OpenAI
- Amazon Bedrock
- Google Vertex AI
- Mistral AI
- Groq
- Cohere
- Custom enterprise AI services

---

## Design Principles

The Provider Layer follows these principles:

- Provider-independent architecture
- Unified request interface
- Unified response format
- Automatic provider switching
- Extensible plugin system
- Consistent error handling
- Future-proof design

## Plugin System

GEETA AI Engine is built on a plugin-based architecture that allows new capabilities to be added without modifying the core engine.

Each plugin is loaded through the Plugin Manager and communicates with the engine using well-defined interfaces and the Event Bus.

This design keeps the core engine lightweight, modular, and easy to extend.

---

## Plugin Architecture

```text
                    GEETA AI ENGINE
                           │
                    Plugin Manager
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   IDE Plugins      AI Provider Plugins   Language Plugins
        │                  │                  │
        ▼                  ▼                  ▼
    VS Code          OpenAI Provider      Python
    PyCharm          Claude Provider      JavaScript
    CLI              Gemini Provider      Java
                     Ollama Provider      C#
                     DeepSeek Provider    C++
```

---

## Plugin Categories

### IDE Plugins

Provide integration with development environments.

Examples:

- VS Code
- PyCharm
- IntelliJ IDEA
- CLI
- Future desktop applications

---

### Language Plugins

Provide language-specific intelligence.

Examples:

- Python
- JavaScript
- TypeScript
- Java
- C#
- C++
- Rust
- Go

---

### AI Provider Plugins

Allow communication with different AI models.

Examples:

- OpenAI
- Claude
- Gemini
- DeepSeek
- Ollama
- OpenRouter

---

### Tool Plugins

Provide integration with external tools.

Examples:

- Git
- Docker
- Kubernetes
- Terminal
- Browser Automation
- Database Tools

---

## Plugin Lifecycle

Every plugin follows the same lifecycle.

```text
Load Plugin
      │
      ▼
Validate
      │
      ▼
Initialize
      │
      ▼
Register Services
      │
      ▼
Register Events
      │
      ▼
Start Plugin
      │
      ▼
Running
      │
      ▼
Shutdown
      │
      ▼
Unload
```

---

## Plugin Responsibilities

A plugin may:

- Register services
- Listen for events
- Publish events
- Extend AI capabilities
- Add UI components
- Register commands
- Add language support
- Integrate external tools

Plugins should **not** modify the core engine directly.

---

## Plugin Directory

```text
src/
└── plugins/
    ├── vscode/
    ├── pycharm/
    ├── python/
    ├── javascript/
    ├── docker/
    ├── git/
    └── terminal/
```

---

## Design Goals

The Plugin System is designed to provide:

- Loose coupling
- High scalability
- Independent deployment
- Easy maintenance
- Future extensibility
- Stable core architecture
- Simple third-party integration

---

## Future Plugin Ecosystem

Planned plugin categories include:

- AI Agents
- Cloud Providers
- DevOps Tools
- Mobile Development
- Web Development
- Database Integrations
- Security Analysis
- Performance Profiling
- Testing Frameworks
- Documentation Tools

## API Overview

GEETA AI Engine exposes both REST APIs and WebSocket APIs to enable communication with IDEs, desktop applications, command-line tools, and future third-party integrations.

The API layer is designed to provide secure, scalable, and real-time communication between clients and the engine.

---

## API Architecture

```text
                  Client Applications
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      ▼                    ▼                    ▼
 VS Code Extension     Desktop App          CLI Client
      │                    │                    │
      └────────────────────┼────────────────────┘
                           │
                    REST / WebSocket
                           │
                           ▼
                 GEETA AI ENGINE API
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    Service Layer     Event Bus      Plugin Manager
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                     Core Engine
```

---

## Communication Protocols

| Protocol | Purpose |
|-----------|---------|
| REST API | Configuration, project management, status |
| WebSocket | Real-time diagnostics and AI communication |
| Event Bus | Internal engine communication |

---

## REST API

The REST API is used for standard request-response operations.

Typical operations include:

- Start Engine
- Stop Engine
- Load Project
- Reload Configuration
- Provider Management
- Project Status
- Memory Management

---

## WebSocket API

The WebSocket server provides real-time communication.

Typical events include:

- File Changed
- Error Detected
- Project Indexed
- AI Analysis Started
- Patch Generated
- Patch Applied
- Tests Completed

---

## Example Request

```http
POST /api/v1/projects/open
```

```json
{
  "project_path": "D:/Projects/MyApplication"
}
```

---

## Example Response

```json
{
  "success": true,
  "project_id": "project_001",
  "status": "loaded"
}
```

---

## WebSocket Event Example

```json
{
  "event": "error_detected",
  "timestamp": "2026-01-10T14:35:20Z",
  "project": "MyApplication",
  "severity": "error",
  "message": "ModuleNotFoundError"
}
```

---

## API Versioning

The API follows semantic versioning.

Example:

```text
/api/v1/
/api/v2/
```

Future versions will remain backward compatible whenever possible.

---

## Authentication (Future)

Planned authentication methods include:

- API Keys
- JWT Tokens
- OAuth 2.0
- Enterprise SSO

---

## Error Response Format

All APIs return a consistent response structure.

```json
{
  "success": false,
  "error": {
    "code": "PROJECT_NOT_FOUND",
    "message": "The specified project does not exist."
  }
}
```

---

## Design Principles

The API layer is designed with the following goals:

- Consistent request format
- Consistent response format
- Versioned endpoints
- Real-time communication
- Secure by design
- Extensible architecture
- IDE-independent integration

## Development Roadmap

GEETA AI Engine is being developed incrementally through well-defined milestones. Each version introduces new capabilities while maintaining stability, scalability, and backward compatibility.

---

## Version 1.0 — Foundation

**Status:** 🚧 In Development

### Objectives

- Project Bootstrap
- Configuration System
- Logging Framework
- Database Layer
- Event Bus
- Dependency Injection
- Service Container
- Plugin Manager
- Core Application Lifecycle

---

## Version 1.1 — Project Intelligence

**Status:** 📋 Planned

### Objectives

- Workspace Scanner
- Project Indexer
- AST Parser
- Symbol Index
- Dependency Graph
- Project Context Builder
- Project Memory

---

## Version 1.2 — Runtime Monitoring

**Status:** 📋 Planned

### Objectives

- File Listener
- Terminal Listener
- Process Listener
- Python Traceback Reader
- Log Collector
- VS Code Diagnostics Integration

---

## Version 1.3 — AI Engine

**Status:** 📋 Planned

### Objectives

- Prompt Engine
- Context Engine
- Multi-Provider Support
- AI Response Processing
- Root Cause Analysis
- Intelligent Suggestions

---

## Version 1.4 — Intelligent Patch Engine

**Status:** 📋 Planned

### Objectives

- Patch Generator
- Unified Diff
- Patch Validator
- Preview Changes
- One-click Apply
- Rollback Support

---

## Version 2.0 — IDE Integration

**Status:** 📋 Planned

### Objectives

- VS Code Extension
- Live AI Chat
- Diagnostics Panel
- Code Actions
- Real-time Debugging
- Workspace Synchronization

---

## Version 2.5 — Multi-Agent System

**Status:** 📋 Planned

### AI Agents

- Debug Agent
- Coding Agent
- Review Agent
- Refactoring Agent
- Documentation Agent
- Testing Agent

---

## Version 3.0 — Autonomous Software Engineering

**Status:** 🔮 Vision

### Long-Term Goals

- Autonomous Coding
- Autonomous Debugging
- Autonomous Refactoring
- Intelligent Project Planning
- Automated Testing
- Performance Optimization
- Security Analysis
- DevOps Assistance

---

## Long-Term Vision

GEETA AI Engine is designed to evolve from an AI-assisted debugging platform into a comprehensive software engineering engine capable of understanding, maintaining, and improving complex software systems while keeping developers in control of important decisions.

---

## Roadmap Summary

| Version | Focus | Status |
|----------|--------|--------|
| v1.0 | Foundation | 🚧 In Development |
| v1.1 | Project Intelligence | 📋 Planned |
| v1.2 | Runtime Monitoring | 📋 Planned |
| v1.3 | AI Engine | 📋 Planned |
| v1.4 | Patch Engine | 📋 Planned |
| v2.0 | IDE Integration | 📋 Planned |
| v2.5 | Multi-Agent System | 📋 Planned |
| v3.0 | Autonomous Engineering | 🔮 Vision |

## Core Design Principles

GEETA AI Engine is built around a set of engineering principles that guide every architectural and implementation decision. These principles ensure the project remains scalable, maintainable, and reliable as it grows.

---

### Clean Architecture

The project is organized into independent layers with clear responsibilities. Business logic remains isolated from external frameworks and infrastructure.

---

### SOLID Principles

Every module follows SOLID design principles to maximize maintainability, flexibility, and testability.

---

### Event-Driven Architecture

Components communicate through a centralized Event Bus instead of direct dependencies, enabling loose coupling and better scalability.

---

### Plugin-Based Design

New functionality should be added through plugins whenever possible. The core engine should remain lightweight and stable.

---

### Dependency Injection

Core services are resolved through a Service Container instead of creating direct object dependencies.

---

### Separation of Concerns

Each module has a single responsibility and should focus on one specific area of the system.

---

### Provider Independence

The engine must never depend on a single AI provider. Every provider should implement a common interface.

---

### Security by Design

Security considerations are integrated into the architecture from the beginning, including secure configuration handling, secret management, and input validation.

---

### Performance First

The engine should minimize unnecessary computation, reduce memory usage, and optimize startup time while maintaining code readability.

---

### Testability

Every major component should be independently testable through unit and integration tests.

---

### Extensibility

The architecture should support future IDEs, programming languages, AI providers, and plugins without requiring significant changes to the core engine.

---

### Maintainability

Code should prioritize clarity, consistency, and documentation over unnecessary complexity.

---

### Developer Experience

The engine should provide a predictable, consistent, and productive development experience for both users and contributors.

---

## Engineering Philosophy

GEETA AI Engine is designed to evolve through incremental improvements rather than large-scale rewrites. Stability, modularity, and long-term maintainability take priority over short-term feature additions.

Every architectural decision should answer the following questions:

- Is it modular?
- Is it maintainable?
- Is it testable?
- Is it extensible?
- Is it secure?
- Is it consistent with the existing architecture?

If the answer to any of these questions is **No**, the design should be reconsidered before implementation.

## Core Design Principles

GEETA AI Engine is built around a set of engineering principles that guide every architectural and implementation decision. These principles ensure the project remains scalable, maintainable, and reliable as it grows.

---

### Clean Architecture

The project is organized into independent layers with clear responsibilities. Business logic remains isolated from external frameworks and infrastructure.

---

### SOLID Principles

Every module follows SOLID design principles to maximize maintainability, flexibility, and testability.

---

### Event-Driven Architecture

Components communicate through a centralized Event Bus instead of direct dependencies, enabling loose coupling and better scalability.

---

### Plugin-Based Design

New functionality should be added through plugins whenever possible. The core engine should remain lightweight and stable.

---

### Dependency Injection

Core services are resolved through a Service Container instead of creating direct object dependencies.

---

### Separation of Concerns

Each module has a single responsibility and should focus on one specific area of the system.

---

### Provider Independence

The engine must never depend on a single AI provider. Every provider should implement a common interface.

---

### Security by Design

Security considerations are integrated into the architecture from the beginning, including secure configuration handling, secret management, and input validation.

---

### Performance First

The engine should minimize unnecessary computation, reduce memory usage, and optimize startup time while maintaining code readability.

---

### Testability

Every major component should be independently testable through unit and integration tests.

---

### Extensibility

The architecture should support future IDEs, programming languages, AI providers, and plugins without requiring significant changes to the core engine.

---

### Maintainability

Code should prioritize clarity, consistency, and documentation over unnecessary complexity.

---

### Developer Experience

The engine should provide a predictable, consistent, and productive development experience for both users and contributors.

---

## Engineering Philosophy

GEETA AI Engine is designed to evolve through incremental improvements rather than large-scale rewrites. Stability, modularity, and long-term maintainability take priority over short-term feature additions.

Every architectural decision should answer the following questions:

- Is it modular?
- Is it maintainable?
- Is it testable?
- Is it extensible?
- Is it secure?
- Is it consistent with the existing architecture?

If the answer to any of these questions is **No**, the design should be reconsidered before implementation.

## Performance Goals

GEETA AI Engine is designed with performance, scalability, and responsiveness as core engineering objectives.

The following targets represent the expected performance goals for stable releases.

---

## Engine Performance

| Metric | Target |
|---------|---------|
| Engine Startup Time | Less than 2 seconds |
| Configuration Loading | Less than 100 ms |
| Plugin Initialization | Less than 500 ms |
| Event Dispatch Time | Less than 10 ms |

---

## Project Intelligence

| Metric | Target |
|---------|---------|
| Small Project Indexing (<100 files) | Less than 2 seconds |
| Medium Project Indexing (<1,000 files) | Less than 5 seconds |
| Large Project Indexing (<10,000 files) | Less than 30 seconds |
| Incremental Re-indexing | Less than 500 ms |

---

## File Monitoring

| Metric | Target |
|---------|---------|
| File Change Detection | Less than 100 ms |
| Terminal Output Detection | Real-time |
| Traceback Detection | Less than 100 ms |
| Diagnostics Processing | Less than 200 ms |

---

## AI Processing

> AI response time depends on the selected provider and network conditions. The targets below apply only to internal engine processing.

| Metric | Target |
|---------|---------|
| Context Building | Less than 500 ms |
| Prompt Generation | Less than 100 ms |
| Response Processing | Less than 200 ms |
| Patch Generation | Less than 300 ms |
| Patch Validation | Less than 200 ms |

---

## Memory Usage

| Scenario | Target |
|----------|---------|
| Idle Engine | Less than 200 MB |
| Medium Project | Less than 500 MB |
| Large Project | Less than 1 GB |

---

## Database Performance

| Metric | Target |
|---------|---------|
| Database Connection | Less than 100 ms |
| Project Save | Less than 200 ms |
| Error History Lookup | Less than 50 ms |
| Memory Retrieval | Less than 100 ms |

---

## Scalability Goals

GEETA AI Engine is designed to support:

- Projects containing more than 100,000 source files
- Multiple concurrent AI providers
- Multiple IDE integrations
- Plugin-based extensions
- Cross-platform development
- Enterprise-scale codebases

---

## Performance Principles

Every new feature should:

- Minimize CPU usage
- Reduce memory consumption
- Avoid unnecessary disk I/O
- Prevent blocking operations
- Support asynchronous execution
- Scale with project size
- Preserve responsiveness

---

## Continuous Optimization

Performance is considered a continuous engineering objective.

Every major release should improve or maintain:

- Startup performance
- Runtime responsiveness
- Memory efficiency
- AI processing speed
- Project indexing performance
- Overall developer experience

## Module Dependency Graph

GEETA AI Engine follows a layered dependency model.

Each module depends only on lower-level services and communicates with other modules through well-defined interfaces and the Event Bus. This minimizes coupling and improves maintainability.

---

## High-Level Dependency Flow

```text
                 Configuration
                       │
                       ▼
                    Logger
                       │
                       ▼
                    Database
                       │
                       ▼
                Service Container
                       │
                       ▼
                   Event Bus
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
     Listeners    Plugin Manager   Services
         │             │             │
         └─────────────┼─────────────┘
                       ▼
                  Collectors
                       │
                       ▼
                  Analyzers
                       │
                       ▼
              Project Intelligence
                       │
                       ▼
                Context Builder
                       │
                       ▼
               AI Provider Manager
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
      OpenAI       Claude        Gemini
         │             │             │
         └─────────────┼─────────────┘
                       ▼
                 AI Response
                       │
                       ▼
                 Patch Generator
                       │
                       ▼
                 Patch Validator
                       │
                       ▼
                  Patch Applier
                       │
                       ▼
                 Memory Engine
                       │
                       ▼
                   API Layer
                       │
                       ▼
                 VS Code Plugin
```

---

## Layer Responsibilities

### Configuration Layer

Responsible for:

- Loading settings
- Environment variables
- Runtime configuration
- Application startup configuration

---

### Core Layer

Responsible for:

- Event Bus
- Dependency Injection
- Service Management
- Plugin Management

---

### Monitoring Layer

Responsible for:

- File monitoring
- Terminal monitoring
- Runtime diagnostics
- Traceback collection

---

### Intelligence Layer

Responsible for:

- Workspace indexing
- AST parsing
- Symbol indexing
- Dependency analysis
- Context generation

---

### AI Layer

Responsible for:

- Provider selection
- Prompt generation
- AI communication
- Response processing

---

### Patch Layer

Responsible for:

- Patch generation
- Diff creation
- Validation
- Safe application
- Rollback

---

### Memory Layer

Responsible for:

- Error history
- Project memory
- Session memory
- AI context persistence

---

### Integration Layer

Responsible for:

- REST API
- WebSocket
- VS Code Extension
- Future IDE integrations

---

## Dependency Rules

The following architectural rules must always be respected:

- Upper layers may depend on lower layers.
- Lower layers must never depend on higher layers.
- Communication between modules should use interfaces or the Event Bus.
- Circular dependencies are not allowed.
- Business logic must remain independent of IDE-specific integrations.
- AI providers must be replaceable without modifying the core engine.
- Plugins must extend the engine without changing core modules.

## Repository Standards

GEETA AI Engine follows a consistent development workflow to ensure maintainability, code quality, and long-term scalability.

Every contribution should follow the standards defined below.

---

## Branch Strategy

The repository uses the following branch structure.

| Branch | Purpose |
|---------|---------|
| `main` | Stable production releases |
| `develop` | Active development |
| `feature/*` | New features |
| `bugfix/*` | Bug fixes |
| `hotfix/*` | Emergency production fixes |
| `release/*` | Release preparation |

Example:

```text
main

develop

feature/logger

feature/database

bugfix/event-bus

release/v1.0.0
```

---

## Commit Message Convention

Use meaningful commit messages.

Examples:

```text
feat: add configuration system

feat: implement event bus

fix: resolve database connection issue

refactor: simplify service container

docs: update README

test: add logger unit tests
```

---

## Code Style

All code should follow the project's coding standards.

### Python

- Python 3.12+
- Type hints required
- Docstrings required
- Maximum line length: 100 characters
- Follow PEP 8
- Prefer composition over inheritance
- Avoid global state

---

## Naming Conventions

### Files

```text
snake_case.py
```

Examples

```text
event_bus.py

project_indexer.py

patch_generator.py
```

---

### Classes

```text
PascalCase
```

Examples

```text
EventBus

PatchGenerator

ProjectIndexer
```

---

### Functions

```text
snake_case()
```

Examples

```text
build_context()

generate_patch()

load_configuration()
```

---

### Constants

```text
UPPER_CASE
```

Example

```text
DEFAULT_PROVIDER

MAX_WORKERS
```

---

## Documentation Standards

Every public class should include:

- Description
- Constructor documentation
- Method documentation
- Parameters
- Return values
- Exceptions

---

## Testing Standards

Every module should include:

- Unit tests
- Integration tests (where applicable)
- Error handling tests
- Edge case tests

No feature is considered complete without tests.

---

## Pull Request Checklist

Before creating a Pull Request, verify:

- Code builds successfully
- Unit tests pass
- No linting errors
- Documentation updated
- New functionality tested
- No unnecessary dependencies added

---

## Code Review Checklist

During review, verify:

- Architecture compliance
- SOLID principles
- Performance impact
- Security considerations
- Error handling
- Test coverage
- Documentation quality
- Maintainability

---

## Quality Principles

Every contribution should improve at least one of the following:

- Readability
- Maintainability
- Performance
- Reliability
- Scalability
- Testability

Short-term shortcuts that reduce long-term maintainability should be avoided.

---

## Development Philosophy

Build for the next ten years, not just the next release.

Every module should be:

- Modular
- Reusable
- Testable
- Extensible
- Well documented
- Production ready

## Frequently Asked Questions (FAQ)

This section answers common questions about GEETA AI Engine.

---

### What is GEETA AI Engine?

GEETA AI Engine is an enterprise-grade AI software engineering engine designed to understand software projects, analyze code, detect errors, generate intelligent fixes, and provide a modular platform for AI-assisted development.

---

### Is GEETA AI Engine an IDE?

No.

GEETA AI Engine is the intelligence layer that powers AI-assisted development.

It is designed to integrate with IDEs such as:

- VS Code
- PyCharm
- Future desktop applications
- Command-line tools

---

### Which programming languages are supported?

### Current

- Python

### Planned

- JavaScript
- TypeScript
- Java
- C#
- C++
- Rust
- Go

---

### Which AI providers are supported?

The engine is designed to support multiple AI providers.

Examples include:

- OpenAI
- Claude
- Gemini
- DeepSeek
- Ollama
- OpenRouter

Additional providers can be added through the Provider Plugin System.

---

### Does GEETA AI Engine require an internet connection?

It depends on the selected AI provider.

Cloud providers require internet access.

Local providers such as Ollama can run completely offline.

---

### Is the project open source?

The licensing model is defined in the LICENSE file.

Refer to the License section for details.

---

### Can I develop my own plugins?

Yes.

The Plugin System is designed to allow third-party extensions without modifying the core engine.

Plugins can extend:

- IDE integrations
- AI providers
- Programming languages
- Developer tools
- Automation workflows

---

### Is Windows supported?

Yes.

The project is intended to support:

- Windows
- Linux
- macOS

---

### Where should I report bugs?

Bug reports should be submitted through the project's GitHub Issues page.

Please include:

- Operating System
- Python Version
- Error Message
- Steps to Reproduce
- Logs (if available)

---

### Where can I request new features?

Feature requests should be submitted through GitHub Discussions or GitHub Issues using the Feature Request template.

---

### Is commercial use allowed?

Please refer to the LICENSE file for licensing terms.

## Contributing

Thank you for your interest in contributing to GEETA AI Engine.

Our goal is to build a high-quality, enterprise-grade AI software engineering platform. Every contribution should improve the project's quality, maintainability, and long-term vision.

---

## Before You Start

Before contributing, please ensure that you have:

- Read the project documentation
- Reviewed the architecture documentation
- Installed the development environment
- Understood the coding standards
- Read the Repository Standards section

---

## Development Workflow

Follow this workflow for every contribution.

```text
Fork Repository
       │
       ▼
Create Feature Branch
       │
       ▼
Implement Feature
       │
       ▼
Write Tests
       │
       ▼
Update Documentation
       │
       ▼
Run All Tests
       │
       ▼
Submit Pull Request
```

---

## Creating a Feature Branch

Create a new branch from the latest `develop` branch.

Example:

```bash
git checkout develop

git pull origin develop

git checkout -b feature/logger-system
```

---

## Commit Messages

Use descriptive commit messages following conventional commits.

Examples:

```text
feat: add plugin manager

fix: resolve database initialization issue

docs: update installation guide

refactor: improve dependency injection

test: add event bus unit tests
```

---

## Coding Standards

Every contribution should follow these standards:

- Python 3.12+
- Type hints required
- Docstrings required
- Unit tests required
- Integration tests when applicable
- Follow PEP 8
- Keep functions focused and small
- Avoid duplicate code
- Prefer composition over inheritance

---

## Documentation Requirements

If you add or modify functionality, update the relevant documentation.

This may include:

- README.md
- Architecture documentation
- API documentation
- Configuration guide
- Code comments (where appropriate)

---

## Testing Requirements

Before submitting a Pull Request, verify that:

- All unit tests pass
- Integration tests pass
- No linting errors exist
- Type checking passes
- Documentation has been updated

---

## Pull Request Checklist

Before opening a Pull Request:

- [ ] Feature works as expected
- [ ] Existing functionality is not broken
- [ ] Tests have been added or updated
- [ ] Documentation has been updated
- [ ] Code follows project standards
- [ ] Commit history is clean

---

## Code Review

Every Pull Request will be reviewed for:

- Architecture compliance
- Code quality
- Readability
- Maintainability
- Performance
- Security
- Test coverage
- Documentation quality

---

## Reporting Issues

When reporting a bug, include:

- Operating System
- Python Version
- Project Version
- Steps to Reproduce
- Expected Behavior
- Actual Behavior
- Error Messages
- Relevant Logs

---

## Suggesting Features

Feature requests should include:

- Problem Statement
- Proposed Solution
- Expected Benefits
- Possible Alternatives
- Additional Context

---

## Community Guidelines

Please maintain a professional and respectful environment.

We encourage:

- Constructive feedback
- Clear communication
- Helpful discussions
- Collaborative problem solving

Respectful collaboration helps the project grow successfully.


## Acknowledgements

GEETA AI Engine is built upon the Python ecosystem and many outstanding open-source projects.

We sincerely acknowledge the developers and maintainers of the following technologies and communities.

---

## Core Technologies

- Python
- PySide6
- SQLAlchemy
- Pydantic
- Loguru
- Watchdog
- HTTPX
- WebSockets
- Alembic

---

## AI Technologies

GEETA AI Engine is designed to work with modern Large Language Models including:

- OpenAI
- Anthropic Claude
- Google Gemini
- DeepSeek
- Ollama
- OpenRouter

---

## Development Tools

- Git
- GitHub
- Ruff
- Black
- MyPy
- Pytest

---

## Inspiration

This project is inspired by modern AI-assisted software engineering practices and the broader open-source developer community.

The goal is not to replicate any existing product, but to build an extensible and modular AI engineering platform with its own architecture and capabilities.

---

## Special Thanks

Special thanks to:

- The Python Community
- Open Source Contributors
- AI Research Community
- Software Engineering Community
- Everyone who contributes ideas, bug reports, documentation, testing, and code.

---

# GEETA AI Engine

**Enterprise AI Coding & Debugging Engine**

> Understand • Analyze • Debug • Patch • Automate

---

### Current Status

🚧 Active Development

Version:

```text
v1.0.0 Alpha
```

---

### Repository

```text
GEETA_AI_ENGINE
```

---

### Documentation

Complete project documentation is available inside the `docs/` directory.

---

### Future Vision

GEETA AI Engine is being developed as a modular AI Software Engineering Platform capable of understanding software projects, assisting developers, and evolving toward autonomous software engineering.

Every release is designed to strengthen the foundation while maintaining stability, maintainability, and extensibility.

---

**Thank you for your interest in GEETA AI Engine.**
## Patch Engine Development Started