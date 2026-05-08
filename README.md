<div align="center">

# 🔬 VisuAI Research Agent

**Transform Research Data Into Stunning Visual Intelligence — Powered by AI**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/muhammadyasirimam/visuai-research-agent?style=social)](https://github.com/muhammadyasirimam/visuai-research-agent)
[![ResearchGate](https://img.shields.io/badge/ResearchGate-1,710%20Reads-00CCBB)](https://www.researchgate.net/profile/Muhammad-Yasir-Imam)
[![Google Scholar](https://img.shields.io/badge/Google%20Scholar-19%20Citations-4285F4)](https://scholar.google.com/citations?user=b80oc1UAAAAJ)

<img src="assets/images/banner.png" alt="VisuAI Banner" width="800"/>

**An AI-powered autonomous agent that transforms raw research datasets into publication-ready, interactive visualizations — tailored to your research domain, methodology, and audience.**

[🚀 Quick Start](#quick-start) • [📖 Documentation](docs/) • [🎨 Examples](examples/) • [🤝 Contribute](CONTRIBUTING.md)

</div>

---

## 🎯 What is VisuAI?

**VisuAI Research Agent** is an open-source AI agent framework designed specifically for researchers, data scientists, and academics who need to:

- 📊 **Auto-detect** the best visualization types for their data
- 🧠 **Understand context** — knows if you're doing ML, epidemiology, finance, or social science
- 🎨 **Generate publication-quality** charts, graphs, and interactive dashboards
- 🤖 **Explain insights** in natural language with XAI (Explainable AI) support
- 🔗 **Export** to LaTeX, PDF, HTML, Jupyter, PowerPoint, and more
- 🌐 **Deploy** as a web app, API, or GitHub Pages site

> *"Built by a researcher, for researchers. From 49% to Gold Medal — I know the struggle of making data tell its story."*  
> — **Muhammad Yasir Imam**, Founder & Lead Researcher

---

## ✨ Key Features

| Feature | Description | Status |
|---------|-------------|--------|
| 🤖 **AI Agent Orchestration** | Multi-agent system (Analyzer → Visualizer → Explainer → Exporter) | ✅ Ready |
| 📊 **Auto-Chart Detection** | Smart algorithm picks optimal chart type from 50+ options | ✅ Ready |
| 🧠 **Domain Intelligence** | Specialized modes: ML/AI, Healthcare, Finance, Social Science, Engineering | ✅ Ready |
| 🔍 **XAI Integration** | SHAP, LIME, attention maps, feature importance visualizations | ✅ Ready |
| 🌐 **Interactive Dashboards** | Streamlit + Plotly + D3.js web apps | ✅ Ready |
| 📄 **Publication Export** | LaTeX, PDF, PPT, HTML, Jupyter notebooks | ✅ Ready |
| 🗣️ **Natural Language** | Chat with your data — "Show me correlations in my dataset" | ✅ Ready |
| 🔄 **Real-time Processing** | Stream data and get live visualizations | ✅ Ready |
| 🧩 **Plugin System** | Extend with custom visualizers, parsers, and agents | ✅ Ready |
| ☁️ **Cloud Ready** | Docker, GitHub Actions, AWS/GCP/Azure deployment | ✅ Ready |

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/muhammadyasirimam/visuai-research-agent.git
cd visuai-research-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Basic Usage

```python
from visuai import ResearchAgent

# Initialize the agent
agent = ResearchAgent(
    domain="machine_learning",  # or "healthcare", "finance", "social_science"
    output_format="interactive"
)

# Load your data
agent.load_data("path/to/your/dataset.csv")

# Let the AI agent analyze and visualize
results = agent.run(
    query="Show me feature correlations and model performance metrics",
    export_formats=["html", "pdf", "jupyter"]
)

# Access results
results.show()  # Opens interactive dashboard
results.save("output/")  # Saves all formats
```

### CLI Usage

```bash
# Quick visualization
visuai analyze data.csv --domain healthcare --output ./results

# With natural language
visuai chat --data data.csv --query "Show me trends over time"

# Generate full research report
visuai report --data data.csv --template ieee --output report.pdf

# Launch web interface
visuai web --port 8501
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VisuAI Research Agent                      │
├─────────────────────────────────────────────────────────────┤
│  🎯 User Input (Data + Query + Domain)                      │
│                    ↓                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Analyzer   │→│ Visualizer  │→│  Explainer   │         │
│  │   Agent     │  │   Agent     │  │   Agent      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│        ↓                ↓                ↓                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Orchestrator (LangGraph)                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                    ↓                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Parser    │  │   Chart     │  │   Export    │         │
│  │   Engine    │  │   Engine    │  │   Engine    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                    ↓                                         │
│  📊 Interactive Dashboard / 📄 PDF / 🌐 Web App            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 Research Domains Supported

| Domain | Specializations | Sample Visualizations |
|--------|-----------------|----------------------|
| 🤖 **Machine Learning** | Model performance, confusion matrices, ROC curves, learning curves, SHAP plots | Feature importance, decision boundaries, training dynamics |
| 🏥 **Healthcare & Bio** | Survival curves, heatmaps, genomic visualizations, clinical pathways | Kaplan-Meier, volcano plots, pathway diagrams |
| 💰 **Finance & Economics** | Time series, candlestick charts, portfolio analysis, risk metrics | Efficient frontier, VaR analysis, correlation matrices |
| 🌍 **Social Science** | Survey results, demographic maps, network graphs, sentiment analysis | Choropleth maps, network diagrams, word clouds |
| 🔬 **Engineering** | Signal processing, CAD visualizations, simulation results, sensor data | FFT plots, 3D meshes, heatmaps, oscilloscope views |
| 📈 **General Statistics** | Distributions, regressions, hypothesis tests, ANOVA | Box plots, Q-Q plots, residual plots |

---

## 🎨 Visualization Gallery

<div align="center">

| Interactive Dashboard | XAI SHAP Analysis | Publication Chart |
|:---:|:---:|:---:|
| <img src="assets/demo/dashboard.gif" width="250"/> | <img src="assets/demo/shap.png" width="250"/> | <img src="assets/demo/publication.png" width="250"/> |
| **Network Graph** | **Geospatial Map** | **Time Series** |
| <img src="assets/demo/network.png" width="250"/> | <img src="assets/demo/map.png" width="250"/> | <img src="assets/demo/timeseries.png" width="250"/> |

</div>

---

## 🛠️ Advanced Configuration

```python
from visuai import ResearchAgent, Config

config = Config(
    # AI Model Settings
    llm_provider="openai",  # or "anthropic", "google", "local"
    model="gpt-4o",
    temperature=0.3,

    # Visualization Settings
    theme="publication",  # "publication", "dark", "colorblind", "minimal"
    color_palette="seaborn",
    figure_dpi=300,

    # XAI Settings
    xai_method="shap",  # "shap", "lime", "attention", "permutation"
    xai_samples=100,

    # Export Settings
    export_formats=["html", "pdf", "latex", "pptx"],
    latex_template="ieee",

    # Performance
    parallel_processing=True,
    max_workers=4,
    cache_results=True
)

agent = ResearchAgent(config=config)
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=visuai --cov-report=html

# Run specific test suite
pytest tests/unit/test_agents.py -v
pytest tests/integration/test_end_to_end.py -v
```

---

## 🤝 Contributing

We welcome contributions from researchers, developers, and data scientists!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📖 Citation

If you use VisuAI in your research, please cite:

```bibtex
@software{visuai2026,
  author = {Imam, Muhammad Yasir},
  title = {VisuAI Research Agent: AI-Powered Research Data Visualization},
  year = {2026},
  url = {https://github.com/muhammadyasirimam/visuai-research-agent},
  orcid = {0000-0002-7495-4179}
}
```

---

## 📬 Connect With The Author

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-muhammadyasirimam-181717?logo=github)](https://github.com/muhammadyasirimam)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Muhammad%20Yasir%20Imam-0A66C2?logo=linkedin)](https://linkedin.com/in/muhammadyasirimam)
[![ResearchGate](https://img.shields.io/badge/ResearchGate-Profile-00CCBB?logo=researchgate)](https://www.researchgate.net/profile/Muhammad-Yasir-Imam)
[![Google Scholar](https://img.shields.io/badge/Google%20Scholar-Profile-4285F4?logo=googlescholar)](https://scholar.google.com/citations?user=b80oc1UAAAAJ)
[![Medium](https://img.shields.io/badge/Medium-@muhammadyasirimam-000000?logo=medium)](https://medium.com/@muhammadyasirimam)
[![ORCID](https://img.shields.io/badge/ORCID-0000--0002--7495--4179-A6CE39?logo=orcid)](https://orcid.org/0000-0002-7495-4179)
[![MYI News World](https://img.shields.io/badge/MYI%20News%20World-Website-FF5722)](https://myinewsworld.com)

</div>

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**⭐ Star this repo if it helps your research!**  
**🍴 Fork it to build your own visualization tools!**

*Built with ❤️ by Muhammad Yasir Imam*  
*From a mud house in Pakistan to the world of open-source AI*

</div>
