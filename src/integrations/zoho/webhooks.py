"""
Zoho Webhook Handler for SOP Triggers.

Receives webhooks from Zoho CRM and triggers corresponding SOPs:
- Record create/update/delete events
- Deal stage changes
- Field value changes
- Scheduled workflow triggers
"""

from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
import hashlib
import hmac
import json


class ZohoWebhookHandler:
    """
    Handler for incoming Zoho CRM webhooks.
    
    Maps webhook events to SOP triggers.
    """
    
    # Standard Zoho webhook event types
    EVENT_TYPES = {
        "module.create": "record_created",
        "module.edit": "record_updated", 
        "module.delete": "record_deleted",
        "deal.stage_change": "deal_stage_changed",
        "deal.won": "deal_won",
        "deal.lost": "deal_lost",
        "lead.convert": "lead_converted",
    }
    
    def __init__(self, webhook_secret: Optional[str] = None):
        """
        Initialize webhook handler.
        
        Args:
            webhook_secret: Secret for validating webhook signatures
        """
        self.webhook_secret = webhook_secret
        self._callbacks: Dict[str, List[Callable]] = {}
        self._sop_mappings: Dict[str, List[Dict[str, Any]]] = {}
    
    def register_callback(self, event_type: str, callback: Callable):
        """
        Register a callback for an event type.
        
        Args:
            event_type: Event type to listen for
            callback: Function to call when event occurs
        """
        if event_type not in self._callbacks:
            self._callbacks[event_type] = []
        self._callbacks[event_type].append(callback)
    
    def map_to_sop(
        self,
        event_type: str,
        sop_id: str,
        entity: str,
        conditions: Optional[Dict[str, Any]] = None
    ):
        """
        Map a webhook event to an SOP trigger.
        
        Args:
            event_type: Webhook event type
            sop_id: SOP to trigger
            entity: Entity the SOP belongs to
            conditions: Optional conditions for triggering
        """
        if event_type not in self._sop_mappings:
            self._sop_mappings[event_type] = []
        
        self._sop_mappings[event_type].append({
            "sop_id": sop_id,
            "entity": entity,
            "conditions": conditions or {}
        })
    
    def validate_signature(
        self,
        payload: bytes,
        signature: str
    ) -> bool:
        """
        Validate webhook signature.
        
        Args:
            payload: Raw request body
            signature: Signature from X-Zoho-Signature header
            
        Returns:
            True if signature is valid
        """
        if not self.webhook_secret:
            return True  # No secret configured, skip validation
        
        expected = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected, signature)
    
    def parse_webhook(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse a Zoho webhook payload into normalized format.
        
        Args:
            data: Raw webhook payload
            
        Returns:
            Normalized event data
        """
        # Extract common fields
        event_type = data.get("operation") or data.get("event_type", "unknown")
        module = data.get("module", {}).get("api_name", "Unknown")
        
        # Normalize to our event types
        normalized_type = self.EVENT_TYPES.get(
            f"{module.lower()}.{event_type}",
            event_type
        )
        
        # Extract record data
        record_data = data.get("data", [{}])[0] if isinstance(data.get("data"), list) else data.get("data", {})
        
        return {
            "event_type": normalized_type,
            "original_event": event_type,
            "module": module,
            "record_id": record_data.get("id"),
            "record": record_data,
            "timestamp": datetime.now().isoformat(),
            "user": data.get("user", {}).get("name", "System"),
            "raw": data
        }
    
    def process_webhook(
        self,
        data: Dict[str, Any],
        signature: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process an incoming webhook.
        
        Args:
            data: Webhook payload
            signature: Optional signature for validation
            
        Returns:
            Processing result with triggered SOPs
        """
        # Validate signature if provided
        if signature and not self.validate_signature(json.dumps(data).encode(), signature):
            return {
                "success": False,
                "error": "Invalid webhook signature"
            }
        
        # Parse webhook
        event = self.parse_webhook(data)
        event_type = event["event_type"]
        
        # Execute callbacks
        callbacks_run = 0
        for callback in self._callbacks.get(event_type, []):
            try:
                callback(event)
                callbacks_run += 1
            except Exception as e:
                print(f"Callback error: {e}")
        
        # Find matching SOP triggers
        triggered_sops = []
        for mapping in self._sop_mappings.get(event_type, []):
            if self._check_conditions(event, mapping.get("conditions", {})):
                triggered_sops.append({
                    "sop_id": mapping["sop_id"],
                    "entity": mapping["entity"],
                    "event": event
                })
        
        return {
            "success": True,
            "event_type": event_type,
            "module": event["module"],
            "record_id": event["record_id"],
            "callbacks_run": callbacks_run,
            "triggered_sops": triggered_sops
        }
    
    def _check_conditions(
        self,
        event: Dict[str, Any],
        conditions: Dict[str, Any]
    ) -> bool:
        """
        Check if event matches trigger conditions.
        
        Args:
            event: Parsed event data
            conditions: Conditions to check
            
        Returns:
            True if all conditions match
        """
        if not conditions:
            return True
        
        record = event.get("record", {})
        
        for field, expected in conditions.items():
            actual = record.get(field)
            
            if isinstance(expected, dict):
                # Complex condition
                op = expected.get("op", "equals")
                value = expected.get("value")
                
                if op == "equals" and actual != value:
                    return False
                elif op == "not_equals" and actual == value:
                    return False
                elif op == "contains" and value not in str(actual):
                    return False
                elif op == "in" and actual not in value:
                    return False
            else:
                # Simple equality
                if actual != expected:
                    return False
        
        return True
    
    def get_mappings_summary(self) -> Dict[str, Any]:
        """Get summary of configured SOP mappings."""
        return {
            "event_types": list(self._sop_mappings.keys()),
            "total_mappings": sum(len(m) for m in self._sop_mappings.values()),
            "mappings": {
                event: [
                    {"sop": m["sop_id"], "entity": m["entity"]}
                    for m in mappings
                ]
                for event, mappings in self._sop_mappings.items()
            }
        }


class ZohoWebhookRouter:
    """
    FastAPI router for Zoho webhooks.
    
    Add to your FastAPI app:
        app.include_router(ZohoWebhookRouter(handler).router, prefix="/webhooks")
    """
    
    def __init__(
        self,
        handler: ZohoWebhookHandler,
        sop_engine = None
    ):
        self.handler = handler
        self.sop_engine = sop_engine
        self._setup_router()
    
    def _setup_router(self):
        """Set up FastAPI router."""
        from fastapi import APIRouter, Request, HTTPException
        from fastapi.responses import JSONResponse
        
        self.router = APIRouter(tags=["Zoho Webhooks"])
        
        @self.router.post("/zoho")
        async def receive_webhook(request: Request):
            """Receive Zoho webhook."""
            try:
                data = await request.json()
                signature = request.headers.get("X-Zoho-Signature")
                
                result = self.handler.process_webhook(data, signature)
                
                if not result["success"]:
                    raise HTTPException(status_code=400, detail=result["error"])
                
                # Trigger SOPs if engine is available
                if self.sop_engine and result.get("triggered_sops"):
                    for trigger in result["triggered_sops"]:
                        try:
                            self.sop_engine.execute_sop(
                                trigger["sop_id"],
                                trigger["entity"],
                                event=trigger["event"]
                            )
                        except Exception as e:
                            print(f"SOP trigger error: {e}")
                
                return JSONResponse({
                    "status": "ok",
                    "processed": True,
                    "sops_triggered": len(result.get("triggered_sops", []))
                })
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.router.get("/zoho/mappings")
        async def get_mappings():
            """Get webhook to SOP mappings."""
            return self.handler.get_mappings_summary()


# Example usage and configuration
def setup_webhook_mappings(handler: ZohoWebhookHandler):
    """
    Configure default webhook to SOP mappings.
    
    Call this during app startup to set up mappings.
    """
    # Deal won → Announcement SOP
    handler.map_to_sop(
        event_type="deal_won",
        sop_id="mhi_contract_win_announcement",
        entity="mighty_house_inc"
    )
    
    # Lead created → Onboarding SOP
    handler.map_to_sop(
        event_type="record_created",
        sop_id="dsaic_customer_onboarding",
        entity="dsaic",
        conditions={"module": "Leads", "Lead_Source": "Website"}
    )
    
    # Deal stage change to "Closed Won" → Celebration
    handler.map_to_sop(
        event_type="deal_stage_changed",
        sop_id="cs_certification_complete",
        entity="computer_store",
        conditions={"Stage": "Closed Won"}
    )


if __name__ == "__main__":
    # Test webhook handler
    handler = ZohoWebhookHandler()
    setup_webhook_mappings(handler)
    
    print("Webhook Mappings:")
    print(json.dumps(handler.get_mappings_summary(), indent=2))
    
    # Simulate a webhook
    test_webhook = {
        "operation": "edit",
        "module": {"api_name": "Deals"},
        "data": [{
            "id": "123456789",
            "Deal_Name": "Test Deal",
            "Stage": "Closed Won",
            "Amount": 50000
        }]
    }
    
    result = handler.process_webhook(test_webhook)
    print(f"\nWebhook processed: {result}")
