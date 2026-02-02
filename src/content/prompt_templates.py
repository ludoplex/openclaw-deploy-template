"""
Prompt Templates for Multi-Entity Content Generation.

Entity-specific voice profiles, content templates, and media prompts
for Canva (images) and Sora 2 (videos).
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass


class ContentType(Enum):
    SOCIAL_POST = "social_post"
    IMAGE_PROMPT = "image_prompt"
    VIDEO_PROMPT = "video_prompt"
    BLOG_POST = "blog_post"
    EMAIL = "email"
    PRESS_RELEASE = "press_release"


class Platform(Enum):
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    DISCORD = "discord"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    TWITCH = "twitch"
    WHATNOT = "whatnot"


@dataclass
class VoiceProfile:
    """Brand voice configuration."""
    name: str
    tone: str
    personality: str
    keywords: List[str]
    emoji_style: str
    hashtags: List[str]
    avoid: List[str]


# =============================================================================
# ENTITY VOICE PROFILES
# =============================================================================

VOICE_PROFILES: Dict[str, VoiceProfile] = {
    "mighty_house_inc": VoiceProfile(
        name="Mighty House Inc.",
        tone="Professional, trustworthy, community-focused",
        personality="Your reliable local tech experts who treat every customer like family",
        keywords=["local", "trusted", "expert", "community", "quality", "reliable"],
        emoji_style="moderate",  # Professional but warm
        hashtags=["#MightyHouseInc", "#LocalTech", "#TechRepair", "#WheatlandWY", "#CommunityTech"],
        avoid=["slang", "overly casual", "aggressive sales language"]
    ),
    
    "dsaic": VoiceProfile(
        name="DSAIC",
        tone="Developer-friendly, innovative, technical but approachable",
        personality="Fellow developers who understand the craft and ship quality tools",
        keywords=["developer", "tools", "productivity", "open-source", "API", "integration"],
        emoji_style="minimal",  # Clean, dev-focused
        hashtags=["#DevTools", "#SaaS", "#DeveloperExperience", "#API", "#OpenSource"],
        avoid=["marketing speak", "buzzwords without substance", "non-technical hype"]
    ),
    
    "computer_store": VoiceProfile(
        name="The Computer Store",
        tone="Fun, energetic, gaming-enthusiast, community hub",
        personality="Your local gaming hangout run by people who actually play",
        keywords=["gaming", "LAN party", "esports", "community", "fun", "tournament"],
        emoji_style="heavy",  # Gaming culture loves emojis
        hashtags=["#GamingCommunity", "#LANParty", "#LocalEsports", "#PCGaming", "#WheatlandGamers"],
        avoid=["boring corporate speak", "outdated gaming references"]
    ),
}


# =============================================================================
# PLATFORM CONSTRAINTS
# =============================================================================

PLATFORM_LIMITS: Dict[str, Dict[str, Any]] = {
    "twitter": {"max_chars": 280, "supports_threads": True, "hashtag_limit": 3},
    "linkedin": {"max_chars": 3000, "supports_articles": True, "professional": True},
    "facebook": {"max_chars": 63206, "supports_long": True},
    "instagram": {"max_chars": 2200, "hashtag_limit": 30, "visual_required": True},
    "discord": {"max_chars": 2000, "supports_embeds": True, "no_markdown_tables": True},
    "tiktok": {"max_chars": 2200, "video_required": True, "trending_sounds": True},
    "youtube": {"title_max": 100, "description_max": 5000},
    "twitch": {"max_chars": 500, "streaming_focus": True},
    "whatnot": {"max_chars": 1000, "commerce_focus": True},
}


# =============================================================================
# CONTENT TEMPLATES
# =============================================================================

SOCIAL_TEMPLATES = {
    # Contract Win Announcement
    "contract_win": {
        "twitter": """🎉 Exciting news! {company} has been awarded a {contract_type} contract!

{brief_description}

Thank you to our amazing team and partners who made this possible.

{hashtags}""",
        
        "linkedin": """🏆 Contract Award Announcement

{company} is proud to announce that we have been awarded a {contract_type} contract for {project_name}.

{detailed_description}

This achievement reflects our commitment to delivering excellence in {service_area}. We're grateful for the trust placed in our team and look forward to exceeding expectations.

Key Highlights:
• {highlight_1}
• {highlight_2}
• {highlight_3}

{hashtags}""",
        
        "discord": """🎊 **BIG NEWS!**

We just won a {contract_type} contract!

{brief_description}

Thank you to everyone who made this happen! 🙏""",
    },
    
    # Gaming Event
    "gaming_event": {
        "twitter": """🎮 {event_type} ALERT!

📅 {date}
🕐 {time}
🏆 {prize_info}

{brief_description}

Sign up: {signup_link}

{hashtags}""",
        
        "discord": """# 🎮 {event_name}

**When:** {date} at {time}
**Where:** The Computer Store, Wheatland
**Prize Pool:** {prize_info}

{detailed_description}

**Games:**
{game_list}

**How to Enter:**
{entry_info}

React with 🎮 if you're coming!""",
        
        "tiktok": """🔥 {event_type} this {day}!

{prize_info} up for grabs 💰
{game} tournament 🎮

Link in bio to sign up ⬆️

{hashtags}""",
        
        "facebook": """🎮 {event_name} 🎮

Join us for an epic {event_type} at The Computer Store!

📅 Date: {date}
⏰ Time: {time}
📍 Location: The Computer Store, Wheatland, WY
🏆 Prizes: {prize_info}

{detailed_description}

{entry_info}

Tag your squad! 👥

{hashtags}""",
    },
    
    # Product Launch
    "product_launch": {
        "twitter": """🚀 Introducing {product_name}!

{value_proposition}

{key_feature}

Try it now: {link}

{hashtags}""",
        
        "linkedin": """🚀 Announcing {product_name}

We're excited to introduce our latest solution for {target_audience}.

**The Problem:**
{problem_statement}

**Our Solution:**
{product_name} provides {solution_description}

**Key Features:**
• {feature_1}
• {feature_2}
• {feature_3}

{cta}

{hashtags}""",
        
        "discord": """# 🚀 New Release: {product_name}

{value_proposition}

**What's New:**
{feature_list}

**Get Started:**
{getting_started}

Questions? Drop them below! 👇""",
    },
    
    # Live Show (Whatnot/Twitch)
    "live_show": {
        "whatnot": """🔴 GOING LIVE!

{show_title}

{show_description}

Starting at {time}!

Follow to get notified 🔔""",
        
        "twitch": """🔴 LIVE NOW

{stream_title}

{game_or_activity}

Come hang out! 💬""",
        
        "discord": """# 🔴 LIVE IN {countdown}!

**{show_title}**

{show_description}

**Platform:** {platform}
**Time:** {time}

Set a reminder! 🔔""",
    },
}


# =============================================================================
# IMAGE PROMPT TEMPLATES (for Canva/DALL-E/Midjourney)
# =============================================================================

IMAGE_PROMPTS = {
    "contract_win": {
        "celebration": """Create a professional celebration graphic for a government contract win. 
Include: handshake silhouette, American flag elements (subtle), achievement badge/trophy icon.
Colors: Navy blue, gold accents, white.
Text space for: Company name, "Contract Awarded", contract value.
Style: Corporate, trustworthy, patriotic but not over-the-top.
Dimensions: {dimensions}""",
        
        "announcement": """Design a professional announcement banner for a business achievement.
Include: Company logo placeholder, confetti elements (subtle), upward arrow or growth icon.
Colors: {brand_colors}
Text: "{headline}"
Style: LinkedIn-appropriate, professional, celebratory.
Dimensions: {dimensions}""",
    },
    
    "gaming_event": {
        "tournament": """Create an exciting esports tournament announcement graphic.
Include: Gaming controllers, trophy icon, neon glow effects, energy/action elements.
Colors: {brand_colors}, neon accents (purple, cyan, pink).
Text space for: Event name, date, prize pool.
Style: Gaming/esports aesthetic, energetic, modern.
Dimensions: {dimensions}""",
        
        "lan_party": """Design a LAN party event poster.
Include: Multiple gaming setups, social/community vibe, RGB lighting effects.
Colors: Dark background with {brand_colors} accents.
Text: "{event_name}" prominently displayed.
Style: Gaming community, fun, welcoming to all skill levels.
Dimensions: {dimensions}""",
    },
    
    "product_launch": {
        "announcement": """Create a product launch announcement graphic.
Include: Abstract tech elements, launch/rocket metaphor (subtle), feature icons.
Colors: {brand_colors}
Text space for: Product name, tagline, key feature.
Style: Modern SaaS, clean, developer-friendly.
Dimensions: {dimensions}""",
        
        "feature_highlight": """Design a feature highlight graphic for {feature_name}.
Include: Icon representing the feature, before/after or problem/solution visual.
Colors: {brand_colors}
Style: Clean, informative, technical but accessible.
Dimensions: {dimensions}""",
    },
    
    "service_promo": {
        "repair": """Create a tech repair service promotional graphic.
Include: Tools icon, computer/phone being fixed, transformation visual (broken to fixed).
Colors: {brand_colors}, trust-inspiring blue, problem-red to solution-green gradient.
Text: "{service_name} - ${price}"
Style: Professional, trustworthy, local business feel.
Dimensions: {dimensions}""",
        
        "special_offer": """Design a special offer/discount promotional graphic.
Include: Discount badge, service icon, urgency elements (limited time).
Colors: {brand_colors}, attention-grabbing accents.
Text: "{offer_headline}", "{discount_amount}"
Style: Eye-catching but not cheap-looking, trustworthy.
Dimensions: {dimensions}""",
    },
}


# =============================================================================
# VIDEO PROMPT TEMPLATES (for Sora 2/Runway/Pika)
# =============================================================================

VIDEO_PROMPTS = {
    "contract_win": {
        "celebration": """Professional celebration video for contract win announcement.
Scene 1 (3s): Office team working diligently, focused atmosphere.
Scene 2 (3s): Email/notification arrives with good news, excitement begins.
Scene 3 (4s): Team celebration - handshakes, high-fives, professional joy.
Scene 4 (5s): Text overlay: "{company} Awarded {contract_type}" with logo.
Style: Corporate, warm, authentic joy. Not over-the-top.
Music: Uplifting, professional, subtle build to celebration.
Duration: 15 seconds.""",
    },
    
    "gaming_event": {
        "tournament_hype": """Exciting esports tournament promotional video.
Scene 1 (2s): Dramatic close-up of gaming peripherals, RGB lights.
Scene 2 (3s): Quick cuts of intense gameplay moments.
Scene 3 (3s): Crowd/community reaction shots, cheering.
Scene 4 (3s): Trophy/prize reveal with spotlight.
Scene 5 (4s): Event details text overlay with registration CTA.
Style: High energy, esports broadcast quality, modern gaming aesthetic.
Music: Electronic, building intensity, drop at trophy reveal.
Duration: 15 seconds.""",
        
        "lan_party_invite": """Welcoming LAN party invitation video.
Scene 1 (3s): Empty gaming center, lights coming on.
Scene 2 (4s): Time-lapse of people arriving, setting up.
Scene 3 (4s): Fun moments - laughing, high-fives, snacks.
Scene 4 (4s): Event details with "Join Us!" message.
Style: Warm, inclusive, community-focused. All skill levels welcome vibe.
Music: Fun, upbeat, not aggressive.
Duration: 15 seconds.""",
    },
    
    "product_launch": {
        "announcement": """Product launch announcement video for developers.
Scene 1 (3s): Developer frustrated with old way of doing things.
Scene 2 (4s): Discovery moment - finding the new product.
Scene 3 (4s): Clean UI demo showing key features.
Scene 4 (4s): Satisfaction/productivity boost visualization.
End card: Product name, tagline, website.
Style: Clean, minimal, developer-friendly aesthetic.
Music: Modern, subtle, tech-forward.
Duration: 15 seconds.""",
    },
    
    "repair_service": {
        "problem_solution": """Tech repair service promotional video.
Scene 1 (3s): Customer with broken device, frustrated expression.
Scene 2 (4s): Brings device to repair shop, friendly greeting.
Scene 3 (4s): Technician working on device, professional environment.
Scene 4 (4s): Happy customer receiving fixed device, relief/joy.
End card: Service name, price, "Same Day Service" badge.
Style: Warm, trustworthy, local business authenticity.
Music: Problem-to-solution arc, starts tense, ends uplifting.
Duration: 15 seconds.""",
    },
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_voice_profile(entity: str) -> VoiceProfile:
    """Get voice profile for an entity."""
    return VOICE_PROFILES.get(entity, VOICE_PROFILES["mighty_house_inc"])


def get_platform_limits(platform: str) -> Dict[str, Any]:
    """Get character limits and constraints for a platform."""
    return PLATFORM_LIMITS.get(platform, {"max_chars": 2000})


def get_template(content_type: str, template_name: str, platform: str = None) -> Optional[str]:
    """Get a content template."""
    if content_type == "social":
        templates = SOCIAL_TEMPLATES.get(template_name, {})
        if platform:
            return templates.get(platform)
        return templates
    elif content_type == "image":
        return IMAGE_PROMPTS.get(template_name, {})
    elif content_type == "video":
        return VIDEO_PROMPTS.get(template_name, {})
    return None


def fill_template(template: str, variables: Dict[str, Any]) -> str:
    """Fill a template with variables."""
    result = template
    for key, value in variables.items():
        result = result.replace(f"{{{key}}}", str(value))
    return result


def generate_hashtags(entity: str, topic: str, count: int = 5) -> List[str]:
    """Generate relevant hashtags for content."""
    profile = get_voice_profile(entity)
    base_tags = profile.hashtags[:3]  # Always include brand tags
    
    # Topic-specific tags would be generated by LLM
    # This is a placeholder for the structure
    topic_tags = [f"#{topic.replace(' ', '')}" for _ in range(count - 3)]
    
    return base_tags + topic_tags[:count - len(base_tags)]


def adapt_for_platform(content: str, platform: str) -> str:
    """Adapt content for platform-specific requirements."""
    limits = get_platform_limits(platform)
    max_chars = limits.get("max_chars", 2000)
    
    # Truncate if needed
    if len(content) > max_chars:
        content = content[:max_chars - 3] + "..."
    
    # Platform-specific adjustments
    if platform == "discord" and limits.get("no_markdown_tables"):
        # Convert tables to bullet lists (simplified)
        content = content.replace("|", "•")
    
    return content


# =============================================================================
# BRAND COLOR SCHEMES
# =============================================================================

BRAND_COLORS = {
    "mighty_house_inc": {
        "primary": "#1E3A5F",  # Navy blue
        "secondary": "#4A90D9",  # Lighter blue
        "accent": "#FFD700",  # Gold
        "background": "#FFFFFF",
        "text": "#333333",
    },
    "dsaic": {
        "primary": "#6366F1",  # Indigo
        "secondary": "#818CF8",  # Light indigo
        "accent": "#10B981",  # Green
        "background": "#0F172A",  # Dark slate
        "text": "#F8FAFC",
    },
    "computer_store": {
        "primary": "#8B5CF6",  # Purple
        "secondary": "#06B6D4",  # Cyan
        "accent": "#F472B6",  # Pink
        "background": "#1F2937",  # Dark gray
        "text": "#FFFFFF",
    },
}


def get_brand_colors(entity: str) -> Dict[str, str]:
    """Get brand colors for an entity."""
    return BRAND_COLORS.get(entity, BRAND_COLORS["mighty_house_inc"])
