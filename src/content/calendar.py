# src/content/calendar.py
"""
Content calendar management for scheduled social media posts.
Based on the Wheatland, WY + Global visibility strategy.
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from enum import Enum


class AudienceType(Enum):
    """Target audience type."""
    LOCAL = "local"       # Wheatland, WY & regional
    GLOBAL = "global"     # Worldwide reach
    BOTH = "both"         # Dual targeting


class Platform(Enum):
    """Social media platforms."""
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    TWITTER = "twitter"
    YOUTUBE = "youtube"
    DISCORD = "discord"
    LINKEDIN = "linkedin"


@dataclass
class PostingWindow:
    """Optimal posting time window."""
    platform: Platform
    days: List[str]  # Mon, Tue, etc.
    start_time: time  # MT timezone
    end_time: time
    audience: AudienceType
    reason: str = ""


@dataclass
class ScheduledPost:
    """A scheduled content post."""
    id: str
    platform: Platform
    scheduled_time: datetime
    content_type: str
    theme: str
    audience: AudienceType
    template_id: Optional[str] = None
    variables: Dict[str, Any] = field(default_factory=dict)
    status: str = "scheduled"  # scheduled, posted, failed


# =============================================================================
# OPTIMAL POSTING TIMES (Mountain Time)
# =============================================================================

LOCAL_POSTING_WINDOWS = [
    PostingWindow(
        platform=Platform.FACEBOOK,
        days=["Tue", "Wed", "Thu"],
        start_time=time(9, 0),
        end_time=time(11, 0),
        audience=AudienceType.LOCAL,
        reason="Seniors/adults check mid-morning"
    ),
    PostingWindow(
        platform=Platform.FACEBOOK,
        days=["Tue", "Wed", "Thu"],
        start_time=time(13, 0),
        end_time=time(15, 0),
        audience=AudienceType.LOCAL,
        reason="Lunch break browsing"
    ),
    PostingWindow(
        platform=Platform.FACEBOOK,
        days=["Sat", "Sun"],
        start_time=time(10, 0),
        end_time=time(12, 0),
        audience=AudienceType.LOCAL,
        reason="Weekend browsing before errands"
    ),
    PostingWindow(
        platform=Platform.INSTAGRAM,
        days=["Wed", "Thu", "Fri"],
        start_time=time(11, 0),
        end_time=time(13, 0),
        audience=AudienceType.LOCAL,
        reason="Lunch break scrolling"
    ),
    PostingWindow(
        platform=Platform.INSTAGRAM,
        days=["Sun"],
        start_time=time(10, 0),
        end_time=time(12, 0),
        audience=AudienceType.LOCAL,
        reason="Post-church browsing"
    ),
    PostingWindow(
        platform=Platform.TIKTOK,
        days=["Tue", "Wed", "Thu"],
        start_time=time(19, 0),
        end_time=time(21, 0),
        audience=AudienceType.LOCAL,
        reason="After dinner, teens online"
    ),
    PostingWindow(
        platform=Platform.TIKTOK,
        days=["Sat"],
        start_time=time(11, 0),
        end_time=time(13, 0),
        audience=AudienceType.LOCAL,
        reason="Weekend leisure"
    ),
]

GLOBAL_POSTING_WINDOWS = [
    PostingWindow(
        platform=Platform.FACEBOOK,
        days=["Wed", "Thu", "Fri"],
        start_time=time(7, 0),
        end_time=time(9, 0),
        audience=AudienceType.GLOBAL,
        reason="2-4 PM UTC - Europe afternoon"
    ),
    PostingWindow(
        platform=Platform.INSTAGRAM,
        days=["Tue", "Wed", "Thu"],
        start_time=time(10, 0),
        end_time=time(12, 0),
        audience=AudienceType.GLOBAL,
        reason="5-7 PM UTC - Europe evening"
    ),
    PostingWindow(
        platform=Platform.TIKTOK,
        days=["Tue", "Wed", "Thu"],
        start_time=time(17, 0),
        end_time=time(19, 0),
        audience=AudienceType.GLOBAL,
        reason="12-2 AM UTC - Asia morning"
    ),
    PostingWindow(
        platform=Platform.YOUTUBE,
        days=["Thu", "Fri", "Sat"],
        start_time=time(12, 0),
        end_time=time(15, 0),
        audience=AudienceType.GLOBAL,
        reason="7-10 PM UTC - Global prime time"
    ),
]

ALL_POSTING_WINDOWS = LOCAL_POSTING_WINDOWS + GLOBAL_POSTING_WINDOWS


# =============================================================================
# WEEKLY SCHEDULE TEMPLATE
# =============================================================================

WEEKLY_SCHEDULE = [
    # Monday
    {"day": "Mon", "platform": "facebook", "time": "09:00", "content_type": "service_spotlight", "audience": "local"},
    {"day": "Mon", "platform": "instagram", "time": "11:00", "content_type": "tip_quote", "audience": "both"},
    
    # Tuesday
    {"day": "Tue", "platform": "facebook", "time": "10:00", "content_type": "repair_promo", "audience": "local"},
    {"day": "Tue", "platform": "tiktok", "time": "19:00", "content_type": "gaming_fun", "audience": "global"},
    
    # Wednesday
    {"day": "Wed", "platform": "instagram", "time": "11:00", "content_type": "before_after", "audience": "both"},
    {"day": "Wed", "platform": "facebook", "time": "13:00", "content_type": "senior_learning", "audience": "local"},
    
    # Thursday
    {"day": "Thu", "platform": "tiktok", "time": "18:00", "content_type": "repair_video", "audience": "global"},
    {"day": "Thu", "platform": "instagram", "time": "12:00", "content_type": "reels_trending", "audience": "global"},
    
    # Friday
    {"day": "Fri", "platform": "facebook", "time": "09:00", "content_type": "weekend_gaming", "audience": "local"},
    {"day": "Fri", "platform": "instagram", "time": "11:00", "content_type": "behind_scenes", "audience": "both"},
    
    # Saturday
    {"day": "Sat", "platform": "tiktok", "time": "11:00", "content_type": "entertainment", "audience": "global"},
    {"day": "Sat", "platform": "instagram", "time": "10:00", "content_type": "customer_story", "audience": "both"},
    
    # Sunday
    {"day": "Sun", "platform": "facebook", "time": "12:00", "content_type": "community_family", "audience": "local"},
]


# =============================================================================
# SEASONAL THEMES
# =============================================================================

MONTHLY_THEMES = {
    1: {  # January
        "theme": "New Year Fresh Start",
        "focus": ["Fresh Windows installs", "tune-ups", "tax prep"],
        "key_dates": ["MLK Day (3rd Monday)"],
    },
    2: {  # February
        "theme": "Tax Refund Season",
        "focus": ["upgrades", "trade-ins", "Valentine gaming"],
        "key_dates": ["Valentine's Day", "Presidents' Day"],
    },
    3: {  # March
        "theme": "Spring Forward",
        "focus": ["spring cleaning", "gaming tournaments", "spring break"],
        "key_dates": ["Daylight Saving", "Spring Break", "March Madness"],
    },
    4: {  # April
        "theme": "Tax Deadline & Spring",
        "focus": ["tax help", "trade-in", "graduation prep"],
        "key_dates": ["April 15 Tax Deadline", "Earth Day (Apr 22)"],
    },
    5: {  # May
        "theme": "Graduation Tech",
        "focus": ["student deals", "Mother's Day", "summer prep"],
        "key_dates": ["Mother's Day (2nd Sunday)", "Memorial Day"],
    },
    6: {  # June
        "theme": "Summer Gaming",
        "focus": ["LAN parties", "kids programs", "Father's Day"],
        "key_dates": ["Father's Day (3rd Sunday)", "Summer Solstice"],
    },
    7: {  # July
        "theme": "Independence & Summer Fun",
        "focus": ["gaming events", "beat the heat", "road trip tech"],
        "key_dates": ["July 4th", "Prime Day deals"],
    },
    8: {  # August
        "theme": "Back to School",
        "focus": ["student laptops", "certifications", "school prep"],
        "key_dates": ["Back to School (late Aug)", "Wyoming State Fair"],
    },
    9: {  # September
        "theme": "Fall Fresh Start",
        "focus": ["certifications", "business services", "gaming leagues"],
        "key_dates": ["Labor Day", "Fall Equinox"],
    },
    10: {  # October
        "theme": "Halloween & Fall Gaming",
        "focus": ["horror games", "costume contests", "early holiday"],
        "key_dates": ["Halloween", "Hunting Season Opens"],
    },
    11: {  # November
        "theme": "Thankful Tech",
        "focus": ["Black Friday", "holiday prep", "gift guides"],
        "key_dates": ["Veterans Day", "Thanksgiving", "Black Friday"],
    },
    12: {  # December
        "theme": "Holiday Season",
        "focus": ["gift cards", "setup services", "New Year prep"],
        "key_dates": ["Christmas", "Boxing Day", "New Year's Eve"],
    },
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_optimal_posting_time(
    platform: Platform,
    audience: AudienceType,
    target_date: Optional[datetime] = None,
) -> datetime:
    """
    Get the optimal posting time for a platform and audience.
    
    Args:
        platform: Target platform
        audience: Target audience type
        target_date: Optional specific date (defaults to next available)
        
    Returns:
        Optimal datetime for posting
    """
    target_date = target_date or datetime.now()
    day_name = target_date.strftime("%a")
    
    # Find matching windows
    windows = [
        w for w in ALL_POSTING_WINDOWS
        if w.platform == platform
        and (w.audience == audience or w.audience == AudienceType.BOTH)
        and day_name in w.days
    ]
    
    if windows:
        window = windows[0]
        return target_date.replace(
            hour=window.start_time.hour,
            minute=window.start_time.minute,
            second=0,
            microsecond=0
        )
    
    # Default to noon if no window found
    return target_date.replace(hour=12, minute=0, second=0, microsecond=0)


def get_weekly_schedule(start_date: datetime) -> List[Dict[str, Any]]:
    """
    Generate a week's posting schedule starting from a date.
    
    Args:
        start_date: Start of the week (Monday)
        
    Returns:
        List of scheduled post dictionaries
    """
    schedule = []
    day_offsets = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
    
    for slot in WEEKLY_SCHEDULE:
        day_offset = day_offsets[slot["day"]]
        post_date = start_date + timedelta(days=day_offset)
        hour, minute = map(int, slot["time"].split(":"))
        post_time = post_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        schedule.append({
            "scheduled_time": post_time,
            "platform": slot["platform"],
            "content_type": slot["content_type"],
            "audience": slot["audience"],
        })
    
    return sorted(schedule, key=lambda x: x["scheduled_time"])


def get_monthly_theme(month: int) -> Dict[str, Any]:
    """Get the theme and focus for a given month."""
    return MONTHLY_THEMES.get(month, {"theme": "General", "focus": [], "key_dates": []})


def get_upcoming_key_dates(days_ahead: int = 30) -> List[Dict[str, Any]]:
    """
    Get upcoming key dates for content planning.
    
    Args:
        days_ahead: Number of days to look ahead
        
    Returns:
        List of upcoming key dates with suggested content
    """
    # This would be enhanced with actual date calculations
    now = datetime.now()
    current_month = now.month
    
    dates = []
    for month_offset in range(2):  # Current and next month
        month = ((current_month - 1 + month_offset) % 12) + 1
        theme = get_monthly_theme(month)
        for key_date in theme.get("key_dates", []):
            dates.append({
                "date_name": key_date,
                "month": month,
                "theme": theme["theme"],
            })
    
    return dates


def should_avoid_posting(dt: datetime) -> Tuple[bool, str]:
    """
    Check if a datetime should be avoided for posting.
    
    Based on Wheatland, WY local patterns:
    - Family dinner time: 5-7 PM
    - Sunday church: 9 AM - 12 PM (be careful)
    
    Returns:
        Tuple of (should_avoid, reason)
    """
    hour = dt.hour
    day = dt.strftime("%a")
    
    # Family dinner time
    if 17 <= hour < 19:
        return True, "Family dinner time (5-7 PM) - lower engagement"
    
    # Sunday morning church
    if day == "Sun" and 9 <= hour < 12:
        return True, "Sunday church hours - post before 9 AM or after 12 PM"
    
    return False, ""
