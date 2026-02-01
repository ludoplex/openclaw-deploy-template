# src/content/templates.py
"""
Content template management for social media posts.
Provides reusable templates for different content types and entities.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class ContentCategory(Enum):
    """Content categories."""
    ANNOUNCEMENT = "announcement"
    EVENT = "event"
    PROMOTION = "promotion"
    EDUCATIONAL = "educational"
    CELEBRATION = "celebration"
    REMINDER = "reminder"
    ENGAGEMENT = "engagement"


@dataclass
class ContentTemplate:
    """A reusable content template."""
    id: str
    name: str
    entity: str
    category: ContentCategory
    platforms: List[str]
    template: str
    variables: List[str]
    hashtags: List[str] = field(default_factory=list)
    media_required: bool = False
    notes: str = ""


# =============================================================================
# MIGHTY HOUSE INC. TEMPLATES
# =============================================================================

MHI_TEMPLATES = [
    ContentTemplate(
        id="mhi_contract_win",
        name="Government Contract Win",
        entity="mighty_house_inc",
        category=ContentCategory.CELEBRATION,
        platforms=["linkedin", "twitter", "facebook"],
        template="""🎉 Exciting News!

Mighty House Inc. is proud to announce we've been awarded a contract with {{agency}}!

{{contract_description}}

As an EDWOSB-certified small business, we're committed to delivering excellence in IT solutions for our government partners.

Thank you to our amazing team! 🙏

#MightyHouseInc #EDWOSB #GovCon #SmallBusiness""",
        variables=["agency", "contract_description"],
        hashtags=["#MightyHouseInc", "#EDWOSB", "#GovCon"],
    ),
    
    ContentTemplate(
        id="mhi_capability_highlight",
        name="Capability Highlight",
        entity="mighty_house_inc",
        category=ContentCategory.EDUCATIONAL,
        platforms=["linkedin", "twitter"],
        template="""💡 Did you know?

Mighty House Inc. specializes in {{capability}}.

{{details}}

Looking for a reliable IT partner? Let's talk.

#ITSolutions #MightyHouseInc #EDWOSB""",
        variables=["capability", "details"],
    ),
    
    ContentTemplate(
        id="mhi_team_spotlight",
        name="Team Member Spotlight",
        entity="mighty_house_inc",
        category=ContentCategory.CELEBRATION,
        platforms=["linkedin", "facebook"],
        template="""👏 Team Spotlight!

Meet {{name}}, our {{role}}.

{{bio}}

We're proud to have such talented professionals on our team!

#MightyHouseInc #TeamSpotlight #SmallBusiness""",
        variables=["name", "role", "bio"],
        media_required=True,
    ),
]


# =============================================================================
# DSAIC TEMPLATES
# =============================================================================

DSAIC_TEMPLATES = [
    ContentTemplate(
        id="dsaic_feature_release",
        name="Feature Release",
        entity="dsaic",
        category=ContentCategory.ANNOUNCEMENT,
        platforms=["twitter", "discord", "mastodon"],
        template="""🚀 New Feature Alert!

{{feature_name}} is now live!

{{feature_description}}

Try it out: {{link}}

#DSAIC #DevTools #NewFeature""",
        variables=["feature_name", "feature_description", "link"],
    ),
    
    ContentTemplate(
        id="dsaic_tip",
        name="Developer Tip",
        entity="dsaic",
        category=ContentCategory.EDUCATIONAL,
        platforms=["twitter", "discord", "mastodon"],
        template="""💡 Pro Tip:

{{tip}}

{{code_example}}

#DevTips #DSAIC""",
        variables=["tip", "code_example"],
    ),
    
    ContentTemplate(
        id="dsaic_customer_story",
        name="Customer Success Story",
        entity="dsaic",
        category=ContentCategory.CELEBRATION,
        platforms=["twitter", "linkedin"],
        template="""🎉 Customer Spotlight!

{{company}} is using DSAIC to {{use_case}}.

"{{quote}}" - {{person}}, {{title}}

Thanks for being part of our community!

#DSAIC #CustomerSuccess""",
        variables=["company", "use_case", "quote", "person", "title"],
    ),
]


# =============================================================================
# COMPUTER STORE TEMPLATES
# =============================================================================

CS_TEMPLATES = [
    ContentTemplate(
        id="cs_tournament_announce",
        name="Tournament Announcement",
        entity="computer_store",
        category=ContentCategory.EVENT,
        platforms=["discord", "facebook", "twitter", "instagram"],
        template="""🎮 TOURNAMENT ALERT! 🏆

{{game}} Tournament at Computer Store!

📅 {{date}}
⏰ {{time}}
💰 Entry: {{entry_fee}}
🎁 Prizes: {{prizes}}

Register now - limited spots!

#Gaming #Tournament #ComputerStore #Wheatland""",
        variables=["game", "date", "time", "entry_fee", "prizes"],
        media_required=True,
    ),
    
    ContentTemplate(
        id="cs_stream_live",
        name="Stream Going Live",
        entity="computer_store",
        category=ContentCategory.ANNOUNCEMENT,
        platforms=["discord", "twitter"],
        template="""🔴 WE'RE LIVE!

{{stream_title}}

Join us on Twitch: twitch.tv/MightyHouseInc

{{description}}

#Live #Twitch #Gaming""",
        variables=["stream_title", "description"],
    ),
    
    ContentTemplate(
        id="cs_deal",
        name="Daily Deal",
        entity="computer_store",
        category=ContentCategory.PROMOTION,
        platforms=["discord", "facebook", "instagram"],
        template="""🔥 TODAY'S DEAL 🔥

{{item}}
Was: ${{original_price}}
NOW: ${{sale_price}}

{{details}}

In-store only. While supplies last!

#Deals #ComputerStore #Wheatland""",
        variables=["item", "original_price", "sale_price", "details"],
        media_required=True,
    ),
    
    ContentTemplate(
        id="cs_whatnot_live",
        name="Whatnot Show Promo",
        entity="computer_store",
        category=ContentCategory.EVENT,
        platforms=["discord", "facebook", "twitter", "tiktok"],
        template="""🔴 LIVE AUCTION {{time}}!

{{show_title}}

🎁 What's up for grabs:
{{featured_items}}

📺 Whatnot: whatnot.com/user/computerstorewy

Don't miss the deals!

#Whatnot #LiveSelling #Deals""",
        variables=["time", "show_title", "featured_items"],
    ),
    
    ContentTemplate(
        id="cs_repair_promo",
        name="Repair Service Promo",
        entity="computer_store",
        category=ContentCategory.PROMOTION,
        platforms=["facebook", "instagram"],
        template="""🔧 {{service_name}} - Just ${{price}}!

{{description}}

✅ {{benefit_1}}
✅ {{benefit_2}}
✅ {{benefit_3}}

Walk-ins welcome or call to schedule!
📍 Computer Store, Wheatland WY

#ComputerRepair #TechSupport #Wheatland""",
        variables=["service_name", "price", "description", "benefit_1", "benefit_2", "benefit_3"],
    ),
    
    ContentTemplate(
        id="cs_lan_night",
        name="LAN Night Promo",
        entity="computer_store",
        category=ContentCategory.EVENT,
        platforms=["discord", "facebook", "instagram"],
        template="""🎮 LAN NIGHT {{day}}! 🎮

${{hourly_rate}}/hour or ${{all_night_rate}} all-night pass!

🕹️ 15+ gaming PCs
🎯 Latest games
🍕 Snacks & drinks available

{{special_note}}

#LANParty #Gaming #Wheatland #ComputerStore""",
        variables=["day", "hourly_rate", "all_night_rate", "special_note"],
    ),
]


# =============================================================================
# TEMPLATE REGISTRY
# =============================================================================

ALL_TEMPLATES = MHI_TEMPLATES + DSAIC_TEMPLATES + CS_TEMPLATES

TEMPLATE_REGISTRY: Dict[str, ContentTemplate] = {t.id: t for t in ALL_TEMPLATES}


def get_template(template_id: str) -> Optional[ContentTemplate]:
    """Get a template by ID."""
    return TEMPLATE_REGISTRY.get(template_id)


def get_templates_by_entity(entity: str) -> List[ContentTemplate]:
    """Get all templates for an entity."""
    return [t for t in ALL_TEMPLATES if t.entity == entity]


def get_templates_by_category(category: ContentCategory) -> List[ContentTemplate]:
    """Get all templates in a category."""
    return [t for t in ALL_TEMPLATES if t.category == category]


def render_template(
    template_id: str,
    variables: Dict[str, Any],
    platform: Optional[str] = None,
) -> str:
    """
    Render a template with variables.
    
    Args:
        template_id: Template ID
        variables: Variable values
        platform: Optional platform for formatting
        
    Returns:
        Rendered content
    """
    template = get_template(template_id)
    if not template:
        raise ValueError(f"Template not found: {template_id}")
    
    content = template.template
    
    # Replace variables
    for var in template.variables:
        placeholder = "{{" + var + "}}"
        value = variables.get(var, f"[{var}]")
        content = content.replace(placeholder, str(value))
    
    return content


def list_templates() -> List[Dict[str, Any]]:
    """List all available templates."""
    return [
        {
            "id": t.id,
            "name": t.name,
            "entity": t.entity,
            "category": t.category.value,
            "platforms": t.platforms,
            "variables": t.variables,
        }
        for t in ALL_TEMPLATES
    ]
