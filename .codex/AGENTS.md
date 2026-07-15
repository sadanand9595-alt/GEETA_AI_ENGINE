# GEETA AI ENGINE v3.0 — Engineering Handbook

This document is the permanent engineering guide for Codex sessions working in
this repository. Apply these rules to every investigation, implementation,
review, and maintenance task.

## 1. Project Overview

GEETA AI ENGINE v3.0 is a Python and PySide6 desktop software-engineering
platform. Its goal is to provide an IDE-style experience with project-aware AI
assistance for coding, debugging, code review, refactoring, test generation,
patching, runtime analysis, and integrations.

The repository contains a desktop UI at the root and a broader engine under
`src/`. Treat the actively imported execution path as the source of truth for
runtime behavior; do not assume that a similarly named module elsewhere is
wired into the application.

## 2. Enterprise Architecture

Use separation of concerns and dependency direction:

- UI components render state and forward user intent; they do not own provider,
  filesystem orchestration, or business-policy logic.
- Editor, workspace, AI, provider, patch, runtime, Git, memory, and plugin
  concerns remain in their respective modules.
- Prefer explicit interfaces, constructor injection, events, and signals over
  hidden global coupling.
- Keep I/O at system boundaries and keep business logic independently testable.
- Preserve extension points for event-driven, plugin-based, and multi-provider
  behavior.

## 3. Folder Structure

- `src/`: long-term engine modules, including editor, AI, agents, workspace,
  providers, runtime, integrations, plugins, memory, and core infrastructure.
- `ui/`: current desktop UI composition and widgets used by the root launcher.
- `core/`, `config/`, `services/`, `providers/`, `database/`: root-level
  runtime infrastructure where actively used.
- `tests/`: automated tests.
- `docs/`: project documentation.
- `assets/`: visual and static assets.
- `.codex/`: repository-specific Codex guidance.

Do not move, duplicate, or consolidate modules merely because names overlap.
First establish the active import and entry-point path.

## 4. File Numbering Rules

When a task assigns a file number, treat it as immutable project tracking
metadata: create or update exactly the requested file and retain the number in
task documentation or file headers when the surrounding convention uses one.
Do not renumber existing files, infer missing numbers, or introduce a new
numbering scheme without an explicit request.

## 5. Coding Standards

Target Python 3.12 or newer. Follow the repository configuration: Black and
Ruff use a 100-character line length, and MyPy is strict. Prefer small,
cohesive classes and functions, clear domain names, immutable inputs where
practical, and public APIs with docstrings.

## 6. SOLID Principles

- **Single responsibility:** each class and module has one primary reason to
  change.
- **Open/closed:** extend behavior through interfaces, composition, plugins, or
  signals instead of destabilizing established code.
- **Liskov substitution:** subclasses and provider implementations preserve the
  contracts expected by callers.
- **Interface segregation:** expose focused APIs rather than broad service
  objects.
- **Dependency inversion:** depend on abstractions and inject concrete
  implementations at composition boundaries.

## 7. Clean Code Rules

Use descriptive names, shallow control flow, early returns, and narrowly scoped
private helpers. Remove duplication by extracting real shared behavior, not by
creating abstraction for a single use. Avoid dead code, commented-out code,
unexplained magic values, and unnecessary wrappers around framework methods.

## 8. Type Hint Rules

Type every function parameter, return value, public attribute, and collection
element. Use modern built-in generics such as `list[str]` and union syntax such
as `Path | None`. Prefer precise domain types, `Protocol`, dataclasses, and
enums over `Any`; use `Any` only at genuine dynamic or external boundaries and
contain it there.

## 9. Logging Standards

Use the project logger via `config.logger.get_logger(__name__)` in `src/`
modules and the established logger pattern in the active runtime layer. Log
meaningful lifecycle events at `INFO`, recoverable abnormal conditions at
`WARNING`, and failures with enough context to diagnose them. Use lazy logging
parameters, never log API keys or sensitive source content, and use
`logger.exception(...)` inside exception handlers when a traceback is useful.

## 10. Error Handling Standards

Catch only exceptions that the current layer can handle. Preserve user data on
failed file operations, return explicit success/failure results where that is
the established API, and give UI callers a usable failure path. Do not suppress
exceptions silently, catch broad `Exception` without a justified boundary, or
replace failures with fabricated success.

## 11. Import Rules

Use absolute project imports consistent with nearby active modules. Keep imports
at module scope except when deferred imports solve a documented cycle or
optional-dependency requirement. Avoid wildcard imports and unused imports.
Before adding a dependency, check `pyproject.toml` and `requirements.txt` and
avoid introducing redundant packages.

## 12. UI Standards

Build predictable, keyboard-friendly UI with clear labels, sensible defaults,
and consistent state feedback. Keep business and AI logic out of widgets;
widgets should delegate to services or emit signals. Preserve unsaved work,
handle file and process failures visibly, and keep user-facing operations
responsive.

## 13. PySide6 Standards

Use PySide6 types, signals, slots, and object ownership correctly. Give widgets
an appropriate parent where practical, avoid blocking the GUI thread, and use
`QProcess`, workers, signals, or async integration for long-running work.
Prefer Qt's built-in editor behavior before reimplementing it. Make widget APIs
extensible for diagnostics, syntax highlighting, minimaps, AI completion, and
LSP clients without hard-coding those integrations.

## 14. Performance Rules

Avoid blocking I/O, expensive indexing, provider calls, and subprocess work on
the UI thread. Process only necessary files, debounce file-system events, cache
derived data with invalidation, and stream or batch large outputs. Measure before
optimizing, but never introduce obvious O(n²) behavior in editor, indexing, or
workspace hot paths.

## 15. AI Integration Rules

Route model access through provider abstractions and configured providers. Build
bounded, relevant context; preserve user control over prompts and patch
application; and report provider failures safely. Never expose credentials in
logs, UI, patches, tests, or committed files. AI-generated edits must be
reviewable through diffs and validation before being applied.

## 16. LSP Ready Rules

Keep editor state, document paths, versioning, diagnostics, selections, and
workspace edits separable from rendering. Use signals or focused interfaces for
completion, hover, definitions, references, formatting, and diagnostics.
Do not couple editor widgets directly to a single language server or language.

## 17. Future Extension Rules

Design new features for composition. Prefer registries, providers, plugins,
events, and explicit capabilities over switch statements that require central
edits for every extension. Maintain backwards-compatible public APIs where
possible and deprecate deliberately when compatibility must change.

## 18. Testing Requirements

Add or update focused tests for behavior changes when the repository's test
structure supports them. Cover success paths, failure paths, and state changes.
For UI code, isolate non-visual behavior and avoid requiring a live display when
possible. Run relevant checks without creating unrelated artifacts; report any
tests that cannot be run and the reason.

## 19. Documentation Rules

Document public modules, classes, and non-obvious decisions. Keep README and
architecture documentation aligned with behavior when a task changes public
capabilities. Explain limitations accurately; do not describe planned features
as working features.

## 20. Git Commit Rules

Keep commits focused and atomic. Use concise imperative commit subjects, such
as `Add VS Code-style editor widget`. Do not mix formatting, refactors, feature
work, and unrelated cleanup in one commit. Never alter unrelated user changes,
rewrite history, or commit secrets.

## 21. Never Break Existing Functionality

Before changing code, identify callers, imports, entry points, and expected
contracts. Preserve compatible behavior unless the task explicitly authorizes a
breaking change. Make the smallest integration change required and verify it.

## 22. Never Use Placeholder Code

Do not add `pass`, ellipses, fake return values, empty handlers, TODO-only
methods, mock production paths, or controls with no meaningful behavior. If a
feature cannot be completed safely, state the limitation and leave the existing
system intact rather than introducing a hollow implementation.

## 23. Always Inspect Existing Project Before Modifying Files

Inspect the relevant files, imports, package configuration, and nearby patterns
before editing. Determine whether an existing component or abstraction should be
extended instead of recreated. Report material architecture findings that affect
the implementation.

## 24. Keep Project Runnable After Every Change

Maintain valid imports, syntax, configuration, and entry points after each
change. Run proportionate non-destructive validation where possible. Do not make
partial migrations or leave broken references for a future task.

## 25. Explain Every Implementation After Finishing

At completion, state what changed, how it integrates with the project, and what
validation was performed. Mention limitations, skipped checks, or follow-up work
plainly when relevant.
