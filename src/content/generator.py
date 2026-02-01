# src/content/generator.py
"""
Content generator facade - provides simple interface for dashboard.
Wraps ai_generator.py functionality.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import sys

# Add workspace to path
workspace = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace))

from src.content.ai_generator import (
    get_generator,
    generate_hashtags as _generate_hashtags,
    generate_content_brief,
)


def generate_post(
    entity: str,
    topic: str,
    platform: str,
    context: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a social media post.
    
    Args:
        entity: Target entity (mighty_house_inc, dsaic, computer_store)
        topic: Topic/subject of the post
        platform: Target platform (twitter, linkedin, discord, etc.)
        context: Additional context for generation
        
    Returns:
        Dict with 'content', 'char_count', 'platform', 'entity'
    """
    gen = get_generator()
    
    # Build prompt
    entity_context = {
        "mighty_house_inc": "B2B IT services, government contracting, EDWOSB small business",
        "dsaic": "SaaS developer tools, software startup, tech innovation",
        "computer_store": "PC gaming, repairs, LAN center, Wheatland Wyoming, local community",
    }
    
    platform_constraints = {
        "twitter": "Max 280 characters. Be punchy and use hashtags.",
        "linkedin": "Professional tone. 1-3 paragraphs. Include call to action.",
        "discord": "Casual/fun tone. Use emoji. No markdown tables.",
        "facebook": "Engaging and shareable. Can be longer. Ask questions.",
        "instagram": "Visual-first language. Heavy hashtag use. Emoji welcome.",
    }
    
    prompt = f"""Write a social media post for {platform}.

Business: {entity_context.get(entity, entity)}
Topic: {topic}
{f"Additional context: {context}" if context else ""}

Platform rules: {platform_constraints.get(platform, "Keep it engaging.")}

Output only the post content, no explanation:"""
    
    content = gen.llm.ask(prompt, max_tokens=300)
    
    # Adapt for platform if needed
    if platform in ["discord", "whatsapp"]:
        content = gen.adapt_for_platform(content, platform)
    
    return {
        "content": content,
        "char_count": len(content),
        "platform": platform,
        "entity": entity,
    }


def generate_hashtags(entity: str, topic: str, count: int = 5) -> List[str]:
    """
    Generate relevant hashtags.
    
    Args:
        entity: Entity context
        topic: Topic/content
        count: Number of hashtags
        
    Returns:
        List of hashtag strings
    """
    return _generate_hashtags(f"{topic} for {entity}", entity, count)


def generate_content_calendar(
    entity: str,
    days: int = 7,
    posts_per_day: int = 2,
) -> List[Dict[str, Any]]:
    """
    Generate a content calendar.
    
    Args:
        entity: Target entity
        days: Number of days to plan
        posts_per_day: Posts per day
        
    Returns:
        List of planned content items
    """
    gen = get_generator()
    
    topics_prompt = f"""Generate {days * posts_per_day} social media post topics for a {entity.replace('_', ' ')} business.
Mix of: announcements, tips, engagement questions, promotions, behind-the-scenes.

Output as a numbered list, one topic per line:"""
    
    topics_response = gen.llm.ask(topics_prompt, max_tokens=500)
    
    # Parse topics
    topics = []
    for line in topics_response.split('\n'):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-')):
            # Remove numbering
            topic = line.lstrip('0123456789.-) ').strip()
            if topic:
                topics.append(topic)
    
    # Build calendar
    from datetime import datetime, timedelta
    calendar = []
    today = datetime.now()
    
    platforms = ["twitter", "linkedin", "facebook"]
    
    for i, topic in enumerate(topics[:days * posts_per_day]):
        day_offset = i // posts_per_day
        post_date = today + timedelta(days=day_offset)
        platform = platforms[i % len(platforms)]
        
        calendar.append({
            "date": post_date.strftime("%Y-%m-%d"),
            "day": post_date.strftime("%A"),
            "topic": topic,
            "platform": platform,
            "entity": entity,
            "status": "planned",
        })
    
    return calendar
