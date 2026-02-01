# src/content/__init__.py
"""
Content management module for social media automation.
"""

from .templates import (
    ContentCategory,
    ContentTemplate,
    get_template,
    get_templates_by_entity,
    get_templates_by_category,
    render_template,
    list_templates,
    MHI_TEMPLATES,
    DSAIC_TEMPLATES,
    CS_TEMPLATES,
    ALL_TEMPLATES,
)

from .calendar import (
    AudienceType,
    Platform,
    PostingWindow,
    ScheduledPost,
    get_optimal_posting_time,
    get_weekly_schedule,
    get_monthly_theme,
    get_upcoming_key_dates,
    should_avoid_posting,
    WEEKLY_SCHEDULE,
    MONTHLY_THEMES,
)

__all__ = [
    # Templates
    "ContentCategory",
    "ContentTemplate",
    "get_template",
    "get_templates_by_entity",
    "get_templates_by_category",
    "render_template",
    "list_templates",
    "MHI_TEMPLATES",
    "DSAIC_TEMPLATES",
    "CS_TEMPLATES",
    "ALL_TEMPLATES",
    
    # Calendar
    "AudienceType",
    "Platform",
    "PostingWindow",
    "ScheduledPost",
    "get_optimal_posting_time",
    "get_weekly_schedule",
    "get_monthly_theme",
    "get_upcoming_key_dates",
    "should_avoid_posting",
    "WEEKLY_SCHEDULE",
    "MONTHLY_THEMES",
]
