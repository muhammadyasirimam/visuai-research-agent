# Quick Start Guide

## 3-Line Quick Start

```python
from visuai import ResearchAgent

agent = ResearchAgent(domain="machine_learning")
agent.load_data("your_data.csv").run("Show me distributions and correlations")
```

## Step-by-Step Tutorial

### 1. Import and Initialize

```python
from visuai import ResearchAgent

# Initialize with your research domain
agent = ResearchAgent(
    domain="healthcare",           # or "machine_learning", "finance", etc.
    llm_provider="openai",         # or "anthropic", "google"
    api_key="your-api-key"         # Or set VISUAI_LLM_API_KEY env var
)
```

### 2. Load Data

```python
# From file
agent.load_data("path/to/dataset.csv")

# From DataFrame
import pandas as pd
df = pd.read_csv("data.csv")
agent.load_data(df)
```

### 3. Generate Visualizations

```python
result = agent.run(
    query="Show me feature correlations and model performance metrics",
    export_formats=["html", "pdf", "png"],
    xai_enabled=True,
    max_charts=10
)
```

### 4. View and Save Results

```python
# Display in notebook/console
result.show()

# Save all outputs
result.save("./my_results")

# Access individual charts
for chart in result.charts:
    print(f"{chart.title}: {chart.figure_path}")
```

### 5. Chat with Your Data

```python
response = agent.chat("What is the correlation between age and blood pressure?")
print(response)
```

## CLI Quick Start

```bash
# Analyze data
visuai analyze data.csv --domain healthcare --output ./results

# Chat with data
visuai chat data.csv --query "Show me trends over time"

# Launch web interface
visuai web --port 8501
```
