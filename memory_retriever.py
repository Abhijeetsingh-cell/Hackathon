from typing import List
from models import Memory
import numpy as np

class MemoryRetriever:
    """
    Retrieve relevant memories from vector store using simple cosine similarity.
    """

    def __init__(self, memory_store):
        self.memory_store = memory_store

    def retrieve_memories(self, query_text: str, user_id: str, top_k: int = 5) -> List[Memory]:
        # Fetch all memories
        memories = self.memory_store.get_user_memories(user_id)
        if not memories:
            return []

        # Compute embeddings using Groq predict for the query
        # Placeholder: just use string length similarity for demo
        query_len = len(query_text)
        scored = []
        for mem in memories:
            score = 1 - abs(len(mem.content) - query_len) / max(len(mem.content), query_len)
            scored.append((score, mem))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [mem for _, mem in scored[:top_k]]

    def get_context_for_turn(self, current_message: str, user_id: str, top_k: int = 5) -> str:
        top_memories = self.retrieve_memories(current_message, user_id, top_k)
        return "\n".join(mem.content for mem in top_memories)

