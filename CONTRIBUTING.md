# Contributing to VisuAI Research Agent

Thank you for your interest in contributing to VisuAI! This project was built by a researcher for researchers, and your contributions help make research data visualization accessible to everyone.

## 🎯 How to Contribute

### Reporting Bugs
- Check if the bug has already been reported in [Issues](https://github.com/muhammadyasirimam/visuai-research-agent/issues)
- Include a clear description and steps to reproduce
- Include your environment details (OS, Python version, VisuAI version)
- Include sample data if possible

### Suggesting Features
- Open a new issue with the `enhancement` label
- Describe the feature and its use case for researchers
- Explain how it would benefit the research community

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest tests/`)
6. Update documentation if needed
7. Commit with clear messages (`git commit -m 'Add amazing feature'`)
8. Push to your fork (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## 🏗️ Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/visuai-research-agent.git
cd visuai-research-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/ -v
```

## 📋 Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Write docstrings for all public functions/classes
- Keep functions focused and under 50 lines when possible
- Use meaningful variable names

## 🧪 Testing

- Write unit tests for new features
- Ensure integration tests pass
- Aim for >80% code coverage
- Test with different data types and sizes

## 📝 Documentation

- Update README.md if adding new features
- Add examples to the `examples/` directory
- Update docstrings
- Add notebook tutorials for complex features

## 🏆 Recognition

Contributors will be:
- Listed in the CONTRIBUTORS.md file
- Mentioned in release notes
- Credited in documentation

## 📬 Contact

- Email: imammuhammadyasir@gmail.com
- GitHub: [@muhammadyasirimam](https://github.com/muhammadyasirimam)
- ResearchGate: [Muhammad Yasir Imam](https://www.researchgate.net/profile/Muhammad-Yasir-Imam)

---

**Thank you for helping make research visualization accessible to everyone!**

*From a mud house in Pakistan to the world — together we build better tools.*
