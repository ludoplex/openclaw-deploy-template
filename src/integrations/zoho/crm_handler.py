"""
Zoho CRM Handler for SOP Automation.

Provides step handlers for CRM operations within SOPs:
- Create records (Leads, Contacts, Deals, etc.)
- Update record fields
- Search/lookup records
- Deal stage changes
- Workflow triggers
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

# Add Zoho API system to path
ZOHO_API_PATH = Path(r"C:\zoho-console-api-module-system")
if ZOHO_API_PATH.exists():
    sys.path.insert(0, str(ZOHO_API_PATH))
    ZOHO_AVAILABLE = True
    try:
        from src.modules.crm.client import CRMClient
        from src.modules.crm.records import RecordManager
        from src.modules.crm.search import SearchManager
    except ImportError as e:
        print(f"Zoho CRM import error: {e}")
        ZOHO_AVAILABLE = False
else:
    ZOHO_AVAILABLE = False


class ZohoCRMHandler:
    """
    High-level handler for Zoho CRM operations in SOP context.
    """
    
    def __init__(self):
        self._client: Optional[CRMClient] = None
        self._connected = False
        self._last_error: Optional[str] = None
    
    @property
    def available(self) -> bool:
        """Check if Zoho CRM is available."""
        return ZOHO_AVAILABLE
    
    @property
    def connected(self) -> bool:
        """Check if connected to CRM."""
        return self._connected
    
    def connect(self) -> bool:
        """Establish connection to Zoho CRM."""
        if not ZOHO_AVAILABLE:
            self._last_error = "Zoho API system not available"
            return False
        
        try:
            self._client = CRMClient()
            result = self._client.test_crm_connection()
            self._connected = result.get("success", False)
            if not self._connected:
                self._last_error = result.get("error", "Unknown error")
            return self._connected
        except Exception as e:
            self._last_error = str(e)
            self._connected = False
            return False
    
    def disconnect(self):
        """Close connection."""
        if self._client:
            self._client = None
        self._connected = False
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, *args):
        self.disconnect()
    
    # ==================== Record Operations ====================
    
    def create_record(
        self,
        module: str,
        data: Dict[str, Any],
        trigger_workflows: bool = True
    ) -> Dict[str, Any]:
        """
        Create a CRM record.
        
        Args:
            module: CRM module (Leads, Contacts, Deals, etc.)
            data: Record field values
            trigger_workflows: Whether to trigger Zoho workflows
            
        Returns:
            Result with record_id or error
        """
        if not self._connected:
            return {"success": False, "error": "Not connected to CRM"}
        
        try:
            triggers = ["workflow", "blueprint"] if trigger_workflows else []
            result = self._client.create_record(module, data, trigger=triggers)
            
            if result.get("status") == "success":
                return {
                    "success": True,
                    "record_id": result.get("details", {}).get("id"),
                    "module": module,
                    "message": f"Created {module} record"
                }
            else:
                return {
                    "success": False,
                    "error": result.get("message", "Creation failed"),
                    "code": result.get("code")
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_record(
        self,
        module: str,
        record_id: str,
        data: Dict[str, Any],
        trigger_workflows: bool = True
    ) -> Dict[str, Any]:
        """
        Update a CRM record.
        
        Args:
            module: CRM module
            record_id: Record ID to update
            data: Fields to update
            trigger_workflows: Whether to trigger Zoho workflows
            
        Returns:
            Result with success status
        """
        if not self._connected:
            return {"success": False, "error": "Not connected to CRM"}
        
        try:
            triggers = ["workflow", "blueprint"] if trigger_workflows else []
            result = self._client.update_record(module, record_id, data, trigger=triggers)
            
            if result.get("status") == "success":
                return {
                    "success": True,
                    "record_id": record_id,
                    "module": module,
                    "message": f"Updated {module} record"
                }
            else:
                return {
                    "success": False,
                    "error": result.get("message", "Update failed")
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_record(
        self,
        module: str,
        record_id: str,
        fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Get a specific record."""
        if not self._connected:
            return {"success": False, "error": "Not connected to CRM"}
        
        try:
            record = self._client.get_record(module, record_id, fields)
            if record:
                return {"success": True, "record": record}
            else:
                return {"success": False, "error": "Record not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_records(
        self,
        module: str,
        criteria: str,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Search for records.
        
        Args:
            module: CRM module
            criteria: Zoho search criteria (e.g., "(Email:equals:test@example.com)")
            limit: Max records to return
            
        Returns:
            Result with records list
        """
        if not self._connected:
            return {"success": False, "error": "Not connected to CRM"}
        
        try:
            records = self._client.search_records(module, criteria, per_page=limit)
            return {
                "success": True,
                "records": records,
                "count": len(records)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_deal_stage(
        self,
        deal_id: str,
        stage: str,
        probability: Optional[int] = None,
        closing_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update deal stage with optional fields.
        
        Args:
            deal_id: Deal record ID
            stage: New stage name
            probability: Win probability (0-100)
            closing_date: Expected close date (YYYY-MM-DD)
        """
        data = {"Stage": stage}
        if probability is not None:
            data["Probability"] = probability
        if closing_date:
            data["Closing_Date"] = closing_date
        
        return self.update_record("Deals", deal_id, data)
    
    # ==================== Entity-Specific Helpers ====================
    
    def create_lead(
        self,
        first_name: str,
        last_name: str,
        email: str,
        company: Optional[str] = None,
        phone: Optional[str] = None,
        source: str = "SOP Automation",
        **extra_fields
    ) -> Dict[str, Any]:
        """Create a lead with standard fields."""
        data = {
            "First_Name": first_name,
            "Last_Name": last_name,
            "Email": email,
            "Lead_Source": source,
        }
        if company:
            data["Company"] = company
        if phone:
            data["Phone"] = phone
        data.update(extra_fields)
        
        return self.create_record("Leads", data)
    
    def create_contact(
        self,
        first_name: str,
        last_name: str,
        email: str,
        account_id: Optional[str] = None,
        phone: Optional[str] = None,
        **extra_fields
    ) -> Dict[str, Any]:
        """Create a contact with standard fields."""
        data = {
            "First_Name": first_name,
            "Last_Name": last_name,
            "Email": email,
        }
        if account_id:
            data["Account_Name"] = {"id": account_id}
        if phone:
            data["Phone"] = phone
        data.update(extra_fields)
        
        return self.create_record("Contacts", data)
    
    def create_deal(
        self,
        deal_name: str,
        stage: str,
        amount: float,
        account_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        closing_date: Optional[str] = None,
        **extra_fields
    ) -> Dict[str, Any]:
        """Create a deal with standard fields."""
        data = {
            "Deal_Name": deal_name,
            "Stage": stage,
            "Amount": amount,
        }
        if account_id:
            data["Account_Name"] = {"id": account_id}
        if contact_id:
            data["Contact_Name"] = {"id": contact_id}
        if closing_date:
            data["Closing_Date"] = closing_date
        else:
            # Default to 30 days from now
            data["Closing_Date"] = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        data.update(extra_fields)
        
        return self.create_record("Deals", data)
    
    def create_task(
        self,
        subject: str,
        due_date: str,
        owner_id: Optional[str] = None,
        related_to: Optional[Dict[str, str]] = None,
        priority: str = "Normal",
        status: str = "Not Started",
        **extra_fields
    ) -> Dict[str, Any]:
        """Create a task."""
        data = {
            "Subject": subject,
            "Due_Date": due_date,
            "Priority": priority,
            "Status": status,
        }
        if owner_id:
            data["Owner"] = {"id": owner_id}
        if related_to:
            # related_to should be {"module": "Deals", "id": "123456"}
            data["What_Id"] = {"id": related_to["id"]}
            data["$se_module"] = related_to["module"]
        data.update(extra_fields)
        
        return self.create_record("Tasks", data)


class CRMStepHandler:
    """
    SOP Step Handler for CRM operations.
    
    Processes CRM step types from SOP workflows:
    - crm_create: Create a record
    - crm_update: Update a record
    - crm_search: Search for records
    - crm_deal_stage: Update deal stage
    """
    
    def __init__(self, crm_handler: Optional[ZohoCRMHandler] = None):
        self.crm = crm_handler or ZohoCRMHandler()
        self._connected = False
    
    def ensure_connected(self) -> bool:
        """Ensure CRM connection is established."""
        if not self._connected:
            self._connected = self.crm.connect()
        return self._connected
    
    def handle_step(
        self,
        step_type: str,
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle a CRM step in an SOP workflow.
        
        Args:
            step_type: Type of CRM operation
            config: Step configuration from YAML
            context: Current execution context with variables
            
        Returns:
            Step result with success status and data
        """
        if not self.ensure_connected():
            return {
                "success": False,
                "error": "Could not connect to Zoho CRM",
                "skipped": True
            }
        
        # Substitute variables in config
        config = self._substitute_vars(config, context)
        
        handlers = {
            "crm_create": self._handle_create,
            "crm_update": self._handle_update,
            "crm_search": self._handle_search,
            "crm_deal_stage": self._handle_deal_stage,
            "crm_create_task": self._handle_create_task,
        }
        
        handler = handlers.get(step_type)
        if not handler:
            return {"success": False, "error": f"Unknown CRM step type: {step_type}"}
        
        return handler(config, context)
    
    def _substitute_vars(
        self,
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Replace {{variable}} placeholders with context values."""
        import re
        
        def replace_vars(value):
            if isinstance(value, str):
                pattern = r'\{\{(\w+)\}\}'
                matches = re.findall(pattern, value)
                for var in matches:
                    if var in context.get("variables", {}):
                        value = value.replace(f"{{{{{var}}}}}", str(context["variables"][var]))
                return value
            elif isinstance(value, dict):
                return {k: replace_vars(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [replace_vars(v) for v in value]
            return value
        
        return replace_vars(config)
    
    def _handle_create(
        self,
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle crm_create step."""
        module = config.get("module", "Leads")
        data = config.get("data", {})
        
        result = self.crm.create_record(module, data)
        
        # Store record_id in context for later steps
        if result.get("success") and result.get("record_id"):
            context.setdefault("variables", {})
            context["variables"][f"crm_{module.lower()}_id"] = result["record_id"]
        
        return result
    
    def _handle_update(
        self,
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle crm_update step."""
        module = config.get("module", "Leads")
        record_id = config.get("record_id")
        data = config.get("data", {})
        
        if not record_id:
            return {"success": False, "error": "No record_id specified"}
        
        return self.crm.update_record(module, record_id, data)
    
    def _handle_search(
        self,
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle crm_search step."""
        module = config.get("module", "Leads")
        criteria = config.get("criteria", "")
        limit = config.get("limit", 10)
        store_as = config.get("store_as", "search_results")
        
        result = self.crm.search_records(module, criteria, limit)
        
        # Store results in context
        if result.get("success"):
            context.setdefault("variables", {})
            context["variables"][store_as] = result.get("records", [])
        
        return result
    
    def _handle_deal_stage(
        self,
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle crm_deal_stage step."""
        deal_id = config.get("deal_id")
        stage = config.get("stage")
        probability = config.get("probability")
        closing_date = config.get("closing_date")
        
        if not deal_id or not stage:
            return {"success": False, "error": "deal_id and stage are required"}
        
        return self.crm.update_deal_stage(deal_id, stage, probability, closing_date)
    
    def _handle_create_task(
        self,
        config: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle crm_create_task step."""
        subject = config.get("subject", "Task from SOP")
        due_date = config.get("due_date", (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
        related_to = config.get("related_to")
        priority = config.get("priority", "Normal")
        
        return self.crm.create_task(
            subject=subject,
            due_date=due_date,
            related_to=related_to,
            priority=priority
        )


# CLI test
if __name__ == "__main__":
    print("Testing Zoho CRM Handler...")
    print(f"Zoho API available: {ZOHO_AVAILABLE}")
    
    if ZOHO_AVAILABLE:
        with ZohoCRMHandler() as crm:
            if crm.connected:
                print("✓ Connected to Zoho CRM")
                
                # Test search
                result = crm.search_records("Leads", "(Lead_Source:equals:Web)", limit=5)
                print(f"Search result: {result.get('count', 0)} leads found")
            else:
                print(f"✗ Connection failed: {crm._last_error}")
    else:
        print("Zoho API system not found at expected path")
