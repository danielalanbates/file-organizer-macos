#!/usr/bin/env python3
"""
File Organizer - Smart File Organization by Size
=================================================

MIT License
Copyright (c) 2025 Daniel

Scan directories and organize files by size with real-time progress tracking.
Cross-platform compatible (macOS, Linux, Windows).

Features:
    - Find largest files efficiently using heap queue
    - Real-time progress reporting
    - Configurable result limits
    - Error handling for inaccessible files

Dependencies:
    - Standard library only

Example:
    >>> from file_organizer import FileOrganizer
    >>> organizer = FileOrganizer()
    >>> largest = organizer.find_largest_files("/Users/daniel/Documents", top_n=10)
    >>> for size, path in largest:
    ...     print(f"{size / (1024**3):.2f} GB - {path}")
"""

import os
import heapq
from typing import List, Tuple, Optional
from pathlib import Path


class FileOrganizer:
    """Organize and analyze files by size and other criteria."""

    def __init__(self, progress_callback: Optional[callable] = None):
        """
        Initialize the file organizer.

        Args:
            progress_callback: Optional function to call with progress updates
                               Signature: callback(current_count: int, current_path: str)
        """
        self.progress_callback = progress_callback
        self.scan_count = 0
        self.error_count = 0
        self.errors = []

    def find_largest_files(
        self,
        start_path: str,
        top_n: int = 10,
        file_extension: Optional[str] = None
    ) -> List[Tuple[int, str]]:
        """
        Find the largest files in a directory tree.

        Args:
            start_path: Root directory to start scanning
            top_n: Number of largest files to return (1-100)
            file_extension: Optional filter by extension (e.g., '.pdf', '.mp4')

        Returns:
            List of (file_size, file_path) tuples, sorted by size descending

        Raises:
            ValueError: If top_n is not between 1 and 100
            FileNotFoundError: If start_path doesn't exist

        Example:
            >>> organizer = FileOrganizer()
            >>> largest = organizer.find_largest_files("/Users/daniel/Documents", top_n=5)
            >>> for size, path in largest:
            ...     print(f"{size / (1024**2):.2f} MB - {path}")
        """
        # Validate inputs
        if not 1 <= top_n <= 100:
            raise ValueError("top_n must be between 1 and 100")

        if not os.path.exists(start_path):
            raise FileNotFoundError(f"Path does not exist: {start_path}")

        # Reset counters
        self.scan_count = 0
        self.error_count = 0
        self.errors = []

        file_sizes = []
        start_path_obj = Path(start_path)

        print(f"\n🔍 Scanning: {start_path}")
        print(f"   Filter: {file_extension if file_extension else 'All files'}")
        print(f"   Finding top {top_n} largest files...\n")

        # Walk the directory tree
        for dirpath, dirnames, filenames in os.walk(start_path):
            # Filter hidden directories for performance
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]

            for filename in filenames:
                # Skip hidden files
                if filename.startswith('.'):
                    continue

                # Apply extension filter if specified
                if file_extension and not filename.endswith(file_extension):
                    continue

                filepath = os.path.join(dirpath, filename)

                try:
                    file_size = os.path.getsize(filepath)
                    file_sizes.append((file_size, filepath))
                    self.scan_count += 1

                    # Report progress every 100 files
                    if self.scan_count % 100 == 0:
                        progress_msg = f"📂 Scanned {self.scan_count:,} files... {dirpath}"
                        print(f"\r{progress_msg[:80]}", end="", flush=True)

                        if self.progress_callback:
                            self.progress_callback(self.scan_count, dirpath)

                except (OSError, FileNotFoundError, PermissionError) as e:
                    self.error_count += 1
                    self.errors.append((filepath, str(e)))
                    continue

        # Clear progress line
        print(f"\r{' ' * 80}\r", end="")

        # Get the top N largest files
        largest_files = heapq.nlargest(top_n, file_sizes, key=lambda x: x[0])

        # Print summary
        print(f"✅ Scan complete!")
        print(f"   Files scanned: {self.scan_count:,}")
        print(f"   Errors: {self.error_count:,}")
        print(f"   Largest files found: {len(largest_files)}\n")

        return largest_files

    def format_size(self, size_bytes: int) -> str:
        """
        Format file size in human-readable format.

        Args:
            size_bytes: Size in bytes

        Returns:
            Formatted string (e.g., "1.23 GB", "456.78 MB")

        Example:
            >>> organizer = FileOrganizer()
            >>> organizer.format_size(1234567890)
            '1.15 GB'
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    def print_results(self, results: List[Tuple[int, str]]) -> None:
        """
        Print formatted results.

        Args:
            results: List of (size, path) tuples

        Example:
            >>> organizer = FileOrganizer()
            >>> results = organizer.find_largest_files("/path", top_n=5)
            >>> organizer.print_results(results)
        """
        if not results:
            print("No files found.")
            return

        print("📊 Largest Files:")
        print("=" * 80)

        for idx, (size, path) in enumerate(results, 1):
            formatted_size = self.format_size(size)
            # Shorten path if too long
            display_path = path
            if len(path) > 60:
                display_path = "..." + path[-57:]

            print(f"{idx:2d}. {formatted_size:>12} - {display_path}")

        if self.errors:
            print(f"\n⚠️  {self.error_count} files could not be accessed")

    def get_directory_stats(self, path: str) -> dict:
        """
        Get statistics about a directory.

        Args:
            path: Directory path to analyze

        Returns:
            Dictionary with statistics

        Example:
            >>> organizer = FileOrganizer()
            >>> stats = organizer.get_directory_stats("/Users/daniel/Documents")
            >>> print(f"Total size: {organizer.format_size(stats['total_size'])}")
        """
        total_size = 0
        file_count = 0
        dir_count = 0

        for dirpath, dirnames, filenames in os.walk(path):
            dir_count += len(dirnames)
            for filename in filenames:
                file_count += 1
                try:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
                except (OSError, FileNotFoundError):
                    continue

        return {
            "total_size": total_size,
            "file_count": file_count,
            "directory_count": dir_count,
            "average_file_size": total_size / file_count if file_count > 0 else 0
        }


def main():
    """Command-line interface for file organization."""
    import sys

    print("=" * 80)
    print("File Organizer - Find Largest Files")
    print("=" * 80)

    # Get path from arguments or use home directory
    if len(sys.argv) > 1:
        search_path = sys.argv[1]
    else:
        search_path = os.path.expanduser("~/Documents")

    # Get top_n from arguments
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    organizer = FileOrganizer()

    try:
        results = organizer.find_largest_files(search_path, top_n=top_n)
        organizer.print_results(results)

        # Show directory stats
        print("\n" + "=" * 80)
        stats = organizer.get_directory_stats(search_path)
        print(f"\n📁 Directory Statistics:")
        print(f"   Total size: {organizer.format_size(stats['total_size'])}")
        print(f"   Files: {stats['file_count']:,}")
        print(f"   Directories: {stats['directory_count']:,}")
        print(f"   Average file size: {organizer.format_size(stats['average_file_size'])}")

    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
