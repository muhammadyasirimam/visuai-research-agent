#!/usr/bin/env python3
"""Setup script for VisuAI Research Agent."""

from setuptools import setup, find_packages
import os

# Read README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="visuai-research-agent",
    version="1.0.0",
    author="Muhammad Yasir Imam",
    author_email="imammuhammadyasir@gmail.com",
    description="AI-Powered Research Data Visualization Agent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muhammadyasirimam/visuai-research-agent",
    project_urls={
        "Bug Tracker": "https://github.com/muhammadyasirimam/visuai-research-agent/issues",
        "Documentation": "https://muhammadyasirimam.github.io/visuai-research-agent",
        "ResearchGate": "https://www.researchgate.net/profile/Muhammad-Yasir-Imam",
        "Google Scholar": "https://scholar.google.com/citations?user=b80oc1UAAAAJ",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.2.0",
            "pytest-cov>=5.0.0",
            "black>=24.4.0",
            "isort>=5.13.0",
            "flake8>=7.1.0",
            "mypy>=1.10.0",
            "pre-commit>=3.7.0",
        ],
        "docs": [
            "mkdocs>=1.6.0",
            "mkdocs-material>=9.5.0",
            "mkdocstrings>=0.25.0",
        ],
        "gpu": [
            "cuda-python>=12.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "visuai=visuai.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "visuai": [
            "templates/*.html",
            "templates/*.tex",
            "templates/*.pptx",
            "assets/*.png",
            "assets/*.css",
            "config/*.yaml",
        ],
    },
    zip_safe=False,
)
