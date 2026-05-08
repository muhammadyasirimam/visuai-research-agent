# API Reference

## ResearchAgent

### Constructor

```python
ResearchAgent(
    config=None,
    domain="general",
    output_format="interactive",
    llm_provider="openai",
    api_key=None
)
```

**Parameters:**
- `config` (Config): Custom configuration object
- `domain` (str): Research domain
- `output_format` (str): Default output format
- `llm_provider` (str): LLM provider name
- `api_key` (str): API key for LLM

### Methods

#### load_data()

```python
agent.load_data(source, **kwargs)
```

Load data from file path or DataFrame.

**Parameters:**
- `source` (str|DataFrame): Data source
- `**kwargs`: Additional loading arguments

**Returns:** Self (for method chaining)

#### run()

```python
agent.run(
    query,
    chart_types=None,
    export_formats=None,
    xai_enabled=True,
    statistical_tests=True,
    max_charts=10
)
```

Run the full visualization pipeline.

**Parameters:**
- `query` (str): Natural language query
- `chart_types` (list): Specific chart types
- `export_formats` (list): Export formats
- `xai_enabled` (bool): Enable XAI
- `statistical_tests` (bool): Run statistical tests
- `max_charts` (int): Maximum charts

**Returns:** VisualizationResult

#### chat()

```python
agent.chat(query)
```

Chat with data using natural language.

**Parameters:**
- `query` (str): Question about data

**Returns:** str (AI response)

#### quick_chart()

```python
agent.quick_chart(chart_type, x=None, y=None, **kwargs)
```

Generate a single chart quickly.

## Config

```python
from visuai.core.config import Config

config = Config()
config.llm.provider = "openai"
config.llm.model = "gpt-4o"
config.visualization.theme = "publication"
config.xai.method = "shap"
```

## VisualizationResult

### Methods

- `show()`: Display all results
- `save(output_dir)`: Save results to directory
- `to_dict()`: Convert to dictionary
