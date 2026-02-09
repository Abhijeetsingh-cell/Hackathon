# Contributing to AI Memory System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-memory-system
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. **Run tests**
```bash
pytest tests/ -v
```

## Code Style

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Add docstrings to all classes and functions
- Keep functions focused and single-purpose

## Testing

- Write tests for all new features
- Maintain test coverage above 80%
- Run tests before submitting PR

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## Pull Request Process

1. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
- Write clean, documented code
- Add tests for new functionality
- Update documentation as needed

3. **Test your changes**
```bash
pytest tests/ -v
```

4. **Commit your changes**
```bash
git add .
git commit -m "Add feature: description of your changes"
```

5. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

6. **Create a Pull Request**
- Provide a clear description of changes
- Reference any related issues
- Ensure all tests pass

## Areas for Contribution

### High Priority
- [ ] Improve memory extraction accuracy
- [ ] Add support for more LLM providers
- [ ] Implement memory consolidation
- [ ] Add metrics and monitoring
- [ ] Improve documentation

### Features
- [ ] Multi-modal memory (images, audio)
- [ ] Memory versioning and conflict resolution
- [ ] Advanced forgetting mechanisms
- [ ] Cross-user pattern learning
- [ ] API server implementation

### Optimizations
- [ ] Faster embedding generation
- [ ] Improved retrieval algorithms
- [ ] Memory compression techniques
- [ ] Caching strategies

## Code Review Checklist

Before submitting:
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation updated
- [ ] No sensitive data in commits
- [ ] Commit messages are clear
- [ ] No breaking changes (or clearly documented)

## Reporting Issues

When reporting issues, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version)
- Relevant logs or error messages

## Questions?

Feel free to open an issue for questions or discussions about the project.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
