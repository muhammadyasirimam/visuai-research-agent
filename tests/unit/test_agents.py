"""
Unit tests for VisuAI agents.

Author: Muhammad Yasir Imam
"""

import pytest
import pandas as pd
import numpy as np

from visuai.core.config import Config
from visuai.agents.analyzer import AnalyzerAgent
from visuai.agents.visualizer import VisualizerAgent
from visuai.agents.explainer import ExplainerAgent
from visuai.agents.exporter import ExporterAgent


@pytest.fixture
def sample_data():
    """Create sample dataset for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'feature_a': np.random.randn(100),
        'feature_b': np.random.randn(100),
        'feature_c': np.random.randn(100),
        'category': np.random.choice(['A', 'B', 'C'], 100),
        'target': np.random.randn(100)
    })


@pytest.fixture
def config():
    """Create test configuration."""
    return Config()


class TestAnalyzerAgent:
    """Test AnalyzerAgent functionality."""

    def test_initialization(self, config):
        agent = AnalyzerAgent(config)
        assert agent.config == config

    def test_analyze(self, config, sample_data):
        agent = AnalyzerAgent(config)
        analysis = agent.analyze(sample_data, "Show distributions", "general")

        assert "query" in analysis
        assert "domain" in analysis
        assert "data_shape" in analysis
        assert "columns" in analysis
        assert "recommended_charts" in analysis
        assert len(analysis["recommended_charts"]) > 0

    def test_analyze_column_numeric(self, config, sample_data):
        agent = AnalyzerAgent(config)
        info = agent._analyze_column(sample_data['feature_a'])

        assert info["type"] == "numeric"
        assert "mean" in info
        assert "std" in info
        assert "min" in info
        assert "max" in info

    def test_analyze_column_categorical(self, config, sample_data):
        agent = AnalyzerAgent(config)
        info = agent._analyze_column(sample_data['category'])

        assert info["type"] == "categorical"
        assert "top_values" in info

    def test_recommend_charts(self, config, sample_data):
        agent = AnalyzerAgent(config)
        recommendations = agent._recommend_charts(sample_data, "correlation", "general")

        assert len(recommendations) > 0
        chart_types = [r["type"] for r in recommendations]
        assert "correlation_heatmap" in chart_types or "scatter" in chart_types

    def test_should_use_xai(self, config, sample_data):
        agent = AnalyzerAgent(config)

        assert agent._should_use_xai(sample_data, "explain feature importance") == True
        assert agent._should_use_xai(sample_data, "show distribution") == False

    def test_generate_insights(self, config, sample_data):
        agent = AnalyzerAgent(config)
        insights = agent._generate_insights(sample_data)

        assert len(insights) > 0
        assert any("records" in i for i in insights)


class TestVisualizerAgent:
    """Test VisualizerAgent functionality."""

    def test_initialization(self, config):
        agent = VisualizerAgent(config)
        assert agent.config == config

    def test_create_histogram(self, config, sample_data):
        agent = VisualizerAgent(config)
        chart = agent.create_chart(sample_data, "histogram", columns=["feature_a"], title="Test Histogram")

        assert chart.chart_type == "histogram"
        assert chart.title == "Test Histogram"
        assert chart.figure_path is not None

    def test_create_scatter(self, config, sample_data):
        agent = VisualizerAgent(config)
        chart = agent.create_chart(sample_data, "scatter", columns=["feature_a", "feature_b"], title="Test Scatter")

        assert chart.chart_type == "scatter"
        assert len(chart.insights) > 0

    def test_create_correlation_heatmap(self, config, sample_data):
        agent = VisualizerAgent(config)
        chart = agent.create_chart(sample_data, "correlation_heatmap", title="Test Heatmap")

        assert chart.chart_type == "correlation_heatmap"

    def test_visualize(self, config, sample_data):
        agent = VisualizerAgent(config)
        analysis = {
            "recommended_charts": [
                {"type": "histogram", "columns": ["feature_a"], "reason": "Distribution"},
                {"type": "scatter", "columns": ["feature_a", "feature_b"], "reason": "Relationship"}
            ]
        }
        charts = agent.visualize(sample_data, analysis, max_charts=2)

        assert len(charts) == 2
        assert all(c.figure_path is not None for c in charts)


class TestExplainerAgent:
    """Test ExplainerAgent functionality."""

    def test_initialization(self, config):
        agent = ExplainerAgent(config)
        assert agent.config == config

    def test_fallback_narrative(self, config, sample_data):
        agent = ExplainerAgent(config)
        analysis = {"domain": "general", "data_shape": (100, 5)}
        charts = []
        xai_results = []
        statistical_results = []

        narrative = agent._fallback_narrative("test query", analysis, charts, xai_results, statistical_results)

        assert "Research Visualization Report" in narrative
        assert "test query" in narrative

    def test_chat_fallback(self, config, sample_data):
        agent = ExplainerAgent(config)
        response = agent.chat(sample_data, "What is the shape?")

        assert "rows" in response.lower()
        assert "columns" in response.lower()


class TestExporterAgent:
    """Test ExporterAgent functionality."""

    def test_initialization(self, config):
        agent = ExporterAgent(config)
        assert agent.config == config

    def test_export_html(self, config):
        agent = ExporterAgent(config)
        from visuai.core.result import ChartResult

        chart = ChartResult(
            chart_id="test_1",
            chart_type="histogram",
            title="Test",
            description="Test chart",
            data_summary={},
            insights=["Test insight"]
        )

        paths = agent.export([chart], "Test narrative", ["html", "markdown"], "test_session")

        assert "html" in paths or "markdown" in paths
