# Tutorials

## Tutorial 1: Healthcare Data Visualization

```python
from visuai import ResearchAgent
import pandas as pd

# Load patient data
data = pd.read_csv("patients.csv")

# Initialize for healthcare domain
agent = ResearchAgent(domain="healthcare")
agent.load_data(data)

# Generate clinical visualizations
result = agent.run(
    query="Show patient demographics, vital signs distributions, and risk factor analysis",
    export_formats=["html", "pdf"],
    xai_enabled=True
)

result.save("./clinical_report")
```

## Tutorial 2: Machine Learning Model Analysis

```python
from visuai import ResearchAgent

# Load model results
agent = ResearchAgent(domain="machine_learning")
agent.load_data("model_results.csv")

# Generate ML visualizations
result = agent.run(
    query="Show confusion matrix, ROC curve, feature importance, and SHAP explanations",
    export_formats=["html", "png", "jupyter"],
    xai_enabled=True,
    max_charts=8
)
```

## Tutorial 3: Financial Time Series

```python
from visuai import ResearchAgent

agent = ResearchAgent(domain="finance")
agent.load_data("stock_prices.csv")

result = agent.run(
    query="Show candlestick charts, moving averages, correlation matrix, and risk metrics",
    export_formats=["html", "pdf"]
)
```

## Tutorial 4: Social Science Survey Data

```python
from visuai import ResearchAgent

agent = ResearchAgent(domain="social_science")
agent.load_data("survey_responses.csv")

result = agent.run(
    query="Show demographic breakdowns, Likert scale distributions, and cross-tabulations",
    export_formats=["html", "pptx"]
)
```
