# src/content/ai_generator.py
"""
AI-powered content generation using local LLM (Qwen via llamafile).

Integrates with templates.py to provide:
- Template variable generation
- Content variations
- Platform-specific adaptations
- Hashtag suggestions
- Tone adjustments
"""

import sys
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add workspace to path for local_llm import
workspace = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace))

from local_llm import LlamafileDelegate, ask_local, generate_json, format_for_platform
from src.content.templates import (
    ContentTemplate,
    get_template,
    render_template,
    get_templates_by_entity,
    ContentCategory,
)


class AIContentGenerator:
    """
    AI-powered content generator using local LLM.
    
    Delegates simple tasks to Qwen (local) to save cloud API costs.
    Complex reasoning still goes to Claude when needed.
    """
    
    def __init__(self):
        """Initialize with local LLM delegate."""
        self.llm = LlamafileDelegate()
        self.mode = "server" if self.llm.server_url else "cli"
    
    def generate_variation(
        self,
        template_id: str,
        variables: Dict[str, Any],
        tone: str = "professional",
    ) -> str:
        """
        Generate a content variation from a template.
        
        Args:
            template_id: Template to use
            variables: Variable values
            tone: Desired tone (professional, casual, excited, urgent)
            
        Returns:
            Generated content variation
        """
        # First render the base template
        base_content = render_template(template_id, variables)
        
        # Ask local LLM for a variation
        prompt = f"""Rewrite this social media post with a {tone} tone.
Keep the same information but vary the wording.
Output only the rewritten post, no explanation.

Original:
{base_content}

Rewritten:"""
        
        return self.llm.ask(prompt, max_tokens=300)
    
    def suggest_variables(
        self,
        template_id: str,
        context: str,
    ) -> Dict[str, str]:
        """
        Suggest variable values based on context.
        
        Args:
            template_id: Template to fill
            context: Context/description to extract values from
            
        Returns:
            Suggested variable values
        """
        template = get_template(template_id)
        if not template:
            return {}
        
        prompt = f"""Extract these fields from the context below.
Fields needed: {', '.join(template.variables)}

Context: {context}

Output valid JSON with the field names as keys:"""
        
        result = self.llm.ask(prompt, max_tokens=200, temperature=0.3)
        
        # Try to parse JSON
        import json
        try:
            start = result.find('{')
            end = result.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(result[start:end])
        except:
            pass
        
        return {}
    
    def adapt_for_platform(
        self,
        content: str,
        platform: str,
    ) -> str:
        """
        Adapt content for a specific platform.
        
        Args:
            content: Original content
            platform: Target platform (twitter, linkedin, discord, etc.)
            
        Returns:
            Platform-adapted content
        """
        return format_for_platform(content, platform)
    
    def generate_hashtags(
        self,
        content: str,
        entity: str,
        count: int = 5,
    ) -> List[str]:
        """
        Generate relevant hashtags for content.
        
        Args:
            content: Content to generate hashtags for
            entity: Entity context (mhi, dsaic, computer_store)
            count: Number of hashtags to generate
            
        Returns:
            List of hashtag suggestions
        """
        entity_context = {
            "mighty_house_inc": "government contracting, EDWOSB, IT services, small business",
            "dsaic": "SaaS, developer tools, software, tech startup",
            "computer_store": "gaming, PC repair, LAN center, Wheatland Wyoming",
        }
        
        context = entity_context.get(entity, "business")
        
        prompt = f"""Generate {count} relevant hashtags for this post.
Business context: {context}

Post: {content}

Output only the hashtags, one per line, starting with #:"""
        
        result = self.llm.ask(prompt, max_tokens=100)
        
        # Parse hashtags
        hashtags = []
        for line in result.split('\n'):
            line = line.strip()
            if line.startswith('#'):
                hashtags.append(line.split()[0])  # Take first word only
        
        return hashtags[:count]
    
    def generate_content_brief(
        self,
        entity: str,
        category: str,
        topic: str,
    ) -> Dict[str, Any]:
        """
        Generate a complete content brief with AI assistance.
        
        Args:
            entity: Target entity
            category: Content category
            topic: Topic/subject matter
            
        Returns:
            Content brief with suggested content, hashtags, timing
        """
        prompt = f"""Create a social media content brief.
Entity: {entity}
Category: {category}
Topic: {topic}

Output JSON with these fields:
- headline: Catchy headline (max 10 words)
- body: Main content (2-3 sentences)
- cta: Call to action
- suggested_platforms: List of best platforms for this content

Output only valid JSON:"""
        
        result = generate_json(f"content brief for {entity} about {topic}")
        
        # Add hashtags
        if "body" in result:
            result["hashtags"] = self.generate_hashtags(
                result.get("body", topic),
                entity,
            )
        
        return result
    
    def bulk_generate(
        self,
        template_id: str,
        variable_sets: List[Dict[str, Any]],
        platforms: List[str],
    ) -> List[Dict[str, str]]:
        """
        Generate content for multiple variable sets and platforms.
        
        Args:
            template_id: Template to use
            variable_sets: List of variable dictionaries
            platforms: Target platforms
            
        Returns:
            List of generated content items
        """
        results = []
        
        for variables in variable_sets:
            base_content = render_template(template_id, variables)
            
            for platform in platforms:
                adapted = self.adapt_for_platform(base_content, platform)
                results.append({
                    "variables": variables,
                    "platform": platform,
                    "content": adapted,
                })
        
        return results


# Convenience functions for direct use
_generator: Optional[AIContentGenerator] = None


def get_generator() -> AIContentGenerator:
    """Get or create the global generator instance."""
    global _generator
    if _generator is None:
        _generator = AIContentGenerator()
    return _generator


def generate_variation(template_id: str, variables: Dict[str, Any], tone: str = "professional") -> str:
    """Generate a content variation."""
    return get_generator().generate_variation(template_id, variables, tone)


def suggest_variables(template_id: str, context: str) -> Dict[str, str]:
    """Suggest variable values from context."""
    return get_generator().suggest_variables(template_id, context)


def generate_hashtags(content: str, entity: str, count: int = 5) -> List[str]:
    """Generate hashtags for content."""
    return get_generator().generate_hashtags(content, entity, count)


def generate_content_brief(entity: str, category: str, topic: str) -> Dict[str, Any]:
    """Generate a content brief."""
    return get_generator().generate_content_brief(entity, category, topic)
