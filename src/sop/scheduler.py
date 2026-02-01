# src/sop/scheduler.py
"""
SOP Scheduler - Handles scheduled and recurring SOP triggers.

Supports:
- Cron expressions
- Interval-based scheduling
- One-time scheduled runs
- Time window restrictions
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import re


class ScheduleType(Enum):
    """Types of schedules."""
    CRON = "cron"
    INTERVAL = "interval"
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class Schedule:
    """A scheduled SOP execution."""
    id: str
    sop_id: str
    entity: str
    schedule_type: ScheduleType
    expression: str  # Cron expr, interval like "4h", or ISO datetime
    enabled: bool = True
    last_run: Optional[str] = None
    next_run: Optional[str] = None
    run_count: int = 0
    max_runs: Optional[int] = None  # None = unlimited
    time_window: Optional[Dict[str, str]] = None  # {"start": "09:00", "end": "17:00"}
    days_of_week: Optional[List[int]] = None  # 0=Mon, 6=Sun
    variables: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        d = asdict(self)
        d['schedule_type'] = self.schedule_type.value
        return d
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Schedule':
        """Create from dictionary."""
        data['schedule_type'] = ScheduleType(data['schedule_type'])
        return cls(**data)


class SOPScheduler:
    """
    Manages scheduled SOP executions.
    
    Stores schedules in a JSON file and provides methods to:
    - Add/remove/update schedules
    - Check which schedules are due
    - Calculate next run times
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize scheduler with storage path."""
        self.storage_path = storage_path or Path(__file__).parent.parent.parent / "data" / "schedules.json"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._schedules: Dict[str, Schedule] = {}
        self._load()
    
    def _load(self):
        """Load schedules from storage."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    for sched_data in data.get('schedules', []):
                        sched = Schedule.from_dict(sched_data)
                        self._schedules[sched.id] = sched
            except Exception as e:
                print(f"Error loading schedules: {e}")
    
    def _save(self):
        """Save schedules to storage."""
        data = {
            'schedules': [s.to_dict() for s in self._schedules.values()],
            'updated_at': datetime.now().isoformat()
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_schedule(self, schedule: Schedule) -> str:
        """Add a new schedule."""
        # Calculate next run
        schedule.next_run = self._calculate_next_run(schedule)
        self._schedules[schedule.id] = schedule
        self._save()
        return schedule.id
    
    def remove_schedule(self, schedule_id: str) -> bool:
        """Remove a schedule."""
        if schedule_id in self._schedules:
            del self._schedules[schedule_id]
            self._save()
            return True
        return False
    
    def update_schedule(self, schedule_id: str, updates: Dict) -> bool:
        """Update a schedule."""
        if schedule_id not in self._schedules:
            return False
        
        schedule = self._schedules[schedule_id]
        for key, value in updates.items():
            if hasattr(schedule, key):
                setattr(schedule, key, value)
        
        schedule.next_run = self._calculate_next_run(schedule)
        self._save()
        return True
    
    def get_schedule(self, schedule_id: str) -> Optional[Schedule]:
        """Get a schedule by ID."""
        return self._schedules.get(schedule_id)
    
    def list_schedules(self, entity: Optional[str] = None) -> List[Schedule]:
        """List all schedules, optionally filtered by entity."""
        schedules = list(self._schedules.values())
        if entity:
            schedules = [s for s in schedules if s.entity == entity]
        return schedules
    
    def get_due_schedules(self) -> List[Schedule]:
        """Get schedules that are due to run now."""
        now = datetime.now()
        due = []
        
        for schedule in self._schedules.values():
            if not schedule.enabled:
                continue
            
            if schedule.max_runs and schedule.run_count >= schedule.max_runs:
                continue
            
            if not schedule.next_run:
                continue
            
            next_run = datetime.fromisoformat(schedule.next_run)
            if next_run <= now:
                # Check time window
                if self._in_time_window(schedule, now):
                    # Check day of week
                    if self._on_allowed_day(schedule, now):
                        due.append(schedule)
        
        return due
    
    def mark_run(self, schedule_id: str, success: bool = True):
        """Mark a schedule as having run."""
        if schedule_id not in self._schedules:
            return
        
        schedule = self._schedules[schedule_id]
        schedule.last_run = datetime.now().isoformat()
        schedule.run_count += 1
        schedule.next_run = self._calculate_next_run(schedule)
        self._save()
    
    def _calculate_next_run(self, schedule: Schedule) -> Optional[str]:
        """Calculate the next run time for a schedule."""
        now = datetime.now()
        
        if schedule.schedule_type == ScheduleType.ONCE:
            # One-time run
            if schedule.last_run:
                return None  # Already ran
            return schedule.expression  # ISO datetime
        
        elif schedule.schedule_type == ScheduleType.INTERVAL:
            # Interval like "4h", "30m", "1d"
            interval = self._parse_interval(schedule.expression)
            if schedule.last_run:
                last = datetime.fromisoformat(schedule.last_run)
                return (last + interval).isoformat()
            return (now + interval).isoformat()
        
        elif schedule.schedule_type == ScheduleType.DAILY:
            # Daily at specific time
            target_time = datetime.strptime(schedule.expression, "%H:%M").time()
            next_run = datetime.combine(now.date(), target_time)
            if next_run <= now:
                next_run += timedelta(days=1)
            return next_run.isoformat()
        
        elif schedule.schedule_type == ScheduleType.WEEKLY:
            # Weekly on specific day at time (e.g., "MON 09:00")
            parts = schedule.expression.split()
            day_map = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6}
            target_day = day_map.get(parts[0].upper(), 0)
            target_time = datetime.strptime(parts[1] if len(parts) > 1 else "09:00", "%H:%M").time()
            
            days_ahead = target_day - now.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            
            next_run = datetime.combine(now.date() + timedelta(days=days_ahead), target_time)
            return next_run.isoformat()
        
        elif schedule.schedule_type == ScheduleType.CRON:
            # Simplified cron (would need croniter for full support)
            # For now, just return 1 hour from now as placeholder
            return (now + timedelta(hours=1)).isoformat()
        
        return None
    
    def _parse_interval(self, expression: str) -> timedelta:
        """Parse interval expression like '4h', '30m', '1d'."""
        match = re.match(r'(\d+)([smhd])', expression.lower())
        if not match:
            return timedelta(hours=1)  # Default
        
        value = int(match.group(1))
        unit = match.group(2)
        
        if unit == 's':
            return timedelta(seconds=value)
        elif unit == 'm':
            return timedelta(minutes=value)
        elif unit == 'h':
            return timedelta(hours=value)
        elif unit == 'd':
            return timedelta(days=value)
        
        return timedelta(hours=1)
    
    def _in_time_window(self, schedule: Schedule, now: datetime) -> bool:
        """Check if current time is within schedule's time window."""
        if not schedule.time_window:
            return True
        
        start = datetime.strptime(schedule.time_window.get('start', '00:00'), '%H:%M').time()
        end = datetime.strptime(schedule.time_window.get('end', '23:59'), '%H:%M').time()
        current = now.time()
        
        if start <= end:
            return start <= current <= end
        else:
            # Overnight window (e.g., 22:00 - 06:00)
            return current >= start or current <= end
    
    def _on_allowed_day(self, schedule: Schedule, now: datetime) -> bool:
        """Check if current day is in schedule's allowed days."""
        if not schedule.days_of_week:
            return True
        return now.weekday() in schedule.days_of_week


# Convenience functions
_scheduler: Optional[SOPScheduler] = None


def get_scheduler() -> SOPScheduler:
    """Get or create global scheduler instance."""
    global _scheduler
    if _scheduler is None:
        _scheduler = SOPScheduler()
    return _scheduler


def add_sop_schedule(
    sop_id: str,
    entity: str,
    schedule_type: str,
    expression: str,
    **kwargs
) -> str:
    """Add a scheduled SOP execution."""
    import uuid
    scheduler = get_scheduler()
    schedule = Schedule(
        id=str(uuid.uuid4())[:8],
        sop_id=sop_id,
        entity=entity,
        schedule_type=ScheduleType(schedule_type),
        expression=expression,
        **kwargs
    )
    return scheduler.add_schedule(schedule)


def get_due_sops() -> List[Dict]:
    """Get list of SOPs that are due to run."""
    scheduler = get_scheduler()
    return [s.to_dict() for s in scheduler.get_due_schedules()]
