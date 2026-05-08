"""
Configuration module for VisuAI Research Agent.

Handles all configuration settings, environment variables,
and domain-specific presets.

Author: Muhammad Yasir Imam
"""

import os
import yaml
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path


@dataclass
class LLMConfig:
    """Configuration for LLM providers."""
    provider: str = "openai"  # openai, anthropic, google, local
    model: str = "gpt-4o"
    temperature: float = 0.3
    max_tokens: int = 4096
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    timeout: int = 60


@dataclass
class VisualizationConfig:
    """Configuration for visualization engine."""
    theme: str = "publication"  # publication, dark, colorblind, minimal, neon
    color_palette: str = "seaborn"
    figure_dpi: int = 300
    figure_format: str = "png"
    interactive: bool = True
    animation_enabled: bool = False
    default_width: int = 1200
    default_height: int = 800
    font_family: str = "DejaVu Sans"
    font_size: int = 12
    save_metadata: bool = True


@dataclass
class XAIConfig:
    """Configuration for Explainable AI."""
    method: str = "shap"  # shap, lime, attention, permutation, integrated_gradients
    samples: int = 100
    background_samples: int = 100
    plot_type: str = "summary"  # summary, waterfall, force, dependence
    show_values: bool = True
    max_display_features: int = 20


@dataclass
class ExportConfig:
    """Configuration for export formats."""
    formats: List[str] = field(default_factory=lambda: ["html", "pdf"])
    latex_template: str = "ieee"  # ieee, acm, nature, science, custom
    pdf_engine: str = "weasyprint"
    html_template: str = "default"
    pptx_template: str = "default"
    jupyter_template: str = "default"
    output_dir: str = "./visuai_output"


@dataclass
class DomainConfig:
    """Domain-specific configuration presets."""
    domain: str = "general"  # general, machine_learning, healthcare, finance, social_science, engineering
    specialized_charts: List[str] = field(default_factory=list)
    statistical_tests: List[str] = field(default_factory=list)
    recommended_metrics: List[str] = field(default_factory=list)
    citation_style: str = "ieee"


@dataclass
class Config:
    """Main configuration class for VisuAI Research Agent."""

    # Core settings
    llm: LLMConfig = field(default_factory=LLMConfig)
    visualization: VisualizationConfig = field(default_factory=VisualizationConfig)
    xai: XAIConfig = field(default_factory=XAIConfig)
    export: ExportConfig = field(default_factory=ExportConfig)
    domain: DomainConfig = field(default_factory=DomainConfig)

    # Performance settings
    parallel_processing: bool = True
    max_workers: int = 4
    cache_results: bool = True
    cache_dir: str = "./.visuai_cache"

    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
    verbose: bool = False

    # Security
    sanitize_inputs: bool = True
    max_file_size_mb: int = 500
    allowed_extensions: List[str] = field(default_factory=lambda: [
        ".csv", ".xlsx", ".xls", ".json", ".parquet", ".hdf5", ".h5",
        ".txt", ".tsv", ".db", ".sqlite", ".pdf", ".docx"
    ])

    @classmethod
    def from_yaml(cls, path: str) -> "Config":
        """Load configuration from YAML file."""
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls._from_dict(data)

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        config = cls()

        # LLM settings
        config.llm.provider = os.getenv("VISUAI_LLM_PROVIDER", config.llm.provider)
        config.llm.model = os.getenv("VISUAI_LLM_MODEL", config.llm.model)
        config.llm.api_key = os.getenv("VISUAI_LLM_API_KEY")
        config.llm.temperature = float(os.getenv("VISUAI_LLM_TEMPERATURE", config.llm.temperature))

        # Visualization settings
        config.visualization.theme = os.getenv("VISUAI_THEME", config.visualization.theme)
        config.visualization.dpi = int(os.getenv("VISUAI_DPI", config.visualization.figure_dpi))

        # Domain
        config.domain.domain = os.getenv("VISUAI_DOMAIN", config.domain.domain)

        return config

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> "Config":
        """Create Config from dictionary."""
        config = cls()

        if "llm" in data:
            config.llm = LLMConfig(**data["llm"])
        if "visualization" in data:
            config.visualization = VisualizationConfig(**data["visualization"])
        if "xai" in data:
            config.xai = XAIConfig(**data["xai"])
        if "export" in data:
            config.export = ExportConfig(**data["export"])
        if "domain" in data:
            config.domain = DomainConfig(**data["domain"])

        for key, value in data.items():
            if hasattr(config, key) and key not in ["llm", "visualization", "xai", "export", "domain"]:
                setattr(config, key, value)

        return config

    def to_dict(self) -> Dict[str, Any]:
        """Convert Config to dictionary."""
        return {
            "llm": self.llm.__dict__,
            "visualization": self.visualization.__dict__,
            "xai": self.xai.__dict__,
            "export": self.export.__dict__,
            "domain": self.domain.__dict__,
            "parallel_processing": self.parallel_processing,
            "max_workers": self.max_workers,
            "cache_results": self.cache_results,
            "log_level": self.log_level,
            "verbose": self.verbose,
        }

    def save(self, path: str) -> None:
        """Save configuration to YAML file."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False)


# Domain-specific presets
DOMAIN_PRESETS = {
    "machine_learning": {
        "specialized_charts": [
            "confusion_matrix", "roc_curve", "precision_recall", "learning_curve",
            "feature_importance", "shap_summary", "decision_boundary", "residual_plot",
            "calibration_curve", "lift_chart", "gain_chart", "ks_statistic"
        ],
        "statistical_tests": [
            "chi_square", "t_test", "anova", "mann_whitney", "kolmogorov_smirnov"
        ],
        "recommended_metrics": [
            "accuracy", "precision", "recall", "f1_score", "auc_roc", "log_loss",
            "mae", "rmse", "r2_score", "mape"
        ],
        "citation_style": "ieee"
    },
    "healthcare": {
        "specialized_charts": [
            "kaplan_meier", "survival_curve", "forest_plot", "volcano_plot",
            "manhattan_plot", "heatmap_clinical", "pathway_diagram", "patient_timeline",
            "dose_response", "pharmacokinetic", "genomic_ideogram"
        ],
        "statistical_tests": [
            "log_rank", "cox_regression", "kaplan_meier", "fisher_exact", "mcnemar"
        ],
        "recommended_metrics": [
            "sensitivity", "specificity", "ppv", "npv", "likelihood_ratio",
            "number_needed_to_treat", "hazard_ratio", "odds_ratio"
        ],
        "citation_style": "vancouver"
    },
    "finance": {
        "specialized_charts": [
            "candlestick", "efficient_frontier", "var_analysis", "drawdown_chart",
            "correlation_matrix", "rolling_statistics", "seasonal_decomposition",
            "autocorrelation", "partial_autocorrelation", "qq_plot_returns"
        ],
        "statistical_tests": [
            "adf_test", "kpss_test", "ljung_box", "jarque_bera", "durbin_watson"
        ],
        "recommended_metrics": [
            "sharpe_ratio", "sortino_ratio", "treynor_ratio", "information_ratio",
            "max_drawdown", "calmar_ratio", "omega_ratio", "skewness", "kurtosis"
        ],
        "citation_style": "apa"
    },
    "social_science": {
        "specialized_charts": [
            "choropleth_map", "network_graph", "word_cloud", "sentiment_timeline",
            "demographic_pyramid", "survey_likert", "thematic_map", "flow_map",
            "sankey_diagram", "treemap_hierarchical", "bubble_chart"
        ],
        "statistical_tests": [
            "chi_square", "cronbach_alpha", "kruskal_wallis", "friedman",
            "spearman_correlation", "kendall_tau"
        ],
        "recommended_metrics": [
            "response_rate", "cronbach_alpha", "kmo_measure", "factor_loadings",
            "r_squared", "adjusted_r_squared", "aic", "bic"
        ],
        "citation_style": "apa"
    },
    "engineering": {
        "specialized_charts": [
            "fft_spectrum", "bode_plot", "nyquist_plot", "signal_heatmap",
            "3d_mesh", "contour_plot", "vector_field", "streamlines",
            "stress_strain", "fatigue_curve", "s_n_diagram"
        ],
        "statistical_tests": [
            "anderson_darling", "shapiro_wilk", "grubbs_test", "dixon_test"
        ],
        "recommended_metrics": [
            "snr", "thd", "ber", "fer", "mse", "psnr", "ssim"
        ],
        "citation_style": "ieee"
    }
}
