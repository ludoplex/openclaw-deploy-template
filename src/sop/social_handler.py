# src/sop/social_handler.py
"""
Social media step handlers for SOP Engine.
Integrates with MixPost for scheduling and posting.
"""

import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from .step_types import (
    Entity, Platform, VoiceProfile,
    SocialPostConfig, ContentGenerateConfig,
    get_entity_config, get_platform_config, adapt_content_for_platform,
)


@dataclass
class StepResult:
    """Result of a step execution."""
    step_id: str
    step_name: str
    success: bool
    error: Optional[str] = None
    data: Dict[str, Any] = None
    duration_ms: int = 0
    
    def __post_init__(self):
        if self.data is None:
            self.data = {}


class SocialPostHandler:
    """
    Handles social_post step type.
    Posts content to social media via MixPost integration.
    """
    
    def __init__(self, mixpost_client=None):
        """
        Initialize the handler.
        
        Args:
            mixpost_client: MixPost API client instance
        """
        self.mixpost_client = mixpost_client
    
    def handle(
        self,
        step: Any,
        event: Dict[str, Any],
        sop: Any,
    ) -> StepResult:
        """
        Execute a social_post step.
        
        Args:
            step: Step definition
            event: Trigger event data
            sop: Parent SOP definition
            
        Returns:
            StepResult with execution details
        """
        try:
            config = self._parse_config(step, event, sop)
            
            # Validate we have content
            if not config.content and not config.template:
                return StepResult(
                    step_id=step.id,
                    step_name=step.name,
                    success=False,
                    error="No content or template provided"
                )
            
            # Resolve template if needed
            content = config.content
            if config.template:
                content = self._resolve_template(config.template, config.variables)
            
            # Add hashtags
            if config.hashtags:
                content += "\n\n" + " ".join(config.hashtags)
            
            # Create posts for each platform
            results = []
            for platform in config.platforms:
                platform_content = adapt_content_for_platform(
                    content,
                    platform,
                    Entity(sop.entity) if hasattr(sop, 'entity') else None
                )
                
                # Apply platform-specific overrides
                if platform.value in config.platform_overrides:
                    overrides = config.platform_overrides[platform.value]
                    if "content" in overrides:
                        platform_content = overrides["content"]
                
                result = self._post_to_platform(
                    platform=platform,
                    content=platform_content,
                    media=config.media,
                    schedule_type=config.schedule_type,
                    scheduled_at=config.scheduled_at,
                )
                results.append(result)
            
            # Check if all succeeded
            all_success = all(r.get("success", False) for r in results)
            
            return StepResult(
                step_id=step.id,
                step_name=step.name,
                success=all_success,
                data={
                    "platforms": [p.value for p in config.platforms],
                    "results": results,
                    "content_length": len(content),
                }
            )
            
        except Exception as e:
            return StepResult(
                step_id=step.id,
                step_name=step.name,
                success=False,
                error=str(e)
            )
    
    def _parse_config(
        self,
        step: Any,
        event: Dict[str, Any],
        sop: Any,
    ) -> SocialPostConfig:
        """Parse step config into SocialPostConfig."""
        config_data = getattr(step, 'config', {}) or {}
        if isinstance(config_data, dict):
            pass
        else:
            config_data = {}
        
        # Parse platforms
        platforms_raw = config_data.get("platforms", [])
        platforms = []
        for p in platforms_raw:
            try:
                platforms.append(Platform(p) if isinstance(p, str) else p)
            except ValueError:
                pass
        
        # If no platforms specified, use entity defaults
        if not platforms and hasattr(sop, 'entity'):
            entity_config = get_entity_config(Entity(sop.entity))
            primary = entity_config.get("platforms", {}).get("primary", [])
            platforms = primary[:2]  # Default to first 2 primary platforms
        
        # Resolve content with variables
        content = config_data.get("content", "")
        variables = {**event.get("data", {}), **config_data.get("variables", {})}
        
        if content:
            content = self._interpolate_variables(content, variables)
        
        # Get entity hashtags if not specified
        hashtags = config_data.get("hashtags", [])
        if not hashtags and hasattr(sop, 'entity'):
            entity_config = get_entity_config(Entity(sop.entity))
            hashtags = entity_config.get("hashtags", [])[:3]
        
        return SocialPostConfig(
            platforms=platforms,
            content=content,
            template=config_data.get("template"),
            variables=variables,
            media=config_data.get("media", []),
            hashtags=hashtags,
            schedule_type=config_data.get("schedule_type", "immediate"),
            scheduled_at=config_data.get("scheduled_at"),
            entity_voice=config_data.get("entity_voice"),
            platform_overrides=config_data.get("platform_overrides", {}),
        )
    
    def _interpolate_variables(self, template: str, variables: Dict[str, Any]) -> str:
        """Replace {{variable}} placeholders with values."""
        result = template
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        return result
    
    def _resolve_template(self, template_id: str, variables: Dict[str, Any]) -> str:
        """Load and resolve a content template."""
        # TODO: Load from template store
        # For now, return placeholder
        return f"[Template: {template_id}]"
    
    def _post_to_platform(
        self,
        platform: Platform,
        content: str,
        media: List[Dict[str, str]],
        schedule_type: str,
        scheduled_at: Optional[datetime],
    ) -> Dict[str, Any]:
        """
        Post content to a specific platform via MixPost.
        
        Returns:
            Dict with success status and details
        """
        if not self.mixpost_client:
            # Dry run mode - return what would be posted
            return {
                "success": True,
                "dry_run": True,
                "platform": platform.value,
                "content": content[:100] + "..." if len(content) > 100 else content,
                "media_count": len(media),
                "schedule_type": schedule_type,
            }
        
        try:
            # Map to MixPost API
            post_data = {
                "content": content,
                "platforms": [platform.value],
                "media": media,
            }
            
            if schedule_type == "scheduled" and scheduled_at:
                post_data["scheduled_at"] = scheduled_at.isoformat()
            elif schedule_type == "optimal":
                # Use platform's best posting times
                platform_config = get_platform_config(platform)
                best_times = platform_config.get("best_times", ["12:00"])
                # Schedule for next best time
                post_data["scheduled_at"] = self._next_best_time(best_times)
            
            # Call MixPost API
            response = self.mixpost_client.create_post(post_data)
            
            return {
                "success": True,
                "platform": platform.value,
                "post_id": response.get("id"),
                "scheduled_at": post_data.get("scheduled_at"),
            }
            
        except Exception as e:
            return {
                "success": False,
                "platform": platform.value,
                "error": str(e),
            }
    
    def _next_best_time(self, best_times: List[str]) -> str:
        """Calculate next optimal posting time."""
        now = datetime.now()
        today_times = []
        
        for time_str in best_times:
            hour, minute = map(int, time_str.split(":"))
            dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if dt > now:
                today_times.append(dt)
        
        if today_times:
            return min(today_times).isoformat()
        else:
            # Next day, first best time
            hour, minute = map(int, best_times[0].split(":"))
            next_day = now + timedelta(days=1)
            return next_day.replace(hour=hour, minute=minute, second=0, microsecond=0).isoformat()


class ContentGenerateHandler:
    """
    Handles content_generate step type.
    Uses AI to generate content based on prompts.
    """
    
    def __init__(self, ai_client=None):
        """
        Initialize the handler.
        
        Args:
            ai_client: AI/LLM client for generation
        """
        self.ai_client = ai_client
    
    def handle(
        self,
        step: Any,
        event: Dict[str, Any],
        sop: Any,
    ) -> StepResult:
        """
        Execute a content_generate step.
        
        Args:
            step: Step definition
            event: Trigger event data
            sop: Parent SOP definition
            
        Returns:
            StepResult with generated content
        """
        try:
            config = self._parse_config(step, event, sop)
            
            # Build the prompt
            prompt = self._build_prompt(config, event, sop)
            
            # Generate content
            if self.ai_client:
                generated = self._generate_with_ai(prompt, config)
            else:
                # Stub mode - return placeholder
                generated = f"[Generated {config.content_type.value} content for: {prompt[:50]}...]"
            
            # Store in event context for later steps
            event.setdefault("generated", {})[config.output_variable] = generated
            
            return StepResult(
                step_id=step.id,
                step_name=step.name,
                success=True,
                data={
                    "content_type": config.content_type.value,
                    "output_variable": config.output_variable,
                    "content_length": len(generated),
                    "content_preview": generated[:200] + "..." if len(generated) > 200 else generated,
                }
            )
            
        except Exception as e:
            return StepResult(
                step_id=step.id,
                step_name=step.name,
                success=False,
                error=str(e)
            )
    
    def _parse_config(
        self,
        step: Any,
        event: Dict[str, Any],
        sop: Any,
    ) -> ContentGenerateConfig:
        """Parse step config into ContentGenerateConfig."""
        config_data = getattr(step, 'config', {}) or {}
        
        return ContentGenerateConfig(
            content_type=ContentGenerateConfig(config_data.get("type", "social_post")),
            prompt_template=config_data.get("prompt_template", ""),
            variables={**event.get("data", {}), **config_data.get("variables", {})},
            tone=config_data.get("tone", "professional"),
            length=config_data.get("length", "medium"),
            output_variable=config_data.get("output_variable", "generated_content"),
            model=config_data.get("model"),
            max_tokens=config_data.get("max_tokens", 500),
            temperature=config_data.get("temperature", 0.7),
        )
    
    def _build_prompt(
        self,
        config: ContentGenerateConfig,
        event: Dict[str, Any],
        sop: Any,
    ) -> str:
        """Build the AI prompt from template and context."""
        prompt = config.prompt_template
        
        # Interpolate variables
        for key, value in config.variables.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in prompt:
                prompt = prompt.replace(placeholder, str(value))
        
        # Add entity context
        if hasattr(sop, 'entity'):
            entity_config = get_entity_config(Entity(sop.entity))
            tone_guidelines = entity_config.get("tone_guidelines", "")
            prompt = f"""
{tone_guidelines}

Tone: {config.tone}
Length: {config.length}

Task: {prompt}
"""
        
        return prompt.strip()
    
    def _generate_with_ai(self, prompt: str, config: ContentGenerateConfig) -> str:
        """Generate content using AI client."""
        response = self.ai_client.generate(
            prompt=prompt,
            model=config.model,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
        )
        return response.get("content", "")


class CrossEntityTriggerHandler:
    """
    Handles cross_entity_trigger step type.
    Triggers SOPs in other entities.
    """
    
    def __init__(self, sop_engine=None):
        """
        Initialize the handler.
        
        Args:
            sop_engine: Reference to main SOP engine for cross-entity calls
        """
        self.sop_engine = sop_engine
    
    def handle(
        self,
        step: Any,
        event: Dict[str, Any],
        sop: Any,
    ) -> StepResult:
        """
        Execute a cross_entity_trigger step.
        
        Args:
            step: Step definition
            event: Trigger event data
            sop: Parent SOP definition
            
        Returns:
            StepResult with trigger details
        """
        try:
            config_data = getattr(step, 'config', {}) or {}
            
            target_entity = config_data.get("target_entity")
            target_sop = config_data.get("target_sop")
            payload = config_data.get("payload", {})
            wait_for_completion = config_data.get("wait_for_completion", False)
            
            if not target_entity or not target_sop:
                return StepResult(
                    step_id=step.id,
                    step_name=step.name,
                    success=False,
                    error="target_entity and target_sop are required"
                )
            
            # Build cross-entity event
            cross_event = {
                "event_type": "cross_entity",
                "source_entity": sop.entity if hasattr(sop, 'entity') else "unknown",
                "source_sop": sop.id if hasattr(sop, 'id') else "unknown",
                "data": {**event.get("data", {}), **payload},
            }
            
            if self.sop_engine:
                # Get target SOP
                target_definition = self.sop_engine.get_definition(target_sop)
                if not target_definition:
                    return StepResult(
                        step_id=step.id,
                        step_name=step.name,
                        success=False,
                        error=f"Target SOP not found: {target_sop}"
                    )
                
                if wait_for_completion:
                    # Execute synchronously
                    result = self.sop_engine.execute_sop(target_definition, cross_event)
                    return StepResult(
                        step_id=step.id,
                        step_name=step.name,
                        success=result.success,
                        data={
                            "target_entity": target_entity,
                            "target_sop": target_sop,
                            "target_result": {
                                "success": result.success,
                                "error": result.error,
                            }
                        }
                    )
                else:
                    # Queue for async execution (placeholder)
                    return StepResult(
                        step_id=step.id,
                        step_name=step.name,
                        success=True,
                        data={
                            "target_entity": target_entity,
                            "target_sop": target_sop,
                            "queued": True,
                        }
                    )
            else:
                # Dry run mode
                return StepResult(
                    step_id=step.id,
                    step_name=step.name,
                    success=True,
                    data={
                        "dry_run": True,
                        "target_entity": target_entity,
                        "target_sop": target_sop,
                        "payload_keys": list(payload.keys()),
                    }
                )
                
        except Exception as e:
            return StepResult(
                step_id=step.id,
                step_name=step.name,
                success=False,
                error=str(e)
            )
