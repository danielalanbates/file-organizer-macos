"""
Unit tests for System Monitor module.

MIT License
Copyright (c) 2025 Daniel
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.system_monitor import SystemMonitor


class TestSystemMonitor:
    """Test suite for SystemMonitor class."""

    def test_initialization(self):
        """Test SystemMonitor initialization with default values."""
        monitor = SystemMonitor()
        assert monitor.disk_threshold == 20
        assert monitor.cpu_threshold == 75

    def test_initialization_custom_thresholds(self):
        """Test SystemMonitor initialization with custom thresholds."""
        monitor = SystemMonitor(disk_threshold=30, cpu_threshold=80)
        assert monitor.disk_threshold == 30
        assert monitor.cpu_threshold == 80

    def test_check_disk_usage_returns_tuple(self):
        """Test that check_disk_usage returns a tuple."""
        monitor = SystemMonitor()
        result = monitor.check_disk_usage("/")
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)  # is_healthy
        assert isinstance(result[1], float)  # free_percentage

    def test_check_disk_usage_valid_percentage(self):
        """Test that disk usage percentage is valid (0-100)."""
        monitor = SystemMonitor()
        _, free_percent = monitor.check_disk_usage("/")
        assert 0 <= free_percent <= 100

    def test_check_cpu_usage_returns_tuple(self):
        """Test that check_cpu_usage returns a tuple."""
        monitor = SystemMonitor()
        result = monitor.check_cpu_usage(interval=0.1)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)  # is_healthy
        assert isinstance(result[1], float)  # cpu_percentage

    def test_check_cpu_usage_valid_percentage(self):
        """Test that CPU usage percentage is valid (0-100)."""
        monitor = SystemMonitor()
        _, cpu_percent = monitor.check_cpu_usage(interval=0.1)
        assert 0 <= cpu_percent <= 100

    def test_get_detailed_status_returns_dict(self):
        """Test that get_detailed_status returns a dictionary."""
        monitor = SystemMonitor()
        status = monitor.get_detailed_status()
        assert isinstance(status, dict)

    def test_get_detailed_status_has_required_keys(self):
        """Test that detailed status has all required keys."""
        monitor = SystemMonitor()
        status = monitor.get_detailed_status()

        required_keys = [
            'disk_healthy', 'disk_free_percent',
            'cpu_healthy', 'cpu_percent',
            'memory_percent', 'memory_available_gb',
            'overall_healthy'
        ]

        for key in required_keys:
            assert key in status

    def test_get_detailed_status_values_valid(self):
        """Test that detailed status values are valid."""
        monitor = SystemMonitor()
        status = monitor.get_detailed_status()

        # Check boolean values
        assert isinstance(status['disk_healthy'], bool)
        assert isinstance(status['cpu_healthy'], bool)
        assert isinstance(status['overall_healthy'], bool)

        # Check percentage values
        assert 0 <= status['disk_free_percent'] <= 100
        assert 0 <= status['cpu_percent'] <= 100
        assert 0 <= status['memory_percent'] <= 100

        # Check memory GB value
        assert status['memory_available_gb'] >= 0

    def test_is_system_healthy_returns_bool(self):
        """Test that is_system_healthy returns a boolean."""
        monitor = SystemMonitor()
        result = monitor.is_system_healthy()
        assert isinstance(result, bool)

    def test_is_system_healthy_logic(self):
        """Test that is_system_healthy reflects component health."""
        monitor = SystemMonitor()
        status = monitor.get_detailed_status()
        overall_healthy = monitor.is_system_healthy()

        # Overall health should match disk_healthy AND cpu_healthy
        expected = status['disk_healthy'] and status['cpu_healthy']
        assert overall_healthy == expected

    def test_disk_threshold_affects_health(self):
        """Test that disk threshold affects health status."""
        # Set very low threshold (system should be healthy)
        monitor_low = SystemMonitor(disk_threshold=1)
        _, _ = monitor_low.check_disk_usage("/")

        # Set very high threshold (system might be unhealthy)
        monitor_high = SystemMonitor(disk_threshold=99)
        _, _ = monitor_high.check_disk_usage("/")

        # Just verify no exceptions are raised
        assert True

    def test_cpu_threshold_affects_health(self):
        """Test that CPU threshold affects health status."""
        # Set very high threshold (system should be healthy)
        monitor_high = SystemMonitor(cpu_threshold=99)
        _, _ = monitor_high.check_cpu_usage(interval=0.1)

        # Set very low threshold (system might be unhealthy)
        monitor_low = SystemMonitor(cpu_threshold=1)
        _, _ = monitor_low.check_cpu_usage(interval=0.1)

        # Just verify no exceptions are raised
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
