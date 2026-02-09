# Usage Examples

This document provides practical examples of using the AI Memory System.

## Basic Setup

```python
from voice_agent import VoiceAgent
import os

# Set your API key
os.environ["ANTHROPIC_API_KEY"] = "your-api-key-here"

# Create an agent
agent = VoiceAgent(
    user_id="user_123",
    vector_db_path="./data/vector_store",
    use_llm_extraction=True  # Use LLM for better extraction
)
```

## Example 1: Simple Conversation with Memory

```python
# Turn 1: User shares information
response = agent.process_turn("My name is Alice and I work as a doctor")
print(response)

# Turn 2: User asks something unrelated
response = agent.process_turn("What's the weather like?")
print(response)

# Turn 50: Agent should remember Alice's profession
response = agent.process_turn("What kind of medical resources would help me?")
print(response)
# Agent will recall that user is a doctor
```

## Example 2: Language Preference (Problem Statement)

```python
# Turn 1: Critical preference
agent.process_turn("My preferred language is Kannada")

# ... many turns later ...

# Turn 937: Make a request
response = agent.process_turn("Can you call me tomorrow?")
# Agent will remember language preference and respond accordingly
```

## Example 3: Searching Memories

```python
# Search for specific memories
memories = agent.search_memories("dietary restrictions", top_k=5)

for memory in memories:
    print(f"- {memory.content} (importance: {memory.importance})")
```

## Example 4: Viewing User Profile

```python
# Get summary of what the system knows
summary = agent.get_user_profile_summary()
print(summary)

# Output:
# User Profile Summary (Total memories: 15)
# 
# PREFERENCES (5):
#   • Preferred language is Kannada (importance: 0.90)
#   • Likes formal communication (importance: 0.70)
#   ...
```

## Example 5: Category-Specific Retrieval

```python
from memory_retriever import MemoryRetriever
from models import MemoryCategory

retriever = MemoryRetriever(agent.memory_store)

# Get all commitments
commitments = retriever.retrieve_by_category(
    user_id="user_123",
    category=MemoryCategory.COMMITMENT,
    top_k=10
)

print("User's commitments:")
for commit in commitments:
    print(f"- {commit.content}")
```

## Example 6: Recent Memories

```python
# Get memories from last 7 days
recent = retriever.retrieve_recent_memories(
    user_id="user_123",
    days=7,
    top_k=20
)

print(f"Found {len(recent)} recent memories")
```

## Example 7: Manual Memory Management

```python
# Add a memory manually
from models import Memory, MemoryCategory

manual_memory = Memory(
    user_id="user_123",
    content="User is allergic to shellfish",
    category=MemoryCategory.CONSTRAINT,
    importance=0.95
)

memory_id = agent.memory_store.add_memory(manual_memory)

# Delete a memory
agent.forget_memory(memory_id)
```

## Example 8: Multi-User Setup

```python
# Create agents for different users
alice_agent = VoiceAgent(user_id="alice", vector_db_path="./data/vector_store")
bob_agent = VoiceAgent(user_id="bob", vector_db_path="./data/vector_store")

# Each has isolated memories
alice_agent.process_turn("I love hiking")
bob_agent.process_turn("I prefer swimming")

# Alice's agent won't see Bob's memories
alice_memories = alice_agent.search_memories("exercise", top_k=5)
# Will only return Alice's hiking preference
```

## Example 9: Memory Statistics

```python
from voice_agent import MemoryManager

manager = MemoryManager(vector_db_path="./data/vector_store")

# Get statistics for a user
stats = manager.get_user_stats("user_123")

print(f"Total memories: {stats['total']}")
print(f"Average importance: {stats['avg_importance']:.2f}")
print(f"Memories by category: {stats['by_category']}")
```

## Example 10: Exporting Memories

```python
# Export all memories to JSON
manager.export_user_memories(
    user_id="user_123",
    output_file="user_123_memories.json"
)

# The exported JSON will contain all memories with metadata
```

## Example 11: Custom Memory Extraction

```python
# Use simple rule-based extraction (no API key needed)
agent = VoiceAgent(
    user_id="user_123",
    vector_db_path="./data/vector_store",
    use_llm_extraction=False  # Use rule-based extractor
)

# Process turns - will extract based on keywords
agent.process_turn("I prefer email over phone calls")
# System will detect "prefer" keyword and store as preference
```

## Example 12: Conversation Summary

```python
# After multiple turns
for i in range(10):
    agent.process_turn(f"Message {i}")

# Get conversation summary
summary = agent.get_conversation_summary()
print(summary)

# Output:
# Conversation Summary
# Total turns: 10
# User: user_123
# 
# Recent turns:
# Turn 6: User: Message 6...
# ...
```

## Example 13: Custom Retrieval Parameters

```python
from memory_retriever import MemoryRetriever

# Create retriever with custom weights
retriever = MemoryRetriever(
    memory_store=agent.memory_store,
    recency_weight=0.5,      # Prioritize recent memories
    importance_weight=0.3,    # Moderate importance weight
    relevance_weight=0.2,     # Lower semantic relevance
    time_decay_enabled=True,
    half_life_days=14         # Faster decay (2 weeks)
)

# Use for retrieval
results = retriever.retrieve_memories(
    query_text="user preferences",
    user_id="user_123",
    top_k=10
)
```

## Example 14: Production Setup with Configuration

```python
import yaml
from voice_agent import VoiceAgent

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Create agent with config
agent = VoiceAgent(
    user_id="user_123",
    vector_db_path=config['storage']['vector_db_path'],
    model=config['extraction']['model'],
    use_llm_extraction=True
)
```

## Example 15: Error Handling

```python
try:
    response = agent.process_turn("Hello!")
    print(response)
except Exception as e:
    print(f"Error processing turn: {e}")
    
    # Fallback to simple extraction
    agent = VoiceAgent(
        user_id="user_123",
        vector_db_path="./data/vector_store",
        use_llm_extraction=False
    )
    response = agent.process_turn("Hello!")
```

## Advanced: Custom Embedding Model

```python
from memory_store import MemoryStore

# Use a different embedding model
store = MemoryStore(
    vector_db_path="./data/vector_store",
    embedding_model="sentence-transformers/all-mpnet-base-v2"  # Larger, more accurate
)
```

## Testing Without API Key

```python
# For testing or development without API key
from memory_extractor import SimpleMemoryExtractor

agent = VoiceAgent(
    user_id="test_user",
    vector_db_path="./test_data",
    use_llm_extraction=False  # Use rule-based extraction
)

# Will work without API key, but extraction quality is lower
agent.process_turn("I prefer morning meetings")
```

## Performance Tips

1. **Batch Processing**: Process multiple messages before retrieving memories
2. **Adjust top_k**: Use smaller values (3-5) for faster retrieval
3. **Category Filters**: Filter by category when you know what you're looking for
4. **Time Decay**: Enable time decay to prioritize recent memories
5. **Regular Cleanup**: Periodically remove very old, low-importance memories

## Common Patterns

### Pattern 1: Initialize Once, Use Many Times
```python
# Initialize agent once for the session
agent = VoiceAgent(user_id="user_123", vector_db_path="./data/vector_store")

# Process many turns
for message in user_messages:
    response = agent.process_turn(message)
    send_to_user(response)
```

### Pattern 2: Context-Aware Responses
```python
# Agent automatically retrieves relevant memories
response = agent.process_turn(
    user_message="What diet should I follow?",
    retrieve_memories=True,  # Retrieves dietary preferences, allergies
    top_k_memories=5
)
```

### Pattern 3: Memory Inspection
```python
# Check what was remembered after a turn
memories_before = len(agent.memory_store.get_user_memories("user_123"))
agent.process_turn("I'm moving to Tokyo next month")
memories_after = len(agent.memory_store.get_user_memories("user_123"))

print(f"New memories: {memories_after - memories_before}")
```
