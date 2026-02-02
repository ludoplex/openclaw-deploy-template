# src/sop/engine.py
"""
Enhanced SOP Engine with social media and cross-entity capabilities.
Wraps the base Zoho SOP engine with additional step handlers.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from .step_types import (
    StepType, Entity, Platform, VoiceProfile,
    get_entity_config, adapt_content_for_platform,
)
from .social_handler import (
    SocialPostHandler, ContentGenerateHandler, CrossEntityTriggerHandler,
    StepResult,
)

# CRM integration
try:
    from ..integrations.zoho.crm_handler import CRMStepHandler, ZohoCRMHandler
    CRM_AVAILABLE = True
except ImportError:
    CRM_AVAILABLE = False
    CRMStepHandler = None


class EnhancedSOPEngine:
    """
    Enhanced SOP Engine with social, content, and cross-entity capabilities.
    
    Extends the base Zoho SOP engine with additional step handlers:
    - social_post: Post to social media via MixPost
    - content_generate: AI-powered content generation
    - cross_entity_trigger: Trigger SOPs in other entities
    - schedule_content: Queue content for later posting
    - delay: Wait for time/condition
    - webhook_send: Send outbound webhooks
    """
    
    def __init__(
        self,
        base_engine=None,
        mixpost_client=None,
        ai_client=None,
    ):
        """
        Initialize the enhanced engine.
        
        Args:
            base_engine: Base SOP engine instance (from zoho-console-api-module-system)
            mixpost_client: MixPost API client
            ai_client: AI/LLM client for content generation
        """
        self.base_engine = base_engine
        self.mixpost_client = mixpost_client
        self.ai_client = ai_client
        
        # Initialize handlers
        self.social_handler = SocialPostHandler(mixpost_client)
        self.content_handler = ContentGenerateHandler(ai_client)
        self.cross_entity_handler = CrossEntityTriggerHandler(self)
        
        # CRM handler
        self.crm_handler = CRMStepHandler() if CRM_AVAILABLE else None
        
        # Extended step handlers
        self._extended_handlers = {
            StepType.SOCIAL_POST: self.social_handler.handle,
            StepType.CONTENT_GENERATE: self.content_handler.handle,
            StepType.CROSS_ENTITY_TRIGGER: self.cross_entity_handler.handle,
            StepType.SCHEDULE_CONTENT: self._handle_schedule_content,
            StepType.DELAY: self._handle_delay,
            StepType.WEBHOOK_SEND: self._handle_webhook_send,
            StepType.DATA_SYNC: self._handle_data_sync,
            StepType.LOOP: self._handle_loop,
            StepType.TRANSFORM: self._handle_transform,
        }
        
        # Add CRM handlers if available
        if self.crm_handler:
            self._extended_handlers.update({
                StepType.CRM_CREATE: self._handle_crm_step,
                StepType.CRM_UPDATE: self._handle_crm_step,
                StepType.CRM_SEARCH: self._handle_crm_step,
                StepType.CRM_DEAL_STAGE: self._handle_crm_step,
                StepType.CRM_CREATE_TASK: self._handle_crm_step,
            })
        
        # Loaded definitions (local + base)
        self._definitions: Dict[str, Any] = {}
        
        # Execution history
        self._history: List[Dict] = []
    
    def load_definitions(self, path: Optional[Path] = None) -> int:
        """
        Load SOP definitions from workspace and base engine.
        
        Args:
            path: Path to SOP definitions directory
            
        Returns:
            Number of definitions loaded
        """
        import yaml
        
        count = 0
        search_path = path or Path(__file__).parent.parent.parent / "sops"
        
        # Load from all entity directories
        for entity_dir in search_path.iterdir():
            if entity_dir.is_dir():
                for yaml_file in entity_dir.glob("*.yaml"):
                    if yaml_file.name == "sop-schema.yaml":
                        continue
                    try:
                        with open(yaml_file, "r", encoding="utf-8") as f:
                            data = yaml.safe_load(f)
                        if data and "sop_id" in data:
                            self._definitions[data["sop_id"]] = data
                            count += 1
                    except Exception as e:
                        print(f"Error loading {yaml_file}: {e}")
        
        # Load from base engine if available
        if self.base_engine:
            base_count = self.base_engine.load_definitions()
            for sop_id, defn in self.base_engine._definitions.items():
                if sop_id not in self._definitions:
                    self._definitions[sop_id] = defn
                    count += 1
        
        return count
    
    def get_definition(self, sop_id: str) -> Optional[Dict]:
        """Get a specific SOP definition by ID."""
        return self._definitions.get(sop_id)
    
    def list_definitions(
        self,
        entity: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Dict]:
        """
        List SOP definitions with optional filtering.
        
        Args:
            entity: Filter by entity
            tags: Filter by tags (any match)
            
        Returns:
            List of matching definitions
        """
        definitions = list(self._definitions.values())
        
        if entity:
            definitions = [d for d in definitions if d.get("entity") == entity]
        
        if tags:
            definitions = [
                d for d in definitions
                if any(tag in d.get("tags", []) for tag in tags)
            ]
        
        return definitions
    
    def execute_step(
        self,
        step: Dict[str, Any],
        event: Dict[str, Any],
        sop: Dict[str, Any],
    ) -> StepResult:
        """
        Execute a single step.
        
        Args:
            step: Step definition
            event: Trigger event data
            sop: Parent SOP definition
            
        Returns:
            StepResult with execution details
        """
        step_type_str = step.get("type", "")
        
        # Convert to StepType enum
        try:
            step_type = StepType(step_type_str)
        except ValueError:
            # Try base engine
            if self.base_engine:
                return self.base_engine._execute_step(step, event, sop)
            return StepResult(
                step_id=step.get("id", "unknown"),
                step_name=step.get("name", "Unknown"),
                success=False,
                error=f"Unknown step type: {step_type_str}"
            )
        
        # Check for extended handler
        handler = self._extended_handlers.get(step_type)
        if handler:
            # Create step object for handler
            class StepObj:
                pass
            step_obj = StepObj()
            for k, v in step.items():
                setattr(step_obj, k, v)
            
            class SOPObj:
                pass
            sop_obj = SOPObj()
            for k, v in sop.items():
                setattr(sop_obj, k, v)
            
            return handler(step_obj, event, sop_obj)
        
        # Fall back to base engine
        if self.base_engine:
            return self.base_engine._execute_step(step, event, sop)
        
        return StepResult(
            step_id=step.get("id", "unknown"),
            step_name=step.get("name", "Unknown"),
            success=False,
            error=f"No handler for step type: {step_type_str}"
        )
    
    def execute_sop(
        self,
        sop_id: str,
        event: Optional[Dict[str, Any]] = None,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Execute an SOP by ID.
        
        Args:
            sop_id: SOP definition ID
            event: Trigger event data (optional)
            dry_run: If True, simulate without side effects
            
        Returns:
            Execution result with step results
        """
        sop = self.get_definition(sop_id)
        if not sop:
            return {
                "success": False,
                "error": f"SOP not found: {sop_id}",
                "sop_id": sop_id,
            }
        
        event = event or {"event_type": "manual", "data": {}}
        
        result = {
            "success": True,
            "sop_id": sop_id,
            "sop_name": sop.get("name", sop_id),
            "entity": sop.get("entity"),
            "dry_run": dry_run,
            "step_results": [],
            "started_at": None,
            "completed_at": None,
        }
        
        import time
        from datetime import datetime
        
        result["started_at"] = datetime.now().isoformat()
        
        # Execute each step
        for step in sop.get("steps", []):
            # Check condition
            condition = step.get("condition")
            if condition and not self._evaluate_condition(condition, event):
                continue
            
            # Execute step
            if dry_run:
                step_result = StepResult(
                    step_id=step.get("id", "unknown"),
                    step_name=step.get("name", "Unknown"),
                    success=True,
                    data={"dry_run": True, "type": step.get("type")}
                )
            else:
                step_result = self.execute_step(step, event, sop)
            
            result["step_results"].append({
                "step_id": step_result.step_id,
                "step_name": step_result.step_name,
                "success": step_result.success,
                "error": step_result.error,
                "data": step_result.data,
                "duration_ms": step_result.duration_ms,
            })
            
            # Handle failure
            if not step_result.success:
                on_failure = step.get("on_failure", "stop")
                if on_failure == "stop":
                    result["success"] = False
                    result["error"] = step_result.error
                    break
        
        result["completed_at"] = datetime.now().isoformat()
        
        # Add to history
        self._history.append(result)
        
        return result
    
    def _evaluate_condition(self, condition: str, event: Dict[str, Any]) -> bool:
        """Evaluate a condition string against event data."""
        # Simple condition evaluation
        data = event.get("data", {})
        
        try:
            # Handle common operators
            for op in ["==", "!=", ">=", "<=", ">", "<", " contains ", " in "]:
                if op in condition:
                    parts = condition.split(op, 1)
                    if len(parts) == 2:
                        field = parts[0].strip()
                        value = parts[1].strip().strip('"').strip("'")
                        field_value = data.get(field)
                        
                        if field_value is None:
                            return False
                        
                        if op == "==":
                            return str(field_value) == value
                        elif op == "!=":
                            return str(field_value) != value
                        elif op == " contains ":
                            return value in str(field_value)
                        elif op == " in ":
                            return str(field_value) in value
                        else:
                            # Numeric comparison
                            try:
                                fv = float(field_value)
                                v = float(value)
                                if op == ">=":
                                    return fv >= v
                                elif op == "<=":
                                    return fv <= v
                                elif op == ">":
                                    return fv > v
                                elif op == "<":
                                    return fv < v
                            except ValueError:
                                return False
            return True
        except Exception:
            return False
    
    # Extended step handlers
    
    def _handle_schedule_content(
        self,
        step: Any,
        event: Dict[str, Any],
        sop: Any,
    ) -> StepResult:
        """Handle schedule_content step - queue content for later."""
        config = getattr(step, 'config', {}) or {}
        
        # Add to scheduling queue
        queue_entry = {
            "content": config.get("content"),
            "platforms": config.get("platforms", []),
            "scheduled_at": config.get("scheduled_at"),
            "entity": sop.entity if hasattr(sop, 'entity') else None,
        }
        
        return StepResult(
            step_id=step.id,
            step_name=step.name,
            success=True,
            data={"queued": True, "entry": queue_entry}
        )
    
    def _handle_delay(
        self,
        step: Any,
        event: Dict[str, Any],
        sop: Any,
    ) -> StepResult:
        """Handle delay step - wait for duration or condition."""
        config = getattr(step, 'config', {}) or {}
        
        duration = config.get("duration")
        until = config.get("until")
        until_condition = config.get("until_condition")
        
        # In async execution, this would schedule continuation
        # For now, return success with delay info
        return StepResult(
            step_id=step.id,
            step_name=step.name,
            success=True,
            data={
                "delay_type": "duration" if duration else ("until" if until else "condition"),
                "duration": duration,
                "until": until,
                "until_condition": until_condition,
            }
        )
    
    def _handle_webhook_send(
        self,
        step: Any,
        event: Dict[str, Any],
        sop: Any,
    ) -> StepResult:
        """Handle webhook_send step - send outbound HTTP request."""
        config = getattr(step, 'config', {}) or {}
        
        url = config.get("url")
        method = config.get("method", "POST")
        headers = config.get("headers", {})
        body = config.get("body", {})
        
        if not url:
            return StepResult(
                step_id=step.id,
                step_name=step.name,
                success=False,
                error="No URL specified for webhook"
            )
        
        try:
            import requests
            
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=body,
                timeout=config.get("timeout_seconds", 30),
            )
            
            return StepResult(
                step_id=step.id,
                step_name=step.name,
                success=response.ok,
                data={
                    "status_code": response.status_code,
                    "response_length": len(response.content),
                }
            )
        except Exception as e:
            return StepResult(
                step_id=step.id,
                step_name=step.name,
                success=False,
                error=str(e)
            )
    
    def _handle_data_sync(
        self,
        step: Any,
        event: Dict[str, Any],
        sop: Any,
    ) -> StepResult:
        """Handle data_sync step - sync data between entities."""
        config = getattr(step, 'config', {}) or {}
        
        return StepResult(
            step_id=step.id,
            step_name=step.name,
            success=True,
            data={"message": "Data sync placeholder", "config": config}
        )
    
    def _handle_loop(
        self,
        step: Any,
        event: Dict[str, Any],
        sop: Any,
    ) -> StepResult:
        """Handle loop step - iterate over collection."""
        config = getattr(step, 'config', {}) or {}
        
        return StepResult(
            step_id=step.id,
            step_name=step.name,
            success=True,
            data={"message": "Loop step placeholder", "config": config}
        )
    
    def _handle_transform(
        self,
        step: Any,
        event: Dict[str, Any],
        sop: Any,
    ) -> StepResult:
        """Handle transform step - transform data."""
        config = getattr(step, 'config', {}) or {}
        
        return StepResult(
            step_id=step.id,
            step_name=step.name,
            success=True,
            data={"message": "Transform step placeholder", "config": config}
        )
    
    def _handle_crm_step(
        self,
        step: Any,
        event: Dict[str, Any],
        sop: Any,
    ) -> StepResult:
        """Handle CRM steps - Zoho CRM operations."""
        if not self.crm_handler:
            return StepResult(
                step_id=step.id if hasattr(step, 'id') else 'unknown',
                step_name=step.name if hasattr(step, 'name') else 'CRM Step',
                success=False,
                error="CRM integration not available"
            )
        
        step_type = step.type if hasattr(step, 'type') else 'crm_create'
        config = getattr(step, 'config', {}) or {}
        
        # Build context with variables from event
        context = {
            "variables": event.get("variables", event.get("data", {})),
            "event": event,
            "entity": sop.entity if hasattr(sop, 'entity') else None,
        }
        
        # Execute CRM operation
        result = self.crm_handler.handle_step(step_type, config, context)
        
        return StepResult(
            step_id=step.id if hasattr(step, 'id') else 'unknown',
            step_name=step.name if hasattr(step, 'name') else 'CRM Step',
            success=result.get("success", False),
            error=result.get("error"),
            data=result
        )
    
    def get_history(self, limit: int = 100) -> List[Dict]:
        """Get recent execution history."""
        return self._history[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics."""
        return {
            "definitions_loaded": len(self._definitions),
            "executions": len(self._history),
            "by_entity": {
                entity: len([d for d in self._definitions.values() if d.get("entity") == entity])
                for entity in ["mighty_house_inc", "dsaic", "computer_store", "cross_entity"]
            },
            "extended_step_types": list(self._extended_handlers.keys()),
        }


# Convenience function for quick testing
def create_engine(
    mixpost_client=None,
    ai_client=None,
    load_definitions: bool = True,
) -> EnhancedSOPEngine:
    """
    Create and optionally configure an EnhancedSOPEngine.
    
    Args:
        mixpost_client: MixPost client instance
        ai_client: AI client instance
        load_definitions: Whether to load definitions on creation
        
    Returns:
        Configured EnhancedSOPEngine
    """
    engine = EnhancedSOPEngine(
        mixpost_client=mixpost_client,
        ai_client=ai_client,
    )
    
    if load_definitions:
        engine.load_definitions()
    
    return engine
