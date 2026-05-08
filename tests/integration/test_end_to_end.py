"""
End-to-end integration tests for VisuAI.

Author: Muhammad Yasir Imam
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os

from visuai.core.agent import ResearchAgent
from visuai.core.config import Config


@pytest.fixture
def sample_dataset():
    """Create a comprehensive sample dataset."""
    np.random.seed(42)
    n = 200
    return pd.DataFrame({
        'age': np.random.randint(18, 80, n),
        'income': np.random.lognormal(10, 0.5, n),
        'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n),
        'gender': np.random.choice(['Male', 'Female'], n),
        'satisfaction': np.random.randint(1, 11, n),
        'churn': np.random.choice([0, 1], n, p=[0.7, 0.3])
    })


class TestEndToEnd:
    """End-to-end integration tests."""

    def test_full_pipeline(self, sample_dataset):
        """Test the complete visualization pipeline."""
        agent = ResearchAgent(domain="general", llm_provider="local")
        agent.load_data(sample_dataset)

        result = agent.run(
            query="Show me distributions, correlations, and category breakdowns",
            export_formats=["html", "markdown"],
            xai_enabled=False,
            statistical_tests=True,
            max_charts=5
        )

        assert result is not None
        assert len(result.charts) > 0
        assert result.execution_time > 0
        assert result.session_id is not None

    def test_domain_specific(self, sample_dataset):
        """Test domain-specific visualization."""
        agent = ResearchAgent(domain="machine_learning")
        agent.load_data(sample_dataset)

        result = agent.run(
            query="Analyze feature relationships for prediction",
            export_formats=["html"],
            xai_enabled=True,
            max_charts=3
        )

        assert len(result.charts) > 0

    def test_chat_functionality(self, sample_dataset):
        """Test chat with data."""
        agent = ResearchAgent()
        agent.load_data(sample_dataset)

        response = agent.chat("How many rows are in the dataset?")

        assert "200" in response or "rows" in response.lower()

    def test_quick_chart(self, sample_dataset):
        """Test quick chart generation."""
        agent = ResearchAgent()
        agent.load_data(sample_dataset)

        chart = agent.quick_chart("histogram", x="age")

        assert chart.chart_type == "histogram"
        assert chart.figure_path is not None

    def test_save_results(self, sample_dataset):
        """Test result saving."""
        agent = ResearchAgent()
        agent.load_data(sample_dataset)

        result = agent.run(
            query="Show basic stats",
            export_formats=["html"],
            max_charts=2
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            result.save(tmpdir)
            assert os.path.exists(os.path.join(tmpdir, "report.json"))
