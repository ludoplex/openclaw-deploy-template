# src/sop/step_types.py
"""
Extended step types for SOP Automation App.
Adds social media, content generation, and cross-entity capabilities.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


class StepType(Enum):
    """All available step types."""
    
    # --- Core Steps (existing) ---
    VALIDATION = "validation"
    NOTIFICATION = "notification"
    CREATE_TASK = "create_task"
    FIELD_UPDATE = "field_update"
    CREATE_RECORD = "create_record"
    API_CALL = "api_call"
    CONDITION = "condition"
    APPROVAL = "approval"
    
    # --- Social/Content Steps (new) ---
    SOCIAL_POST = "social_post"
    CONTENT_GENERATE = "content_generate"
    SCHEDULE_CONTENT = "schedule_content"
    
    # --- Cross-Entity Steps (new) ---
    CROSS_ENTITY_TRIGGER = "cross_entity_trigger"
    DATA_SYNC = "data_sync"
    
    # --- Utility Steps (new) ---
    DELAY = "delay"
    LOOP = "loop"
    TRANSFORM = "transform"
    WEBHOOK_SEND = "webhook_send"


class Entity(Enum):
    """Entity identifiers."""
    MIGHTY_HOUSE_INC = "mighty_house_inc"
    DSAIC = "dsaic"
    COMPUTER_STORE = "computer_store"
    CROSS_ENTITY = "cross_entity"


class Platform(Enum):
    """Social media platforms."""
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    DISCORD = "discord"
    TIKTOK = "tiktok"
    MASTODON = "mastodon"
    THREADS = "threads"
    TWITCH = "twitch"
    YOUTUBE = "youtube"


class ContentType(Enum):
    """Content types for generation."""
    SOCIAL_POST = "social_post"
    BLOG = "blog"
    EMAIL = "email"
    VIDEO_SCRIPT = "video_script"
    IMAGE_PROMPT = "image_prompt"


class VoiceProfile(Enum):
    """Brand voice profiles."""
    MHI_PROFESSIONAL = "mhi_professional"
    DSAIC_DEVELOPER = "dsaic_developer"
    CS_GAMING = "cs_gaming"


# =============================================================================
# STEP CONFIGURATIONS
# =============================================================================

@dataclass
class SocialPostConfig:
    """Configuration for social_post step."""
    platforms: List[Platform]
    content: str
    template: Optional[str] = None
    variables: Dict[str, Any] = field(default_factory=dict)
    media: List[Dict[str, str]] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    schedule_type: str = "immediate"  # immediate, scheduled, optimal
    scheduled_at: Optional[datetime] = None
    entity_voice: Optional[VoiceProfile] = None
    
    # Platform-specific overrides
    platform_overrides: Dict[str, Dict[str, Any]] = field(default_factory=dict)


@dataclass
class ContentGenerateConfig:
    """Configuration for content_generate step."""
    content_type: ContentType
    prompt_template: str
    variables: Dict[str, Any] = field(default_factory=dict)
    tone: str = "professional"  # professional, casual, enthusiastic, technical
    length: str = "medium"  # short, medium, long
    output_variable: str = "generated_content"
    
    # AI provider settings
    model: Optional[str] = None
    max_tokens: int = 500
    temperature: float = 0.7


@dataclass
class CrossEntityTriggerConfig:
    """Configuration for cross_entity_trigger step."""
    target_entity: Entity
    target_sop: str
    payload: Dict[str, Any] = field(default_factory=dict)
    wait_for_completion: bool = False
    timeout_seconds: int = 300


@dataclass
class DelayConfig:
    """Configuration for delay step."""
    duration: Optional[str] = None  # e.g., "30m", "2h", "1d"
    until: Optional[datetime] = None
    until_condition: Optional[str] = None


@dataclass
class WebhookSendConfig:
    """Configuration for webhook_send step."""
    url: str
    method: str = "POST"
    headers: Dict[str, str] = field(default_factory=dict)
    body: Dict[str, Any] = field(default_factory=dict)
    timeout_seconds: int = 30
    retry_count: int = 3


# =============================================================================
# ENTITY CONFIGURATIONS
# =============================================================================

ENTITY_CONFIGS = {
    Entity.MIGHTY_HOUSE_INC: {
        "hashtags": [
            "#MightyHouseInc",
            "#EDWOSB",
            "#GovCon",
            "#ITSolutions",
            "#SmallBusiness",
        ],
        "platforms": {
            "primary": [Platform.LINKEDIN, Platform.TWITTER],
            "secondary": [Platform.FACEBOOK],
        },
        "voice": VoiceProfile.MHI_PROFESSIONAL,
        "zoho_prefix": "MHI",
        "tone_guidelines": """
            Professional and authoritative. Focus on expertise, reliability,
            and government contracting experience. Use industry terminology
            appropriately. Emphasize EDWOSB status when relevant.
        """,
    },
    Entity.DSAIC: {
        "hashtags": [
            "#DSAIC",
            "#SaaS",
            "#DevTools",
            "#CloudSolutions",
            "#OpenSource",
        ],
        "platforms": {
            "primary": [Platform.TWITTER, Platform.DISCORD, Platform.MASTODON],
            "secondary": [Platform.LINKEDIN],
        },
        "voice": VoiceProfile.DSAIC_DEVELOPER,
        "zoho_prefix": "DSAIC",
        "tone_guidelines": """
            Technical but approachable. Developer-friendly language.
            Open source ethos. Focus on innovation, efficiency, and
            developer experience. Use code snippets when relevant.
        """,
    },
    Entity.COMPUTER_STORE: {
        "hashtags": [
            "#ComputerStore",
            "#LANCenter",
            "#Gaming",
            "#ITCertification",
            "#Wheatland",
            "#Wyoming",
        ],
        "platforms": {
            "primary": [Platform.DISCORD, Platform.FACEBOOK, Platform.TIKTOK],
            "secondary": [Platform.INSTAGRAM, Platform.TWITCH],
        },
        "voice": VoiceProfile.CS_GAMING,
        "zoho_prefix": "CS",
        "tone_guidelines": """
            Enthusiastic and community-focused. Gaming culture aware.
            Local pride (Wheatland, Wyoming). Friendly and helpful.
            Mix of professional (repairs/certs) and fun (gaming/events).
        """,
    },
}


# =============================================================================
# PLATFORM CONFIGURATIONS
# =============================================================================

PLATFORM_CONFIGS = {
    Platform.FACEBOOK: {
        "max_chars": 63206,
        "supports_markdown": False,
        "supports_hashtags": True,
        "image_formats": ["jpg", "png", "gif"],
        "video_formats": ["mp4", "mov"],
        "best_times": ["9:00", "13:00", "16:00"],
    },
    Platform.INSTAGRAM: {
        "max_chars": 2200,
        "supports_markdown": False,
        "supports_hashtags": True,
        "hashtag_limit": 30,
        "image_formats": ["jpg", "png"],
        "video_formats": ["mp4"],
        "best_times": ["11:00", "14:00", "19:00"],
    },
    Platform.TWITTER: {
        "max_chars": 280,
        "supports_markdown": False,
        "supports_hashtags": True,
        "image_formats": ["jpg", "png", "gif"],
        "video_formats": ["mp4"],
        "best_times": ["8:00", "12:00", "17:00"],
    },
    Platform.LINKEDIN: {
        "max_chars": 3000,
        "supports_markdown": True,
        "supports_hashtags": True,
        "hashtag_limit": 5,
        "image_formats": ["jpg", "png"],
        "video_formats": ["mp4"],
        "best_times": ["7:30", "12:00", "17:30"],
    },
    Platform.DISCORD: {
        "max_chars": 2000,
        "supports_markdown": True,
        "supports_tables": False,  # Important: no markdown tables!
        "supports_hashtags": False,
        "image_formats": ["jpg", "png", "gif", "webp"],
        "video_formats": ["mp4", "webm"],
        "link_suppression": True,  # Wrap in <> to suppress embeds
    },
    Platform.TIKTOK: {
        "max_chars": 2200,
        "supports_markdown": False,
        "supports_hashtags": True,
        "hashtag_limit": 100,
        "video_only": True,
        "video_formats": ["mp4"],
        "best_times": ["7:00", "10:00", "19:00"],
    },
    Platform.MASTODON: {
        "max_chars": 500,
        "supports_markdown": True,
        "supports_hashtags": True,
        "image_formats": ["jpg", "png", "gif"],
        "video_formats": ["mp4", "webm"],
    },
    Platform.TWITCH: {
        "max_chars": 500,
        "notification_only": True,
        "best_times": ["19:00", "20:00", "21:00"],
    },
}


def get_entity_config(entity: Entity) -> Dict[str, Any]:
    """Get configuration for an entity."""
    return ENTITY_CONFIGS.get(entity, {})


def get_platform_config(platform: Platform) -> Dict[str, Any]:
    """Get configuration for a platform."""
    return PLATFORM_CONFIGS.get(platform, {})


def get_entity_hashtags(entity: Entity, limit: int = 5) -> List[str]:
    """Get hashtags for an entity."""
    config = get_entity_config(entity)
    hashtags = config.get("hashtags", [])
    return hashtags[:limit]


def adapt_content_for_platform(
    content: str,
    platform: Platform,
    entity: Optional[Entity] = None,
) -> str:
    """
    Adapt content for a specific platform's requirements.
    
    Args:
        content: Original content
        platform: Target platform
        entity: Optional entity for hashtags
        
    Returns:
        Adapted content
    """
    config = get_platform_config(platform)
    max_chars = config.get("max_chars", 1000)
    
    # Truncate if needed
    if len(content) > max_chars:
        content = content[:max_chars - 3] + "..."
    
    # Handle Discord-specific formatting
    if platform == Platform.DISCORD:
        # Remove markdown tables (not supported)
        import re
        content = re.sub(r'\|[^\n]+\|', '', content)
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Wrap links to suppress embeds if multiple
        links = re.findall(r'https?://\S+', content)
        if len(links) > 1:
            for link in links[1:]:  # Keep first embed
                content = content.replace(link, f'<{link}>')
    
    # Add hashtags if supported and entity provided
    if entity and config.get("supports_hashtags"):
        hashtag_limit = config.get("hashtag_limit", 5)
        hashtags = get_entity_hashtags(entity, hashtag_limit)
        
        # Check if we have room
        hashtag_str = " " + " ".join(hashtags)
        if len(content) + len(hashtag_str) <= max_chars:
            content += hashtag_str
    
    return content
