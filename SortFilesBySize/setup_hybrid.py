"""
py2app setup script for File Automation Suite Hybrid App
Builds a standalone macOS application bundle

Usage:
    python setup_hybrid.py py2app
"""

from setuptools import setup

APP = ['file_automation_hybrid.py']
DATA_FILES = [
    ('src', ['src/system_monitor.py', 'src/file_organizer.py', 'src/__init__.py'])
]

OPTIONS = {
    'argv_emulation': False,  # Don't emulate command line for menu bar app
    'iconfile': 'assets/app_icon.icns',  # TODO: Create this
    'plist': {
        'CFBundleName': 'File Automation Suite',
        'CFBundleDisplayName': 'File Automation Suite',
        'CFBundleGetInfoString': 'Automate and organize your Mac files',
        'CFBundleIdentifier': 'com.daniel.fileautomationsuite',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': '© 2025 Daniel. All rights reserved.',

        # macOS version requirements
        'LSMinimumSystemVersion': '11.0',  # macOS Big Sur and later
        'NSHighResolutionCapable': True,

        # Launch behavior - MENU BAR ONLY (NO DOCK ICON!)
        'LSUIElement': True,  # ⭐ This hides the dock icon!
        'LSBackgroundOnly': False,

        # Permissions (required for full functionality)
        'NSAppleEventsUsageDescription': 'File Automation Suite needs to run AppleScript for Time Machine monitoring.',
        'NSSystemAdministrationUsageDescription': 'File Automation Suite needs to check system backup status.',

        # App category
        'LSApplicationCategoryType': 'public.app-category.utilities',
    },
    'packages': ['rumps', 'psutil', 'tkinter'],
    'includes': ['src.system_monitor', 'src.file_organizer'],
    'excludes': [],
    'resources': [],
    'optimize': 2,  # Optimize Python bytecode
}

setup(
    name='File Automation Suite',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['rumps', 'psutil'],
)
