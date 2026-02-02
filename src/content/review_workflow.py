# src/content/review_workflow.py
"""
Content review workflow: AI Draft → Human Review → Publish

Connects content generation with approval system and publishing.
"""

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path
from enum import Enum


class ContentStatus(Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"


@dataclass
class ContentDraft:
    """A content draft in the review pipeline."""
    id: str
    entity: str
    platform: str
    content: str
    hashtags: List[str] = field(default_factory=list)
    media_urls: List[str] = field(default_factory=list)
    status: ContentStatus = ContentStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = "ai"
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[str] = None
    review_notes: str = ""
    scheduled_for: Optional[datetime] = None
    published_at: Optional[datetime] = None
    publish_result: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "entity": self.entity,
            "platform": self.platform,
            "content": self.content,
            "hashtags": self.hashtags,
            "media_urls": self.media_urls,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "reviewed_by": self.reviewed_by,
            "review_notes": self.review_notes,
            "scheduled_for": self.scheduled_for.isoformat() if self.scheduled_for else None,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "publish_result": self.publish_result,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContentDraft":
        return cls(
            id=data["id"],
            entity=data["entity"],
            platform=data["platform"],
            content=data["content"],
            hashtags=data.get("hashtags", []),
            media_urls=data.get("media_urls", []),
            status=ContentStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            created_by=data.get("created_by", "ai"),
            reviewed_at=datetime.fromisoformat(data["reviewed_at"]) if data.get("reviewed_at") else None,
            reviewed_by=data.get("reviewed_by"),
            review_notes=data.get("review_notes", ""),
            scheduled_for=datetime.fromisoformat(data["scheduled_for"]) if data.get("scheduled_for") else None,
            published_at=datetime.fromisoformat(data["published_at"]) if data.get("published_at") else None,
            publish_result=data.get("publish_result"),
            metadata=data.get("metadata", {}),
        )


class ContentReviewWorkflow:
    """
    Manages the content review workflow.
    
    Flow:
    1. AI generates draft → DRAFT
    2. Submit for review → PENDING_REVIEW
    3. Human reviews:
       - Approve → APPROVED
       - Reject (with notes) → REJECTED
    4. Schedule or publish:
       - Schedule → SCHEDULED
       - Publish now → PUBLISHED
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path(__file__).parent.parent.parent / "data" / "content_drafts.json"
        self.drafts: Dict[str, ContentDraft] = {}
        self._load()
    
    def _load(self):
        """Load drafts from storage."""
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                for draft_data in data.get("drafts", []):
                    draft = ContentDraft.from_dict(draft_data)
                    self.drafts[draft.id] = draft
            except Exception as e:
                print(f"Warning: Could not load drafts: {e}")
    
    def _save(self):
        """Save drafts to storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "drafts": [d.to_dict() for d in self.drafts.values()],
            "updated_at": datetime.now().isoformat(),
        }
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def create_draft(
        self,
        entity: str,
        platform: str,
        content: str,
        hashtags: Optional[List[str]] = None,
        media_urls: Optional[List[str]] = None,
        created_by: str = "ai",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ContentDraft:
        """
        Create a new content draft.
        
        Args:
            entity: Target entity
            platform: Target platform
            content: The content text
            hashtags: Optional hashtags
            media_urls: Optional media URLs
            created_by: Creator identifier
            metadata: Additional metadata
        """
        draft = ContentDraft(
            id=str(uuid.uuid4())[:8],
            entity=entity,
            platform=platform,
            content=content,
            hashtags=hashtags or [],
            media_urls=media_urls or [],
            created_by=created_by,
            metadata=metadata or {},
        )
        
        self.drafts[draft.id] = draft
        self._save()
        return draft
    
    def create_ai_draft(
        self,
        entity: str,
        platform: str,
        topic: str,
        context: Optional[str] = None,
    ) -> ContentDraft:
        """
        Create a draft using AI generation.
        
        Args:
            entity: Target entity
            platform: Target platform
            topic: Topic to generate about
            context: Additional context
        """
        from .generator import generate_post, generate_hashtags
        
        # Generate content
        result = generate_post(entity, topic, platform, context)
        content = result["content"]
        
        # Generate hashtags
        hashtags = generate_hashtags(entity, topic, 5)
        
        return self.create_draft(
            entity=entity,
            platform=platform,
            content=content,
            hashtags=hashtags,
            created_by="ai",
            metadata={
                "topic": topic,
                "context": context,
                "generation_result": result,
            },
        )
    
    def submit_for_review(self, draft_id: str) -> ContentDraft:
        """Submit a draft for human review."""
        draft = self.drafts.get(draft_id)
        if not draft:
            raise ValueError(f"Draft {draft_id} not found")
        
        draft.status = ContentStatus.PENDING_REVIEW
        self._save()
        return draft
    
    def approve(
        self,
        draft_id: str,
        reviewed_by: str,
        notes: str = "",
        edited_content: Optional[str] = None,
    ) -> ContentDraft:
        """
        Approve a draft.
        
        Args:
            draft_id: Draft to approve
            reviewed_by: Reviewer identifier
            notes: Optional review notes
            edited_content: Optional edited content to replace original
        """
        draft = self.drafts.get(draft_id)
        if not draft:
            raise ValueError(f"Draft {draft_id} not found")
        
        if edited_content:
            draft.content = edited_content
        
        draft.status = ContentStatus.APPROVED
        draft.reviewed_at = datetime.now()
        draft.reviewed_by = reviewed_by
        draft.review_notes = notes
        
        self._save()
        return draft
    
    def reject(
        self,
        draft_id: str,
        reviewed_by: str,
        reason: str,
    ) -> ContentDraft:
        """Reject a draft."""
        draft = self.drafts.get(draft_id)
        if not draft:
            raise ValueError(f"Draft {draft_id} not found")
        
        draft.status = ContentStatus.REJECTED
        draft.reviewed_at = datetime.now()
        draft.reviewed_by = reviewed_by
        draft.review_notes = reason
        
        self._save()
        return draft
    
    def schedule(
        self,
        draft_id: str,
        scheduled_for: datetime,
    ) -> ContentDraft:
        """Schedule an approved draft for future publishing."""
        draft = self.drafts.get(draft_id)
        if not draft:
            raise ValueError(f"Draft {draft_id} not found")
        
        if draft.status != ContentStatus.APPROVED:
            raise ValueError(f"Draft must be approved before scheduling (current: {draft.status.value})")
        
        draft.status = ContentStatus.SCHEDULED
        draft.scheduled_for = scheduled_for
        
        self._save()
        return draft
    
    def publish(self, draft_id: str) -> ContentDraft:
        """
        Publish an approved draft immediately.
        
        In production, this would call MixPost API.
        """
        draft = self.drafts.get(draft_id)
        if not draft:
            raise ValueError(f"Draft {draft_id} not found")
        
        if draft.status not in [ContentStatus.APPROVED, ContentStatus.SCHEDULED]:
            raise ValueError(f"Draft must be approved or scheduled (current: {draft.status.value})")
        
        # TODO: Integrate with MixPost when credentials available
        # For now, mark as published
        draft.status = ContentStatus.PUBLISHED
        draft.published_at = datetime.now()
        draft.publish_result = {
            "success": True,
            "message": "Published (MixPost integration pending)",
            "platform": draft.platform,
        }
        
        self._save()
        return draft
    
    def get_pending_review(self, entity: Optional[str] = None) -> List[ContentDraft]:
        """Get drafts pending review."""
        pending = [
            d for d in self.drafts.values()
            if d.status == ContentStatus.PENDING_REVIEW
        ]
        if entity:
            pending = [d for d in pending if d.entity == entity]
        return sorted(pending, key=lambda d: d.created_at)
    
    def get_approved(self, entity: Optional[str] = None) -> List[ContentDraft]:
        """Get approved drafts ready to publish."""
        approved = [
            d for d in self.drafts.values()
            if d.status == ContentStatus.APPROVED
        ]
        if entity:
            approved = [d for d in approved if d.entity == entity]
        return approved
    
    def get_scheduled(self) -> List[ContentDraft]:
        """Get scheduled drafts."""
        return [
            d for d in self.drafts.values()
            if d.status == ContentStatus.SCHEDULED
        ]
    
    def get_draft(self, draft_id: str) -> Optional[ContentDraft]:
        """Get a specific draft."""
        return self.drafts.get(draft_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get workflow statistics."""
        by_status = {}
        by_entity = {}
        by_platform = {}
        
        for draft in self.drafts.values():
            status = draft.status.value
            by_status[status] = by_status.get(status, 0) + 1
            by_entity[draft.entity] = by_entity.get(draft.entity, 0) + 1
            by_platform[draft.platform] = by_platform.get(draft.platform, 0) + 1
        
        return {
            "total": len(self.drafts),
            "pending_review": len(self.get_pending_review()),
            "approved": len(self.get_approved()),
            "scheduled": len(self.get_scheduled()),
            "by_status": by_status,
            "by_entity": by_entity,
            "by_platform": by_platform,
        }


# Global instance
_workflow: Optional[ContentReviewWorkflow] = None


def get_review_workflow() -> ContentReviewWorkflow:
    """Get or create the global review workflow."""
    global _workflow
    if _workflow is None:
        _workflow = ContentReviewWorkflow()
    return _workflow
