"""
Helper utilities for VisuAI.

Author: Muhammad Yasir Imam
"""

import os
import hashlib
from typing import Dict, Any
from datetime import datetime


def generate_session_id() -> str:
    """Generate unique session ID."""
    timestamp = datetime.now().isoformat()
    return hashlib.md5(timestamp.encode()).hexdigest()[:8]


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    invalid_chars = '<>:"/\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def format_number(num: float, precision: int = 2) -> str:
    """Format number with appropriate precision."""
    if abs(num) >= 1e6:
        return f"{num:.2e}"
    elif abs(num) >= 1:
        return f"{num:.{precision}f}"
    else:
        return f"{num:.{precision+2}f}"


def get_file_size(path: str) -> str:
    """Get human-readable file size."""
    size = os.path.getsize(path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"
