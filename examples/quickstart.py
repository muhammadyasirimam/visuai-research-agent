"""
VisuAI Quick Start Guide

Minimal example to get started with VisuAI Research Agent.

Author: Muhammad Yasir Imam
"""

import pandas as pd
import numpy as np
from visuai import ResearchAgent

# 1. Create or load your data
data = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'category': np.random.choice(['A', 'B', 'C'], 100)
})

# 2. Initialize the agent
agent = ResearchAgent(domain="general")

# 3. Load data
agent.load_data(data)

# 4. Generate visualizations
result = agent.run(
    query="Show me the distribution and relationships in my data",
    export_formats=["html", "png"]
)

# 5. View results
result.show()

# 6. Save results
result.save("./my_results")
