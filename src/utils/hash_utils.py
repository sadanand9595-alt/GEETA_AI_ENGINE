"""
==============================================================================
GEETA AI Engine

File        : hash_utils.py
Package     : utils
Description : Hash Utility Functions

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Internal Helper
###############################################################################


def _calculate_hash(
    algorithm: str,
    data: bytes,
) -> str:
    """
    Calculate hash using the specified algorithm.
    """

    hasher = hashlib.new(algorithm)

    hasher.update(data)

    return hasher.hexdigest()


###############################################################################
# String Hashes
###############################################################################


def md5(text: str) -> str:
    """
    Return MD5 hash.
    """

    return _calculate_hash(
        "md5",
        text.encode("utf-8"),
    )


def sha1(text: str) -> str:
    """
    Return SHA1 hash.
    """

    return _calculate_hash(
        "sha1",
        text.encode("utf-8"),
    )


def sha256(text: str) -> str:
    """
    Return SHA256 hash.
    """

    return _calculate_hash(
        "sha256",
        text.encode("utf-8"),
    )


def sha512(text: str) -> str:
    """
    Return SHA512 hash.
    """

    return _calculate_hash(
        "sha512",
        text.encode("utf-8"),
    )


###############################################################################
# File Hashes
###############################################################################


def file_sha256(
    path: Path,
    chunk_size: int = 8192,
) -> str:
    """
    Calculate SHA256 hash of a file.
    """

    logger.debug(
        "Calculating SHA256: %s",
        path,
    )

    digest = hashlib.sha256()

    with path.open("rb") as file:

        while chunk := file.read(chunk_size):

            digest.update(chunk)

    return digest.hexdigest()


def file_md5(
    path: Path,
    chunk_size: int = 8192,
) -> str:
    """
    Calculate MD5 hash of a file.
    """

    logger.debug(
        "Calculating MD5: %s",
        path,
    )

    digest = hashlib.md5()

    with path.open("rb") as file:

        while chunk := file.read(chunk_size):

            digest.update(chunk)

    return digest.hexdigest()
###############################################################################
# Additional File Hashes
###############################################################################


def file_sha1(
    path: Path,
    chunk_size: int = 8192,
) -> str:
    """
    Calculate SHA1 hash of a file.
    """

    logger.debug(
        "Calculating SHA1: %s",
        path,
    )

    digest = hashlib.sha1()

    with path.open("rb") as file:

        while chunk := file.read(chunk_size):

            digest.update(chunk)

    return digest.hexdigest()


def file_sha512(
    path: Path,
    chunk_size: int = 8192,
) -> str:
    """
    Calculate SHA512 hash of a file.
    """

    logger.debug(
        "Calculating SHA512: %s",
        path,
    )

    digest = hashlib.sha512()

    with path.open("rb") as file:

        while chunk := file.read(chunk_size):

            digest.update(chunk)

    return digest.hexdigest()


###############################################################################
# Verification
###############################################################################


def verify_hash(
    text: str,
    expected_hash: str,
    algorithm: str = "sha256",
) -> bool:
    """
    Verify text against an expected hash.

    Args:
        text:
            Source text.

        expected_hash:
            Expected hexadecimal hash.

        algorithm:
            Hash algorithm.

    Returns:
        True if hashes match.
    """

    actual_hash = _calculate_hash(
        algorithm,
        text.encode("utf-8"),
    )

    return actual_hash.lower() == expected_hash.lower()


def verify_file_hash(
    path: Path,
    expected_hash: str,
    algorithm: str = "sha256",
) -> bool:
    """
    Verify file hash.

    Args:
        path:
            File path.

        expected_hash:
            Expected hexadecimal hash.

        algorithm:
            Hash algorithm.

    Returns:
        True if hashes match.
    """

    if algorithm == "md5":
        actual = file_md5(path)

    elif algorithm == "sha1":
        actual = file_sha1(path)

    elif algorithm == "sha512":
        actual = file_sha512(path)

    else:
        actual = file_sha256(path)

    return actual.lower() == expected_hash.lower()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "md5",
    "sha1",
    "sha256",
    "sha512",
    "file_md5",
    "file_sha1",
    "file_sha256",
    "file_sha512",
    "verify_hash",
    "verify_file_hash",
]