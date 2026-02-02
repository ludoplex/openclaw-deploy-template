"""
Content Generation and Management System.

Provides:
- AI content generation (local LLM)
- Entity-specific voice profiles
- Multi-platform content templates
- Image and video prompt generation (Canva/Sora 2)
- Content approval workflow
- Content calendar management
"""

from .generator import generate_post, generate_hashtags

# Templates (social media content templates)
from .templates import (
    ContentTemplate,
    ContentCategory,
    get_template,
    get_templates_by_entity,
    render_template,
    list_templates,
)

# AI Generator
from .ai_generator import AIContentGenerator, get_generator

# Marketing Prompt Library (Canva/Sora 2)
from .prompt_templates import (
    MediaType,
    MediaPrompt,
    ServicePrompts,
    PromptTemplateLibrary,
    get_prompt_library,
    reload_library,
)

# Media Generation Pipeline
from .media_generator import (
    RequestStatus,
    OutputFormat,
    MediaRequest,
    MediaGeneratorPipeline,
    get_media_pipeline,
)

__all__ = [
    # Generation
    "generate_post",
    "generate_hashtags",
    "AIContentGenerator",
    "get_generator",
    
    # Content Templates
    "ContentTemplate",
    "ContentCategory",
    "get_template",
    "get_templates_by_entity",
    "render_template",
    "list_templates",
    
    # Marketing Prompt Library
    "MediaType",
    "MediaPrompt",
    "ServicePrompts",
    "PromptTemplateLibrary",
    "get_prompt_library",
    "reload_library",
    
    # Media Pipeline
    "RequestStatus",
    "OutputFormat",
    "MediaRequest",
    "MediaGeneratorPipeline",
    "get_media_pipeline",
]
