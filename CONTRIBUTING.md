# Contributing to GEETA AI Engine

First of all, thank you for your interest in contributing to **GEETA AI Engine**.

This project aims to build an enterprise-grade AI Coding & Debugging Engine through clean architecture, modular design, and high-quality engineering practices.

Every contribution, whether it is code, documentation, testing, or feedback, is appreciated.

---

# Before You Contribute

Please ensure that you have:

- Read the README.
- Understood the project architecture.
- Followed the Repository Standards.
- Set up the development environment.
- Pulled the latest changes from the repository.

---

# Development Workflow

Every contribution should follow this workflow.

```text
Fork Repository
        │
        ▼
Clone Repository
        │
        ▼
Create Feature Branch
        │
        ▼
Implement Changes
        │
        ▼
Write Tests
        │
        ▼
Update Documentation
        │
        ▼
Run Quality Checks
        │
        ▼
Commit Changes
        │
        ▼
Push Branch
        │
        ▼
Open Pull Request
```

---

# Branch Strategy

Always create a new branch before starting work.

Examples

```bash
git checkout develop

git pull origin develop

git checkout -b feature/logger-system
```

Branch naming examples

```text
feature/database

feature/event-bus

feature/plugin-manager

bugfix/logger

hotfix/database

release/v1.0.0
```

---

# Commit Message Convention

Follow Conventional Commits.

Examples

```text
feat: add database manager

feat: implement event bus

fix: resolve logger initialization

docs: update README

refactor: simplify service container

test: add unit tests for database
```

---

# Coding Standards

Every contribution must follow these standards.

## Python

- Python 3.12+
- Type hints required
- Docstrings required
- Follow PEP 8
- Maximum line length: 100
- Avoid global variables
- Keep functions focused
- Prefer composition over inheritance

---

# Code Quality

Before submitting code, ensure that:

- Code builds successfully.
- No linting errors exist.
- No type-checking errors exist.
- Unit tests pass.
- Integration tests pass (if applicable).

---

# Testing Requirements

Every new feature should include appropriate tests.

Testing includes:

- Unit Tests
- Integration Tests
- Error Handling Tests
- Edge Case Tests

Features without tests should not be considered complete.

---

# Documentation

Whenever functionality changes, update the relevant documentation.

Possible files include:

- README.md
- CHANGELOG.md
- Architecture Documents
- API Documentation
- Configuration Guide

---

# Pull Request Checklist

Before opening a Pull Request, verify the following:

- [ ] Project builds successfully
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code follows project standards
- [ ] No unnecessary dependencies added
- [ ] Commit history is clean

---

# Code Review

Every Pull Request may be reviewed for:

- Architecture
- Readability
- Maintainability
- Performance
- Security
- Test Coverage
- Documentation
- Coding Standards

Changes may be requested before merging.

---

# Reporting Bugs

When reporting an issue, include:

- Operating System
- Python Version
- Project Version
- Steps to Reproduce
- Expected Result
- Actual Result
- Error Messages
- Relevant Logs

Providing complete information helps reproduce and resolve issues more efficiently.

---

# Feature Requests

Feature requests should include:

- Problem Description
- Proposed Solution
- Expected Benefits
- Possible Alternatives
- Additional Context

---

# Code of Conduct

All contributors are expected to follow the project's Code of Conduct.

Please maintain a respectful, constructive, and collaborative environment.

---

# Questions

If you have questions regarding development or contributions, please open a GitHub Discussion or create an Issue.

---

Thank you for contributing to **GEETA AI Engine**.