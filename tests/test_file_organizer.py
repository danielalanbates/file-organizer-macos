"""
Unit tests for File Organizer module.

MIT License
Copyright (c) 2025 Daniel
"""

import pytest
import sys
import os
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.file_organizer import FileOrganizer


class TestFileOrganizer:
    """Test suite for FileOrganizer class."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory with test files."""
        temp_path = tempfile.mkdtemp()

        # Create test files of various sizes
        test_files = [
            ('small.txt', 100),
            ('medium.txt', 1000),
            ('large.txt', 10000),
            ('huge.pdf', 100000),
            ('video.mp4', 50000),
        ]

        for filename, size in test_files:
            filepath = os.path.join(temp_path, filename)
            with open(filepath, 'wb') as f:
                f.write(b'0' * size)

        # Create subdirectory with files
        subdir = os.path.join(temp_path, 'subdir')
        os.makedirs(subdir)

        with open(os.path.join(subdir, 'nested.txt'), 'wb') as f:
            f.write(b'0' * 5000)

        yield temp_path

        # Cleanup
        shutil.rmtree(temp_path)

    def test_initialization(self):
        """Test FileOrganizer initialization."""
        organizer = FileOrganizer()
        assert organizer.scan_count == 0
        assert organizer.error_count == 0
        assert organizer.errors == []

    def test_initialization_with_callback(self):
        """Test FileOrganizer initialization with progress callback."""
        callback_called = []

        def callback(count, path):
            callback_called.append((count, path))

        organizer = FileOrganizer(progress_callback=callback)
        assert organizer.progress_callback is not None

    def test_find_largest_files_returns_list(self, temp_dir):
        """Test that find_largest_files returns a list."""
        organizer = FileOrganizer()
        result = organizer.find_largest_files(temp_dir, top_n=5)
        assert isinstance(result, list)

    def test_find_largest_files_correct_count(self, temp_dir):
        """Test that find_largest_files returns correct number of results."""
        organizer = FileOrganizer()

        # Request 3 files
        result = organizer.find_largest_files(temp_dir, top_n=3)
        assert len(result) <= 3  # May be less if fewer files exist

        # Request 10 files (more than exist)
        result = organizer.find_largest_files(temp_dir, top_n=10)
        assert len(result) <= 10

    def test_find_largest_files_sorted_by_size(self, temp_dir):
        """Test that results are sorted by size (descending)."""
        organizer = FileOrganizer()
        result = organizer.find_largest_files(temp_dir, top_n=10)

        # Check that sizes are in descending order
        for i in range(len(result) - 1):
            assert result[i][0] >= result[i + 1][0]

    def test_find_largest_files_correct_largest(self, temp_dir):
        """Test that the largest file is correctly identified."""
        organizer = FileOrganizer()
        result = organizer.find_largest_files(temp_dir, top_n=1)

        assert len(result) == 1
        # huge.pdf (100000 bytes) should be largest
        largest_size, largest_path = result[0]
        assert largest_size == 100000
        assert 'huge.pdf' in largest_path

    def test_find_largest_files_filter_extension(self, temp_dir):
        """Test filtering by file extension."""
        organizer = FileOrganizer()

        # Find only PDF files
        result = organizer.find_largest_files(temp_dir, top_n=10, file_extension='.pdf')

        # Should only find huge.pdf
        assert len(result) == 1
        assert result[0][1].endswith('.pdf')

    def test_find_largest_files_invalid_top_n(self, temp_dir):
        """Test that invalid top_n raises ValueError."""
        organizer = FileOrganizer()

        with pytest.raises(ValueError):
            organizer.find_largest_files(temp_dir, top_n=0)

        with pytest.raises(ValueError):
            organizer.find_largest_files(temp_dir, top_n=101)

    def test_find_largest_files_invalid_path(self):
        """Test that invalid path raises FileNotFoundError."""
        organizer = FileOrganizer()

        with pytest.raises(FileNotFoundError):
            organizer.find_largest_files("/nonexistent/path")

    def test_scan_count_increments(self, temp_dir):
        """Test that scan count increments correctly."""
        organizer = FileOrganizer()
        organizer.find_largest_files(temp_dir, top_n=10)

        # Should have scanned at least some files
        assert organizer.scan_count > 0

    def test_format_size_bytes(self):
        """Test format_size for bytes."""
        organizer = FileOrganizer()
        assert organizer.format_size(512) == "512.00 B"

    def test_format_size_kilobytes(self):
        """Test format_size for kilobytes."""
        organizer = FileOrganizer()
        assert organizer.format_size(1024) == "1.00 KB"

    def test_format_size_megabytes(self):
        """Test format_size for megabytes."""
        organizer = FileOrganizer()
        assert organizer.format_size(1048576) == "1.00 MB"

    def test_format_size_gigabytes(self):
        """Test format_size for gigabytes."""
        organizer = FileOrganizer()
        assert organizer.format_size(1073741824) == "1.00 GB"

    def test_get_directory_stats_returns_dict(self, temp_dir):
        """Test that get_directory_stats returns a dictionary."""
        organizer = FileOrganizer()
        stats = organizer.get_directory_stats(temp_dir)
        assert isinstance(stats, dict)

    def test_get_directory_stats_has_required_keys(self, temp_dir):
        """Test that directory stats has required keys."""
        organizer = FileOrganizer()
        stats = organizer.get_directory_stats(temp_dir)

        required_keys = ['total_size', 'file_count', 'directory_count', 'average_file_size']
        for key in required_keys:
            assert key in stats

    def test_get_directory_stats_correct_values(self, temp_dir):
        """Test that directory stats are correct."""
        organizer = FileOrganizer()
        stats = organizer.get_directory_stats(temp_dir)

        # We created 6 files (5 in root, 1 in subdir)
        assert stats['file_count'] == 6

        # We created 1 subdirectory
        assert stats['directory_count'] == 1

        # Total size should be sum of all files
        expected_size = 100 + 1000 + 10000 + 100000 + 50000 + 5000
        assert stats['total_size'] == expected_size

        # Average should be total / count
        assert stats['average_file_size'] == expected_size / 6

    def test_print_results_no_exception(self, temp_dir):
        """Test that print_results doesn't raise exceptions."""
        organizer = FileOrganizer()
        results = organizer.find_largest_files(temp_dir, top_n=5)

        # Should not raise any exception
        organizer.print_results(results)
        assert True

    def test_print_results_empty_list(self):
        """Test print_results with empty list."""
        organizer = FileOrganizer()
        # Should not raise any exception
        organizer.print_results([])
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
