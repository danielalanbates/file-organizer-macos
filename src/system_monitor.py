#!/usr/bin/env python3
"""
System Monitor - CPU and Disk Usage Monitor
=============================================

MIT License
Copyright (c) 2025 Daniel

Monitor system resources (CPU, disk usage) and alert on threshold violations.
Cross-platform compatible (macOS, Linux, Windows).

Dependencies:
    - psutil: For system monitoring

Example:
    >>> from system_monitor import SystemMonitor
    >>> monitor = SystemMonitor()
    >>> if monitor.is_system_healthy():
    ...     print("System is healthy")
"""

import shutil
import psutil
from typing import Dict, Tuple


class SystemMonitor:
    """Monitor system resources and provide health status."""

    def __init__(self, disk_threshold: int = 20, cpu_threshold: int = 75):
        """
        Initialize the system monitor with configurable thresholds.

        Args:
            disk_threshold: Minimum free disk space percentage (default: 20%)
            cpu_threshold: Maximum CPU usage percentage (default: 75%)
        """
        self.disk_threshold = disk_threshold
        self.cpu_threshold = cpu_threshold

    def check_disk_usage(self, path: str = "/") -> Tuple[bool, float]:
        """
        Check if disk has sufficient free space.

        Args:
            path: Path to check (default: root "/" on Unix, "C:" on Windows)

        Returns:
            Tuple of (is_healthy, free_percentage)

        Example:
            >>> monitor = SystemMonitor()
            >>> is_healthy, free_pct = monitor.check_disk_usage()
            >>> print(f"Disk free: {free_pct:.1f}%")
        """
        du = shutil.disk_usage(path)
        free_percent = (du.free / du.total) * 100
        return free_percent > self.disk_threshold, free_percent

    def check_cpu_usage(self, interval: float = 1.0) -> Tuple[bool, float]:
        """
        Check if CPU usage is below threshold.

        Args:
            interval: Measurement interval in seconds (default: 1.0)

        Returns:
            Tuple of (is_healthy, cpu_percentage)

        Example:
            >>> monitor = SystemMonitor()
            >>> is_healthy, cpu_pct = monitor.check_cpu_usage()
            >>> print(f"CPU usage: {cpu_pct:.1f}%")
        """
        cpu_percent = psutil.cpu_percent(interval)
        return cpu_percent < self.cpu_threshold, cpu_percent

    def get_detailed_status(self, disk_path: str = "/") -> Dict[str, any]:
        """
        Get detailed system status information.

        Args:
            disk_path: Path to check disk usage (default: "/")

        Returns:
            Dictionary containing detailed system metrics

        Example:
            >>> monitor = SystemMonitor()
            >>> status = monitor.get_detailed_status()
            >>> print(f"Memory used: {status['memory_percent']:.1f}%")
        """
        disk_healthy, disk_free = self.check_disk_usage(disk_path)
        cpu_healthy, cpu_usage = self.check_cpu_usage()

        memory = psutil.virtual_memory()

        return {
            "disk_healthy": disk_healthy,
            "disk_free_percent": disk_free,
            "cpu_healthy": cpu_healthy,
            "cpu_percent": cpu_usage,
            "memory_percent": memory.percent,
            "memory_available_gb": memory.available / (1024 ** 3),
            "overall_healthy": disk_healthy and cpu_healthy
        }

    def is_system_healthy(self, disk_path: str = "/") -> bool:
        """
        Check if system is overall healthy.

        Args:
            disk_path: Path to check disk usage (default: "/")

        Returns:
            True if both disk and CPU are healthy, False otherwise

        Example:
            >>> monitor = SystemMonitor()
            >>> if not monitor.is_system_healthy():
            ...     print("WARNING: System resources critical!")
        """
        disk_healthy, _ = self.check_disk_usage(disk_path)
        cpu_healthy, _ = self.check_cpu_usage()
        return disk_healthy and cpu_healthy


def main():
    """Command-line interface for system monitoring."""
    monitor = SystemMonitor()

    print("System Monitor")
    print("=" * 50)

    status = monitor.get_detailed_status()

    print(f"\n📊 Disk Usage:")
    print(f"   Free Space: {status['disk_free_percent']:.1f}%")
    print(f"   Status: {'✅ OK' if status['disk_healthy'] else '❌ LOW SPACE'}")

    print(f"\n💻 CPU Usage:")
    print(f"   Current: {status['cpu_percent']:.1f}%")
    print(f"   Status: {'✅ OK' if status['cpu_healthy'] else '❌ HIGH LOAD'}")

    print(f"\n🧠 Memory:")
    print(f"   Used: {status['memory_percent']:.1f}%")
    print(f"   Available: {status['memory_available_gb']:.1f} GB")

    print(f"\n{'✅ System Healthy' if status['overall_healthy'] else '❌ SYSTEM ALERT'}")


if __name__ == "__main__":
    main()
