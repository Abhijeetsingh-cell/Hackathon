# Quick Start Guide

Get up and running with the AI Memory System in 5 minutes.

## Prerequisites

- Python 3.9 or higher
- pip package manager
- (Optional) Anthropic API key for LLM-based extraction

## Installation

### Step 1: Extract the ZIP file

```bash
unzip ai-memory-system.zip
cd ai-memory-system
```

### Step 2: Create virtual environment

```bash
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set up environment (Optional)

For LLM-based extraction:

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Running the Demo

### Basic Demo (No API Key Required)

```bash
python demo.py
```

This will run through 6 demos showing:
1. Basic memory storage and retrieval
2. Long context problem solution (Turn 1 → Turn 937)
3. Memory categorization
4. Semantic search
5. Persistence across sessions
6. Memory statistics

### With API Key (Better Extraction)

```bash
export ANTHROPIC_API_KEY="your-key-here"  # Linux/Mac
# OR
set ANTHROPIC_API_KEY="your-key-here"     # Windows

python demo.py
```

## Your First Script

Create a file `my_agent.py`:

```python
from voice_agent import VoiceAgent

# Create agent (works without API key using simple extraction)
agent = VoiceAgent(
    user_id="my_user",
    vector_db_path="./my_data/vector_store",
    use_llm_extraction=False  # Set to True if you have API key
)

# Turn 1: Share information
print("Turn 1:")
response = agent.process_turn("My preferred language is Kannada")
print(f"Agent: {response}\n")

# Turn 2: Later request
print("Turn 2:")
response = agent.process_turn("Can you help me with something?")
print(f"Agent: {response}\n")

# Check what was remembered
print("\nStored memories:")
print(agent.get_user_profile_summary())
```

Run it:

```bash
python my_agent.py
```

## Next Steps

### 1. Explore Examples

```bash
# View usage examples
cat USAGE_EXAMPLES.md

# View architecture
cat ARCHITECTURE.md
```

### 2. Run Tests

```bash
pytest tests/ -v
```

### 3. Try the API Server

```bash
# Install FastAPI dependencies
pip install uvicorn fastapi

# Run server
python api_server.py

# Test it
curl http://localhost:8000/health
```

### 4. Customize Configuration

Edit `config.yaml` to customize:
- Retrieval parameters
- Memory decay settings
- Embedding models
- Storage paths

## Common Use Cases

### Use Case 1: Remember User Preferences

```python
agent.process_turn("I prefer formal communication")
# Later...
agent.process_turn("Send an email to my client")
# Agent remembers preference for formal style
```

### Use Case 2: Track Commitments

```python
agent.process_turn("Remind me to call John at 3 PM tomorrow")
# Later...
agent.process_turn("What's on my schedule?")
# Agent recalls the commitment
```

### Use Case 3: Maintain Context

```python
agent.process_turn("I'm working on a machine learning project")
agent.process_turn("It uses Python and TensorFlow")
# Much later...
agent.process_turn("What tools should I use?")
# Agent remembers project context
```

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: ChromaDB errors

**Solution**: Clear the database
```bash
rm -rf data/vector_store
```

### Issue: API key not found

**Solution**: Either:
1. Set environment variable: `export ANTHROPIC_API_KEY="..."`
2. Use simple extraction: `use_llm_extraction=False`

### Issue: Slow embeddings

**Solution**: Use smaller model in config.yaml
```yaml
embeddings:
  model: "sentence-transformers/all-MiniLM-L6-v2"  # Smaller, faster
```

## Getting Help

- Read the full README.md
- Check USAGE_EXAMPLES.md for code examples
- Review ARCHITECTURE.md for system design
- Open an issue for bugs or questions

## What's Next?

Now that you have the basics working:

1. **Integrate with your app**: Use `VoiceAgent` in your application
2. **Customize extraction**: Modify extraction prompts for your domain
3. **Deploy the API**: Use `api_server.py` for production
4. **Scale up**: Configure for multiple users and larger datasets
5. **Contribute**: See CONTRIBUTING.md to help improve the system

Happy coding! 🚀
