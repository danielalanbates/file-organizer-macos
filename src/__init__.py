"""
File Automation Suite - Core Package
=====================================

MIT License
Copyright (c) 2025 Daniel

Cross-platform file automation and system monitoring toolkit.
"""

__version__ = "1.0.0"
__author__ = "Daniel"
__license__ = "MIT"

from .system_monitor import SystemMonitor
from .file_organizer import FileOrganizer

__all__ = ['SystemMonitor', 'FileOrganizer']
