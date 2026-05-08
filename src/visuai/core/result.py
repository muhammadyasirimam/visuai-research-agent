
"""
Result handling module for VisuAI Research Agent.

Manages visualization outputs, exports, and result aggregation.

Author: Muhammad Yasir Imam
"""

import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class ChartResult:
    """Individual chart result."""
    chart_id: str
    chart_type: str
    title: str
    description: str
    data_summary: Dict[str, Any]
    figure_path: Optional[str] = None
    html_path: Optional[str] = None
    interactive_html: Optional[str] = None
    insights: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class XAIResult:
    """XAI explanation result."""
    method: str
    feature_importance: Dict[str, float]
    shap_values: Optional[Any] = None
    lime_explanation: Optional[Any] = None
    plots: List[str] = field(default_factory=list)
    global_explanation: str = ""
    local_explanations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        if self.shap_values is not None:
            result["shap_values"] = "<shap_values_object>"
        if self.lime_explanation is not None:
            result["lime_explanation"] = "<lime_explanation_object>"
        return result


@dataclass
class StatisticalResult:
    """Statistical analysis result."""
    test_name: str
    statistic: float
    p_value: float
    effect_size: Optional[float] = None
    confidence_interval: Optional[tuple] = None
    interpretation: str = ""
    assumptions_checked: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class VisualizationResult:
    """Complete visualization result from the agent."""

    session_id: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    query: str = ""
    domain: str = "general"
    data_source: str = ""
    data_shape: tuple = (0, 0)
    charts: List[ChartResult] = field(default_factory=list)
    xai_results: List[XAIResult] = field(default_factory=list)
    statistical_results: List[StatisticalResult] = field(default_factory=list)
    narrative: str = ""
    export_paths: Dict[str, str] = field(default_factory=dict)
    execution_time: float = 0.0
    model_used: str = ""
    tokens_used: int = 0

    def show(self) -> None:
        """Display all results."""
        print(f"\n{'='*60}")
        print(f"🎯 VisuAI Research Agent Results")
        print(f"{'='*60}")
        print(f"Query: {self.query}")
        print(f"Domain: {self.domain}")
        print(f"Charts Generated: {len(self.charts)}")
        print(f"XAI Analyses: {len(self.xai_results)}")
        print(f"Statistical Tests: {len(self.statistical_results)}")
        print(f"Execution Time: {self.execution_time:.2f}s")
        print(f"{'='*60}\n")

        if self.narrative:
            print("📖 AI Narrative:")
            print(self.narrative)
            print()

        for i, chart in enumerate(self.charts, 1):
            print(f"📊 Chart {i}: {chart.title} ({chart.chart_type})")
            if chart.insights:
                print("   Insights:")
                for insight in chart.insights:
                    print(f"   • {insight}")
            print()

    def save(self, output_dir: str = "./visuai_output") -> "VisualizationResult":
        """Save all results to output directory."""
        os.makedirs(output_dir, exist_ok=True)
        report_path = os.path.join(output_dir, "report.json")
        with open(report_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2, default=str)

        for chart in self.charts:
            if chart.figure_path and os.path.exists(chart.figure_path):
                import shutil
                dest = os.path.join(output_dir, os.path.basename(chart.figure_path))
                shutil.copy2(chart.figure_path, dest)
            if chart.html_path and os.path.exists(chart.html_path):
                import shutil
                dest = os.path.join(output_dir, os.path.basename(chart.html_path))
                shutil.copy2(chart.html_path, dest)

        self.export_paths["json_report"] = report_path
        self.export_paths["output_dir"] = output_dir
        print(f"✅ Results saved to: {output_dir}")
        return self

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "query": self.query,
            "domain": self.domain,
            "data_source": self.data_source,
            "data_shape": self.data_shape,
            "charts": [c.to_dict() for c in self.charts],
            "xai_results": [x.to_dict() for x in self.xai_results],
            "statistical_results": [s.to_dict() for s in self.statistical_results],
            "narrative": self.narrative,
            "export_paths": self.export_paths,
            "execution_time": self.execution_time,
            "model_used": self.model_used,
            "tokens_used": self.tokens_used,
        }
