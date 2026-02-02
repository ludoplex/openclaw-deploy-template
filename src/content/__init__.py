"""
Content Generation and Management System.

Provides:
- AI content generation (local LLM)
- Entity-specific voice profiles
- Multi-platform content templates
- Image and video prompt generation
- Content approval workflow
- Content calendar management
"""

from .generator import generate_post, generate_hashtags
from .templates import ContentTemplates
from .calendar import ContentCalendar
from .ai_generator import AIContentGenerator
from .prompt_templates import (
    VOICE_PROFILES,
    SOCIAL_TEMPLATES,
    IMAGE_PROMPTS,
    VIDEO_PROMPTS,
    get_voice_profile,
    get_platform_limits,
    get_template,
    fill_template,
    get_brand_colors,
)
from .approval import (
    ContentStatus,
    ContentItem,
    ContentApprovalManager,
    get_approval_manager,
    get_pending_reviews,
    quick_approve,
    quick_reject,
)

__all__ = [
    # Generation
    "generate_post",
    "generate_hashtags",
    "ContentTemplates",
    "AIContentGenerator",
    
    # Templates
    "VOICE_PROFILES",
    "SOCIAL_TEMPLATES", 
    "IMAGE_PROMPTS",
    "VIDEO_PROMPTS",
    "get_voice_profile",
    "get_platform_limits",
    "get_template",
    "fill_template",
    "get_brand_colors",
    
    # Approval
    "ContentStatus",
    "ContentItem",
    "ContentApprovalManager",
    "get_approval_manager",
    "get_pending_reviews",
    "quick_approve",
    "quick_reject",
    
    # Calendar
    "ContentCalendar",
]
