"""
Core data models for the AI Memory System
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

from typing import List
from dataclasses import dataclass

@dataclass
class Memory:
    id: str
    user_id: str
    content: str
    importance: float = 0.5
    category: str = "general"
    created_at: str = None  # optionally datetime

@dataclass
class ExtractionResult:
    success: bool
    facts: List[Memory]

@dataclass
class ConversationTurn:
    turn_number: int
    user_id: str
    user_message: str
    assistant_message: str


class MemoryCategory(str, Enum):
    """Categories for organizing memories"""
    PREFERENCE = "preferences"
    COMMITMENT = "commitments"
    RELATIONSHIP = "relationships"
    CONSTRAINT = "constraints"
    INSTRUCTION = "instructions"
    CONTEXT = "context"
    PERSONAL_INFO = "personal_info"


class Memory(BaseModel):
    """A single memory fact"""
    id: Optional[str] = None
    user_id: str
    content: str  # The actual fact/memory
    category: MemoryCategory
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: datetime = Field(default_factory=datetime.utcnow)
    access_count: int = 0
    source_turn: Optional[int] = None  # Which conversation turn this came from
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def update_access(self):
        """Update access statistics"""
        self.last_accessed = datetime.utcnow()
        self.access_count += 1
    
    def compute_current_importance(self, time_decay_enabled: bool = True, 
                                   half_life_days: int = 30) -> float:
        """
        Compute current importance with time decay
        
        Args:
            time_decay_enabled: Whether to apply time decay
            half_life_days: Days for importance to halve
            
        Returns:
            Current importance score
        """
        if not time_decay_enabled:
            return self.importance
        
        # Calculate time decay
        days_elapsed = (datetime.utcnow() - self.created_at).days
        decay_factor = 0.5 ** (days_elapsed / half_life_days)
        
        # Apply decay but maintain minimum threshold
        decayed_importance = self.importance * decay_factor
        return max(decayed_importance, 0.1)


class ConversationTurn(BaseModel):
    """A single turn in the conversation"""
    turn_number: int
    user_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    extracted_memories: List[str] = Field(default_factory=list)  # Memory IDs


class MemoryQuery(BaseModel):
    """Query for retrieving relevant memories"""
    query_text: str
    user_id: str
    top_k: int = 5
    category_filter: Optional[List[MemoryCategory]] = None
    min_importance: float = 0.0
    include_embeddings: bool = False


class MemorySearchResult(BaseModel):
    """Result from memory search"""
    memory: Memory
    relevance_score: float  # Combined score from similarity, recency, importance
    similarity_score: float  # Pure semantic similarity
    
    class Config:
        arbitrary_types_allowed = True


class MemoryExtractionResult(BaseModel):
    """Result from extracting memories from a conversation turn"""
    facts: List[Dict[str, Any]]  # List of extracted facts with metadata
    turn_number: int
    success: bool
    error_message: Optional[str] = None


class UserProfile(BaseModel):
    """User profile containing aggregate memory statistics"""
    user_id: str
    total_memories: int = 0
    memory_categories: Dict[MemoryCategory, int] = Field(default_factory=dict)
    first_interaction: Optional[datetime] = None
    last_interaction: Optional[datetime] = None
    total_turns: int = 0
