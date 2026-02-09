"""
FastAPI Server for AI Memory System

Example REST API for the memory system.
Run with: uvicorn api_server:app --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

from voice_agent import VoiceAgent, MemoryManager
from models import MemoryCategory

app = FastAPI(
    title="AI Memory System API",
    description="REST API for persistent AI memory",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active agents
active_agents = {}

# Request/Response models
class TurnRequest(BaseModel):
    user_id: str
    message: str
    retrieve_memories: bool = True
    extract_memories: bool = True
    top_k: int = 5

class TurnResponse(BaseModel):
    user_id: str
    turn_number: int
    response: str
    memories_retrieved: int
    memories_extracted: int

class MemorySearchRequest(BaseModel):
    user_id: str
    query: str
    top_k: int = 5
    category: Optional[str] = None

class MemoryItem(BaseModel):
    id: str
    content: str
    category: str
    importance: float
    created_at: str
    access_count: int

class UserStatsResponse(BaseModel):
    user_id: str
    total_memories: int
    by_category: dict
    avg_importance: float


def get_or_create_agent(user_id: str) -> VoiceAgent:
    """Get existing agent or create new one"""
    if user_id not in active_agents:
        active_agents[user_id] = VoiceAgent(
            user_id=user_id,
            vector_db_path=os.getenv("VECTOR_DB_PATH", "./data/vector_store"),
            use_llm_extraction=True
        )
    return active_agents[user_id]


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "AI Memory System API",
        "version": "1.0.0",
        "endpoints": [
            "/turn",
            "/memories/search",
            "/memories/stats",
            "/memories/export",
            "/health"
        ]
    }


@app.post("/turn", response_model=TurnResponse)
async def process_turn(request: TurnRequest):
    """
    Process a conversation turn
    
    - **user_id**: User identifier
    - **message**: User's message
    - **retrieve_memories**: Whether to retrieve relevant memories
    - **extract_memories**: Whether to extract new memories
    - **top_k**: Number of memories to retrieve
    """
    try:
        agent = get_or_create_agent(request.user_id)
        
        # Count memories before
        memories_before = len(agent.memory_store.get_user_memories(request.user_id, limit=10000))
        
        # Process turn
        response = agent.process_turn(
            user_message=request.message,
            retrieve_memories=request.retrieve_memories,
            extract_memories=request.extract_memories,
            top_k_memories=request.top_k
        )
        
        # Count memories after
        memories_after = len(agent.memory_store.get_user_memories(request.user_id, limit=10000))
        
        return TurnResponse(
            user_id=request.user_id,
            turn_number=agent.turn_number,
            response=response,
            memories_retrieved=request.top_k if request.retrieve_memories else 0,
            memories_extracted=memories_after - memories_before
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/memories/search")
async def search_memories(request: MemorySearchRequest):
    """
    Search memories for a user
    
    - **user_id**: User identifier
    - **query**: Search query
    - **top_k**: Number of results
    - **category**: Optional category filter
    """
    try:
        agent = get_or_create_agent(request.user_id)
        
        # Apply category filter if specified
        category_filter = None
        if request.category:
            category_filter = [MemoryCategory(request.category)]
        
        # Search
        results = agent.memory_retriever.retrieve_memories(
            query_text=request.query,
            user_id=request.user_id,
            top_k=request.top_k,
            category_filter=category_filter
        )
        
        # Format results
        memories = [
            MemoryItem(
                id=result.memory.id,
                content=result.memory.content,
                category=result.memory.category.value,
                importance=result.memory.importance,
                created_at=result.memory.created_at.isoformat(),
                access_count=result.memory.access_count
            )
            for result in results
        ]
        
        return {
            "user_id": request.user_id,
            "query": request.query,
            "total_results": len(memories),
            "memories": memories
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memories/stats/{user_id}", response_model=UserStatsResponse)
async def get_user_stats(user_id: str):
    """
    Get memory statistics for a user
    
    - **user_id**: User identifier
    """
    try:
        manager = MemoryManager()
        stats = manager.get_user_stats(user_id)
        
        return UserStatsResponse(
            user_id=user_id,
            total_memories=stats.get("total", 0),
            by_category=stats.get("by_category", {}),
            avg_importance=stats.get("avg_importance", 0.0)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memories/export/{user_id}")
async def export_memories(user_id: str):
    """
    Export all memories for a user
    
    - **user_id**: User identifier
    """
    try:
        agent = get_or_create_agent(user_id)
        memories = agent.memory_store.get_user_memories(user_id, limit=10000)
        
        return {
            "user_id": user_id,
            "total_memories": len(memories),
            "memories": [
                {
                    "id": m.id,
                    "content": m.content,
                    "category": m.category.value,
                    "importance": m.importance,
                    "created_at": m.created_at.isoformat(),
                    "last_accessed": m.last_accessed.isoformat(),
                    "access_count": m.access_count,
                    "source_turn": m.source_turn
                }
                for m in memories
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/memories/{user_id}/{memory_id}")
async def delete_memory(user_id: str, memory_id: str):
    """
    Delete a specific memory
    
    - **user_id**: User identifier
    - **memory_id**: Memory identifier
    """
    try:
        agent = get_or_create_agent(user_id)
        success = agent.forget_memory(memory_id)
        
        if success:
            return {"message": "Memory deleted successfully", "memory_id": memory_id}
        else:
            raise HTTPException(status_code=404, detail="Memory not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/memories/{user_id}")
async def clear_all_memories(user_id: str):
    """
    Clear all memories for a user (use with caution!)
    
    - **user_id**: User identifier
    """
    try:
        agent = get_or_create_agent(user_id)
        count = agent.clear_all_memories()
        
        return {
            "message": f"Cleared {count} memories",
            "user_id": user_id,
            "count": count
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_users": len(active_agents)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
