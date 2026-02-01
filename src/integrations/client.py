# src/integrations/mixpost/client.py
"""
Mixpost API Client for social media scheduling and publishing.

Integrates with self-hosted Mixpost (mixpost-malone) instance
for the influencer development pipeline.
"""

import os
import requests
from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class SocialAccount:
    """Represents a connected social media account."""
    id: str
    name: str
    provider: str  # twitter, facebook, instagram, linkedin, tiktok, youtube
    username: str


@dataclass
class Post:
    """Represents a social media post."""
    id: str
    content: str
    accounts: List[str]
    scheduled_at: Optional[datetime]
    published_at: Optional[datetime]
    status: str  # draft, scheduled, published, failed


class MixpostClient:
    """
    Client for interacting with self-hosted Mixpost API.
    
    Mixpost provides Buffer-like social media scheduling without
    subscriptions or limits.
    
    Documentation: https://docs.mixpost.app/
    """
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_token: Optional[str] = None
    ):
        """
        Initialize the Mixpost client.
        
        Args:
            base_url: Mixpost instance URL (e.g., https://mixpost.mightyhouseinc.com)
            api_token: API authentication token
        """
        self.base_url = (base_url or os.getenv("MIXPOST_URL", "")).rstrip("/")
        self.api_token = api_token or os.getenv("MIXPOST_API_TOKEN", "")
        
        self._session = requests.Session()
        if self.api_token:
            self._session.headers["Authorization"] = f"Bearer {self.api_token}"
        self._session.headers["Accept"] = "application/json"
        self._session.headers["Content-Type"] = "application/json"
    
    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make an authenticated request to Mixpost."""
        if not self.base_url:
            raise RuntimeError("Mixpost URL not configured")
        
        url = f"{self.base_url}/api/{endpoint}"
        response = self._session.request(method, url, **kwargs)
        
        if response.status_code >= 400:
            raise RuntimeError(f"Mixpost API error: {response.status_code} - {response.text}")
        
        return response.json() if response.text else {}
    
    # ==================== Workspaces ====================
    
    def get_workspaces(self) -> List[Dict[str, Any]]:
        """
        Get all workspaces.
        
        Returns:
            List of workspace dictionaries
        """
        result = self._request("GET", "workspaces")
        return result.get("data", [])
    
    # ==================== Social Accounts ====================
    
    def get_accounts(self, workspace_id: Optional[str] = None) -> List[SocialAccount]:
        """
        Get connected social media accounts.
        
        Args:
            workspace_id: Optional workspace filter
            
        Returns:
            List of SocialAccount objects
        """
        endpoint = "accounts"
        if workspace_id:
            endpoint = f"workspaces/{workspace_id}/accounts"
        
        result = self._request("GET", endpoint)
        
        return [
            SocialAccount(
                id=acc.get("id", ""),
                name=acc.get("name", ""),
                provider=acc.get("provider", ""),
                username=acc.get("username", ""),
            )
            for acc in result.get("data", [])
        ]
    
    def get_account_by_provider(
        self,
        provider: str,
        workspace_id: Optional[str] = None
    ) -> Optional[SocialAccount]:
        """
        Get account by provider name.
        
        Args:
            provider: Provider name (twitter, instagram, etc.)
            workspace_id: Optional workspace filter
            
        Returns:
            SocialAccount or None
        """
        accounts = self.get_accounts(workspace_id)
        for acc in accounts:
            if acc.provider.lower() == provider.lower():
                return acc
        return None
    
    # ==================== Posts ====================
    
    def get_posts(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        workspace_id: Optional[str] = None
    ) -> List[Post]:
        """
        Get posts.
        
        Args:
            status: Filter by status (draft, scheduled, published, failed)
            limit: Maximum results
            workspace_id: Optional workspace filter
            
        Returns:
            List of Post objects
        """
        endpoint = "posts"
        if workspace_id:
            endpoint = f"workspaces/{workspace_id}/posts"
        
        params = {"per_page": limit}
        if status:
            params["status"] = status
        
        result = self._request("GET", endpoint, params=params)
        
        return [
            Post(
                id=post.get("id", ""),
                content=post.get("content", ""),
                accounts=post.get("accounts", []),
                scheduled_at=self._parse_datetime(post.get("scheduled_at")),
                published_at=self._parse_datetime(post.get("published_at")),
                status=post.get("status", "draft"),
            )
            for post in result.get("data", [])
        ]
    
    def create_post(
        self,
        content: str,
        account_ids: List[str],
        schedule_at: Optional[datetime] = None,
        media_ids: Optional[List[str]] = None,
        workspace_id: Optional[str] = None
    ) -> Post:
        """
        Create a new post.
        
        Args:
            content: Post content/text
            account_ids: List of account IDs to post to
            schedule_at: Optional schedule time (posts immediately if None)
            media_ids: Optional media attachment IDs
            workspace_id: Optional workspace ID
            
        Returns:
            Created Post object
        """
        endpoint = "posts"
        if workspace_id:
            endpoint = f"workspaces/{workspace_id}/posts"
        
        data = {
            "content": content,
            "accounts": account_ids,
        }
        
        if schedule_at:
            data["scheduled_at"] = schedule_at.isoformat()
        if media_ids:
            data["media"] = media_ids
        
        result = self._request("POST", endpoint, json=data)
        post_data = result.get("data", {})
        
        return Post(
            id=post_data.get("id", ""),
            content=post_data.get("content", content),
            accounts=account_ids,
            scheduled_at=schedule_at,
            published_at=None,
            status="scheduled" if schedule_at else "draft",
        )
    
    def schedule_post(
        self,
        post_id: str,
        schedule_at: datetime,
        workspace_id: Optional[str] = None
    ) -> Post:
        """
        Schedule an existing post.
        
        Args:
            post_id: Post ID
            schedule_at: Schedule time
            workspace_id: Optional workspace ID
            
        Returns:
            Updated Post object
        """
        endpoint = f"posts/{post_id}/schedule"
        if workspace_id:
            endpoint = f"workspaces/{workspace_id}/posts/{post_id}/schedule"
        
        data = {"scheduled_at": schedule_at.isoformat()}
        result = self._request("POST", endpoint, json=data)
        
        post_data = result.get("data", {})
        return Post(
            id=post_id,
            content=post_data.get("content", ""),
            accounts=post_data.get("accounts", []),
            scheduled_at=schedule_at,
            published_at=None,
            status="scheduled",
        )
    
    def publish_now(
        self,
        post_id: str,
        workspace_id: Optional[str] = None
    ) -> Post:
        """
        Publish a post immediately.
        
        Args:
            post_id: Post ID
            workspace_id: Optional workspace ID
            
        Returns:
            Updated Post object
        """
        endpoint = f"posts/{post_id}/publish"
        if workspace_id:
            endpoint = f"workspaces/{workspace_id}/posts/{post_id}/publish"
        
        result = self._request("POST", endpoint)
        post_data = result.get("data", {})
        
        return Post(
            id=post_id,
            content=post_data.get("content", ""),
            accounts=post_data.get("accounts", []),
            scheduled_at=None,
            published_at=datetime.now(),
            status="published",
        )
    
    def delete_post(
        self,
        post_id: str,
        workspace_id: Optional[str] = None
    ) -> bool:
        """
        Delete a post.
        
        Args:
            post_id: Post ID
            workspace_id: Optional workspace ID
            
        Returns:
            True if deleted
        """
        endpoint = f"posts/{post_id}"
        if workspace_id:
            endpoint = f"workspaces/{workspace_id}/posts/{post_id}"
        
        self._request("DELETE", endpoint)
        return True
    
    # ==================== Media ====================
    
    def upload_media(
        self,
        file_path: str,
        workspace_id: Optional[str] = None
    ) -> str:
        """
        Upload media file.
        
        Args:
            file_path: Path to media file
            workspace_id: Optional workspace ID
            
        Returns:
            Media ID
        """
        endpoint = "media"
        if workspace_id:
            endpoint = f"workspaces/{workspace_id}/media"
        
        with open(file_path, "rb") as f:
            files = {"file": f}
            # Need to temporarily remove content-type for file upload
            headers = dict(self._session.headers)
            del headers["Content-Type"]
            
            response = self._session.post(
                f"{self.base_url}/api/{endpoint}",
                files=files,
                headers=headers
            )
        
        if response.status_code >= 400:
            raise RuntimeError(f"Media upload failed: {response.text}")
        
        result = response.json()
        return result.get("data", {}).get("id", "")
    
    # ==================== Analytics ====================
    
    def get_analytics(
        self,
        account_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        workspace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get analytics for an account.
        
        Args:
            account_id: Social account ID
            start_date: Start date for analytics
            end_date: End date for analytics
            workspace_id: Optional workspace ID
            
        Returns:
            Analytics dictionary
        """
        endpoint = f"accounts/{account_id}/analytics"
        if workspace_id:
            endpoint = f"workspaces/{workspace_id}/accounts/{account_id}/analytics"
        
        params = {}
        if start_date:
            params["from"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["to"] = end_date.strftime("%Y-%m-%d")
        
        result = self._request("GET", endpoint, params=params)
        return result.get("data", {})
    
    # ==================== Helpers ====================
    
    def _parse_datetime(self, value: Optional[str]) -> Optional[datetime]:
        """Parse ISO datetime string."""
        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    
    # ==================== Influencer Pipeline Integration ====================
    
    def create_influencer_post(
        self,
        influencer_handle: str,
        content: str,
        platforms: List[str],
        schedule_at: Optional[datetime] = None,
        workspace_id: Optional[str] = None
    ) -> List[Post]:
        """
        Create posts for an influencer across multiple platforms.
        
        Args:
            influencer_handle: Influencer's handle/username
            content: Post content (with {handle} placeholder)
            platforms: List of platforms to post to
            schedule_at: Optional schedule time
            workspace_id: Optional workspace ID
            
        Returns:
            List of created Post objects
        """
        # Format content with influencer handle
        formatted_content = content.replace("{handle}", influencer_handle)
        
        # Get account IDs for specified platforms
        accounts = self.get_accounts(workspace_id)
        account_ids = [
            acc.id for acc in accounts
            if acc.provider.lower() in [p.lower() for p in platforms]
        ]
        
        if not account_ids:
            raise RuntimeError(f"No accounts found for platforms: {platforms}")
        
        return [self.create_post(
            content=formatted_content,
            account_ids=account_ids,
            schedule_at=schedule_at,
            workspace_id=workspace_id
        )]
    
    def schedule_partner_promotion(
        self,
        partner_name: str,
        content: str,
        hashtags: List[str],
        schedule_times: List[datetime],
        workspace_id: Optional[str] = None
    ) -> List[Post]:
        """
        Schedule promotional posts for a partner.
        
        Args:
            partner_name: Partner/sponsor name
            content: Promotion content
            hashtags: List of hashtags
            schedule_times: List of schedule times
            workspace_id: Optional workspace ID
            
        Returns:
            List of scheduled Post objects
        """
        # Add hashtags to content
        hashtag_str = " ".join(f"#{tag}" for tag in hashtags)
        full_content = f"{content}\n\n{hashtag_str}"
        
        # Get all accounts
        accounts = self.get_accounts(workspace_id)
        account_ids = [acc.id for acc in accounts]
        
        posts = []
        for schedule_time in schedule_times:
            post = self.create_post(
                content=full_content,
                account_ids=account_ids,
                schedule_at=schedule_time,
                workspace_id=workspace_id
            )
            posts.append(post)
        
        return posts
    
    # ==================== Connection Test ====================
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the API connection.
        
        Returns:
            Connection status and account info
        """
        try:
            workspaces = self.get_workspaces()
            accounts = self.get_accounts()
            
            return {
                "success": True,
                "base_url": self.base_url,
                "workspaces": len(workspaces),
                "connected_accounts": len(accounts),
                "platforms": list(set(acc.provider for acc in accounts)),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

