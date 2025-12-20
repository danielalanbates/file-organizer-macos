#!/usr/bin/env python3
"""
Mac Reminders and Calendar Automation
Uses AppleScript to interact with native macOS apps
"""

import subprocess
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class MacAutomation:
    def __init__(self):
        self.reminder_lists = self._get_reminder_lists()
        
    def _run_applescript(self, script: str) -> str:
        """Run AppleScript and return output"""
        try:
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"AppleScript error: {result.stderr}")
                return ""
        except Exception as e:
            print(f"Error running AppleScript: {e}")
            return ""
    
    def _get_reminder_lists(self) -> List[str]:
        """Get all reminder lists"""
        script = '''
        tell application "Reminders"
            set listNames to {}
            repeat with lst in lists
                set end of listNames to name of lst
            end repeat
            return listNames
        end tell
        '''
        result = self._run_applescript(script)
        if result:
            # Parse the AppleScript list format
            return [item.strip() for item in result.split(',')]
        return []
    
    def create_reminder(self, title: str, list_name: str = "Reminders", 
                       due_date: str = None, notes: str = "") -> bool:
        """Create a new reminder"""
        script = f'''
        tell application "Reminders"
            set targetList to list "{list_name}"
            set newReminder to make new reminder at end of reminders of targetList
            set name of newReminder to "{title}"
            set body of newReminder to "{notes}"
        '''
        
        if due_date:
            script += f'\n    set due date of newReminder to date "{due_date}"'
        
        script += '\nend tell'
        
        result = self._run_applescript(script)
        return result != ""
    
    def create_calendar_event(self, title: str, start_date: str, end_date: str = None,
                             location: str = "", notes: str = "") -> bool:
        """Create a calendar event"""
        if not end_date:
            # Default to 1 hour duration
            start_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
            end_dt = start_dt + timedelta(hours=1)
            end_date = end_dt.strftime("%Y-%m-%d %H:%M")
        
        script = f'''
        tell application "Calendar"
            set targetCalendar to calendar "Calendar" -- Default calendar
            set newEvent to make new event at end of events of targetCalendar
            set summary of newEvent to "{title}"
            set start date of newEvent to date "{start_date}"
            set end date of newEvent to date "{end_date}"
            set location of newEvent to "{location}"
            set description of newEvent to "{notes}"
        end tell
        '''
        
        result = self._run_applescript(script)
        return result != ""
    
    def create_workout_schedule(self, workout_program: Dict, start_date: str = None):
        """Create calendar events for workout program"""
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
        
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        
        # Create workout schedule for first month
        for week_num in range(1, 5):  # 4 weeks
            week_data = workout_program["weeks"].get(f"week_{week_num}", {})
            
            for day_num in range(1, 6):  # 5 days per week
                day_data = week_data.get(f"day_{day_num}", {})
                if not day_data:
                    continue
                
                # Calculate date for this workout
                days_offset = (week_num - 1) * 7 + (day_num - 1)
                workout_date = start_dt + timedelta(days=days_offset)
                
                # Skip weekends, adjust to weekdays
                while workout_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
                    workout_date += timedelta(days=1)
                
                # Create calendar event
                event_title = f"Workout: {day_data['focus']}"
                event_start = workout_date.strftime("%Y-%m-%d 07:00")  # 7 AM workout
                event_end = workout_date.strftime("%Y-%m-%d 08:15")    # 75 minutes
                
                # Create exercise list for notes
                exercises = []
                for exercise in day_data.get('exercises', [])[:3]:  # First 3 exercises
                    exercises.append(f"• {exercise['name']}")
                
                notes = f"Duration: {day_data.get('estimated_duration', '60-75 minutes')}\\n\\nExercises:\\n" + "\\n".join(exercises)
                
                self.create_calendar_event(
                    title=event_title,
                    start_date=event_start,
                    end_date=event_end,
                    location="Gym",
                    notes=notes
                )
                
                print(f"Created workout event for {workout_date.strftime('%Y-%m-%d')}: {day_data['focus']}")
    
    def create_fitness_reminders(self):
        """Create fitness-related reminders based on your documents"""
        fitness_reminders = [
            {
                'title': 'Log body measurements',
                'due_date': '2025-10-21 09:00',
                'notes': 'Weekly measurement tracking for lean bulk progress'
            },
            {
                'title': 'Meal prep for the week',
                'due_date': '2025-10-20 16:00',
                'notes': 'Prepare meals according to lean bulk nutrition plan'
            },
            {
                'title': 'Review workout progress',
                'due_date': '2025-10-27 19:00',
                'notes': 'Check if weights need to be increased for progressive overload'
            },
            {
                'title': 'Schedule rest day activity',
                'due_date': '2025-10-26 10:00',
                'notes': 'Light activity like walking or yoga on rest day'
            }
        ]
        
        for reminder in fitness_reminders:
            self.create_reminder(
                title=reminder['title'],
                list_name="Fitness",
                due_date=reminder['due_date'],
                notes=reminder['notes']
            )
            print(f"Created reminder: {reminder['title']}")
    
    def create_goal_deadline_reminders(self, goals: List[Dict]):
        """Create reminders for goal deadlines"""
        for goal in goals:
            if goal.get('target_date'):
                target_dt = datetime.strptime(goal['target_date'], '%Y-%m-%d')
                
                # Create reminder 1 week before deadline
                reminder_date = target_dt - timedelta(days=7)
                reminder_title = f"Goal deadline approaching: {goal['title']}"
                reminder_notes = f"Target date: {goal['target_date']}\\nCurrent progress: {goal.get('progress', 0)}%"
                
                self.create_reminder(
                    title=reminder_title,
                    due_date=reminder_date.strftime("%Y-%m-%d 09:00"),
                    notes=reminder_notes,
                    list_name="Goals"
                )
                print(f"Created goal reminder for: {goal['title']}")
    
    def create_recurring_maintenance_reminders(self):
        """Create recurring reminders for personal maintenance tasks"""
        maintenance_tasks = [
            {
                'title': 'Backup personal documents',
                'interval_days': 7,
                'notes': 'Weekly backup verification and cloud sync check'
            },
            {
                'title': 'Review and update goals',
                'interval_days': 30,
                'notes': 'Monthly goal progress review and adjustment'
            },
            {
                'title': 'Organize digital photos',
                'interval_days': 14,
                'notes': 'Sort and tag recent photos, create albums'
            },
            {
                'title': 'Clean up downloads folder',
                'interval_days': 7,
                'notes': 'Sort files and clear unnecessary downloads'
            }
        ]
        
        start_date = datetime.now()
        
        for task in maintenance_tasks:
            # Create next 4 occurrences
            for i in range(4):
                due_date = start_date + timedelta(days=task['interval_days'] * (i + 1))
                
                self.create_reminder(
                    title=task['title'],
                    due_date=due_date.strftime("%Y-%m-%d 10:00"),
                    notes=task['notes'],
                    list_name="Maintenance"
                )
            
            print(f"Created recurring reminders for: {task['title']}")

def main():
    automation = MacAutomation()
    
    print("Available Reminder Lists:", automation.reminder_lists)
    
    # Create fitness reminders
    automation.create_fitness_reminders()
    
    # Create maintenance reminders
    automation.create_recurring_maintenance_reminders()
    
    print("\nReminders and calendar events created successfully!")
    print("Check your Reminders and Calendar apps to see the new items.")

if __name__ == "__main__":
    main()