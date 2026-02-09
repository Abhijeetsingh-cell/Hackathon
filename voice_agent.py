# voice_agent.py
from typing import List
from groq import Groq

from models import ConversationTurn
from memory_store import MemoryStore
from memory_retriever import MemoryRetriever
from memory_extractor import MemoryExtractor


class VoiceAgent:
    SYSTEM_PROMPT = (
        "You are a helpful AI assistant with long-term memory. "
        "Use remembered information when relevant."
    )

    def __init__(self, user_id: str, groq_api_key: str, vector_db_path="./data/vector_store"):
        self.user_id = user_id
        self.client = Groq(api_key=groq_api_key)

        self.turn_number = 0
        self.conversation_history: List[ConversationTurn] = []

        self.memory_store = MemoryStore(vector_db_path=vector_db_path)
        self.memory_retriever = MemoryRetriever(self.memory_store)
        self.memory_extractor = MemoryExtractor()

    def process_turn(self, user_message: str) -> str:
        self.turn_number += 1

        memory_context = self.memory_retriever.get_context_for_turn(
            current_message=user_message,
            user_id=self.user_id,
            top_k=5,
        )

        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
        ]

        if memory_context:
            messages.append(
                {
                    "role": "system",
                    "content": f"Relevant memory:\n{memory_context}"
                }
            )

        messages.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.7,
                max_tokens=512,
            )
            assistant_message = response.choices[0].message.content
        except Exception as e:
            assistant_message = f"[Groq API error: {e}]"

        extraction = self.memory_extractor.extract_memories(
            user_message=user_message,
            assistant_message=assistant_message,
            user_id=self.user_id,
            turn_number=self.turn_number,
        )

        if extraction.success and extraction.facts:
            self.memory_store.add_facts(self.user_id, extraction.facts)

        self.conversation_history.append(
            ConversationTurn(
                turn_number=self.turn_number,
                user_id=self.user_id,
                user_message=user_message,
                assistant_message=assistant_message,
            )
        )

        return assistant_message






