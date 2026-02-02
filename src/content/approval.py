"""
Content Approval Workflow System.

Manages the lifecycle of generated content from draft to published:
1. Generate (AI creates draft)
2. Review (human reviews/edits)
3. Approve (human approves)
4. Schedule (queued for posting)
5. Publish (sent to platforms)
"""

from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path
import uuid


class ContentStatus(Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    CHANGES_REQUESTED = "changes_requested"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    REJECTED = "rejected"
    ARCHIVED = "archived"


@dataclass
class ContentItem:
    """A piece of content in the approval pipeline."""
    id: str
    entity: str
    content_type: str  # social_post, image_prompt, video_prompt
    platform: str
    content: str
    status: ContentStatus
    
    # Metadata
    topic: str = ""
    campaign: str = ""
    created_at: str = ""
    updated_at: str = ""
    created_by: str = "ai"  # ai or human
    
    # AI generation info
    prompt_used: str = ""
    model_used: str = ""
    generation_params: Dict[str, Any] = field(default_factory=dict)
    
    # Review tracking
    reviewer: Optional[str] = None
    review_notes: str = ""
    edit_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Scheduling
    scheduled_at: Optional[str] = None
    published_at: Optional[str] = None
    publish_result: Dict[str, Any] = field(default_factory=dict)
    
    # Related content (for multi-platform campaigns)
    campaign_id: Optional[str] = None
    related_content_ids: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "entity": self.entity,
            "content_type": self.content_type,
            "platform": self.platform,
            "content": self.content,
            "status": self.status.value,
            "topic": self.topic,
            "campaign": self.campaign,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "created_by": self.created_by,
            "prompt_used": self.prompt_used,
            "model_used": self.model_used,
            "generation_params": self.generation_params,
            "reviewer": self.reviewer,
            "review_notes": self.review_notes,
            "edit_history": self.edit_history,
            "scheduled_at": self.scheduled_at,
            "published_at": self.published_at,
            "publish_result": self.publish_result,
            "campaign_id": self.campaign_id,
            "related_content_ids": self.related_content_ids,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContentItem":
        data["status"] = ContentStatus(data.get("status", "draft"))
        return cls(**data)


class ContentApprovalManager:
    """
    Manages content through the approval workflow.
    
    Provides:
    - Content creation and storage
    - Status transitions
    - Review tracking
    - Bulk operations for campaigns
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path(__file__).parent.parent.parent / "data" / "content"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._content: Dict[str, ContentItem] = {}
        self._load_content()
    
    def _load_content(self):
        """Load content from storage."""
        content_file = self.storage_path / "content_items.json"
        if content_file.exists():
            with open(content_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item_data in data:
                    item = ContentItem.from_dict(item_data)
                    self._content[item.id] = item
    
    def _save_content(self):
        """Save content to storage."""
        content_file = self.storage_path / "content_items.json"
        data = [item.to_dict() for item in self._content.values()]
        with open(content_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    
    # ==================== CRUD Operations ====================
    
    def create_content(
        self,
        entity: str,
        content_type: str,
        platform: str,
        content: str,
        topic: str = "",
        campaign: str = "",
        prompt_used: str = "",
        model_used: str = "local_llm",
        campaign_id: Optional[str] = None,
    ) -> ContentItem:
        """Create a new content item in draft status."""
        item = ContentItem(
            id=str(uuid.uuid4())[:8],
            entity=entity,
            content_type=content_type,
            platform=platform,
            content=content,
            status=ContentStatus.DRAFT,
            topic=topic,
            campaign=campaign,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            prompt_used=prompt_used,
            model_used=model_used,
            campaign_id=campaign_id,
        )
        
        self._content[item.id] = item
        self._save_content()
        return item
    
    def get_content(self, content_id: str) -> Optional[ContentItem]:
        """Get a content item by ID."""
        return self._content.get(content_id)
    
    def list_content(
        self,
        entity: Optional[str] = None,
        status: Optional[ContentStatus] = None,
        platform: Optional[str] = None,
        campaign_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[ContentItem]:
        """List content with optional filters."""
        items = list(self._content.values())
        
        if entity:
            items = [i for i in items if i.entity == entity]
        if status:
            items = [i for i in items if i.status == status]
        if platform:
            items = [i for i in items if i.platform == platform]
        if campaign_id:
            items = [i for i in items if i.campaign_id == campaign_id]
        
        # Sort by created_at descending
        items.sort(key=lambda x: x.created_at, reverse=True)
        
        return items[:limit]
    
    def update_content(
        self,
        content_id: str,
        new_content: str,
        editor: str = "human",
    ) -> Optional[ContentItem]:
        """Update content text and track edit history."""
        item = self._content.get(content_id)
        if not item:
            return None
        
        # Track edit history
        item.edit_history.append({
            "timestamp": datetime.now().isoformat(),
            "editor": editor,
            "previous_content": item.content,
            "new_content": new_content,
        })
        
        item.content = new_content
        item.updated_at = datetime.now().isoformat()
        
        self._save_content()
        return item
    
    def delete_content(self, content_id: str) -> bool:
        """Delete a content item."""
        if content_id in self._content:
            del self._content[content_id]
            self._save_content()
            return True
        return False
    
    # ==================== Status Transitions ====================
    
    def submit_for_review(self, content_id: str) -> Optional[ContentItem]:
        """Submit content for human review."""
        item = self._content.get(content_id)
        if not item:
            return None
        
        if item.status in [ContentStatus.DRAFT, ContentStatus.CHANGES_REQUESTED]:
            item.status = ContentStatus.PENDING_REVIEW
            item.updated_at = datetime.now().isoformat()
            self._save_content()
        
        return item
    
    def request_changes(
        self,
        content_id: str,
        reviewer: str,
        notes: str,
    ) -> Optional[ContentItem]:
        """Request changes to content."""
        item = self._content.get(content_id)
        if not item:
            return None
        
        item.status = ContentStatus.CHANGES_REQUESTED
        item.reviewer = reviewer
        item.review_notes = notes
        item.updated_at = datetime.now().isoformat()
        
        self._save_content()
        return item
    
    def approve(
        self,
        content_id: str,
        reviewer: str,
        notes: str = "",
    ) -> Optional[ContentItem]:
        """Approve content for scheduling/publishing."""
        item = self._content.get(content_id)
        if not item:
            return None
        
        item.status = ContentStatus.APPROVED
        item.reviewer = reviewer
        item.review_notes = notes
        item.updated_at = datetime.now().isoformat()
        
        self._save_content()
        return item
    
    def reject(
        self,
        content_id: str,
        reviewer: str,
        reason: str,
    ) -> Optional[ContentItem]:
        """Reject content."""
        item = self._content.get(content_id)
        if not item:
            return None
        
        item.status = ContentStatus.REJECTED
        item.reviewer = reviewer
        item.review_notes = reason
        item.updated_at = datetime.now().isoformat()
        
        self._save_content()
        return item
    
    def schedule(
        self,
        content_id: str,
        scheduled_at: str,
    ) -> Optional[ContentItem]:
        """Schedule approved content for future publishing."""
        item = self._content.get(content_id)
        if not item:
            return None
        
        if item.status == ContentStatus.APPROVED:
            item.status = ContentStatus.SCHEDULED
            item.scheduled_at = scheduled_at
            item.updated_at = datetime.now().isoformat()
            self._save_content()
        
        return item
    
    def mark_published(
        self,
        content_id: str,
        publish_result: Dict[str, Any],
    ) -> Optional[ContentItem]:
        """Mark content as published with result details."""
        item = self._content.get(content_id)
        if not item:
            return None
        
        item.status = ContentStatus.PUBLISHED
        item.published_at = datetime.now().isoformat()
        item.publish_result = publish_result
        item.updated_at = datetime.now().isoformat()
        
        self._save_content()
        return item
    
    def archive(self, content_id: str) -> Optional[ContentItem]:
        """Archive content."""
        item = self._content.get(content_id)
        if not item:
            return None
        
        item.status = ContentStatus.ARCHIVED
        item.updated_at = datetime.now().isoformat()
        
        self._save_content()
        return item
    
    # ==================== Campaign Operations ====================
    
    def create_campaign(
        self,
        name: str,
        entity: str,
        topic: str,
        platforms: List[str],
    ) -> str:
        """Create a content campaign and generate drafts for each platform."""
        campaign_id = str(uuid.uuid4())[:8]
        content_ids = []
        
        for platform in platforms:
            item = self.create_content(
                entity=entity,
                content_type="social_post",
                platform=platform,
                content="",  # To be generated
                topic=topic,
                campaign=name,
                campaign_id=campaign_id,
            )
            content_ids.append(item.id)
        
        # Link related content
        for cid in content_ids:
            item = self._content[cid]
            item.related_content_ids = [i for i in content_ids if i != cid]
        
        self._save_content()
        return campaign_id
    
    def get_campaign_content(self, campaign_id: str) -> List[ContentItem]:
        """Get all content items for a campaign."""
        return [
            item for item in self._content.values()
            if item.campaign_id == campaign_id
        ]
    
    def approve_campaign(self, campaign_id: str, reviewer: str) -> int:
        """Bulk approve all pending content in a campaign."""
        approved = 0
        for item in self.get_campaign_content(campaign_id):
            if item.status == ContentStatus.PENDING_REVIEW:
                self.approve(item.id, reviewer)
                approved += 1
        return approved
    
    # ==================== Stats ====================
    
    def get_stats(self) -> Dict[str, Any]:
        """Get content pipeline statistics."""
        items = list(self._content.values())
        
        by_status = {}
        for status in ContentStatus:
            by_status[status.value] = len([i for i in items if i.status == status])
        
        by_entity = {}
        for item in items:
            by_entity[item.entity] = by_entity.get(item.entity, 0) + 1
        
        return {
            "total": len(items),
            "by_status": by_status,
            "by_entity": by_entity,
            "pending_review": by_status.get("pending_review", 0),
            "ready_to_publish": by_status.get("approved", 0) + by_status.get("scheduled", 0),
        }


# Singleton instance
_approval_manager: Optional[ContentApprovalManager] = None


def get_approval_manager() -> ContentApprovalManager:
    """Get the singleton approval manager instance."""
    global _approval_manager
    if _approval_manager is None:
        _approval_manager = ContentApprovalManager()
    return _approval_manager


# =============================================================================
# Dashboard Integration Helpers
# =============================================================================

def get_pending_reviews(entity: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get content pending human review."""
    manager = get_approval_manager()
    items = manager.list_content(entity=entity, status=ContentStatus.PENDING_REVIEW)
    return [item.to_dict() for item in items]


def quick_approve(content_id: str, reviewer: str = "dashboard_user") -> Dict[str, Any]:
    """Quick approve a single content item."""
    manager = get_approval_manager()
    item = manager.approve(content_id, reviewer)
    if item:
        return {"success": True, "item": item.to_dict()}
    return {"success": False, "error": "Content not found"}


def quick_reject(content_id: str, reviewer: str, reason: str) -> Dict[str, Any]:
    """Quick reject a content item."""
    manager = get_approval_manager()
    item = manager.reject(content_id, reviewer, reason)
    if item:
        return {"success": True, "item": item.to_dict()}
    return {"success": False, "error": "Content not found"}
