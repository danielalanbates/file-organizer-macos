# File Automation Suite

A comprehensive cross-platform file automation and system monitoring toolkit for macOS, Linux, and Windows.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)]()

---

## Overview

The File Automation Suite is a collection of Python tools designed to automate file management, system monitoring, and productivity tasks. It provides both GUI and CLI interfaces for various automation workflows.

### Key Features

- **System Monitoring**: Track CPU, disk, and memory usage with configurable alerts
- **File Organization**: Find and organize files by size, type, or custom criteria
- **macOS Integration**: AppleScript-based automation for Reminders, Calendar, and Time Machine
- **Master Control App**: Tkinter-based GUI for centralized automation management
- **Cross-Platform**: Core utilities work on macOS, Linux, and Windows

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/03-File_Automation.git
cd 03-File_Automation

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

**System Monitor**
```bash
python src/system_monitor.py
```

**File Organizer**
```bash
# Find 10 largest files in Documents
python src/file_organizer.py ~/Documents 10

# Find largest PDF files
python src/file_organizer.py ~/Documents 20 .pdf
```

**macOS Automation** (macOS only)
```bash
python mac_automation.py
```

**Master Control App** (GUI)
```bash
python copilot_master_app.py
```

---

## Project Structure

```
03-File_Automation/
├── src/                      # Core source code
│   ├── system_monitor.py     # System resource monitoring
│   ├── file_organizer.py     # File organization utilities
│   └── __init__.py
├── tests/                    # Unit tests
│   ├── test_system_monitor.py
│   └── test_file_organizer.py
├── docs/                     # Documentation
├── assets/                   # Icons, images, resources
├── mac_automation.py         # macOS-specific automation (AppleScript)
├── copilot_master_app.py     # Master control GUI application
├── time_machine_monitor.py   # Time Machine backup monitoring
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
├── LICENSE                  # MIT License
├── README.md                # This file
└── CHANGELOG.md             # Version history
```

---

## Components

### 1. System Monitor (`src/system_monitor.py`)

Monitor system resources and get alerts when thresholds are exceeded.

**Features:**
- CPU usage monitoring
- Disk space checking
- Memory usage tracking
- Configurable thresholds
- Detailed status reports

**Example:**
```python
from src.system_monitor import SystemMonitor

monitor = SystemMonitor(disk_threshold=20, cpu_threshold=75)

if not monitor.is_system_healthy():
    status = monitor.get_detailed_status()
    print(f"WARNING: CPU at {status['cpu_percent']:.1f}%")
```

### 2. File Organizer (`src/file_organizer.py`)

Find and organize files efficiently with real-time progress tracking.

**Features:**
- Find largest files using heap queue algorithm
- Filter by file extension
- Real-time progress reporting
- Directory statistics
- Human-readable size formatting

**Example:**
```python
from src.file_organizer import FileOrganizer

organizer = FileOrganizer()
largest = organizer.find_largest_files("/path/to/scan", top_n=20)

for size, path in largest:
    print(f"{organizer.format_size(size)} - {path}")
```

### 3. macOS Automation (`mac_automation.py`)

**macOS Only** - AppleScript-based automation for native macOS apps.

**Features:**
- Create Reminders with due dates
- Schedule Calendar events
- Create workout schedules
- Fitness tracking reminders
- Goal deadline management

**Example:**
```python
from mac_automation import MacAutomation

automation = MacAutomation()

# Create a reminder
automation.create_reminder(
    title="Review project",
    list_name="Work",
    due_date="2025-10-20 14:00",
    notes="Check progress and update timeline"
)

# Create calendar event
automation.create_calendar_event(
    title="Team Meeting",
    start_date="2025-10-21 10:00",
    end_date="2025-10-21 11:00",
    location="Zoom"
)
```

### 4. Time Machine Monitor (`time_machine_monitor.py`)

**macOS Only** - Monitor Time Machine backups and receive alerts.

**Features:**
- Check last backup date
- Menu bar notifications
- Configurable alert thresholds
- Auto-start via LaunchAgent
- Integration with menu bar app

**Usage:**
```bash
python time_machine_monitor.py
```

### 5. Master Control App (`copilot_master_app.py`)

Tkinter-based GUI for centralized automation control.

**Features:**
- Quick action buttons for common tasks
- Script management interface
- VS Code integration
- Code generation prompts
- Real-time status monitoring
- Background script execution

**Usage:**
```bash
python copilot_master_app.py
```

**Screenshots:**
- Quick Actions tab for one-click automation
- Code Generation with Copilot integration
- Script management and execution
- VS Code workspace integration

---

## Configuration

### Environment Variables

Create a `.env` file for custom configuration:

```bash
# System Monitor Thresholds
DISK_THRESHOLD=20        # Minimum free disk space %
CPU_THRESHOLD=75         # Maximum CPU usage %

# File Organizer
DEFAULT_SCAN_PATH=/Users/daniel/Documents
DEFAULT_TOP_N=10

# macOS Automation
COPILOT_WORKSPACE=/Users/daniel/copilot
VSCODE_PATH=/Applications/Visual Studio Code.app
```

### Platform-Specific Notes

**macOS:**
- AppleScript automation requires Accessibility permissions
- Time Machine monitoring requires Full Disk Access
- Menu bar apps use `rumps` library

**Linux:**
- Some GUI features may require additional dependencies
- AppleScript features unavailable

**Windows:**
- Paths use backslashes (`\`)
- Some macOS-specific features unavailable
- Requires Python 3.8+ with tkinter

---

## Dependencies

### Core Dependencies
- Python 3.8+
- psutil >= 5.9.0 (system monitoring)
- tkinter (built-in with Python)

### Optional Dependencies
- watchdog >= 3.0.0 (file system monitoring)
- rumps >= 0.4.0 (macOS menu bar apps)

### Development Dependencies
- pytest >= 7.4.0
- pytest-cov >= 4.1.0
- black >= 23.0.0 (code formatting)
- flake8 >= 6.0.0 (linting)
- mypy >= 1.0.0 (type checking)

Install all dependencies:
```bash
pip install -r requirements.txt
```

---

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_system_monitor.py
```

### Code Quality

```bash
# Format code with Black
black src/ tests/

# Lint with flake8
flake8 src/ tests/

# Type check with mypy
mypy src/
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Format code (`black .`)
7. Commit changes (`git commit -m 'Add amazing feature'`)
8. Push to branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

---

## Testing

The project includes comprehensive unit tests for core functionality:

- `tests/test_system_monitor.py` - System monitoring tests
- `tests/test_file_organizer.py` - File organization tests

Run tests with:
```bash
pytest -v
```

---

## Known Issues

1. **Time Machine Monitor**: Requires Full Disk Access on macOS Catalina+
2. **Menu Bar Apps**: `rumps` installation may fail on some Python versions
3. **AppleScript Permissions**: First run requires manual permission grants
4. **Virtual Environment**: Ensure correct Python version in virtual environment

See [CHANGELOG.md](CHANGELOG.md) for version-specific issues.

---

## Roadmap

### v1.1.0 (Planned)
- [ ] File system watcher for real-time monitoring
- [ ] Cloud backup integration
- [ ] Email notifications for alerts
- [ ] Web dashboard interface

### v1.2.0 (Planned)
- [ ] Android support via Termux
- [ ] iOS Shortcuts integration
- [ ] Automated photo organization
- [ ] Duplicate file detection

### v2.0.0 (Future)
- [ ] Complete cross-platform GUI
- [ ] Plugin system for extensions
- [ ] REST API for remote control
- [ ] Mobile companion apps

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License
Copyright (c) 2025 Daniel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

## Acknowledgments

- Built with Python and cross-platform libraries
- Inspired by Hazel (macOS) and File Juggler (Windows)
- Uses `psutil` for system monitoring
- GUI built with tkinter for maximum compatibility

---

## Support

### Documentation
- [Full Documentation](docs/)
- [API Reference](docs/api.md)
- [Examples](docs/examples.md)

### Issues
Report bugs or request features:
- [GitHub Issues](https://github.com/yourusername/03-File_Automation/issues)

### Changelog
See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## Author

**Daniel**
- GitHub: [@yourusername](https://github.com/yourusername)

---

## Project Status

**Current Version:** 1.0.0
**Status:** Active Development
**Last Updated:** October 2025

---

**Made with Python** 🐍 **Compatible with macOS, Linux, and Windows** 💻
