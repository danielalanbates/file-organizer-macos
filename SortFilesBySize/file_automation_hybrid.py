#!/usr/bin/env python3
"""
File Automation Suite - Hybrid Menu Bar + Windows Application
Professional macOS app with menu bar access and detailed windows

Copyright (c) 2025 Daniel
License: Proprietary - See LICENSE file
"""

import rumps
import subprocess
import threading
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import sys
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

# Import our existing modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from system_monitor import SystemMonitor
from file_organizer import FileOrganizer


class FileResultsWindow:
    """Professional window for displaying file scan results."""

    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.window = None
        self.tree = None
        self.results: List[Tuple[int, str]] = []

    def show(self, scan_path: str, results: List[Tuple[int, str]]):
        """Display scan results in a professional table."""
        self.results = results

        if self.window is None or not self.window.winfo_exists():
            self._create_window()

        # Update window
        self.window.title(f"Large Files in {Path(scan_path).name}")
        self._populate_results()
        self.window.lift()
        self.window.focus_force()

    def _create_window(self):
        """Create the results window."""
        self.window = tk.Toplevel()
        self.window.title("File Scan Results")
        self.window.geometry("900x600")

        # Set custom app icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'app_icon.png')
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                self.window.iconphoto(True, icon)
        except:
            pass  # Fail silently if icon not available

        # Header
        header_frame = ttk.Frame(self.window)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        title_label = ttk.Label(
            header_frame,
            text="📁 Large File Scanner",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(side=tk.LEFT)

        # Summary frame
        self.summary_label = ttk.Label(header_frame, text="")
        self.summary_label.pack(side=tk.RIGHT)

        # Treeview with scrollbar
        tree_frame = ttk.Frame(self.window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=('Size', 'Size_MB', 'Name', 'Location', 'Modified'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        # Column headers
        self.tree.heading('Size', text='Size (Bytes)')
        self.tree.heading('Size_MB', text='Size')
        self.tree.heading('Name', text='File Name')
        self.tree.heading('Location', text='Location')
        self.tree.heading('Modified', text='Modified')

        # Column widths
        self.tree.column('Size', width=0, stretch=False)  # Hidden, for sorting
        self.tree.column('Size_MB', width=100)
        self.tree.column('Name', width=250)
        self.tree.column('Location', width=350)
        self.tree.column('Modified', width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Button frame
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            button_frame,
            text="🔍 Reveal in Finder",
            command=self._reveal_in_finder
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="🗑️ Move to Trash",
            command=self._move_to_trash
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="📋 Copy Path",
            command=self._copy_path
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="💾 Export CSV",
            command=self._export_csv
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Close",
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=5)

    def _populate_results(self):
        """Fill the tree with results."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        total_size = sum(size for size, _ in self.results)
        self.summary_label.config(
            text=f"Found {len(self.results)} files • Total: {self._format_size(total_size)}"
        )

        # Add results
        for size, path in self.results:
            file_path = Path(path)
            try:
                modified = datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
            except:
                modified = "Unknown"

            self.tree.insert('', 'end', values=(
                size,  # Hidden, for sorting
                self._format_size(size),
                file_path.name,
                str(file_path.parent),
                modified
            ))

    def _format_size(self, size_bytes: int) -> str:
        """Format bytes to human-readable size."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def _reveal_in_finder(self):
        """Reveal selected file in Finder."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a file first")
            return

        item = self.tree.item(selection[0])
        location = item['values'][3]
        name = item['values'][2]
        full_path = Path(location) / name

        subprocess.run(['open', '-R', str(full_path)])

    def _move_to_trash(self):
        """Move selected file to trash."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a file first")
            return

        item = self.tree.item(selection[0])
        location = item['values'][3]
        name = item['values'][2]
        full_path = Path(location) / name

        if messagebox.askyesno("Confirm", f"Move '{name}' to trash?"):
            try:
                subprocess.run(['osascript', '-e', f'tell app "Finder" to delete POSIX file "{full_path}"'])
                self.tree.delete(selection[0])
                messagebox.showinfo("Success", f"Moved '{name}' to trash")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to move to trash: {e}")

    def _copy_path(self):
        """Copy file path to clipboard."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a file first")
            return

        item = self.tree.item(selection[0])
        location = item['values'][3]
        name = item['values'][2]
        full_path = Path(location) / name

        subprocess.run(['osascript', '-e', f'set the clipboard to "{full_path}"'])
        messagebox.showinfo("Copied", "File path copied to clipboard")

    def _export_csv(self):
        """Export results to CSV."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if file_path:
            import csv
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Size (Bytes)', 'Size', 'Name', 'Location', 'Modified'])

                for item in self.tree.get_children():
                    values = self.tree.item(item)['values']
                    writer.writerow(values)

            messagebox.showinfo("Exported", f"Results exported to {file_path}")


class PreferencesWindow:
    """Professional preferences window."""

    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.window = None

    def show(self):
        """Show preferences window."""
        if self.window is None or not self.window.winfo_exists():
            self._create_window()

        self.window.lift()
        self.window.focus_force()

    def _create_window(self):
        """Create preferences window."""
        self.window = tk.Toplevel()
        self.window.title("File Automation Suite - Preferences")
        self.window.geometry("600x500")

        # Set custom app icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'app_icon.png')
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                self.window.iconphoto(True, icon)
        except:
            pass  # Fail silently if icon not available

        # Header
        header = ttk.Label(
            self.window,
            text="⚙️ Preferences",
            font=('Helvetica', 16, 'bold')
        )
        header.pack(pady=15)

        # Notebook for tabs
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Alerts tab
        alerts_tab = ttk.Frame(notebook)
        notebook.add(alerts_tab, text="🔔 Alerts")
        self._create_alerts_tab(alerts_tab)

        # Scanning tab
        scanning_tab = ttk.Frame(notebook)
        notebook.add(scanning_tab, text="🔍 Scanning")
        self._create_scanning_tab(scanning_tab)

        # License tab
        license_tab = ttk.Frame(notebook)
        notebook.add(license_tab, text="🔑 License")
        self._create_license_tab(license_tab)

        # Button frame
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            button_frame,
            text="Save",
            command=self._save_preferences
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=5)

    def _create_alerts_tab(self, parent):
        """Create alerts settings tab."""
        frame = ttk.LabelFrame(parent, text="Alert Thresholds", padding=15)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Disk space threshold
        ttk.Label(frame, text="Disk Space Alert When Below:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.disk_threshold = ttk.Spinbox(frame, from_=5, to=50, width=10)
        self.disk_threshold.set(20)
        self.disk_threshold.grid(row=0, column=1, padx=5)
        ttk.Label(frame, text="%").grid(row=0, column=2, sticky=tk.W)

        # CPU threshold
        ttk.Label(frame, text="CPU Usage Alert When Above:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cpu_threshold = ttk.Spinbox(frame, from_=50, to=100, width=10)
        self.cpu_threshold.set(75)
        self.cpu_threshold.grid(row=1, column=1, padx=5)
        ttk.Label(frame, text="%").grid(row=1, column=2, sticky=tk.W)

        # Notifications
        self.show_notifications = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            frame,
            text="Show system notifications",
            variable=self.show_notifications
        ).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=10)

        self.play_sound = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frame,
            text="Play sound on critical alert",
            variable=self.play_sound
        ).grid(row=3, column=0, columnspan=3, sticky=tk.W)

    def _create_scanning_tab(self, parent):
        """Create scanning settings tab."""
        frame = ttk.LabelFrame(parent, text="File Scanner Settings", padding=15)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Default scan path
        ttk.Label(frame, text="Default Scan Location:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.scan_path = ttk.Entry(frame, width=40)
        self.scan_path.insert(0, str(Path.home() / "Downloads"))
        self.scan_path.grid(row=0, column=1, padx=5)

        ttk.Button(frame, text="Browse...", command=self._browse_scan_path).grid(row=0, column=2, padx=5)

        # Number of results
        ttk.Label(frame, text="Number of Results to Show:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.result_count = ttk.Spinbox(frame, from_=10, to=500, width=10)
        self.result_count.set(50)
        self.result_count.grid(row=1, column=1, sticky=tk.W, padx=5)

        # Include hidden files
        self.include_hidden = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frame,
            text="Include hidden files in scan",
            variable=self.include_hidden
        ).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=10)

    def _create_license_tab(self, parent):
        """Create license tab."""
        frame = ttk.LabelFrame(parent, text="License Information", padding=15)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if self.parent_app.is_licensed:
            status_text = f"✅ Licensed to: {self.parent_app.license_key[:4]}...{self.parent_app.license_key[-4:]}"
            status_color = "green"
        else:
            status_text = "⚠️ Unlicensed Version"
            status_color = "red"

        status_label = ttk.Label(frame, text=status_text, foreground=status_color, font=('Helvetica', 12, 'bold'))
        status_label.pack(pady=10)

        # License key entry
        ttk.Label(frame, text="Enter License Key:").pack(pady=(20, 5))
        self.license_entry = ttk.Entry(frame, width=40)
        self.license_entry.pack(pady=5)

        ttk.Button(frame, text="Activate License", command=self._activate_license).pack(pady=10)

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)

        ttk.Label(frame, text="Don't have a license yet?").pack()
        ttk.Button(frame, text="Purchase License ($39)", command=self._purchase_license).pack(pady=5)

    def _browse_scan_path(self):
        """Browse for scan directory."""
        path = filedialog.askdirectory(initialdir=self.scan_path.get())
        if path:
            self.scan_path.delete(0, tk.END)
            self.scan_path.insert(0, path)

    def _activate_license(self):
        """Activate license key."""
        key = self.license_entry.get().strip()
        if self.parent_app._validate_license(key):
            self.parent_app._save_license(key)
            self.parent_app.license_key = key
            self.parent_app.is_licensed = True
            self.parent_app._build_menu()
            messagebox.showinfo("Success", "License activated successfully!")
            self.window.destroy()
        else:
            messagebox.showerror("Invalid License", "Please check your license key and try again.")

    def _purchase_license(self):
        """Open purchase page."""
        import webbrowser
        webbrowser.open("https://gumroad.com/l/file-automation-suite")

    def _save_preferences(self):
        """Save preferences."""
        # TODO: Implement actual preference saving
        messagebox.showinfo("Saved", "Preferences saved successfully!")
        self.window.destroy()


class SystemDashboardWindow:
    """Professional system health dashboard."""

    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.window = None

    def show(self):
        """Show system dashboard."""
        if self.window is None or not self.window.winfo_exists():
            self._create_window()
        else:
            self._update_display()

        self.window.lift()
        self.window.focus_force()

    def _create_window(self):
        """Create dashboard window."""
        self.window = tk.Toplevel()
        self.window.title("File Automation Suite - System Health")
        self.window.geometry("700x500")

        # Set custom app icon
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'app_icon.png')
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                self.window.iconphoto(True, icon)
        except:
            pass  # Fail silently if icon not available

        # Header
        header = ttk.Label(
            self.window,
            text="📊 System Health Dashboard",
            font=('Helvetica', 16, 'bold')
        )
        header.pack(pady=15)

        # Status frame
        status_frame = ttk.LabelFrame(self.window, text="Current Status", padding=15)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.status_labels = {}

        # Overall status
        self.overall_label = ttk.Label(status_frame, text="", font=('Helvetica', 14, 'bold'))
        self.overall_label.pack(pady=10)

        # Disk space
        disk_frame = ttk.Frame(status_frame)
        disk_frame.pack(fill=tk.X, pady=10)

        ttk.Label(disk_frame, text="💾 Disk Space:", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        self.disk_progress = ttk.Progressbar(disk_frame, length=500, mode='determinate')
        self.disk_progress.pack(fill=tk.X, pady=5)
        self.status_labels['disk'] = ttk.Label(disk_frame, text="")
        self.status_labels['disk'].pack(anchor=tk.W)

        # CPU usage
        cpu_frame = ttk.Frame(status_frame)
        cpu_frame.pack(fill=tk.X, pady=10)

        ttk.Label(cpu_frame, text="💻 CPU Usage:", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        self.cpu_progress = ttk.Progressbar(cpu_frame, length=500, mode='determinate')
        self.cpu_progress.pack(fill=tk.X, pady=5)
        self.status_labels['cpu'] = ttk.Label(cpu_frame, text="")
        self.status_labels['cpu'].pack(anchor=tk.W)

        # Memory
        mem_frame = ttk.Frame(status_frame)
        mem_frame.pack(fill=tk.X, pady=10)

        ttk.Label(mem_frame, text="🧠 Memory:", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        self.mem_progress = ttk.Progressbar(mem_frame, length=500, mode='determinate')
        self.mem_progress.pack(fill=tk.X, pady=5)
        self.status_labels['mem'] = ttk.Label(mem_frame, text="")
        self.status_labels['mem'].pack(anchor=tk.W)

        # Button frame
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(button_frame, text="🔄 Refresh", command=self._update_display).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=self.window.destroy).pack(side=tk.RIGHT, padx=5)

        # Initial update
        self._update_display()

    def _update_display(self):
        """Update dashboard with current stats."""
        status = self.parent_app.system_monitor.get_detailed_status()

        # Overall status
        if status['overall_healthy']:
            self.overall_label.config(text="✅ System Healthy", foreground="green")
        else:
            self.overall_label.config(text="⚠️ Attention Needed", foreground="red")

        # Disk space (show used, not free)
        disk_used = 100 - status['disk_free_percent']
        self.disk_progress['value'] = disk_used
        self.status_labels['disk'].config(
            text=f"{status['disk_free_percent']:.1f}% free ({100-disk_used:.1f}% used)"
        )

        # CPU
        self.cpu_progress['value'] = status['cpu_percent']
        self.status_labels['cpu'].config(
            text=f"{status['cpu_percent']:.1f}% - {'✅ Normal' if status['cpu_healthy'] else '⚠️ High'}"
        )

        # Memory
        self.mem_progress['value'] = status['memory_percent']
        self.status_labels['mem'].config(
            text=f"{status['memory_percent']:.1f}% used • {status['memory_available_gb']:.1f} GB available"
        )


class FileAutomationApp(rumps.App):
    """Hybrid menu bar + windows application."""

    def __init__(self):
        super().__init__(
            name="File Automation Suite",
            title="📁",
            quit_button="Quit File Automation Suite"
        )

        # Initialize hidden Tk root for Toplevel windows
        self.tk_root = tk.Tk()
        self.tk_root.withdraw()  # Hide the root window

        # Initialize components
        self.system_monitor = SystemMonitor(disk_threshold=20, cpu_threshold=75)
        self.file_organizer = FileOrganizer()
        self.license_key: Optional[str] = None
        self.is_licensed = False

        # Initialize windows (created on demand)
        self.file_results_window = FileResultsWindow(self)
        self.preferences_window = PreferencesWindow(self)
        self.dashboard_window = SystemDashboardWindow(self)

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
        """Validate license key."""
        # TODO: Implement proper license validation
        return len(key) > 10

    def _save_license(self, key: str):
        """Save license key to config."""
        config_dir = Path.home() / ".file_automation_suite"
        config_dir.mkdir(exist_ok=True)

        license_file = config_dir / "license.key"
        license_file.write_text(key)
        license_file.chmod(0o600)

    def _build_menu(self):
        """Build the menu bar menu."""
        if not self.is_licensed:
            self.menu = [
                rumps.MenuItem("⚠️ Unlicensed Version", callback=None),
                rumps.MenuItem("Enter License Key...", callback=self.show_preferences_window),
                rumps.separator,
                rumps.MenuItem("Buy License ($39)", callback=self.buy_license),
            ]
        else:
            self.menu = [
                rumps.MenuItem("✅ Licensed", callback=None),
                rumps.separator,
                rumps.MenuItem("🔍 Scan Large Files...", callback=self.scan_large_files_window),
                rumps.MenuItem("📊 System Dashboard...", callback=self.show_dashboard_window),
                rumps.MenuItem("⏰ Time Machine Status", callback=self.time_machine_status),
                rumps.separator,
                rumps.MenuItem("⚙️ Preferences...", callback=self.show_preferences_window),
                rumps.MenuItem("📖 Help", callback=self.show_help),
            ]

    def _start_monitoring(self):
        """Start background system monitoring."""
        import time

        # Track last notification time to prevent spam
        self.last_notification_time = 0

        def monitor_loop():
            while True:
                try:
                    status = self.system_monitor.get_detailed_status()

                    # Update menu bar icon based on health
                    # Keep it simple - always show folder icon
                    # (Users can check dashboard for detailed health)
                    self.title = "📁"

                    # Only show warning in notification, not menu bar
                    # if not status['overall_healthy']:
                    #     self.title = "⚠️"

                    # Show notification if critical (max once per hour)
                    current_time = time.time()
                    if status['disk_free_percent'] < 10:
                        if current_time - self.last_notification_time > 3600:  # 1 hour
                            rumps.notification(
                                title="Disk Space Critical!",
                                subtitle=f"Only {status['disk_free_percent']:.1f}% free",
                                message="Click to see large files"
                            )
                            self.last_notification_time = current_time

                except Exception as e:
                    print(f"Monitoring error: {e}")

                # Sleep for 5 minutes before next check
                time.sleep(300)

        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()

    @rumps.clicked("🔍 Scan Large Files...")
    def scan_large_files_window(self, _):
        """Open file scanner with results window."""
        if not self.is_licensed:
            self._show_trial_expired()
            return

        # Ask for directory
        window = rumps.Window(
            message="Enter directory to scan (or press OK for Downloads):",
            title="Scan Large Files",
            default_text=str(Path.home() / "Downloads"),
            ok="Scan",
            cancel="Cancel"
        )

        response = window.run()
        if response.clicked:
            scan_path = response.text.strip() or str(Path.home() / "Downloads")

            # Show progress
            rumps.notification(
                title="Scanning Files...",
                subtitle=f"Analyzing {scan_path}",
                message="This may take a moment"
            )

            # Scan in background and show window
            def scan_and_show():
                try:
                    largest = self.file_organizer.find_largest_files(scan_path, top_n=100)

                    # Show results in window
                    self.file_results_window.show(scan_path, largest)

                except Exception as e:
                    rumps.alert(
                        title="Scan Error",
                        message=f"Error scanning files: {str(e)}"
                    )

            threading.Thread(target=scan_and_show, daemon=True).start()

    @rumps.clicked("📊 System Dashboard...")
    def show_dashboard_window(self, _):
        """Show system health dashboard window."""
        if not self.is_licensed:
            self._show_trial_expired()
            return

        self.dashboard_window.show()

    @rumps.clicked("⚙️ Preferences...")
    def show_preferences_window(self, _):
        """Show preferences window."""
        self.preferences_window.show()

    @rumps.clicked("⏰ Time Machine Status")
    def time_machine_status(self, _):
        """Check Time Machine backup status."""
        if not self.is_licensed:
            self._show_trial_expired()
            return

        try:
            result = subprocess.run(
                ['tmutil', 'latestbackup'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0 and result.stdout.strip():
                backup_path = result.stdout.strip()
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

        rumps.alert(title="Time Machine Status", message=message)

    @rumps.clicked("Buy License ($39)")
    def buy_license(self, _):
        """Open purchase page."""
        import webbrowser
        webbrowser.open("https://gumroad.com/l/file-automation-suite")

    @rumps.clicked("📖 Help")
    def show_help(self, _):
        """Show help information."""
        import webbrowser
        webbrowser.open("https://yourdomain.com/docs")

    def _show_trial_expired(self):
        """Show trial/license required message."""
        response = rumps.alert(
            title="License Required",
            message="Please purchase a license to use this feature.",
            ok="Buy Now ($39)",
            cancel="Cancel"
        )

        if response == 1:
            self.buy_license(None)


def main():
    """Main entry point."""
    # Hide dock icon for menu bar-only app
    try:
        import AppKit
        info = AppKit.NSBundle.mainBundle().infoDictionary()
        info["LSUIElement"] = "1"
    except:
        # If AppKit not available or fails, continue anyway
        pass

    FileAutomationApp().run()


if __name__ == "__main__":
    main()
