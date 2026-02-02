# src/content/media_generator.py
"""
Media generation request flow for Canva images and Sora 2 videos.
Handles prompt customization, request creation, and approval workflow.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum

from .prompt_templates import (
    MediaPrompt, 
    MediaType, 
    get_prompt_library,
    PromptTemplateLibrary,
)


class RequestStatus(Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    GENERATING = "generating"
    COMPLETED = "completed"
    REJECTED = "rejected"
    FAILED = "failed"


class OutputFormat(Enum):
    # Canva image formats
    INSTAGRAM_SQUARE = "1080x1080"
    FACEBOOK_POST = "1200x628"
    INSTAGRAM_STORY = "1080x1920"
    TWITTER_POST = "1200x675"
    LINKEDIN_POST = "1200x627"
    
    # Sora 2 video formats
    TIKTOK_REEL = "9:16"
    YOUTUBE_LANDSCAPE = "16:9"
    INSTAGRAM_REEL = "9:16"
    SQUARE_VIDEO = "1:1"


@dataclass
class MediaRequest:
    """A request for media generation."""
    id: str
    entity: str
    service_id: int
    service_name: str
    media_type: MediaType
    original_prompt: str
    customized_prompt: str
    output_format: OutputFormat
    status: RequestStatus = RequestStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    notes: str = ""
    result_url: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage/API."""
        return {
            "id": self.id,
            "entity": self.entity,
            "service_id": self.service_id,
            "service_name": self.service_name,
            "media_type": self.media_type.value,
            "original_prompt": self.original_prompt,
            "customized_prompt": self.customized_prompt,
            "output_format": self.output_format.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "notes": self.notes,
            "result_url": self.result_url,
            "error_message": self.error_message,
            "metadata": self.metadata,
        }


class MediaGeneratorPipeline:
    """
    Pipeline for creating and managing media generation requests.
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.library = get_prompt_library()
        self.requests: Dict[str, MediaRequest] = {}
        self.storage_path = storage_path or Path(__file__).parent.parent.parent / "data" / "media_requests.json"
        self._load_requests()
    
    def _load_requests(self):
        """Load existing requests from storage."""
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                for req_data in data.get("requests", []):
                    req = self._dict_to_request(req_data)
                    self.requests[req.id] = req
            except Exception as e:
                print(f"Warning: Could not load requests: {e}")
    
    def _save_requests(self):
        """Persist requests to storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "requests": [r.to_dict() for r in self.requests.values()],
            "updated_at": datetime.now().isoformat(),
        }
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def _dict_to_request(self, data: Dict[str, Any]) -> MediaRequest:
        """Convert dictionary back to MediaRequest."""
        return MediaRequest(
            id=data["id"],
            entity=data["entity"],
            service_id=data["service_id"],
            service_name=data["service_name"],
            media_type=MediaType(data["media_type"]),
            original_prompt=data["original_prompt"],
            customized_prompt=data["customized_prompt"],
            output_format=OutputFormat(data["output_format"]),
            status=RequestStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            approved_by=data.get("approved_by"),
            approved_at=datetime.fromisoformat(data["approved_at"]) if data.get("approved_at") else None,
            notes=data.get("notes", ""),
            result_url=data.get("result_url"),
            error_message=data.get("error_message"),
            metadata=data.get("metadata", {}),
        )
    
    def create_image_request(
        self,
        prompt: MediaPrompt,
        output_format: OutputFormat = OutputFormat.INSTAGRAM_SQUARE,
        customizations: Optional[Dict[str, str]] = None,
    ) -> MediaRequest:
        """
        Create an image generation request from a Canva prompt.
        
        Args:
            prompt: MediaPrompt from the library
            output_format: Target image format/size
            customizations: Dict of placeholder -> value replacements
        """
        customized = self._apply_customizations(prompt.prompt, customizations)
        
        request = MediaRequest(
            id=str(uuid.uuid4())[:8],
            entity=prompt.entity,
            service_id=prompt.service_id,
            service_name=prompt.service_name,
            media_type=MediaType.CANVA,
            original_prompt=prompt.prompt,
            customized_prompt=customized,
            output_format=output_format,
            metadata={
                "prompt_variant": prompt.variant,
                "category": prompt.category,
                "price": prompt.price,
            },
        )
        
        self.requests[request.id] = request
        self._save_requests()
        return request
    
    def create_video_request(
        self,
        prompt: MediaPrompt,
        output_format: OutputFormat = OutputFormat.TIKTOK_REEL,
        duration_seconds: int = 15,
        customizations: Optional[Dict[str, str]] = None,
    ) -> MediaRequest:
        """
        Create a video generation request from a Sora 2 prompt.
        
        Args:
            prompt: MediaPrompt from the library
            output_format: Target video aspect ratio
            duration_seconds: Target video duration
            customizations: Dict of placeholder -> value replacements
        """
        customized = self._apply_customizations(prompt.prompt, customizations)
        
        request = MediaRequest(
            id=str(uuid.uuid4())[:8],
            entity=prompt.entity,
            service_id=prompt.service_id,
            service_name=prompt.service_name,
            media_type=MediaType.SORA2,
            original_prompt=prompt.prompt,
            customized_prompt=customized,
            output_format=output_format,
            metadata={
                "prompt_variant": prompt.variant,
                "category": prompt.category,
                "price": prompt.price,
                "duration_seconds": duration_seconds,
            },
        )
        
        self.requests[request.id] = request
        self._save_requests()
        return request
    
    def _apply_customizations(
        self, 
        prompt: str, 
        customizations: Optional[Dict[str, str]]
    ) -> str:
        """Apply customizations to a prompt template."""
        if not customizations:
            return prompt
            
        result = prompt
        for placeholder, value in customizations.items():
            result = result.replace(f"{{{placeholder}}}", value)
            result = result.replace(f"[{placeholder}]", value)
        return result
    
    def submit_for_approval(self, request_id: str) -> MediaRequest:
        """Move a request to pending approval status."""
        request = self.requests.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")
        
        request.status = RequestStatus.PENDING_APPROVAL
        request.updated_at = datetime.now()
        self._save_requests()
        return request
    
    def approve_request(
        self, 
        request_id: str, 
        approved_by: str = "system"
    ) -> MediaRequest:
        """Approve a media generation request."""
        request = self.requests.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")
        
        request.status = RequestStatus.APPROVED
        request.approved_by = approved_by
        request.approved_at = datetime.now()
        request.updated_at = datetime.now()
        self._save_requests()
        return request
    
    def reject_request(
        self, 
        request_id: str, 
        reason: str = ""
    ) -> MediaRequest:
        """Reject a media generation request."""
        request = self.requests.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")
        
        request.status = RequestStatus.REJECTED
        request.notes = reason
        request.updated_at = datetime.now()
        self._save_requests()
        return request
    
    def update_prompt(
        self, 
        request_id: str, 
        new_prompt: str
    ) -> MediaRequest:
        """Update the customized prompt for a request."""
        request = self.requests.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")
        
        request.customized_prompt = new_prompt
        request.updated_at = datetime.now()
        self._save_requests()
        return request
    
    def get_pending_approvals(self) -> List[MediaRequest]:
        """Get all requests pending approval."""
        return [
            r for r in self.requests.values() 
            if r.status == RequestStatus.PENDING_APPROVAL
        ]
    
    def get_requests_by_status(self, status: RequestStatus) -> List[MediaRequest]:
        """Get requests filtered by status."""
        return [r for r in self.requests.values() if r.status == status]
    
    def get_requests_by_entity(self, entity: str) -> List[MediaRequest]:
        """Get all requests for an entity."""
        return [r for r in self.requests.values() if r.entity == entity]
    
    def generate_content_brief(
        self,
        entity: str,
        category: Optional[str] = None,
        media_types: Optional[List[MediaType]] = None,
        count: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Generate a content brief with recommended media to create.
        
        Returns a list of suggestions with prompts and rationale.
        """
        from .ai_generator import get_generator
        
        prompts = self.library.get_all_prompts(
            entity=entity,
            category=category,
            media_type=media_types[0] if media_types and len(media_types) == 1 else None,
        )
        
        if not prompts:
            return []
        
        # Use local LLM to pick and prioritize prompts
        gen = get_generator()
        
        prompt_summaries = "\n".join([
            f"- [{p.service_name}] ({p.media_type.value}): {p.prompt[:100]}..."
            for p in prompts[:20]  # Limit to avoid token overflow
        ])
        
        selection_prompt = f"""Given these marketing prompts for {entity}, select the top {count} to create this week.
Consider variety, seasonal relevance, and engagement potential.

Available prompts:
{prompt_summaries}

Return just the service names of your top {count} picks, one per line:"""
        
        try:
            response = gen.llm.ask(selection_prompt, max_tokens=200)
            selected_names = [line.strip().strip('[]- ') for line in response.split('\n') if line.strip()]
            
            brief = []
            for name in selected_names[:count]:
                matching = [p for p in prompts if name.lower() in p.service_name.lower()]
                if matching:
                    p = matching[0]
                    brief.append({
                        "service": p.service_name,
                        "media_type": p.media_type.value,
                        "prompt_preview": p.prompt[:200] + "...",
                        "category": p.category,
                        "price": p.price,
                        "prompt_id": p.id,
                    })
            
            return brief
            
        except Exception as e:
            # Fallback: random selection
            import random
            selected = random.sample(prompts, min(count, len(prompts)))
            return [
                {
                    "service": p.service_name,
                    "media_type": p.media_type.value,
                    "prompt_preview": p.prompt[:200] + "...",
                    "category": p.category,
                    "price": p.price,
                    "prompt_id": p.id,
                }
                for p in selected
            ]
    
    def export_for_canva(self, request_id: str) -> Dict[str, Any]:
        """
        Export a request in a format ready for Canva AI.
        """
        request = self.requests.get(request_id)
        if not request or request.media_type != MediaType.CANVA:
            raise ValueError(f"Invalid Canva request: {request_id}")
        
        return {
            "prompt": request.customized_prompt,
            "size": request.output_format.value,
            "style": "modern tech aesthetic",
            "brand_colors": {
                "primary": "#1E3A8A",  # Deep blue
                "accent": "#10B981",   # Green
                "warning": "#F59E0B",  # Orange
            },
            "include_logo": True,
            "metadata": {
                "request_id": request.id,
                "service": request.service_name,
                "entity": request.entity,
            },
        }
    
    def export_for_sora(self, request_id: str) -> Dict[str, Any]:
        """
        Export a request in a format ready for Sora 2.
        """
        request = self.requests.get(request_id)
        if not request or request.media_type != MediaType.SORA2:
            raise ValueError(f"Invalid Sora request: {request_id}")
        
        return {
            "prompt": request.customized_prompt,
            "aspect_ratio": request.output_format.value,
            "duration_seconds": request.metadata.get("duration_seconds", 15),
            "style": "commercial, professional, engaging",
            "audio": "upbeat background music",
            "end_card": {
                "text": request.service_name,
                "price": request.metadata.get("price", ""),
                "logo": True,
            },
            "metadata": {
                "request_id": request.id,
                "service": request.service_name,
                "entity": request.entity,
            },
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics."""
        by_status = {}
        by_type = {"canva": 0, "sora2": 0}
        by_entity = {}
        
        for req in self.requests.values():
            # By status
            status = req.status.value
            by_status[status] = by_status.get(status, 0) + 1
            
            # By type
            by_type[req.media_type.value] += 1
            
            # By entity
            by_entity[req.entity] = by_entity.get(req.entity, 0) + 1
        
        return {
            "total_requests": len(self.requests),
            "by_status": by_status,
            "by_media_type": by_type,
            "by_entity": by_entity,
            "pending_approvals": len(self.get_pending_approvals()),
            "library_stats": self.library.to_dict(),
        }


# Global pipeline instance
_pipeline: Optional[MediaGeneratorPipeline] = None


def get_media_pipeline() -> MediaGeneratorPipeline:
    """Get or create the global media pipeline."""
    global _pipeline
    if _pipeline is None:
        _pipeline = MediaGeneratorPipeline()
    return _pipeline
