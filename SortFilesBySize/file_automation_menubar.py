#!/usr/bin/env python3
"""
File Automation Suite - Menu Bar Application
Professional macOS menu bar app for file automation and system monitoring

Copyright (c) 2025 Daniel
License: Proprietary - See LICENSE file
"""

import rumps
import subprocess
import threading
from pathlib import Path
from typing import Optional, Dict
import sys
import os

# Import our existing modules
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
SRC_DIRS = [
    CURRENT_DIR / "src",         # Local components within SortFilesBySize
    PROJECT_ROOT / "src",        # Shared core modules at repo root
]
for src_dir in SRC_DIRS:
    if src_dir.exists():
        sys.path.insert(0, str(src_dir))

from system_monitor import SystemMonitor
from file_organizer import FileOrganizer


class FileAutomationApp(rumps.App):
    """Professional menu bar app for file automation and system monitoring."""

    def __init__(self):
        super().__init__(
            name="File Automation Suite",
            title="📁",  # Menu bar icon
            quit_button="Quit File Automation Suite"
        )

        # Initialize components
        self.system_monitor = SystemMonitor(disk_threshold=20, cpu_threshold=75)
        self.file_organizer = FileOrganizer()
        self.license_key: Optional[str] = None
        self.is_licensed = False

        # Load license
        self._load_license()

        # Build menu
        self._build_menu()

        # Start background monitoring
        self._start_monitoring()

    def _load_license(self):
        """Load and validate license key from config."""
        config_path = Path.home() / ".file_automation_suite" / "license.key"
        if config_path.exists():
            try:
                self.license_key = config_path.read_text().strip()
                self.is_licensed = self._validate_license(self.license_key)
            except Exception as e:
                print(f"Error loading license: {e}")
                self.is_licensed = False
        else:
            self.is_licensed = False

    def _validate_license(self, key: str) -> bool:
        """
        Validate license key.

        For now, accepts any key. Replace with real validation.
        """
        # TODO: Implement proper license validation
        # Could use hashlib + secret salt, or call Gumroad API
        return len(key) > 10

    def _build_menu(self):
        """Build the menu bar menu."""
        if not self.is_licensed:
            self.menu = [
                rumps.MenuItem("⚠️ Unlicensed Version", callback=None),
                rumps.MenuItem("Enter License Key...", callback=self.enter_license),
                rumps.separator,
                rumps.MenuItem("Buy License ($39)", callback=self.buy_license),
            ]
        else:
            self.menu = [
                rumps.MenuItem("✅ Licensed", callback=None),
                rumps.separator,
                rumps.MenuItem("🔍 Find Large Files...", callback=self.find_large_files),
                rumps.MenuItem("📊 System Health Check", callback=self.health_check),
                rumps.MenuItem("⏰ Time Machine Status", callback=self.time_machine_status),
                rumps.separator,
                rumps.MenuItem("⚙️ Preferences...", callback=self.show_preferences),
                rumps.MenuItem("📖 Help", callback=self.show_help),
            ]

    def _start_monitoring(self):
        """Start background system monitoring."""
        def monitor_loop():
            """Background monitoring loop."""
            while True:
                try:
                    status = self.system_monitor.get_detailed_status()

                    # Update menu bar icon based on health
                    if not status['overall_healthy']:
                        self.title = "⚠️"  # Warning icon
                    else:
                        self.title = "📁"  # Normal icon

                    # Show notification if critical
                    if status['disk_free_percent'] < 10:
                        rumps.notification(
                            title="Disk Space Critical!",
                            subtitle=f"Only {status['disk_free_percent']:.1f}% free",
                            message="Click to see large files"
                        )

                except Exception as e:
                    print(f"Monitoring error: {e}")

                # Check every 5 minutes
                rumps.timer(300)

        # Start monitoring thread
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()

    @rumps.clicked("Enter License Key...")
    def enter_license(self, _):
        """Show license entry dialog."""
        window = rumps.Window(
            message="Enter your license key from Gumroad:",
            title="Activate File Automation Suite",
            default_text="XXXX-XXXX-XXXX-XXXX",
            ok="Activate",
            cancel="Cancel"
        )

        response = window.run()
        if response.clicked:
            key = response.text.strip()
            if self._validate_license(key):
                self._save_license(key)
                self.license_key = key
                self.is_licensed = True
                self._build_menu()

                rumps.alert(
                    title="Activation Successful!",
                    message="Thank you for purchasing File Automation Suite!"
                )
            else:
                rumps.alert(
                    title="Invalid License Key",
                    message="Please check your license key and try again."
                )

    def _save_license(self, key: str):
        """Save license key to config."""
        config_dir = Path.home() / ".file_automation_suite"
        config_dir.mkdir(exist_ok=True)

        license_file = config_dir / "license.key"
        license_file.write_text(key)
        license_file.chmod(0o600)  # Read/write for owner only

    @rumps.clicked("Buy License ($39)")
    def buy_license(self, _):
        """Open purchase page."""
        import webbrowser
        webbrowser.open("https://gumroad.com/l/file-automation-suite")
        # TODO: Update with your actual Gumroad link

    @rumps.clicked("🔍 Find Large Files...")
    def find_large_files(self, _):
        """Find and display largest files."""
        if not self.is_licensed:
            self._show_trial_expired()
            return

        # Ask for directory to scan
        window = rumps.Window(
            message="Enter directory to scan (or press OK for Downloads):",
            title="Find Large Files",
            default_text=str(Path.home() / "Downloads"),
            ok="Scan",
            cancel="Cancel"
        )

        response = window.run()
        if response.clicked:
            scan_path = response.text.strip() or str(Path.home() / "Downloads")

            # Show progress notification
            rumps.notification(
                title="Scanning Files...",
                subtitle=f"Analyzing {scan_path}",
                message="This may take a moment"
            )

            # Scan in background
            def scan_and_notify():
                try:
                    largest = self.file_organizer.find_largest_files(scan_path, top_n=10)

                    # Format results
                    results = "\n".join([
                        f"{self.file_organizer.format_size(size)} - {Path(path).name}"
                        for size, path in largest
                    ])

                    # Show results
                    rumps.alert(
                        title=f"Top 10 Largest Files in {Path(scan_path).name}",
                        message=results or "No files found"
                    )
                except Exception as e:
                    rumps.alert(
                        title="Scan Error",
                        message=f"Error scanning files: {str(e)}"
                    )

            threading.Thread(target=scan_and_notify, daemon=True).start()

    @rumps.clicked("📊 System Health Check")
    def health_check(self, _):
        """Show system health status."""
        if not self.is_licensed:
            self._show_trial_expired()
            return

        status = self.system_monitor.get_detailed_status()

        health_emoji = "✅" if status['overall_healthy'] else "⚠️"

        message = f"""
{health_emoji} System Health Report

💾 Disk Space:
   Free: {status['disk_free_percent']:.1f}%
   Status: {'OK' if status['disk_healthy'] else 'LOW SPACE'}

💻 CPU Usage:
   Current: {status['cpu_percent']:.1f}%
   Status: {'OK' if status['cpu_healthy'] else 'HIGH LOAD'}

🧠 Memory:
   Used: {status['memory_percent']:.1f}%
   Available: {status['memory_available_gb']:.1f} GB

Overall: {'Healthy' if status['overall_healthy'] else 'ATTENTION NEEDED'}
        """

        rumps.alert(
            title="System Health Check",
            message=message.strip()
        )

    @rumps.clicked("⏰ Time Machine Status")
    def time_machine_status(self, _):
        """Check Time Machine backup status."""
        if not self.is_licensed:
            self._show_trial_expired()
            return

        try:
            # Use tmutil to check last backup
            result = subprocess.run(
                ['tmutil', 'latestbackup'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0 and result.stdout.strip():
                backup_path = result.stdout.strip()

                # Get backup date from path
                import re
                date_match = re.search(r'(\d{4}-\d{2}-\d{2}-\d{6})', backup_path)
                if date_match:
                    backup_date = date_match.group(1)
                    message = f"✅ Last backup: {backup_date}\n\nBackup location:\n{backup_path}"
                else:
                    message = f"✅ Backup found:\n{backup_path}"
            else:
                message = "⚠️ No Time Machine backups found.\n\nMake sure Time Machine is enabled in System Settings."

        except subprocess.TimeoutExpired:
            message = "⏱️ Timeout checking Time Machine.\n\nThis usually means Time Machine is not configured."
        except Exception as e:
            message = f"❌ Error checking Time Machine:\n{str(e)}"

        rumps.alert(
            title="Time Machine Status",
            message=message
        )

    @rumps.clicked("⚙️ Preferences...")
    def show_preferences(self, _):
        """Show preferences dialog."""
        message = """
File Automation Suite Preferences

Disk Space Alert Threshold: 20%
CPU Usage Alert Threshold: 75%
Auto-Start: Enabled

(Full preferences coming in v1.1)
        """

        rumps.alert(
            title="Preferences",
            message=message.strip()
        )

    @rumps.clicked("📖 Help")
    def show_help(self, _):
        """Show help information."""
        import webbrowser
        webbrowser.open("https://yourdomain.com/docs")
        # TODO: Update with your actual docs URL

    def _show_trial_expired(self):
        """Show trial/license required message."""
        response = rumps.alert(
            title="License Required",
            message="Please purchase a license to use this feature.",
            ok="Buy Now ($39)",
            cancel="Cancel"
        )

        if response == 1:  # OK clicked
            self.buy_license(None)


def main():
    """Main entry point."""
    FileAutomationApp().run()


if __name__ == "__main__":
    main()
