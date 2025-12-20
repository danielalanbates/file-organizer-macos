from setuptools import setup

APP = ['sorter.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,  # For GUI apps
    'packages': ['tkinter'],  # Include tkinter
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)