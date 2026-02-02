# src/sop/approval.py
"""
Approval workflow system for SOP steps that require human approval.
"""

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path
from enum import Enum


class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


@dataclass
class ApprovalRequest:
    """A request for human approval."""
    id: str
    sop_id: str
    sop_name: str
    step_id: str
    step_name: str
    entity: str
    requester: str
    approvers: List[str]
    status: ApprovalStatus = ApprovalStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    resolution_note: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    execution_state: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sop_id": self.sop_id,
            "sop_name": self.sop_name,
            "step_id": self.step_id,
            "step_name": self.step_name,
            "entity": self.entity,
            "requester": self.requester,
            "approvers": self.approvers,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "resolved_by": self.resolved_by,
            "resolution_note": self.resolution_note,
            "context": self.context,
            "execution_state": self.execution_state,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApprovalRequest":
        return cls(
            id=data["id"],
            sop_id=data["sop_id"],
            sop_name=data.get("sop_name", ""),
            step_id=data["step_id"],
            step_name=data.get("step_name", ""),
            entity=data["entity"],
            requester=data["requester"],
            approvers=data["approvers"],
            status=ApprovalStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            expires_at=datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None,
            resolved_at=datetime.fromisoformat(data["resolved_at"]) if data.get("resolved_at") else None,
            resolved_by=data.get("resolved_by"),
            resolution_note=data.get("resolution_note", ""),
            context=data.get("context", {}),
            execution_state=data.get("execution_state", {}),
        )


class ApprovalManager:
    """
    Manages approval requests for SOP steps.
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path(__file__).parent.parent.parent / "data" / "approvals.json"
        self.requests: Dict[str, ApprovalRequest] = {}
        self._load()
    
    def _load(self):
        """Load existing requests from storage."""
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                for req_data in data.get("requests", []):
                    req = ApprovalRequest.from_dict(req_data)
                    self.requests[req.id] = req
            except Exception as e:
                print(f"Warning: Could not load approvals: {e}")
    
    def _save(self):
        """Persist requests to storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "requests": [r.to_dict() for r in self.requests.values()],
            "updated_at": datetime.now().isoformat(),
        }
        self.storage_path.write_text(json.dumps(data, indent=2))
    
    def create_request(
        self,
        sop_id: str,
        sop_name: str,
        step_id: str,
        step_name: str,
        entity: str,
        approvers: List[str],
        requester: str = "system",
        context: Optional[Dict[str, Any]] = None,
        execution_state: Optional[Dict[str, Any]] = None,
        expires_in_hours: Optional[int] = None,
    ) -> ApprovalRequest:
        """
        Create a new approval request.
        
        Args:
            sop_id: The SOP being executed
            sop_name: Human-readable SOP name
            step_id: The step requiring approval
            step_name: Human-readable step name
            entity: The entity context
            approvers: List of approver identifiers (roles, users, channels)
            requester: Who initiated the request
            context: Additional context data
            execution_state: State to restore when approved
            expires_in_hours: Optional expiration time
        """
        request = ApprovalRequest(
            id=str(uuid.uuid4())[:8],
            sop_id=sop_id,
            sop_name=sop_name,
            step_id=step_id,
            step_name=step_name,
            entity=entity,
            requester=requester,
            approvers=approvers,
            context=context or {},
            execution_state=execution_state or {},
        )
        
        if expires_in_hours:
            from datetime import timedelta
            request.expires_at = datetime.now() + timedelta(hours=expires_in_hours)
        
        self.requests[request.id] = request
        self._save()
        return request
    
    def approve(
        self,
        request_id: str,
        approved_by: str,
        note: str = "",
    ) -> ApprovalRequest:
        """Approve a request."""
        request = self.requests.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")
        
        if request.status != ApprovalStatus.PENDING:
            raise ValueError(f"Request {request_id} is not pending (status: {request.status.value})")
        
        request.status = ApprovalStatus.APPROVED
        request.resolved_at = datetime.now()
        request.resolved_by = approved_by
        request.resolution_note = note
        
        self._save()
        return request
    
    def reject(
        self,
        request_id: str,
        rejected_by: str,
        reason: str = "",
    ) -> ApprovalRequest:
        """Reject a request."""
        request = self.requests.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")
        
        if request.status != ApprovalStatus.PENDING:
            raise ValueError(f"Request {request_id} is not pending (status: {request.status.value})")
        
        request.status = ApprovalStatus.REJECTED
        request.resolved_at = datetime.now()
        request.resolved_by = rejected_by
        request.resolution_note = reason
        
        self._save()
        return request
    
    def cancel(self, request_id: str) -> ApprovalRequest:
        """Cancel a pending request."""
        request = self.requests.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")
        
        request.status = ApprovalStatus.CANCELLED
        request.resolved_at = datetime.now()
        
        self._save()
        return request
    
    def get_pending(self, entity: Optional[str] = None) -> List[ApprovalRequest]:
        """Get all pending approval requests."""
        pending = [
            r for r in self.requests.values()
            if r.status == ApprovalStatus.PENDING
        ]
        
        if entity:
            pending = [r for r in pending if r.entity == entity]
        
        # Check for expirations
        now = datetime.now()
        for req in pending:
            if req.expires_at and req.expires_at < now:
                req.status = ApprovalStatus.EXPIRED
                req.resolved_at = now
        
        self._save()
        
        return [r for r in pending if r.status == ApprovalStatus.PENDING]
    
    def get_request(self, request_id: str) -> Optional[ApprovalRequest]:
        """Get a specific request."""
        return self.requests.get(request_id)
    
    def get_by_sop(self, sop_id: str) -> List[ApprovalRequest]:
        """Get all requests for a specific SOP."""
        return [r for r in self.requests.values() if r.sop_id == sop_id]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get approval statistics."""
        by_status = {}
        by_entity = {}
        
        for req in self.requests.values():
            status = req.status.value
            by_status[status] = by_status.get(status, 0) + 1
            by_entity[req.entity] = by_entity.get(req.entity, 0) + 1
        
        return {
            "total": len(self.requests),
            "pending": len(self.get_pending()),
            "by_status": by_status,
            "by_entity": by_entity,
        }


# Global instance
_manager: Optional[ApprovalManager] = None


def get_approval_manager() -> ApprovalManager:
    """Get or create the global approval manager."""
    global _manager
    if _manager is None:
        _manager = ApprovalManager()
    return _manager
