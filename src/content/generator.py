"""
AI Content Generation using local LLM (llamafile + Qwen).
Saves Claude tokens by delegating simple content tasks locally.
"""
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add workspace to path for local_llm import
WORKSPACE = Path(__file__).parent.parent.parent
sys.path.insert(0, str(WORKSPACE))

from local_llm import LlamafileDelegate

# Entity voice profiles
VOICE_PROFILES = {
    "mighty_house_inc": {
        "tone": "professional, confident, trustworthy",
        "audience": "government contracting officers, federal agencies, small business advocates",
        "keywords": ["EDWOSB", "IT solutions", "government contracting", "small business", "excellence"],
        "avoid": ["casual language", "slang", "controversial topics"],
    },
    "dsaic": {
        "tone": "technical, innovative, developer-friendly",
        "audience": "developers, CTOs, tech leads, DevOps engineers",
        "keywords": ["SaaS", "cloud-native", "open source", "API", "automation", "DevTools"],
        "avoid": ["marketing fluff", "buzzwords without substance"],
    },
    "computer_store": {
        "tone": "friendly, exciting, community-focused",
        "audience": "gamers, students, parents, tech enthusiasts",
        "keywords": ["gaming", "LAN center", "IT certification", "Pearson VUE", "esports"],
        "avoid": ["overly technical jargon", "boring corporate speak"],
    },
}

# Platform constraints
PLATFORM_CONSTRAINTS = {
    "twitter": {"max_chars": 280, "hashtags": 3, "format": "punchy, no markdown"},
    "linkedin": {"max_chars": 3000, "hashtags": 5, "format": "professional, can use bullet points"},
    "discord": {"max_chars": 2000, "hashtags": 0, "format": "no markdown tables, wrap links in <>"},
    "facebook": {"max_chars": 5000, "hashtags": 3, "format": "casual, use emojis"},
    "instagram": {"max_chars": 2200, "hashtags": 10, "format": "visual-focused, hashtag heavy"},
    "tiktok": {"max_chars": 300, "hashtags": 5, "format": "trendy, casual, short"},
}


class ContentGenerator:
    """Generate content using local LLM delegation."""
    
    def __init__(self, llamafile_path: Optional[str] = None, model_path: Optional[str] = None):
        """Initialize with local LLM."""
        # Default paths in workspace
        if llamafile_path is None:
            llamafile_path = WORKSPACE / "bin" / "llamafile.exe"
        if model_path is None:
            model_path = WORKSPACE / "models" / "qwen2.5-7b-instruct-q3_k_m.gguf"
        
        self.delegate = LlamafileDelegate(
            llamafile_path=llamafile_path,
            model_path=model_path,
            gpu_layers=99,
            timeout=60
        )
    
    def generate_post(
        self,
        entity: str,
        topic: str,
        platform: str,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate a social media post.
        
        Args:
            entity: Entity ID (mighty_house_inc, dsaic, computer_store)
            topic: What the post is about
            platform: Target platform (twitter, linkedin, etc.)
            context: Additional context or details
            
        Returns:
            Dict with generated content and metadata
        """
        voice = VOICE_PROFILES.get(entity, VOICE_PROFILES["computer_store"])
        constraints = PLATFORM_CONSTRAINTS.get(platform, PLATFORM_CONSTRAINTS["twitter"])
        
        prompt = f"""Generate a {platform} post for a business.

Entity: {entity.replace('_', ' ').title()}
Topic: {topic}
{f'Context: {context}' if context else ''}

Voice/Tone: {voice['tone']}
Target Audience: {voice['audience']}
Keywords to include: {', '.join(voice['keywords'][:3])}

Platform constraints:
- Max {constraints['max_chars']} characters
- Use {constraints['hashtags']} hashtags
- Format: {constraints['format']}

Generate ONLY the post text, ready to publish:"""

        content = self.delegate.ask(prompt, max_tokens=400, temperature=0.7)
        
        return {
            "content": content.strip(),
            "entity": entity,
            "platform": platform,
            "topic": topic,
            "char_count": len(content),
            "generated_by": "local_llm"
        }
    
    def generate_hashtags(self, entity: str, topic: str, count: int = 5) -> List[str]:
        """Generate relevant hashtags."""
        voice = VOICE_PROFILES.get(entity, {})
        keywords = voice.get("keywords", [])
        
        prompt = f"""Generate {count} relevant hashtags for a {entity.replace('_', ' ').title()} post about: {topic}

Related keywords: {', '.join(keywords)}

Output ONLY the hashtags, one per line, with # prefix:"""

        result = self.delegate.ask(prompt, max_tokens=100, temperature=0.5)
        
        # Parse hashtags from response
        hashtags = []
        for line in result.split('\n'):
            line = line.strip()
            if line.startswith('#'):
                hashtags.append(line.split()[0])  # Take first word only
        
        return hashtags[:count]
    
    def adapt_content(self, content: str, from_platform: str, to_platform: str) -> str:
        """Adapt content from one platform to another."""
        to_constraints = PLATFORM_CONSTRAINTS.get(to_platform, PLATFORM_CONSTRAINTS["twitter"])
        
        prompt = f"""Adapt this {from_platform} post for {to_platform}.

Original post:
{content}

{to_platform} constraints:
- Max {to_constraints['max_chars']} characters
- Hashtags: {to_constraints['hashtags']}
- Format: {to_constraints['format']}

Output ONLY the adapted post:"""

        return self.delegate.ask(prompt, max_tokens=400).strip()
    
    def fill_template(self, template: str, variables: Dict[str, str]) -> str:
        """Fill a template with variables using local LLM for polish."""
        # First do simple substitution
        filled = template
        for key, value in variables.items():
            filled = filled.replace(f"{{{{{key}}}}}", value)
        
        # If still has unfilled variables, use LLM
        if "{{" in filled:
            prompt = f"""Complete this social media post template by filling in reasonable values for any remaining {{{{variable}}}} placeholders:

{filled}

Output the completed post:"""
            return self.delegate.ask(prompt, max_tokens=500).strip()
        
        return filled
    
    def summarize_for_post(self, long_text: str, platform: str = "twitter") -> str:
        """Summarize long content for a social post."""
        constraints = PLATFORM_CONSTRAINTS.get(platform, PLATFORM_CONSTRAINTS["twitter"])
        
        return self.delegate.summarize(
            long_text, 
            max_words=constraints["max_chars"] // 5  # Rough word estimate
        )


# Singleton for reuse
_generator: Optional[ContentGenerator] = None


def get_generator() -> ContentGenerator:
    """Get or create the content generator."""
    global _generator
    if _generator is None:
        _generator = ContentGenerator()
    return _generator


# Convenience functions
def generate_post(entity: str, topic: str, platform: str, context: str = None) -> Dict[str, Any]:
    """Quick access to generate_post."""
    return get_generator().generate_post(entity, topic, platform, context)


def generate_hashtags(entity: str, topic: str, count: int = 5) -> List[str]:
    """Quick access to generate_hashtags."""
    return get_generator().generate_hashtags(entity, topic, count)


if __name__ == "__main__":
    # Test
    print("Testing content generation...")
    result = generate_post(
        entity="computer_store",
        topic="Weekend LAN party tournament",
        platform="discord"
    )
    print(f"Generated content:\n{result['content']}")
    print(f"\nCharacter count: {result['char_count']}")
