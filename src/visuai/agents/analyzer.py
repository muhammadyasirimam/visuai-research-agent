"""
Analyzer Agent - Analyzes data and determines optimal visualization strategy.

Author: Muhammad Yasir Imam
"""

import os
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

from ..core.config import Config, DOMAIN_PRESETS


class AnalyzerAgent:
    """Agent responsible for data analysis and visualization strategy."""

    def __init__(self, config: Config):
        self.config = config
        self.domain_preset = DOMAIN_PRESETS.get(config.domain.domain, {})

    def analyze(self, data: pd.DataFrame, query: str, domain: str) -> Dict[str, Any]:
        """Analyze data and determine visualization strategy.

        Args:
            data: Input DataFrame
            query: User query
            domain: Research domain

        Returns:
            Analysis dictionary with recommendations
        """
        analysis = {
            "query": query,
            "domain": domain,
            "data_shape": data.shape,
            "columns": {},
            "recommended_charts": [],
            "xai_recommended": False,
            "statistical_tests": [],
            "insights": []
        }

        # Analyze each column
        for col in data.columns:
            col_info = self._analyze_column(data[col])
            analysis["columns"][col] = col_info

        # Determine chart recommendations
        analysis["recommended_charts"] = self._recommend_charts(data, query, domain)

        # Check if XAI is relevant
        analysis["xai_recommended"] = self._should_use_xai(data, query)

        # Determine statistical tests
        analysis["statistical_tests"] = self._recommend_tests(data, domain)

        # Generate initial insights
        analysis["insights"] = self._generate_insights(data)

        return analysis

    def _analyze_column(self, series: pd.Series) -> Dict[str, Any]:
        """Analyze a single column."""
        info = {
            "dtype": str(series.dtype),
            "null_count": series.isnull().sum(),
            "null_pct": series.isnull().mean() * 100,
            "unique_count": series.nunique(),
            "sample_values": series.dropna().head(5).tolist()
        }

        if pd.api.types.is_numeric_dtype(series):
            info.update({
                "type": "numeric",
                "min": series.min(),
                "max": series.max(),
                "mean": series.mean(),
                "std": series.std(),
                "median": series.median(),
                "skewness": series.skew(),
                "kurtosis": series.kurtosis()
            })
        elif pd.api.types.is_datetime64_any_dtype(series):
            info.update({
                "type": "datetime",
                "min_date": str(series.min()),
                "max_date": str(series.max()),
                "range_days": (series.max() - series.min()).days if not series.isna().all() else 0
            })
        else:
            info.update({
                "type": "categorical",
                "top_values": series.value_counts().head(5).to_dict()
            })

        return info

    def _recommend_charts(self, data: pd.DataFrame, query: str, domain: str) -> List[Dict[str, Any]]:
        """Recommend chart types based on data and query."""
        recommendations = []
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = data.select_dtypes(include=["object", "category"]).columns.tolist()
        datetime_cols = data.select_dtypes(include=["datetime64"]).columns.tolist()

        query_lower = query.lower()

        # Distribution analysis
        if any(word in query_lower for word in ["distribution", "histogram", "frequency", "density"]):
            for col in numeric_cols[:3]:
                recommendations.append({
                    "type": "histogram",
                    "columns": [col],
                    "reason": f"Show distribution of {col}"
                })

        # Correlation analysis
        if len(numeric_cols) >= 2 and any(word in query_lower for word in ["correlation", "relationship", "scatter", "compare"]):
            recommendations.append({
                "type": "correlation_heatmap",
                "columns": numeric_cols,
                "reason": "Show correlations between numeric variables"
            })
            if len(numeric_cols) >= 2:
                recommendations.append({
                    "type": "scatter",
                    "columns": [numeric_cols[0], numeric_cols[1]],
                    "reason": f"Scatter plot of {numeric_cols[0]} vs {numeric_cols[1]}"
                })

        # Time series
        if datetime_cols and any(word in query_lower for word in ["time", "trend", "over time", "temporal"]):
            for dt_col in datetime_cols[:1]:
                for num_col in numeric_cols[:3]:
                    recommendations.append({
                        "type": "line",
                        "columns": [dt_col, num_col],
                        "reason": f"Time series of {num_col} over {dt_col}"
                    })

        # Categorical analysis
        if categorical_cols and any(word in query_lower for word in ["category", "group", "count", "bar"]):
            for cat_col in categorical_cols[:2]:
                recommendations.append({
                    "type": "bar",
                    "columns": [cat_col],
                    "reason": f"Count distribution of {cat_col}"
                })
                if numeric_cols:
                    recommendations.append({
                        "type": "box",
                        "columns": [cat_col, numeric_cols[0]],
                        "reason": f"Distribution of {numeric_cols[0]} by {cat_col}"
                    })

        # Domain-specific charts
        domain_charts = self.domain_preset.get("specialized_charts", [])
        if domain == "machine_learning" and any(word in query_lower for word in ["model", "performance", "accuracy", "confusion"]):
            if "confusion_matrix" in domain_charts:
                recommendations.append({
                    "type": "confusion_matrix",
                    "columns": [],
                    "reason": "Model performance confusion matrix"
                })
            if "roc_curve" in domain_charts:
                recommendations.append({
                    "type": "roc_curve",
                    "columns": [],
                    "reason": "ROC curve for classification model"
                })

        # Default recommendations if none matched
        if not recommendations:
            if len(numeric_cols) >= 2:
                recommendations.append({
                    "type": "scatter",
                    "columns": [numeric_cols[0], numeric_cols[1]],
                    "reason": "Default scatter plot"
                })
            if numeric_cols:
                recommendations.append({
                    "type": "histogram",
                    "columns": [numeric_cols[0]],
                    "reason": "Default distribution plot"
                })
            if categorical_cols:
                recommendations.append({
                    "type": "bar",
                    "columns": [categorical_cols[0]],
                    "reason": "Default categorical plot"
                })

        return recommendations[:10]  # Limit to 10 recommendations

    def _should_use_xai(self, data: pd.DataFrame, query: str) -> bool:
        """Determine if XAI explanations are relevant."""
        query_lower = query.lower()
        xai_keywords = ["explain", "why", "feature importance", "shap", "lime", 
                       "interpret", "reason", "contribution", "impact", "influence"]
        return any(keyword in query_lower for keyword in xai_keywords)

    def _recommend_tests(self, data: pd.DataFrame, domain: str) -> List[str]:
        """Recommend statistical tests."""
        return self.domain_preset.get("statistical_tests", ["t_test", "chi_square"])

    def _generate_insights(self, data: pd.DataFrame) -> List[str]:
        """Generate initial data insights."""
        insights = []

        # Missing data insight
        missing_pct = data.isnull().mean().mean() * 100
        if missing_pct > 0:
            insights.append(f"Dataset has {missing_pct:.1f}% missing values overall")

        # Data size insight
        insights.append(f"Dataset contains {data.shape[0]} records with {data.shape[1]} features")

        # Numeric insights
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            insights.append(f"{len(numeric_cols)} numeric features identified")

        # Categorical insights
        cat_cols = data.select_dtypes(include=["object", "category"]).columns
        if len(cat_cols) > 0:
            insights.append(f"{len(cat_cols)} categorical features identified")

        return insights
