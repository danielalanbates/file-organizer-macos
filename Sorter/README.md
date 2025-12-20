# File Sorter

This script sorts coding files in the current directory into subfolders based on project type, inferred from file extensions.

## macOS App

A macOS app has been built using PyInstaller. You can find it in the `dist/` folder as `sorter.app`. Double-click to run it. It provides a GUI to select a directory and sort its files.

## Usage (Script)

1. Place your coding files in this directory.
2. Run the script using: `python sorter.py`
3. Files will be moved into folders like `python/`, `javascript/`, `web/`, `docs/`, etc., based on their extensions.

## Project Types

- **python**: .py
- **javascript**: .js, .jsx
- **typescript**: .ts, .tsx
- **java**: .java
- **cpp**: .cpp
- **c**: .c
- **csharp**: .cs
- **php**: .php
- **ruby**: .rb
- **go**: .go
- **rust**: .rs
- **web**: .html, .htm, .css, .scss, .sass, .less
- **config**: .json, .xml, .yaml, .yml
- **docs**: .md, .txt
- **scripts**: .sh, .bat, .ps1
- **other**: Unknown extensions
- **no_extension**: Files without extensions

## Notes

- The script excludes itself from being sorted.
- Existing folders are not moved or sorted.
- You can add more extensions to the `PROJECT_TYPES` dictionary in the script.

## Requirements

- Python 3.x
- Run in a directory containing the files you want to sort.