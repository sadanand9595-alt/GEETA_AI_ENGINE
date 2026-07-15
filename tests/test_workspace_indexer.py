"""Tests for incremental workspace indexing orchestration."""

from __future__ import annotations

from pathlib import Path

from workspace.workspace_indexer import WorkspaceIndexer


class _Project:
    def __init__(self) -> None:
        self.builds = 0
        self.refreshes = 0

    def build(self) -> None:
        self.builds += 1

    def refresh(self) -> None:
        self.refreshes += 1


class _Index:
    def __init__(self) -> None:
        self.builds = 0
        self.reindexed: list[Path] = []
        self.removed: list[Path] = []

    def build(self) -> None:
        self.builds += 1

    def reindex_file(self, path: Path) -> None:
        self.reindexed.append(path)

    def remove_file(self, path: Path) -> None:
        self.removed.append(path)


class _Dependencies:
    def __init__(self) -> None:
        self.builds = 0

    def build(self) -> None:
        self.builds += 1


def test_full_and_incremental_indexing_persist_manifest(tmp_path: Path) -> None:
    source = tmp_path / "module.py"
    source.write_text("def first():\n    return 1\n", encoding="utf-8")
    project = _Project()
    symbols = _Index()
    semantic = _Index()
    dependencies = _Dependencies()
    indexer = WorkspaceIndexer(workspace=tmp_path, project=project, symbols=symbols, semantic=semantic, dependencies=dependencies)

    report = indexer.full_index()

    assert report.full
    assert report.indexed == 1
    assert project.builds == symbols.builds == semantic.builds == dependencies.builds == 1
    assert (tmp_path / ".geeta" / "workspace-index.json").is_file()

    source.write_text("def second():\n    return 2\n", encoding="utf-8")
    report = indexer.incremental_index()

    assert report.indexed == 1
    assert symbols.reindexed == [source]
    assert semantic.reindexed == [source]
    assert project.refreshes == 1


def test_deleted_source_removes_incremental_entries(tmp_path: Path) -> None:
    source = tmp_path / "module.py"
    source.write_text("value = 1\n", encoding="utf-8")
    project = _Project()
    symbols = _Index()
    semantic = _Index()
    indexer = WorkspaceIndexer(workspace=tmp_path, project=project, symbols=symbols, semantic=semantic, dependencies=_Dependencies())
    indexer.full_index()

    source.unlink()
    report = indexer.incremental_index()

    assert report.deleted == 1
    assert symbols.removed == [source]
    assert semantic.removed == [source]
