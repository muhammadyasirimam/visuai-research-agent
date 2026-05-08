"""
VisuAI Research Agent - AI-Powered Research Data Visualization

Transform research data into stunning, publication-ready visualizations
with intelligent AI agents tailored to your domain.

Author: Muhammad Yasir Imam
Email: imammuhammadyasir@gmail.com
GitHub: https://github.com/muhammadyasirimam
ORCID: 0000-0002-7495-4179
"""

__version__ = "1.0.0"
__author__ = "Muhammad Yasir Imam"
__email__ = "imammuhammadyasir@gmail.com"
__license__ = "MIT"
__url__ = "https://github.com/muhammadyasirimam/visuai-research-agent"

from .core.agent import ResearchAgent
from .core.config import Config
from .core.result import VisualizationResult

__all__ = [
    "ResearchAgent",
    "Config", 
    "VisualizationResult",
]
