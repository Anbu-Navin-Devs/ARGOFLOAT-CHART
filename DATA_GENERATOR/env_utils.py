"""
Environment variable loading utilities for FloatChart Data Generator.
Searches for .env files in common locations relative to the project structure.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

from dotenv import load_dotenv

# Search order for .env files - covers running from different directories
DEFAULT_ENV_PATHS: Sequence[Path] = (
    Path(".env"),                    # Current directory
    Path("../.env"),                 # Parent directory (project root)
    Path("DATA_GENERATOR/.env"),     # From project root
    Path("ARGO_CHATBOT/.env"),       # Cross-reference chatbot config
)


def load_environment(paths: Iterable[Path] = DEFAULT_ENV_PATHS) -> None:
    """
    Load environment variables from .env files.
    
    Searches through the provided paths and loads the first existing .env file.
    Later files supplement but don't override already-set values.
    
    Args:
        paths: Iterable of Path objects to search for .env files
    """
    loaded_any = False
    for candidate in paths:
        if candidate.exists():
            load_dotenv(candidate, override=False)
            loaded_any = True
    
    if not loaded_any:
        # Fallback: let dotenv try to discover .env automatically
        load_dotenv()
