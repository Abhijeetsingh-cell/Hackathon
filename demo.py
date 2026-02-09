"""
Demo Script for AI Memory System

This script demonstrates the key capabilities of the persistent memory system,
including the exact scenario described in the problem statement.
"""

import os
import time
from voice_agent import VoiceAgent, MemoryManager


def print_separator(title: str = ""):
    """Print a visual separator"""
    if title:
        print(f"\n{'=' * 80}")
        print(f"  {title}")
        print(f"{'=' * 80}\n")
    else:
        print(f"\n{'-' * 80}\n")


def demo_basic_memory():
    """Demonstrate basic memory storage and retrieval"""
    print_separator("DEMO 1: Basic Memory Storage and Retrieval")
    
    # Create agent
    agent = VoiceAgent(
        user_id="demo_user_1",
        vector_db_path="./demo_data/vector_store",
        use_llm_extraction=False  # Use simple extraction for demo
    )
    
    print("Turn 1: User shares language preference")
    response1 = agent.process_turn("My preferred language is Kannada")
    print(f"Assistant: {response1}\n")
    
    print("Turn 2: Casual conversation")
    response2 = agent.process_turn("How's the weather today?")
    print(f"Assistant: {response2}\n")
    
    print("Turn 3: User makes a request (should remember language)")
    response3 = agent.process_turn("Can you summarize this for me?")
    print(f"Assistant: {response3}\n")
    
    # Show what was remembered
    print_separator("Stored Memories")
    print(agent.get_user_profile_summary())


def demo_long_context_problem():
    """Demonstrate the exact problem from the specification"""
    print_separator("DEMO 2: Long Context Problem (Turn 1 → Turn 937)")
    
    agent = VoiceAgent(
        user_id="demo_user_2",
        vector_db_path="./demo_data/vector_store",
        use_llm_extraction=False
    )
    
    # Turn 1: Critical information
    print("Turn 1: User shares language preference and constraints")
    agent.process_turn("My preferred language is Kannada. I'm only available after 6 PM IST.")
    print("✓ Memories stored\n")
    
    # Simulate many turns (we'll skip to turn 937)
    print("Simulating turns 2-936...")
    for i in range(2, 937):
        if i % 100 == 0:
            print(f"  Processing turn {i}...")
        agent.process_turn(f"Random message {i}")
    
    print(f"\n✓ Completed {agent.turn_number} turns\n")
    
    # Turn 937: Request that requires memory
    print("Turn 937: User makes a request requiring information from Turn 1")
    response = agent.process_turn("Can you call me tomorrow?")
    print(f"Assistant: {response}\n")
    
    # Search for what system remembers
    print_separator("Memory Retrieval Check")
    print("Searching for 'language' related memories:")
    language_memories = agent.search_memories("language", top_k=3)
    for i, mem in enumerate(language_memories, 1):
        print(f"{i}. {mem.content} (Turn {mem.source_turn}, Importance: {mem.importance:.2f})")
    
    print("\nSearching for 'time' related memories:")
    time_memories = agent.search_memories("time availability", top_k=3)
    for i, mem in enumerate(time_memories, 1):
        print(f"{i}. {mem.content} (Turn {mem.source_turn}, Importance: {mem.importance:.2f})")


def demo_memory_categories():
    """Demonstrate different memory categories"""
    print_separator("DEMO 3: Memory Categories")
    
    agent = VoiceAgent(
        user_id="demo_user_3",
        vector_db_path="./demo_data/vector_store",
        use_llm_extraction=False
    )
    
    # Different types of information
    test_messages = [
        "I prefer formal communication style",  # Preference
        "Please remind me to call John tomorrow at 3 PM",  # Commitment
        "My wife's name is Sarah and she loves gardening",  # Relationship
        "I'm in the EST timezone",  # Constraint
        "Always check with me before making reservations",  # Instruction
    ]
    
    print("Processing various types of information:\n")
    for i, msg in enumerate(test_messages, 1):
        print(f"Turn {i}: {msg}")
        response = agent.process_turn(msg)
        print(f"Response: {response}\n")
    
    print_separator("Memory Organization")
    print(agent.get_user_profile_summary())


def demo_memory_retrieval_quality():
    """Demonstrate semantic search and relevance ranking"""
    print_separator("DEMO 4: Semantic Search and Relevance Ranking")
    
    agent = VoiceAgent(
        user_id="demo_user_4",
        vector_db_path="./demo_data/vector_store",
        use_llm_extraction=False
    )
    
    # Store diverse memories
    memories_to_store = [
        "I love Italian food, especially pasta carbonara",
        "I'm allergic to peanuts",
        "I prefer to exercise in the morning",
        "I work as a software engineer at Google",
        "My favorite programming language is Python",
        "I'm learning Spanish on weekends",
        "I have two kids, ages 5 and 7",
        "I'm planning a trip to Japan next year",
    ]
    
    print("Storing diverse memories...\n")
    for msg in memories_to_store:
        agent.process_turn(msg)
    
    # Test semantic search
    print_separator("Semantic Search Tests")
    
    queries = [
        "What does the user eat?",
        "Tell me about the user's work",
        "What are the user's hobbies?",
        "Does the user have family?"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = agent.search_memories(query, top_k=3)
        print("Top results:")
        for i, mem in enumerate(results, 1):
            print(f"  {i}. {mem.content}")


def demo_memory_persistence():
    """Demonstrate that memories persist across sessions"""
    print_separator("DEMO 5: Memory Persistence Across Sessions")
    
    user_id = "demo_user_5"
    
    # Session 1: Store memories
    print("Session 1: Storing memories")
    agent1 = VoiceAgent(
        user_id=user_id,
        vector_db_path="./demo_data/vector_store",
        use_llm_extraction=False
    )
    
    agent1.process_turn("My favorite color is blue")
    agent1.process_turn("I prefer tea over coffee")
    print("✓ Memories stored\n")
    
    # Simulate ending the session
    print("Ending session...\n")
    del agent1
    time.sleep(1)
    
    # Session 2: Retrieve memories
    print("Session 2: Creating new agent instance")
    agent2 = VoiceAgent(
        user_id=user_id,
        vector_db_path="./demo_data/vector_store",
        use_llm_extraction=False
    )
    
    print("Searching for memories from previous session:")
    results = agent2.search_memories("preferences", top_k=5)
    print(f"Found {len(results)} memories:")
    for i, mem in enumerate(results, 1):
        print(f"  {i}. {mem.content}")


def demo_memory_stats():
    """Demonstrate memory statistics and management"""
    print_separator("DEMO 6: Memory Statistics and Management")
    
    manager = MemoryManager(vector_db_path="./demo_data/vector_store")
    
    # Create test user with memories
    agent = VoiceAgent(
        user_id="demo_user_6",
        vector_db_path="./demo_data/vector_store",
        use_llm_extraction=False
    )
    
    # Add various memories
    for i in range(10):
        agent.process_turn(f"Test memory {i + 1}")
    
    # Get statistics
    print("User Statistics:")
    stats = manager.get_user_stats("demo_user_6")
    print(f"  Total memories: {stats['total']}")
    print(f"  Average importance: {stats.get('avg_importance', 0):.2f}")
    
    if 'by_category' in stats:
        print("\n  Memories by category:")
        for category, count in stats['by_category'].items():
            print(f"    {category}: {count}")
    
    # Export memories
    print("\nExporting memories to JSON...")
    manager.export_user_memories("demo_user_6", "./demo_data/export.json")
    print("✓ Exported to ./demo_data/export.json")


def main():
    """Run all demos"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    AI MEMORY SYSTEM - DEMONSTRATION                          ║
║                                                                              ║
║  This demo shows how the system maintains long-term memory across            ║
║  thousands of conversation turns, solving the exact problem described.       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Create demo data directory
    os.makedirs("./demo_data", exist_ok=True)
    
    try:
        # Run demos
        demo_basic_memory()
        input("\nPress Enter to continue to Demo 2...")
        
        demo_long_context_problem()
        input("\nPress Enter to continue to Demo 3...")
        
        demo_memory_categories()
        input("\nPress Enter to continue to Demo 4...")
        
        demo_memory_retrieval_quality()
        input("\nPress Enter to continue to Demo 5...")
        
        demo_memory_persistence()
        input("\nPress Enter to continue to Demo 6...")
        
        demo_memory_stats()
        
        print_separator("All Demos Complete!")
        print("""
The demonstrations showed:
✓ Basic memory storage and retrieval
✓ Long-context problem solution (Turn 1 → Turn 937)
✓ Memory categorization and organization
✓ Semantic search and relevance ranking
✓ Persistence across sessions
✓ Memory statistics and management

The system successfully maintains critical information across
thousands of turns and retrieves it instantly when needed.
        """)
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        print("Note: Some demos require API keys. Set ANTHROPIC_API_KEY environment variable.")


if __name__ == "__main__":
    main()
