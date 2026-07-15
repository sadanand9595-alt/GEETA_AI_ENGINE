"""
==============================================================================
GEETA AI ENGINE

File        : test_diff_engine.py
Package     : tests
Description : Unit tests for Diff Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from src.integrations.diff_engine import (
    DiffEngine,
    DiffRequest,
)

def test_generate_diff() -> None:
    """
    Diff generation should succeed.
    """

    engine = DiffEngine()

    request = DiffRequest(
        file_path="example.py",
        original="print('Hello')\n",
        modified="print('Hello World')\n",
    )

    result = engine.generate(
        request,
    )

    assert result.success is True
    assert result.diff
    ###############################################################################
# Empty Diff
###############################################################################


def test_empty_diff() -> None:
    """
    Identical files should produce an empty diff.
    """

    engine = DiffEngine()

    request = DiffRequest(
        file_path="example.py",
        original="print('Hello')\n",
        modified="print('Hello')\n",
    )

    result = engine.generate(
        request,
    )

    assert result.success is True
    assert result.diff == ""

###############################################################################
# Three-Way Merge
###############################################################################


def test_three_way_merge() -> None:
    """
    Three-way merge should resolve simple changes.
    """

    engine = DiffEngine()

    merged = engine.three_way_merge(
        base="A",
        local="B",
        remote="B",
    )

    assert merged == "B"

###############################################################################
# Git Patch
###############################################################################


def test_git_patch() -> None:
    """
    Git patch generation should include file paths.
    """

    engine = DiffEngine()

    request = DiffRequest(
        file_path="example.py",
        original="A\n",
        modified="B\n",
    )

    patch = engine.git_patch(
        request,
    )

    assert "a/example.py" in patch
    assert "b/example.py" in patch
    ###############################################################################
# Statistics
###############################################################################


def test_statistics() -> None:
    """
    Statistics should be returned as a dictionary.
    """

    engine = DiffEngine()

    stats = engine.statistics()

    assert isinstance(
        stats,
        dict,
    )

###############################################################################
# History
###############################################################################


def test_history() -> None:
    """
    History should contain generated diffs.
    """

    engine = DiffEngine()

    request = DiffRequest(
        file_path="example.py",
        original="A\n",
        modified="B\n",
    )

    engine.generate(
        request,
    )

    history = engine.history()

    assert len(history) == 1

###############################################################################
# Clear History
###############################################################################


def test_clear_history() -> None:
    """
    History should be cleared.
    """

    engine = DiffEngine()

    request = DiffRequest(
        file_path="example.py",
        original="A\n",
        modified="B\n",
    )

    engine.generate(
        request,
    )

    engine.clear_history()

    assert engine.history() == []

###############################################################################
# Review Notes
###############################################################################


def test_review_notes() -> None:
    """
    Review notes should return a list.
    """

    engine = DiffEngine()

    request = DiffRequest(
        file_path="example.py",
        original="A\n",
        modified="B\n",
    )

    result = engine.generate(
        request,
    )

    notes = engine.review_notes(
        result,
    )

    assert isinstance(
        notes,
        list,
    )

###############################################################################
# Metadata
###############################################################################


def test_metadata() -> None:
    """
    Metadata should include required fields.
    """

    engine = DiffEngine()

    request = DiffRequest(
        file_path="example.py",
        original="A\n",
        modified="B\n",
    )

    result = engine.generate(
        request,
    )

    metadata = engine.metadata(
        request,
        result,
    )

    assert metadata["file"] == "example.py"

    assert "generated" in metadata

    assert "risk" in metadata