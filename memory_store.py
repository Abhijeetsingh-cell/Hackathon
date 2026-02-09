
"""
Memory Storage Module
Handles persistent storage of memories with vector embeddings
"""

import os
import uuid
from typing import List, Optional
from datetime import datetime

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from models import Memory, MemoryCategory, MemorySearchResult


class MemoryStore:
    """
    Manages persistent storage of memories with semantic search capabilities
    """

    def __init__(
        self,
        vector_db_path: str = "./data/vector_store",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.vector_db_path = vector_db_path
        os.makedirs(vector_db_path, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=vector_db_path,
            settings=Settings(anonymized_telemetry=False),
        )

        self.embedding_model = SentenceTransformer(embedding_model)

        self.collection = self.client.get_or_create_collection(
            name="memories",
            metadata={"hnsw:space": "cosine"},
        )

    def _generate_embedding(self, text: str) -> List[float]:
        return self.embedding_model.encode(text).tolist()

    def add_memory(self, memory: Memory) -> str:
        if not memory.id:
            memory.id = str(uuid.uuid4())

        if memory.embedding is None:
            memory.embedding = self._generate_embedding(memory.content)

        metadata = {
            "user_id": memory.user_id,
            "category": memory.category.value,
            "importance": memory.importance,
            "created_at": memory.created_at.isoformat(),
            "last_accessed": memory.last_accessed.isoformat(),
            "access_count": memory.access_count,
            "source_turn": memory.source_turn or 0,
        }

        self.collection.add(
            ids=[memory.id],
            embeddings=[memory.embedding],
            documents=[memory.content],
            metadatas=[metadata],
        )

        return memory.id

    def add_facts(self, user_id: str, facts: List[Memory]) -> None:
        """
        Add multiple extracted memories at once
        """
        for memory in facts:
            memory.user_id = user_id
            self.add_memory(memory)

    def get_memory(self, memory_id: str) -> Optional[Memory]:
        try:
            result = self.collection.get(
                ids=[memory_id],
                include=["embeddings", "documents", "metadatas"],
            )

            if not result["ids"]:
                return None

            meta = result["metadatas"][0]

            return Memory(
                id=result["ids"][0],
                user_id=meta["user_id"],
                content=result["documents"][0],
                category=MemoryCategory(meta["category"]),
                importance=meta["importance"],
                created_at=datetime.fromisoformat(meta["created_at"]),
                last_accessed=datetime.fromisoformat(meta["last_accessed"]),
                access_count=meta["access_count"],
                source_turn=meta.get("source_turn", 0),
                embedding=result["embeddings"][0],
            )

        except Exception as e:
            print(f"Error retrieving memory {memory_id}: {e}")
            return None

    def search_memories(
        self,
        query_text: str,
        user_id: str,
        top_k: int = 5,
        category_filter: Optional[List[MemoryCategory]] = None,
        min_importance: float = 0.0,
    ) -> List[MemorySearchResult]:

        query_embedding = self._generate_embedding(query_text)

        where_clause = {"user_id": user_id}

        if category_filter:
            where_clause["category"] = {
                "$in": [cat.value for cat in category_filter]
            }

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k * 2, 20),
            where=where_clause,
            include=["embeddings", "documents", "metadatas", "distances"],
        )

        if not results["ids"] or not results["ids"][0]:
            return []

        search_results = []

        for i in range(len(results["ids"][0])):
            meta = results["metadatas"][0][i]

            if meta["importance"] < min_importance:
                continue

            memory = Memory(
                id=results["ids"][0][i],
                user_id=meta["user_id"],
                content=results["documents"][0][i],
                category=MemoryCategory(meta["category"]),
                importance=meta["importance"],
                created_at=datetime.fromisoformat(meta["created_at"]),
                last_accessed=datetime.fromisoformat(meta["last_accessed"]),
                access_count=meta["access_count"],
                source_turn=meta.get("source_turn", 0),
                embedding=results["embeddings"][0][i],
            )

            similarity = 1.0 - results["distances"][0][i]

            search_results.append(
                MemorySearchResult(
                    memory=memory,
                    similarity_score=similarity,
                    relevance_score=similarity,
                )
            )

        return search_results[:top_k]

    def update_memory_access(self, memory_id: str):
        memory = self.get_memory(memory_id)
        if not memory:
            return

        memory.update_access()

        self.collection.update(
            ids=[memory_id],
            metadatas=[
                {
                    "last_accessed": memory.last_accessed.isoformat(),
                    "access_count": memory.access_count,
                }
            ],
        )

    def delete_memory(self, memory_id: str) -> bool:
        try:
            self.collection.delete(ids=[memory_id])
            return True
        except Exception as e:
            print(f"Error deleting memory {memory_id}: {e}")
            return False

    def get_user_memories(self, user_id: str, limit: int = 100) -> List[Memory]:
        results = self.collection.get(
            where={"user_id": user_id},
            limit=limit,
            include=["documents", "metadatas"],
        )

        memories = []

        for i in range(len(results["ids"])):
            meta = results["metadatas"][i]

            memories.append(
                Memory(
                    id=results["ids"][i],
                    user_id=meta["user_id"],
                    content=results["documents"][i],
                    category=MemoryCategory(meta["category"]),
                    importance=meta["importance"],
                    created_at=datetime.fromisoformat(meta["created_at"]),
                    last_accessed=datetime.fromisoformat(meta["last_accessed"]),
                    access_count=meta["access_count"],
                    source_turn=meta.get("source_turn", 0),
                )
            )

        return memories

    def count_user_memories(self, user_id: str) -> int:
        results = self.collection.get(where={"user_id": user_id})
        return len(results["ids"])
