# Installation Guide

## Requirements

- Python 3.9 or higher
- pip package manager
- (Optional) Git for cloning

## Install from Source

```bash
# Clone the repository
git clone https://github.com/muhammadyasirimam/visuai-research-agent.git
cd visuai-research-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Verify Installation

```bash
# Check CLI
visuai --help

# Run tests
pytest tests/ -v

# Check import
python -c "from visuai import ResearchAgent; print('✅ VisuAI installed successfully')"
```

## Optional Dependencies

```bash
# Development tools
pip install -e ".[dev]"

# Documentation tools
pip install -e ".[docs]"

# GPU support (if available)
pip install -e ".[gpu]"
```
