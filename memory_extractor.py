from typing import List
from models import Memory, ExtractionResult

class MemoryExtractor:
    """
    Extract important facts from user/assistant messages using Groq.
    """

    def extract_memories(self, user_message: str, assistant_message: str, user_id: str, turn_number: int) -> ExtractionResult:
        """
        Returns an ExtractionResult with important facts.
        This version uses simple heuristics; you can replace with Groq LLM call if needed.
        """
        facts: List[Memory] = []

        # Simple heuristic example: extract sentences containing "remember", "important", "note"
        combined = f"{user_message}\n{assistant_message}"
        lines = combined.split(".")
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ["remember", "important", "note"]):
                facts.append(Memory(
                    id=f"{user_id}-{turn_number}-{len(facts)}",
                    user_id=user_id,
                    content=line,
                    importance=1.0,
                    category="preferences"
                ))

        return ExtractionResult(success=True, facts=facts)

