# src/content/prompt_templates.py
"""
Marketing prompt template system.
Parses and serves Canva/Sora 2 prompts from marketing-prompts.md files.
"""

import re
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum


class MediaType(Enum):
    CANVA = "canva"
    SORA2 = "sora2"


@dataclass
class MediaPrompt:
    """A single media generation prompt."""
    service_id: int
    service_name: str
    price: str
    media_type: MediaType
    variant: int  # 1 or 2
    prompt: str
    category: str
    entity: str
    
    @property
    def id(self) -> str:
        """Unique identifier for this prompt."""
        return f"{self.entity}_{self.service_id}_{self.media_type.value}_{self.variant}"


@dataclass
class ServicePrompts:
    """All prompts for a single service."""
    service_id: int
    name: str
    price: str
    category: str
    entity: str
    canva_prompts: List[str] = field(default_factory=list)
    sora2_prompts: List[str] = field(default_factory=list)
    
    def get_prompts(self, media_type: MediaType) -> List[MediaPrompt]:
        """Get all prompts of a specific type."""
        prompts = self.canva_prompts if media_type == MediaType.CANVA else self.sora2_prompts
        return [
            MediaPrompt(
                service_id=self.service_id,
                service_name=self.name,
                price=self.price,
                media_type=media_type,
                variant=i + 1,
                prompt=p,
                category=self.category,
                entity=self.entity,
            )
            for i, p in enumerate(prompts)
        ]


class PromptTemplateLibrary:
    """
    Library of marketing prompts parsed from markdown files.
    """
    
    def __init__(self):
        self.services: Dict[str, ServicePrompts] = {}  # key: entity_service_id
        self.by_entity: Dict[str, List[ServicePrompts]] = {}
        self.by_category: Dict[str, List[ServicePrompts]] = {}
        self._loaded_files: List[str] = []
    
    def load_from_markdown(self, filepath: Path, entity: str) -> int:
        """
        Parse marketing prompts from a markdown file.
        
        Returns number of services loaded.
        """
        if not filepath.exists():
            return 0
            
        content = filepath.read_text(encoding='utf-8')
        self._loaded_files.append(str(filepath))
        
        # Track current category and service
        current_category = "General"
        current_service: Optional[ServicePrompts] = None
        service_count = 0
        
        # Regex patterns
        category_pattern = re.compile(r'^## [🔧📚📱🎮💱🔍💰🎨]\s*(.+)$', re.MULTILINE)
        service_pattern = re.compile(r'^### (\d+)\.\s*(.+?)(?:\s*\(([^)]+)\))?$', re.MULTILINE)
        
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Check for category header
            cat_match = category_pattern.match(line)
            if cat_match:
                current_category = cat_match.group(1).strip()
                i += 1
                continue
            
            # Check for service header
            svc_match = service_pattern.match(line)
            if svc_match:
                # Save previous service if exists
                if current_service:
                    key = f"{entity}_{current_service.service_id}"
                    self.services[key] = current_service
                    self._index_service(current_service)
                    service_count += 1
                
                service_id = int(svc_match.group(1))
                service_name = svc_match.group(2).strip()
                price = svc_match.group(3) or "TBD"
                
                current_service = ServicePrompts(
                    service_id=service_id,
                    name=service_name,
                    price=price,
                    category=current_category,
                    entity=entity,
                )
                i += 1
                continue
            
            # Check for prompt blocks
            if current_service and line.startswith('**Canva Prompt'):
                prompt = self._extract_code_block(lines, i + 1)
                if prompt:
                    current_service.canva_prompts.append(prompt)
                i += 1
                continue
                
            if current_service and line.startswith('**Sora 2 Prompt'):
                prompt = self._extract_code_block(lines, i + 1)
                if prompt:
                    current_service.sora2_prompts.append(prompt)
                i += 1
                continue
            
            i += 1
        
        # Save last service
        if current_service:
            key = f"{entity}_{current_service.service_id}"
            self.services[key] = current_service
            self._index_service(current_service)
            service_count += 1
        
        return service_count
    
    def _extract_code_block(self, lines: List[str], start_idx: int) -> Optional[str]:
        """Extract content from a markdown code block."""
        # Find opening ```
        i = start_idx
        while i < len(lines) and not lines[i].strip().startswith('```'):
            i += 1
        
        if i >= len(lines):
            return None
        
        i += 1  # Skip opening ```
        content_lines = []
        
        while i < len(lines) and not lines[i].strip().startswith('```'):
            content_lines.append(lines[i])
            i += 1
        
        return '\n'.join(content_lines).strip() if content_lines else None
    
    def _index_service(self, service: ServicePrompts):
        """Add service to indexes."""
        # By entity
        if service.entity not in self.by_entity:
            self.by_entity[service.entity] = []
        self.by_entity[service.entity].append(service)
        
        # By category
        if service.category not in self.by_category:
            self.by_category[service.category] = []
        self.by_category[service.category].append(service)
    
    def get_service(self, entity: str, service_id: int) -> Optional[ServicePrompts]:
        """Get a specific service's prompts."""
        key = f"{entity}_{service_id}"
        return self.services.get(key)
    
    def get_all_prompts(
        self,
        entity: Optional[str] = None,
        category: Optional[str] = None,
        media_type: Optional[MediaType] = None,
    ) -> List[MediaPrompt]:
        """
        Get prompts with optional filters.
        """
        services = list(self.services.values())
        
        if entity:
            services = [s for s in services if s.entity == entity]
        
        if category:
            services = [s for s in services if s.category == category]
        
        prompts = []
        for service in services:
            if media_type is None or media_type == MediaType.CANVA:
                prompts.extend(service.get_prompts(MediaType.CANVA))
            if media_type is None or media_type == MediaType.SORA2:
                prompts.extend(service.get_prompts(MediaType.SORA2))
        
        return prompts
    
    def get_categories(self, entity: Optional[str] = None) -> List[str]:
        """Get unique categories."""
        if entity:
            services = self.by_entity.get(entity, [])
            return list(set(s.category for s in services))
        return list(self.by_category.keys())
    
    def get_random_prompt(
        self,
        entity: Optional[str] = None,
        category: Optional[str] = None,
        media_type: Optional[MediaType] = None,
    ) -> Optional[MediaPrompt]:
        """Get a random prompt matching filters."""
        import random
        prompts = self.get_all_prompts(entity, category, media_type)
        return random.choice(prompts) if prompts else None
    
    def search_prompts(self, query: str) -> List[MediaPrompt]:
        """Search prompts by keyword."""
        query_lower = query.lower()
        results = []
        
        for prompt in self.get_all_prompts():
            if (query_lower in prompt.service_name.lower() or
                query_lower in prompt.prompt.lower() or
                query_lower in prompt.category.lower()):
                results.append(prompt)
        
        return results
    
    def to_dict(self) -> Dict[str, Any]:
        """Export library stats."""
        return {
            "total_services": len(self.services),
            "entities": list(self.by_entity.keys()),
            "categories": list(self.by_category.keys()),
            "services_by_entity": {
                entity: len(services) 
                for entity, services in self.by_entity.items()
            },
            "total_prompts": {
                "canva": sum(len(s.canva_prompts) for s in self.services.values()),
                "sora2": sum(len(s.sora2_prompts) for s in self.services.values()),
            },
            "loaded_files": self._loaded_files,
        }


# Global library instance
_library: Optional[PromptTemplateLibrary] = None


def get_prompt_library() -> PromptTemplateLibrary:
    """Get or create the global prompt library."""
    global _library
    if _library is None:
        _library = PromptTemplateLibrary()
        _load_default_prompts(_library)
    return _library


def _load_default_prompts(library: PromptTemplateLibrary):
    """Load prompt files from default locations."""
    # Project root
    project_root = Path(__file__).parent.parent.parent
    sops_dir = project_root / "sops"
    
    # Entity mappings
    entity_dirs = {
        "mighty-house-inc": "mighty_house_inc",
        "dsaic": "dsaic", 
        "computer-store": "computer_store",
    }
    
    for dir_name, entity_id in entity_dirs.items():
        prompts_file = sops_dir / dir_name / "marketing-prompts.md"
        if prompts_file.exists():
            count = library.load_from_markdown(prompts_file, entity_id)
            print(f"Loaded {count} services from {prompts_file.name} for {entity_id}")


def reload_library():
    """Force reload of the prompt library."""
    global _library
    _library = None
    return get_prompt_library()
