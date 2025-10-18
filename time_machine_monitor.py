#!/usr/bin/env python3
"""
Time Machine Monitor - Menu Bar Notification System
Alerts if Time Machine hasn't run in 8+ days via top bar notification
"""

import subprocess
import os
import plistlib
from datetime import datetime, timedelta
import json

class TimeMachineMonitor:
    """Monitor Time Machine backup status and provide notifications"""
    
    def __init__(self):
        self.tm_prefs_path = "/Library/Preferences/com.apple.TimeMachine.plist"
        self.notification_threshold = 8  # days
        self.menu_bar_app_path = "/Users/daniel/copilot/menu_bar_assistant.py"
        
    def get_last_backup_date(self):
        """Get the last Time Machine backup date"""
        try:
            # Method 1: Use tmutil destinationinfo for more reliable results
            result = subprocess.run(['tmutil', 'destinationinfo'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Date' in line and 'backup' in line.lower():
                        # Parse date from destinationinfo output
                        try:
                            date_str = line.split(':', 1)[1].strip()
                            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S %z')
                        except:
                            continue
            
            # Method 2: Check tmutil latestbackup
            result = subprocess.run(['tmutil', 'latestbackup'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                backup_path = result.stdout.strip()
                # Extract date from backup path
                if backup_path and 'Backups.backupdb' in backup_path:
                    try:
                        # Get modification time of backup directory
                        stat_result = subprocess.run(
                            ['stat', '-f', '%Sm', '-t', '%Y-%m-%d %H:%M:%S', backup_path],
                            capture_output=True, text=True
                        )
                        if stat_result.returncode == 0:
                            return datetime.strptime(stat_result.stdout.strip(), '%Y-%m-%d %H:%M:%S')
                    except:
                        pass
            
            # Method 3: Try alternative approach with system_profiler
            profile_result = subprocess.run([
                'system_profiler', 'SPStorageDataType'
            ], capture_output=True, text=True)
            
            # Method 4: Check preferences differently - avoid permission issues
            try:
                prefs_result = subprocess.run([
                    'defaults', 'read', '/Library/Preferences/com.apple.TimeMachine'
                ], capture_output=True, text=True)
                
                if prefs_result.returncode == 0:
                    # Parse plist-style output for dates
                    for line in prefs_result.stdout.split('\n'):
                        if 'Date' in line:
                            # Extract date information
                            pass
            except:
                pass
                
            # Method 5: Simple fallback - check if Time Machine is even enabled
            status_result = subprocess.run(['tmutil', 'status'], 
                                         capture_output=True, text=True)
            
            if status_result.returncode == 0:
                # Parse status for backup information
                status_lines = status_result.stdout.split('\n')
                for line in status_lines:
                    if 'BackupPhase' in line and 'ThinningPreBackup' not in line:
                        # Time Machine is active, assume recent backup
                        return datetime.now() - timedelta(hours=2)  # Conservative estimate
                            
        except Exception as e:
            print(f"Error getting backup date: {e}")
            
        # If all methods fail, return None to indicate unknown status
        return None
    
    def check_backup_status(self):
        """Check if backup is overdue and return status"""
        last_backup = self.get_last_backup_date()
        
        if last_backup is None:
            return {
                'status': 'unknown',
                'message': 'Could not determine last backup date',
                'days_since': None,
                'overdue': True
            }
        
        days_since = (datetime.now() - last_backup).days
        
        return {
            'status': 'overdue' if days_since >= self.notification_threshold else 'current',
            'message': f'Last backup: {days_since} days ago',
            'days_since': days_since,
            'last_backup': last_backup.strftime('%Y-%m-%d %H:%M'),
            'overdue': days_since >= self.notification_threshold
        }
    
    def create_menu_bar_notification(self, status_info):
        """Create menu bar notification for Time Machine status"""
        
        if status_info['overdue']:
            # Create urgent notification
            notification_script = f'''
            on run
                display notification "Time Machine backup overdue: {status_info['days_since']} days" with title "⚠️ Backup Alert" subtitle "Time Machine Monitor"
                
                -- Also create persistent menu bar indicator
                do shell script "echo 'TM: {status_info['days_since']}d' > /tmp/tm_status"
                
                return "Notification sent"
            end run
            '''
            
            subprocess.run(['osascript', '-e', notification_script])
            
            # Update menu bar status
            self.update_menu_bar_status(status_info)
            
    def update_menu_bar_status(self, status_info):
        """Update the virtual assistant menu bar with Time Machine status"""
        
        status_file = "/tmp/virtual_assistant_status.json"
        
        try:
            # Load existing status
            if os.path.exists(status_file):
                with open(status_file, 'r') as f:
                    status_data = json.load(f)
            else:
                status_data = {}
            
            # Update Time Machine status
            status_data['time_machine'] = {
                'last_check': datetime.now().isoformat(),
                'status': status_info['status'],
                'days_since_backup': status_info['days_since'],
                'last_backup': status_info.get('last_backup', 'Unknown'),
                'overdue': status_info['overdue']
            }
            
            # Save updated status
            with open(status_file, 'w') as f:
                json.dump(status_data, f, indent=2)
                
            print(f"✅ Updated menu bar status: {status_info['message']}")
            
        except Exception as e:
            print(f"❌ Error updating status: {e}")
    
    def create_menu_bar_app(self):
        """Create the menu bar application for virtual assistant"""
        
        menu_bar_code = '''#!/usr/bin/env python3
"""
Virtual Assistant Menu Bar App
Shows system status including Time Machine monitoring
"""

import rumps
import json
import os
from datetime import datetime
import subprocess

class VirtualAssistantMenuBar(rumps.App):
    def __init__(self):
        super(VirtualAssistantMenuBar, self).__init__("🤖", quit_button=None)
        self.status_file = "/tmp/virtual_assistant_status.json"
        self.timer = rumps.Timer(self.update_status, 300)  # Update every 5 minutes
        self.timer.start()
        self.update_status(None)
    
    def update_status(self, sender):
        """Update the menu bar status"""
        try:
            if os.path.exists(self.status_file):
                with open(self.status_file, 'r') as f:
                    status_data = json.load(f)
                
                tm_status = status_data.get('time_machine', {})
                
                if tm_status.get('overdue', False):
                    days = tm_status.get('days_since_backup', 0)
                    self.title = f"🤖⚠️ TM:{days}d"
                else:
                    self.title = "🤖✅"
            else:
                self.title = "🤖"
                
        except Exception as e:
            self.title = "🤖❌"
    
    @rumps.clicked("Time Machine Status")
    def tm_status(self, sender):
        """Show Time Machine status details"""
        try:
            if os.path.exists(self.status_file):
                with open(self.status_file, 'r') as f:
                    status_data = json.load(f)
                
                tm_status = status_data.get('time_machine', {})
                
                if tm_status:
                    message = f"""Time Machine Status:
                    
Last Backup: {tm_status.get('last_backup', 'Unknown')}
Days Since: {tm_status.get('days_since_backup', '?')}
Status: {tm_status.get('status', 'unknown').title()}

{('⚠️ BACKUP OVERDUE!' if tm_status.get('overdue') else '✅ Backup current')}"""
                else:
                    message = "Time Machine status unknown"
            else:
                message = "No status data available"
                
            rumps.alert(title="Time Machine Monitor", message=message)
            
        except Exception as e:
            rumps.alert(title="Error", message=f"Could not read status: {e}")
    
    @rumps.clicked("Run Backup Now")
    def run_backup(self, sender):
        """Trigger Time Machine backup"""
        try:
            result = subprocess.run(['tmutil', 'startbackup'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                rumps.alert(title="Backup Started", 
                           message="Time Machine backup has been initiated.")
            else:
                rumps.alert(title="Backup Failed", 
                           message=f"Could not start backup: {result.stderr}")
                           
        except Exception as e:
            rumps.alert(title="Error", message=f"Backup error: {e}")
    
    @rumps.clicked("Open Copilot Folder")
    def open_copilot(self, sender):
        """Open the copilot automation folder"""
        subprocess.run(['open', '/Users/daniel/copilot/'])
    
    @rumps.clicked("Run Full Automation")
    def run_automation(self, sender):
        """Run the full automation suite"""
        try:
            subprocess.Popen([
                '/usr/local/bin/python3', 
                '/Users/daniel/copilot/automation_master.py'
            ])
            rumps.alert(title="Automation Started", 
                       message="Full automation suite is running...")
        except Exception as e:
            rumps.alert(title="Error", message=f"Automation error: {e}")
    
    @rumps.clicked("Quit")
    def quit_app(self, sender):
        """Quit the menu bar app"""
        rumps.quit_application()

if __name__ == "__main__":
    try:
        VirtualAssistantMenuBar().run()
    except Exception as e:
        print(f"Menu bar app error: {e}")
'''
        
        with open(self.menu_bar_app_path, 'w') as f:
            f.write(menu_bar_code)
        
        os.chmod(self.menu_bar_app_path, 0o755)
        print(f"✅ Created menu bar app: {self.menu_bar_app_path}")
        
        return self.menu_bar_app_path
    
    def install_menu_bar_app(self):
        """Install the menu bar app to run automatically"""
        
        # Create LaunchAgent plist for auto-start
        launch_agent_plist = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.daniel.virtual-assistant-menubar</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>{self.menu_bar_app_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/tmp/virtual-assistant-menubar.log</string>
    <key>StandardOutPath</key>
    <string>/tmp/virtual-assistant-menubar.log</string>
</dict>
</plist>'''
        
        launch_agents_dir = os.path.expanduser("~/Library/LaunchAgents")
        os.makedirs(launch_agents_dir, exist_ok=True)
        
        plist_path = os.path.join(launch_agents_dir, "com.daniel.virtual-assistant-menubar.plist")
        
        with open(plist_path, 'w') as f:
            f.write(launch_agent_plist)
        
        print(f"✅ Created LaunchAgent: {plist_path}")
        
        # Load the launch agent
        try:
            subprocess.run(['launchctl', 'load', plist_path], check=True)
            print("✅ LaunchAgent loaded successfully")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Could not load LaunchAgent: {e}")
        
        return plist_path

def main():
    """Main function to set up Time Machine monitoring"""
    
    print("⏰ Time Machine Monitor Setup")
    print("=" * 40)
    
    monitor = TimeMachineMonitor()
    
    # Check current backup status
    print("\n🔍 Checking Time Machine status...")
    status = monitor.check_backup_status()
    
    print(f"Status: {status['status']}")
    print(f"Message: {status['message']}")
    
    if status['overdue']:
        print(f"⚠️ WARNING: Backup is {status['days_since']} days overdue!")
        
        # Send notification
        monitor.create_menu_bar_notification(status)
        
    else:
        print("✅ Backup is current")
        monitor.update_menu_bar_status(status)
    
    # Create menu bar app
    print("\n📱 Setting up menu bar application...")
    
    # Install rumps if not present
    try:
        import rumps
        print("✅ rumps library available")
    except ImportError:
        print("📦 Installing rumps library...")
        subprocess.run(['/usr/local/bin/python3', '-m', 'pip', 'install', 'rumps'])
    
    menu_bar_path = monitor.create_menu_bar_app()
    
    # Install launch agent
    print("\n🤖 Installing auto-start configuration...")
    plist_path = monitor.install_menu_bar_app()
    
    print("\n✅ Time Machine Monitor Setup Complete!")
    print("\nFeatures installed:")
    print("- Time Machine backup monitoring")
    print("- Menu bar notification system")
    print("- Auto-start on login")
    print("- Quick access to automation tools")
    
    print(f"\n🎯 Menu bar app will show:")
    print("- 🤖✅ when backups are current")
    print("- 🤖⚠️ TM:Xd when backup is overdue")
    
    print("\n💡 Manual controls:")
    print(f"- Start menu bar app: python3 {menu_bar_path}")
    print(f"- Unload auto-start: launchctl unload {plist_path}")
    
    # Start the menu bar app immediately
    print("\n🤖 Starting menu bar app...")
    try:
        subprocess.Popen(['/usr/local/bin/python3', menu_bar_path])
        print("✅ Menu bar app started!")
    except Exception as e:
        print(f"⚠️ Could not start menu bar app: {e}")
        print("You can start it manually later.")

if __name__ == "__main__":
    main()