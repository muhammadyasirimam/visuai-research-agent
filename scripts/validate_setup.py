#!/usr/bin/env python3
"""
Setup validation script for VisuAI Research Agent.

Run this after installation to verify everything is working.

Author: Muhammad Yasir Imam
"""

import sys
import os


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_imports():
    """Check core imports."""
    try:
        import pandas
        import numpy
        import matplotlib
        import seaborn
        import plotly
        import streamlit
        print("✅ Core dependencies imported")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False


def check_visuai():
    """Check VisuAI installation."""
    try:
        import visuai
        from visuai.core.agent import ResearchAgent
        from visuai.core.config import Config
        print(f"✅ VisuAI v{visuai.__version__} installed")
        return True
    except ImportError as e:
        print(f"❌ VisuAI not installed: {e}")
        return False


def check_api_key():
    """Check API key configuration."""
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        print("✅ API key configured")
        return True
    else:
        print("⚠️ No API key found (set OPENAI_API_KEY or ANTHROPIC_API_KEY)")
        return True  # Not critical


def main():
    print("=" * 60)
    print("🔬 VisuAI Setup Validation")
    print("=" * 60)
    print()

    checks = [
        ("Python Version", check_python_version),
        ("Core Dependencies", check_imports),
        ("VisuAI Package", check_visuai),
        ("API Keys", check_api_key),
    ]

    results = []
    for name, check_func in checks:
        print(f"Checking {name}...")
        result = check_func()
        results.append(result)
        print()

    print("=" * 60)
    if all(results):
        print("✅ All checks passed! VisuAI is ready to use.")
        print()
        print("Next steps:")
        print("  1. Run demo: python examples/demo.py")
        print("  2. Launch web: visuai web --port 8501")
        print("  3. Read docs: https://muhammadyasirimam.github.io/visuai-research-agent")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
