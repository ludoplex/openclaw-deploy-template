# src/sop/__init__.py
"""
SOP Engine - YAML-driven workflow automation for multi-entity operations.

Supports:
- Core Zoho CRM operations (validation, tasks, records, notifications)
- Social media posting via MixPost
- AI-powered content generation
- Cross-entity pipeline triggers
"""

from .step_types import (
    StepType,
    Entity,
    Platform,
    VoiceProfile,
    ContentType,
    SocialPostConfig,
    ContentGenerateConfig,
    CrossEntityTriggerConfig,
    get_entity_config,
    get_platform_config,
    adapt_content_for_platform,
)

from .social_handler import (
    StepResult,
    SocialPostHandler,
    ContentGenerateHandler,
    CrossEntityTriggerHandler,
)

from .engine import (
    EnhancedSOPEngine,
    create_engine,
)

__all__ = [
    # Step Types
    "StepType",
    "Entity",
    "Platform",
    "VoiceProfile",
    "ContentType",
    
    # Configs
    "SocialPostConfig",
    "ContentGenerateConfig",
    "CrossEntityTriggerConfig",
    
    # Handlers
    "StepResult",
    "SocialPostHandler",
    "ContentGenerateHandler",
    "CrossEntityTriggerHandler",
    
    # Engine
    "EnhancedSOPEngine",
    "create_engine",
    
    # Utilities
    "get_entity_config",
    "get_platform_config",
    "adapt_content_for_platform",
]

__version__ = "1.0.0"
