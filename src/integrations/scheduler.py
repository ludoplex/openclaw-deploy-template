# src/integrations/mixpost/scheduler.py
"""
Social media content scheduler for the influencer pipeline.

Coordinates between Zoho CRM/Campaigns and Mixpost for
automated social media posting.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from .client import MixpostClient, Post


@dataclass
class ContentCalendarEntry:
    """Represents a scheduled content entry."""
    title: str
    content: str
    platforms: List[str]
    scheduled_at: datetime
    entity: str  # MHI, DSAIC, Computer Store
    campaign_type: str  # promotion, announcement, influencer, event
    influencer_handle: Optional[str] = None
    hashtags: List[str] = None
    
    def __post_init__(self):
        if self.hashtags is None:
            self.hashtags = []


class SocialScheduler:
    """
    Automated social media scheduler for the multi-entity SOP system.
    
    Integrates with Mixpost to schedule content across entities
    and for the influencer pipeline.
    """
    
    # Default hashtags per entity
    ENTITY_HASHTAGS = {
        "MHI": ["MightyHouseInc", "ITSolutions", "TechServices", "EDWOSB"],
        "DSAIC": ["DSAIC", "SaaS", "TechStartup", "CloudSolutions"],
        "ComputerStore": ["ComputerStore", "TechTraining", "ITCertification", "LANCenter"],
    }
    
    # Default posting times (hours in local time)
    OPTIMAL_POSTING_TIMES = {
        "twitter": [9, 12, 17],      # 9am, 12pm, 5pm
        "linkedin": [8, 10, 14],     # 8am, 10am, 2pm
        "instagram": [11, 14, 19],   # 11am, 2pm, 7pm
        "facebook": [9, 13, 16],     # 9am, 1pm, 4pm
        "tiktok": [12, 15, 21],      # 12pm, 3pm, 9pm
        "youtube": [14, 17, 20],     # 2pm, 5pm, 8pm
    }
    
    def __init__(self, mixpost_client: Optional[MixpostClient] = None):
        """
        Initialize the scheduler.
        
        Args:
            mixpost_client: MixpostClient instance
        """
        self.mixpost = mixpost_client or MixpostClient()
        self._calendar: List[ContentCalendarEntry] = []
    
    def set_client(self, mixpost_client: MixpostClient) -> None:
        """Set the Mixpost client."""
        self.mixpost = mixpost_client
    
    # ==================== Content Calendar ====================
    
    def add_to_calendar(self, entry: ContentCalendarEntry) -> None:
        """Add an entry to the content calendar."""
        self._calendar.append(entry)
    
    def get_calendar(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        entity: Optional[str] = None
    ) -> List[ContentCalendarEntry]:
        """
        Get content calendar entries.
        
        Args:
            start_date: Filter by start date
            end_date: Filter by end date
            entity: Filter by entity
            
        Returns:
            List of ContentCalendarEntry objects
        """
        entries = self._calendar
        
        if start_date:
            entries = [e for e in entries if e.scheduled_at >= start_date]
        if end_date:
            entries = [e for e in entries if e.scheduled_at <= end_date]
        if entity:
            entries = [e for e in entries if e.entity == entity]
        
        return sorted(entries, key=lambda e: e.scheduled_at)
    
    def sync_calendar_to_mixpost(
        self,
        workspace_id: Optional[str] = None
    ) -> List[Post]:
        """
        Sync content calendar to Mixpost.
        
        Creates posts in Mixpost for all pending calendar entries.
        
        Args:
            workspace_id: Optional workspace ID
            
        Returns:
            List of created Post objects
        """
        created_posts = []
        
        for entry in self._calendar:
            # Skip past entries
            if entry.scheduled_at < datetime.now():
                continue
            
            # Combine entity hashtags with entry hashtags
            all_hashtags = self.ENTITY_HASHTAGS.get(entry.entity, []) + entry.hashtags
            hashtag_str = " ".join(f"#{tag}" for tag in all_hashtags)
            
            full_content = f"{entry.content}\n\n{hashtag_str}"
            
            # Get accounts for specified platforms
            accounts = self.mixpost.get_accounts(workspace_id)
            account_ids = [
                acc.id for acc in accounts
                if acc.provider.lower() in [p.lower() for p in entry.platforms]
            ]
            
            if account_ids:
                post = self.mixpost.create_post(
                    content=full_content,
                    account_ids=account_ids,
                    schedule_at=entry.scheduled_at,
                    workspace_id=workspace_id
                )
                created_posts.append(post)
        
        return created_posts
    
    # ==================== Automated Scheduling ====================
    
    def schedule_announcement(
        self,
        title: str,
        content: str,
        entity: str,
        platforms: Optional[List[str]] = None,
        schedule_at: Optional[datetime] = None,
        workspace_id: Optional[str] = None
    ) -> List[Post]:
        """
        Schedule an announcement across platforms.
        
        Args:
            title: Announcement title
            content: Announcement content
            entity: Entity making announcement
            platforms: Target platforms (all if None)
            schedule_at: Schedule time (next optimal time if None)
            workspace_id: Optional workspace ID
            
        Returns:
            List of created Post objects
        """
        if platforms is None:
            platforms = ["twitter", "linkedin", "facebook"]
        
        if schedule_at is None:
            schedule_at = self._get_next_optimal_time(platforms[0])
        
        entry = ContentCalendarEntry(
            title=title,
            content=content,
            platforms=platforms,
            scheduled_at=schedule_at,
            entity=entity,
            campaign_type="announcement",
        )
        
        self.add_to_calendar(entry)
        return self.sync_calendar_to_mixpost(workspace_id)
    
    def schedule_influencer_feature(
        self,
        influencer_handle: str,
        influencer_name: str,
        achievement: str,
        platforms: Optional[List[str]] = None,
        workspace_id: Optional[str] = None
    ) -> List[Post]:
        """
        Schedule a post featuring an influencer.
        
        Args:
            influencer_handle: Influencer's social handle
            influencer_name: Influencer's display name
            achievement: Achievement to highlight
            platforms: Target platforms
            workspace_id: Optional workspace ID
            
        Returns:
            List of created Post objects
        """
        if platforms is None:
            platforms = ["twitter", "instagram", "tiktok"]
        
        content = (
            f"🌟 Spotlight: @{influencer_handle}\n\n"
            f"Congratulations to {influencer_name} for {achievement}!\n\n"
            f"We're proud to have {influencer_name} as part of our creator community. "
            f"Check out their amazing content!"
        )
        
        schedule_at = self._get_next_optimal_time(platforms[0])
        
        entry = ContentCalendarEntry(
            title=f"Influencer Feature: {influencer_name}",
            content=content,
            platforms=platforms,
            scheduled_at=schedule_at,
            entity="ComputerStore",
            campaign_type="influencer",
            influencer_handle=influencer_handle,
            hashtags=["CreatorSpotlight", "InfluencerProgram"],
        )
        
        self.add_to_calendar(entry)
        return self.sync_calendar_to_mixpost(workspace_id)
    
    def schedule_certification_celebration(
        self,
        student_name: str,
        certification: str,
        social_handle: Optional[str] = None,
        platforms: Optional[List[str]] = None,
        workspace_id: Optional[str] = None
    ) -> List[Post]:
        """
        Schedule a post celebrating a student's certification.
        
        Args:
            student_name: Student's name
            certification: Certification achieved
            social_handle: Optional social handle to tag
            platforms: Target platforms
            workspace_id: Optional workspace ID
            
        Returns:
            List of created Post objects
        """
        if platforms is None:
            platforms = ["linkedin", "twitter", "facebook"]
        
        handle_mention = f" @{social_handle}" if social_handle else ""
        
        content = (
            f"🎉 Certification Achievement!\n\n"
            f"Congratulations to {student_name}{handle_mention} "
            f"for earning their {certification} certification!\n\n"
            f"Hard work pays off! Ready for the next level of their IT career. "
            f"We're proud to be part of their journey."
        )
        
        schedule_at = self._get_next_optimal_time(platforms[0])
        
        entry = ContentCalendarEntry(
            title=f"Certification: {student_name} - {certification}",
            content=content,
            platforms=platforms,
            scheduled_at=schedule_at,
            entity="ComputerStore",
            campaign_type="announcement",
            hashtags=["Certified", certification.replace(" ", ""), "ITTraining"],
        )
        
        self.add_to_calendar(entry)
        return self.sync_calendar_to_mixpost(workspace_id)
    
    def schedule_partner_campaign(
        self,
        partner_name: str,
        campaign_content: List[str],
        schedule_days: int = 7,
        platforms: Optional[List[str]] = None,
        entity: str = "MHI",
        workspace_id: Optional[str] = None
    ) -> List[Post]:
        """
        Schedule a multi-day partner promotion campaign.
        
        Args:
            partner_name: Partner/sponsor name
            campaign_content: List of content pieces
            schedule_days: Days to spread content over
            platforms: Target platforms
            entity: Entity running campaign
            workspace_id: Optional workspace ID
            
        Returns:
            List of created Post objects
        """
        if platforms is None:
            platforms = ["twitter", "linkedin", "facebook"]
        
        posts = []
        now = datetime.now()
        
        for i, content in enumerate(campaign_content):
            # Spread posts across schedule_days
            day_offset = (i * schedule_days) // len(campaign_content)
            post_date = now + timedelta(days=day_offset)
            schedule_at = self._get_next_optimal_time(platforms[0], post_date)
            
            entry = ContentCalendarEntry(
                title=f"Partner Campaign: {partner_name} #{i+1}",
                content=content,
                platforms=platforms,
                scheduled_at=schedule_at,
                entity=entity,
                campaign_type="promotion",
                hashtags=["Partner", partner_name.replace(" ", "")],
            )
            
            self.add_to_calendar(entry)
        
        return self.sync_calendar_to_mixpost(workspace_id)
    
    # ==================== Helpers ====================
    
    def _get_next_optimal_time(
        self,
        platform: str,
        base_date: Optional[datetime] = None
    ) -> datetime:
        """Get the next optimal posting time for a platform."""
        now = base_date or datetime.now()
        optimal_hours = self.OPTIMAL_POSTING_TIMES.get(platform.lower(), [9, 12, 17])
        
        current_hour = now.hour
        
        # Find next optimal hour today
        for hour in optimal_hours:
            if hour > current_hour:
                return now.replace(hour=hour, minute=0, second=0, microsecond=0)
        
        # No more optimal times today, use first time tomorrow
        tomorrow = now + timedelta(days=1)
        return tomorrow.replace(hour=optimal_hours[0], minute=0, second=0, microsecond=0)
    
    # ==================== SOP Integration ====================
    
    def handle_sop_event(
        self,
        event_type: str,
        data: Dict[str, Any],
        workspace_id: Optional[str] = None
    ) -> List[Post]:
        """
        Handle SOP events that should trigger social posts.
        
        Args:
            event_type: Type of SOP event
            data: Event data
            workspace_id: Optional workspace ID
            
        Returns:
            List of created Post objects
        """
        handlers = {
            "certification_achieved": self._handle_certification,
            "influencer_tier_up": self._handle_influencer_tier,
            "deal_closed": self._handle_deal_closed,
            "new_partnership": self._handle_partnership,
        }
        
        handler = handlers.get(event_type)
        if handler:
            return handler(data, workspace_id)
        
        return []
    
    def _handle_certification(
        self,
        data: Dict[str, Any],
        workspace_id: Optional[str]
    ) -> List[Post]:
        """Handle certification achievement event."""
        return self.schedule_certification_celebration(
            student_name=data.get("student_name", ""),
            certification=data.get("certification", ""),
            social_handle=data.get("social_handle"),
            workspace_id=workspace_id
        )
    
    def _handle_influencer_tier(
        self,
        data: Dict[str, Any],
        workspace_id: Optional[str]
    ) -> List[Post]:
        """Handle influencer tier upgrade event."""
        tier = data.get("new_tier", "")
        achievement = f"reaching {tier} tier in our influencer program"
        
        return self.schedule_influencer_feature(
            influencer_handle=data.get("social_handle", ""),
            influencer_name=data.get("name", ""),
            achievement=achievement,
            workspace_id=workspace_id
        )
    
    def _handle_deal_closed(
        self,
        data: Dict[str, Any],
        workspace_id: Optional[str]
    ) -> List[Post]:
        """Handle major deal closure event."""
        # Only post for significant public deals
        if not data.get("public_announcement"):
            return []
        
        return self.schedule_announcement(
            title=f"New Partnership: {data.get('account_name')}",
            content=data.get("announcement_content", ""),
            entity=data.get("entity", "MHI"),
            workspace_id=workspace_id
        )
    
    def _handle_partnership(
        self,
        data: Dict[str, Any],
        workspace_id: Optional[str]
    ) -> List[Post]:
        """Handle new partnership event."""
        return self.schedule_announcement(
            title=f"Partnership: {data.get('partner_name')}",
            content=data.get("content", ""),
            entity=data.get("entity", "MHI"),
            workspace_id=workspace_id
        )

