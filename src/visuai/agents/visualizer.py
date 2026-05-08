"""
Visualizer Agent - Generates publication-ready visualizations.

Author: Muhammad Yasir Imam
"""

import os
import uuid
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

from ..core.config import Config, DOMAIN_PRESETS
from ..core.result import ChartResult


class VisualizerAgent:
    """Agent responsible for generating visualizations."""

    def __init__(self, config: Config):
        self.config = config
        self.domain_preset = DOMAIN_PRESETS.get(config.domain.domain, {})
        self._setup_theme()

    def _setup_theme(self):
        """Configure visualization theme."""
        theme = self.config.visualization.theme

        if theme == "publication":
            sns.set_style("whitegrid")
            plt.rcParams.update({
                'figure.dpi': self.config.visualization.figure_dpi,
                'font.size': self.config.visualization.font_size,
                'axes.titlesize': 14,
                'axes.labelsize': 12,
                'figure.figsize': (10, 6),
                'savefig.bbox': 'tight',
                'savefig.pad_inches': 0.1
            })
        elif theme == "dark":
            plt.style.use('dark_background')
            sns.set_style("darkgrid")
        elif theme == "colorblind":
            sns.set_palette("colorblind")

        # Set default color palette
        if self.config.visualization.color_palette == "seaborn":
            sns.set_palette("husl")

    def visualize(self, data: pd.DataFrame, analysis: Dict[str, Any], 
                  chart_types: Optional[List[str]] = None, max_charts: int = 10) -> List[ChartResult]:
        """Generate all recommended visualizations."""
        recommendations = analysis.get("recommended_charts", [])
        charts = []

        for i, rec in enumerate(recommendations[:max_charts]):
            try:
                chart = self.create_chart(
                    data=data,
                    chart_type=rec["type"],
                    columns=rec.get("columns", []),
                    title=rec.get("reason", f"Chart {i+1}"),
                    chart_id=f"chart_{i+1}"
                )
                charts.append(chart)
            except Exception as e:
                print(f"   ⚠️ Failed to create {rec['type']}: {e}")

        return charts

    def create_chart(self, data: pd.DataFrame, chart_type: str, 
                     x: Optional[str] = None, y: Optional[str] = None,
                     columns: Optional[List[str]] = None, 
                     title: str = "", chart_id: str = None,
                     **kwargs) -> ChartResult:
        """Create a single chart."""
        chart_id = chart_id or f"chart_{uuid.uuid4().hex[:8]}"
        columns = columns or []

        # Determine columns to use
        if x and not columns:
            columns = [x]
        if y and len(columns) == 1:
            columns.append(y)

        # Generate chart based on type
        if chart_type == "histogram":
            return self._create_histogram(data, columns, title, chart_id)
        elif chart_type == "scatter":
            return self._create_scatter(data, columns, title, chart_id)
        elif chart_type == "line":
            return self._create_line(data, columns, title, chart_id)
        elif chart_type == "bar":
            return self._create_bar(data, columns, title, chart_id)
        elif chart_type == "box":
            return self._create_box(data, columns, title, chart_id)
        elif chart_type == "correlation_heatmap":
            return self._create_correlation_heatmap(data, columns, title, chart_id)
        elif chart_type == "pairplot":
            return self._create_pairplot(data, columns, title, chart_id)
        elif chart_type == "violin":
            return self._create_violin(data, columns, title, chart_id)
        elif chart_type == "area":
            return self._create_area(data, columns, title, chart_id)
        elif chart_type == "pie":
            return self._create_pie(data, columns, title, chart_id)
        elif chart_type == "confusion_matrix":
            return self._create_confusion_matrix(data, columns, title, chart_id)
        else:
            return self._create_generic(data, columns, title, chart_id)

    def _create_histogram(self, data, columns, title, chart_id):
        col = columns[0] if columns else data.select_dtypes(include=[np.number]).columns[0]
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data=data, x=col, kde=True, ax=ax, color="#2563eb")
        ax.set_title(title or f"Distribution of {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")

        insights = [
            f"Mean: {data[col].mean():.2f}, Std: {data[col].std():.2f}",
            f"Skewness: {data[col].skew():.2f} ({'right-skewed' if data[col].skew() > 0 else 'left-skewed' if data[col].skew() < 0 else 'symmetric'})"
        ]

        return self._save_chart(fig, chart_id, "histogram", title or f"Distribution of {col}", insights, {col: "numeric"})

    def _create_scatter(self, data, columns, title, chart_id):
        x_col = columns[0] if len(columns) > 0 else data.columns[0]
        y_col = columns[1] if len(columns) > 1 else data.columns[1] if len(data.columns) > 1 else data.columns[0]

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=data, x=x_col, y=y_col, ax=ax, alpha=0.6, color="#7c3aed")
        ax.set_title(title or f"{y_col} vs {x_col}")

        # Calculate correlation
        corr = data[[x_col, y_col]].corr().iloc[0, 1]
        insights = [f"Correlation coefficient: {corr:.3f} ({'strong' if abs(corr) > 0.7 else 'moderate' if abs(corr) > 0.3 else 'weak'} {'positive' if corr > 0 else 'negative'} relationship)"]

        return self._save_chart(fig, chart_id, "scatter", title or f"{y_col} vs {x_col}", insights, {x_col: "x", y_col: "y"})

    def _create_line(self, data, columns, title, chart_id):
        x_col = columns[0] if len(columns) > 0 else data.columns[0]
        y_col = columns[1] if len(columns) > 1 else data.select_dtypes(include=[np.number]).columns[0]

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=data, x=x_col, y=y_col, ax=ax, color="#06b6d4", linewidth=2)
        ax.set_title(title or f"{y_col} over {x_col}")
        ax.tick_params(axis='x', rotation=45)

        insights = [f"Trend shows {'increasing' if data[y_col].iloc[-1] > data[y_col].iloc[0] else 'decreasing'} pattern over time"]

        return self._save_chart(fig, chart_id, "line", title or f"{y_col} over {x_col}", insights, {x_col: "time", y_col: "value"})

    def _create_bar(self, data, columns, title, chart_id):
        col = columns[0] if columns else data.select_dtypes(include=["object", "category"]).columns[0]
        value_counts = data[col].value_counts().head(15)

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax, palette="husl")
        ax.set_title(title or f"Distribution of {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
        ax.tick_params(axis='x', rotation=45)

        insights = [
            f"Most frequent: {value_counts.index[0]} ({value_counts.iloc[0]} occurrences, {value_counts.iloc[0]/len(data)*100:.1f}%)",
            f"Total categories: {data[col].nunique()}"
        ]

        return self._save_chart(fig, chart_id, "bar", title or f"Distribution of {col}", insights, {col: "categorical"})

    def _create_box(self, data, columns, title, chart_id):
        cat_col = columns[0] if len(columns) > 0 else data.select_dtypes(include=["object", "category"]).columns[0]
        num_col = columns[1] if len(columns) > 1 else data.select_dtypes(include=[np.number]).columns[0]

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(data=data, x=cat_col, y=num_col, ax=ax, palette="Set2")
        ax.set_title(title or f"{num_col} by {cat_col}")
        ax.tick_params(axis='x', rotation=45)

        insights = [f"Shows distribution spread and outliers across {cat_col} categories"]

        return self._save_chart(fig, chart_id, "box", title or f"{num_col} by {cat_col}", insights, {cat_col: "category", num_col: "value"})

    def _create_correlation_heatmap(self, data, columns, title, chart_id):
        numeric_data = data.select_dtypes(include=[np.number])
        if numeric_data.empty:
            numeric_data = data

        corr_matrix = numeric_data.corr()

        fig, ax = plt.subplots(figsize=(12, 10))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
                   center=0, square=True, linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8})
        ax.set_title(title or "Correlation Matrix")

        # Find strongest correlations
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))
        corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)

        insights = []
        if corr_pairs:
            top = corr_pairs[0]
            insights.append(f"Strongest correlation: {top[0]} ↔ {top[1]} (r={top[2]:.3f})")

        return self._save_chart(fig, chart_id, "correlation_heatmap", title or "Correlation Matrix", insights, {})

    def _create_pairplot(self, data, columns, title, chart_id):
        numeric_cols = data.select_dtypes(include=[np.number]).columns[:5]
        if len(numeric_cols) < 2:
            return self._create_generic(data, columns, title, chart_id)

        g = sns.pairplot(data[numeric_cols], diag_kind="kde", plot_kws={"alpha": 0.6}, corner=True)
        g.fig.suptitle(title or "Pairwise Relationships", y=1.02)

        insights = [f"Pairwise scatter plots for {len(numeric_cols)} numeric features"]

        return self._save_chart(g.fig, chart_id, "pairplot", title or "Pairwise Relationships", insights, {})

    def _create_violin(self, data, columns, title, chart_id):
        cat_col = columns[0] if len(columns) > 0 else data.select_dtypes(include=["object"]).columns[0]
        num_col = columns[1] if len(columns) > 1 else data.select_dtypes(include=[np.number]).columns[0]

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.violinplot(data=data, x=cat_col, y=num_col, ax=ax, palette="muted", inner="box")
        ax.set_title(title or f"{num_col} Distribution by {cat_col}")
        ax.tick_params(axis='x', rotation=45)

        insights = [f"Shows full distribution shape including density peaks"]

        return self._save_chart(fig, chart_id, "violin", title or f"{num_col} Distribution by {cat_col}", insights, {})

    def _create_area(self, data, columns, title, chart_id):
        x_col = columns[0] if len(columns) > 0 else data.columns[0]
        y_col = columns[1] if len(columns) > 1 else data.select_dtypes(include=[np.number]).columns[0]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.fill_between(data[x_col], data[y_col], alpha=0.4, color="#10b981")
        ax.plot(data[x_col], data[y_col], color="#059669", linewidth=2)
        ax.set_title(title or f"{y_col} Area Chart")
        ax.tick_params(axis='x', rotation=45)

        insights = [f"Cumulative visualization of {y_col} over {x_col}"]

        return self._save_chart(fig, chart_id, "area", title or f"{y_col} Area Chart", insights, {})

    def _create_pie(self, data, columns, title, chart_id):
        col = columns[0] if columns else data.select_dtypes(include=["object"]).columns[0]
        value_counts = data[col].value_counts().head(8)

        fig, ax = plt.subplots(figsize=(10, 8))
        colors = plt.cm.Set3(np.linspace(0, 1, len(value_counts)))
        wedges, texts, autotexts = ax.pie(
            value_counts.values, labels=value_counts.index, autopct='%1.1f%%',
            colors=colors, startangle=90, textprops={'fontsize': 10}
        )
        ax.set_title(title or f"{col} Distribution")

        insights = [f"Top category: {value_counts.index[0]} ({value_counts.iloc[0]/len(data)*100:.1f}%)"]

        return self._save_chart(fig, chart_id, "pie", title or f"{col} Distribution", insights, {})

    def _create_confusion_matrix(self, data, columns, title, chart_id):
        # Placeholder for confusion matrix - requires y_true and y_pred
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, "Confusion Matrix\n(Requires model predictions)", 
                ha='center', va='center', fontsize=14, transform=ax.transAxes)
        ax.set_title(title or "Confusion Matrix")
        ax.axis('off')

        return self._save_chart(fig, chart_id, "confusion_matrix", title or "Confusion Matrix", 
                               ["Provide y_true and y_pred to generate actual confusion matrix"], {})

    def _create_generic(self, data, columns, title, chart_id):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, f"Chart Type: Generic\nColumns: {columns}", 
                ha='center', va='center', fontsize=12, transform=ax.transAxes)
        ax.set_title(title or "Generic Chart")
        ax.axis('off')

        return self._save_chart(fig, chart_id, "generic", title or "Generic Chart", ["Generic placeholder chart"], {})

    def _save_chart(self, fig, chart_id, chart_type, title, insights, data_summary):
        """Save chart to file and create ChartResult."""
        os.makedirs("./visuai_output", exist_ok=True)

        # Save matplotlib figure
        fig_path = f"./visuai_output/{chart_id}.png"
        fig.savefig(fig_path, dpi=self.config.visualization.figure_dpi, bbox_inches='tight')
        plt.close(fig)

        # Create interactive Plotly version
        html_path = f"./visuai_output/{chart_id}.html"
        # Note: In production, convert matplotlib to plotly or generate plotly directly

        return ChartResult(
            chart_id=chart_id,
            chart_type=chart_type,
            title=title,
            description=f"Auto-generated {chart_type} chart",
            data_summary=data_summary,
            figure_path=fig_path,
            html_path=html_path,
            insights=insights,
            recommendations=["Consider adjusting colors for publication", "Add statistical annotations if needed"]
        )
