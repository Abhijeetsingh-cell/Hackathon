"""
Setup script for AI Memory System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-memory-system",
    version="1.0.0",
    author="AI Memory System Contributors",
    description="Persistent memory system for AI agents and voice assistants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-memory-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "chromadb>=0.4.0",
        "sentence-transformers>=2.2.0",
        "anthropic>=0.18.0",
        "openai>=1.0.0",
        "sqlalchemy>=2.0.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
        ],
        "api": [
            "uvicorn>=0.23.0",
            "fastapi>=0.100.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-memory-demo=demo:main",
        ],
    },
)
