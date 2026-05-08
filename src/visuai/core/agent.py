"""
Main Research Agent orchestrator for VisuAI.

Coordinates multi-agent workflow: Analyzer -> Visualizer -> Explainer -> Exporter

Author: Muhammad Yasir Imam
"""

import os
import uuid
import time
from typing import List, Dict, Any, Optional

import pandas as pd
import numpy as np

from .config import Config, DOMAIN_PRESETS
from .result import VisualizationResult, ChartResult, XAIResult, StatisticalResult


class ResearchAgent:
    """Main AI agent for research data visualization."""

    def __init__(self, config=None, domain="general", output_format="interactive", llm_provider="openai", api_key=None):
        self.config = config or Config()
        self.config.domain.domain = domain
        self.config.llm.provider = llm_provider
        if api_key:
            self.config.llm.api_key = api_key
        self.output_format = output_format
        self.data = None
        self.data_info = {}
        self.session_id = str(uuid.uuid4())[:8]
        self._init_agents()
        print(f"🚀 VisuAI Research Agent initialized | Session: {self.session_id} | Domain: {domain} | LLM: {llm_provider}")

    def _init_agents(self):
        from ..agents.analyzer import AnalyzerAgent
        from ..agents.visualizer import VisualizerAgent
        from ..agents.explainer import ExplainerAgent
        from ..agents.exporter import ExporterAgent
        self.analyzer = AnalyzerAgent(self.config)
        self.visualizer = VisualizerAgent(self.config)
        self.explainer = ExplainerAgent(self.config)
        self.exporter = ExporterAgent(self.config)

    def load_data(self, source, **kwargs):
        from ..parsers.data_parser import DataParser
        parser = DataParser(self.config)
        if isinstance(source, pd.DataFrame):
            self.data = source.copy()
            self.data_info["source_type"] = "dataframe"
        elif isinstance(source, str):
            self.data = parser.load(source, **kwargs)
            self.data_info["source_type"] = "file"
            self.data_info["file_path"] = source
        else:
            raise ValueError(f"Unsupported data source type: {type(source)}")
        self.data_info["shape"] = self.data.shape
        self.data_info["columns"] = list(self.data.columns)
        print(f"📊 Data loaded: {self.data.shape[0]} rows × {self.data.shape[1]} columns")
        return self

    def run(self, query, chart_types=None, export_formats=None, xai_enabled=True, statistical_tests=True, max_charts=10):
        start_time = time.time()
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        print(f"\n🔍 Processing query: '{query}'")
        print("\n[1/4] 🔬 Analyzing data and query...")
        analysis = self.analyzer.analyze(self.data, query, self.config.domain.domain)
        print("\n[2/4] 🎨 Generating visualizations...")
        charts = self.visualizer.visualize(data=self.data, analysis=analysis, chart_types=chart_types, max_charts=max_charts)
        print("\n[3/4] 🧠 Generating AI explanations...")
        xai_results = []
        if xai_enabled and analysis.get("xai_recommended", False):
            xai_results = self.explainer.explain(data=self.data, analysis=analysis, charts=charts)
        statistical_results = []
        if statistical_tests:
            statistical_results = self._run_statistical_tests(analysis)
        narrative = self.explainer.generate_narrative(query=query, analysis=analysis, charts=charts, xai_results=xai_results, statistical_results=statistical_results)
        print("\n[4/4] 📤 Exporting results...")
        export_formats = export_formats or ["html"]
        export_paths = self.exporter.export(charts=charts, narrative=narrative, formats=export_formats, session_id=self.session_id)
        execution_time = time.time() - start_time
        result = VisualizationResult(
            session_id=self.session_id, query=query, domain=self.config.domain.domain,
            data_source=self.data_info.get("file_path", "dataframe"), data_shape=self.data.shape,
            charts=charts, xai_results=xai_results, statistical_results=statistical_results,
            narrative=narrative, export_paths=export_paths, execution_time=execution_time,
            model_used=self.config.llm.model
        )
        print(f"\n✅ Complete! Generated {len(charts)} charts in {execution_time:.2f}s")
        return result

    def chat(self, query):
        if self.data is None:
            return "❌ Please load data first using load_data()."
        return self.explainer.chat(self.data, query)

    def quick_chart(self, chart_type, x=None, y=None, **kwargs):
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        return self.visualizer.create_chart(self.data, chart_type, x, y, **kwargs)

    def _run_statistical_tests(self, analysis):
        results = []
        domain_preset = DOMAIN_PRESETS.get(self.config.domain.domain, {})
        tests = domain_preset.get("statistical_tests", [])
        for test_name in tests[:3]:
            try:
                result = self._execute_statistical_test(test_name)
                if result:
                    results.append(result)
            except Exception as e:
                print(f"   ⚠️ Test '{test_name}' failed: {e}")
        return results

    def _execute_statistical_test(self, test_name):
        from scipy import stats
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return None
        col1, col2 = numeric_cols[0], numeric_cols[1]
        if test_name == "t_test":
            statistic, p_value = stats.ttest_ind(self.data[col1].dropna(), self.data[col2].dropna())
            return StatisticalResult(test_name="Independent t-test", statistic=statistic, p_value=p_value,
                interpretation=f"t={statistic:.3f}, p={p_value:.3f}. {'Significant' if p_value < 0.05 else 'Not significant'} difference.")
        elif test_name == "chi_square":
            contingency = pd.crosstab(self.data.iloc[:, 0], self.data.iloc[:, 1])
            chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
            return StatisticalResult(test_name="Chi-Square Test", statistic=chi2, p_value=p_value,
                interpretation=f"χ²={chi2:.3f}, p={p_value:.3f}. {'Significant' if p_value < 0.05 else 'Not significant'} association.")
        elif test_name == "shapiro_wilk":
            statistic, p_value = stats.shapiro(self.data[col1].dropna()[:5000])
            return StatisticalResult(test_name="Shapiro-Wilk Normality Test", statistic=statistic, p_value=p_value,
                interpretation=f"W={statistic:.3f}, p={p_value:.3f}. Data is {'normally distributed' if p_value > 0.05 else 'not normally distributed'}.")
        return None
