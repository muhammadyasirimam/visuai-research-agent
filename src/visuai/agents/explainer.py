"""
Explainer Agent - Generates AI explanations and narratives.

Author: Muhammad Yasir Imam
"""

import os
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

from ..core.config import Config
from ..core.result import XAIResult, ChartResult, StatisticalResult


class ExplainerAgent:
    """Agent responsible for generating explanations and narratives."""

    def __init__(self, config: Config):
        self.config = config
        self._init_llm()

    def _init_llm(self):
        try:
            if self.config.llm.provider == "openai":
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    model=self.config.llm.model,
                    temperature=self.config.llm.temperature,
                    api_key=self.config.llm.api_key or os.getenv("OPENAI_API_KEY")
                )
            elif self.config.llm.provider == "anthropic":
                from langchain_anthropic import ChatAnthropic
                self.llm = ChatAnthropic(
                    model="claude-3-sonnet-20240229",
                    temperature=self.config.llm.temperature,
                    api_key=self.config.llm.api_key or os.getenv("ANTHROPIC_API_KEY")
                )
            else:
                self.llm = None
        except Exception as e:
            print(f"   ⚠️ LLM initialization failed: {e}. Using fallback explanations.")
            self.llm = None

    def explain(self, data, analysis, charts):
        results = []
        if self.config.xai.method == "shap":
            results.extend(self._shap_explanation(data, analysis))
        elif self.config.xai.method == "lime":
            results.extend(self._lime_explanation(data, analysis))
        elif self.config.xai.method == "permutation":
            results.extend(self._permutation_importance(data, analysis))
        return results

    def _shap_explanation(self, data, analysis):
        try:
            import shap
            from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
            from sklearn.preprocessing import LabelEncoder
            import matplotlib.pyplot as plt

            numeric_data = data.select_dtypes(include=[np.number]).fillna(data.median(numeric_only=True))
            if numeric_data.empty or len(numeric_data.columns) < 2:
                return []

            target_col = numeric_data.columns[-1]
            feature_cols = [c for c in numeric_data.columns if c != target_col]
            X = numeric_data[feature_cols]
            y = numeric_data[target_col]

            if y.nunique() <= 10:
                model = RandomForestClassifier(n_estimators=50, random_state=42)
                le = LabelEncoder()
                y = le.fit_transform(y.astype(str))
            else:
                model = RandomForestRegressor(n_estimators=50, random_state=42)

            model.fit(X, y)
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X.iloc[:self.config.xai.samples])

            importances = dict(zip(feature_cols, model.feature_importances_))
            importances = dict(sorted(importances.items(), key=lambda x: x[1], reverse=True))

            os.makedirs("./visuai_output", exist_ok=True)
            shap_path = f"./visuai_output/shap_summary_{self.config.domain.domain}.png"

            fig, ax = plt.subplots(figsize=(10, 6))
            if isinstance(shap_values, list):
                shap.summary_plot(shap_values[1], X.iloc[:self.config.xai.samples], 
                                feature_names=feature_cols, show=False)
            else:
                shap.summary_plot(shap_values, X.iloc[:self.config.xai.samples], 
                                feature_names=feature_cols, show=False)
            fig.savefig(shap_path, dpi=150, bbox_inches='tight')
            plt.close(fig)

            result = XAIResult(
                method="SHAP",
                feature_importance=importances,
                shap_values=shap_values,
                plots=[shap_path],
                global_explanation=f"SHAP analysis shows top influencing features on {target_col}",
                local_explanations=[f"{feat}: {imp:.3f}" for feat, imp in list(importances.items())[:5]]
            )
            return [result]
        except Exception as e:
            print(f"   ⚠️ SHAP explanation failed: {e}")
            return []

    def _lime_explanation(self, data, analysis):
        try:
            from lime.lime_tabular import LimeTabularExplainer
            from sklearn.ensemble import RandomForestClassifier

            numeric_data = data.select_dtypes(include=[np.number]).fillna(data.median(numeric_only=True))
            if numeric_data.empty or len(numeric_data.columns) < 2:
                return []

            target_col = numeric_data.columns[-1]
            feature_cols = [c for c in numeric_data.columns if c != target_col]
            X = numeric_data[feature_cols].values
            y = numeric_data[target_col].values
            y_binned = pd.cut(y, bins=3, labels=["low", "medium", "high"])

            model = RandomForestClassifier(n_estimators=50, random_state=42)
            model.fit(X, y_binned)

            explainer = LimeTabularExplainer(
                X, feature_names=feature_cols, class_names=["low", "medium", "high"],
                mode="classification"
            )
            exp = explainer.explain_instance(X[0], model.predict_proba, num_features=5)
            feature_importance = dict(exp.as_list())

            result = XAIResult(
                method="LIME",
                feature_importance=feature_importance,
                lime_explanation=exp,
                global_explanation="LIME local explanation for first instance",
                local_explanations=[f"{feat}: {imp:.3f}" for feat, imp in exp.as_list()[:5]]
            )
            return [result]
        except Exception as e:
            print(f"   ⚠️ LIME explanation failed: {e}")
            return []

    def _permutation_importance(self, data, analysis):
        try:
            from sklearn.inspection import permutation_importance
            from sklearn.ensemble import RandomForestRegressor

            numeric_data = data.select_dtypes(include=[np.number]).fillna(data.median(numeric_only=True))
            if numeric_data.empty or len(numeric_data.columns) < 2:
                return []

            target_col = numeric_data.columns[-1]
            feature_cols = [c for c in numeric_data.columns if c != target_col]
            X = numeric_data[feature_cols]
            y = numeric_data[target_col]

            model = RandomForestRegressor(n_estimators=50, random_state=42)
            model.fit(X, y)

            perm_importance = permutation_importance(model, X, y, n_repeats=10, random_state=42)
            importances = dict(zip(feature_cols, perm_importance.importances_mean))
            importances = dict(sorted(importances.items(), key=lambda x: x[1], reverse=True))

            result = XAIResult(
                method="Permutation Importance",
                feature_importance=importances,
                global_explanation="Permutation importance measures feature contribution by shuffling values",
                local_explanations=[f"{feat}: {imp:.3f}" for feat, imp in list(importances.items())[:5]]
            )
            return [result]
        except Exception as e:
            print(f"   ⚠️ Permutation importance failed: {e}")
            return []

    def generate_narrative(self, query, analysis, charts, xai_results, statistical_results):
        if self.llm:
            try:
                return self._llm_narrative(query, analysis, charts, xai_results, statistical_results)
            except Exception as e:
                print(f"   ⚠️ LLM narrative failed: {e}. Using fallback.")
        return self._fallback_narrative(query, analysis, charts, xai_results, statistical_results)

    def _llm_narrative(self, query, analysis, charts, xai_results, statistical_results):
        from langchain_core.prompts import ChatPromptTemplate

        chart_types_str = ", ".join([c.chart_type for c in charts])
        insights_list = [insight for chart in charts for insight in chart.insights][:5]
        insights_str = "; ".join(insights_list)
        tests_str = ", ".join([t.test_name for t in statistical_results])
        xai_str = ", ".join([x.method for x in xai_results])

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert research data analyst. Write a concise, insightful narrative summarizing the visualization results for a research publication."),
            ("human", f"Query: {query}\nDomain: {analysis.get('domain', 'general')}\nData Shape: {analysis.get('data_shape', (0, 0))}\nCharts Generated: {chart_types_str}\nKey Insights: {insights_str}\nStatistical Tests: {tests_str}\nXAI Results: {xai_str}\n\nWrite a 200-300 word narrative summarizing these findings for a research paper.")
        ])

        chain = prompt | self.llm
        response = chain.invoke({})
        return response.content

    def _fallback_narrative(self, query, analysis, charts, xai_results, statistical_results):
        lines = [
            "## Research Visualization Report",
            "",
            f"**Query:** {query}",
            f"**Domain:** {analysis.get('domain', 'general').title()}",
            f"**Data:** {analysis.get('data_shape', (0, 0))[0]} records x {analysis.get('data_shape', (0, 0))[1]} features",
            "",
            "### Generated Visualizations",
            ""
        ]

        for chart in charts:
            lines.append(f"- **{chart.title}** ({chart.chart_type})")
            for insight in chart.insights:
                lines.append(f"  - {insight}")
            lines.append("")

        if xai_results:
            lines.append("### XAI Explanations")
            for xai in xai_results:
                lines.append(f"- **{xai.method}**: {xai.global_explanation}")
                for local in xai.local_explanations[:3]:
                    lines.append(f"  - {local}")
            lines.append("")

        if statistical_results:
            lines.append("### Statistical Tests")
            for test in statistical_results:
                lines.append(f"- **{test.test_name}**: {test.interpretation}")
            lines.append("")

        lines.append("### Recommendations")
        lines.append("- Review visualizations for publication readiness")
        lines.append("- Consider additional domain-specific analyses")
        lines.append("- Validate statistical assumptions before reporting")

        return "\n".join(lines)

    def chat(self, data, query):
        if self.llm:
            try:
                from langchain_core.prompts import ChatPromptTemplate

                summary = data.describe().to_string() if not data.select_dtypes(include=[np.number]).empty else "No numeric columns"
                columns_str = ", ".join(data.columns.tolist())

                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a research data analyst. Answer questions about the dataset concisely."),
                    ("human", f"Dataset Summary:\n{summary}\n\nColumns: {columns_str}\nShape: {data.shape}\n\nUser Question: {query}\n\nProvide a clear, concise answer with specific numbers from the data.")
                ])

                chain = prompt | self.llm
                response = chain.invoke({})
                return response.content
            except Exception as e:
                return f"❌ LLM chat failed: {e}.\n\nFallback: Dataset has {data.shape[0]} rows and {data.shape[1]} columns."

        return f"Dataset has {data.shape[0]} rows and {data.shape[1]} columns. Columns: {', '.join(data.columns.tolist())}"
