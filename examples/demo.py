"""
VisuAI Research Agent - Demo Script

This script demonstrates the full capabilities of VisuAI
using a sample research dataset.

Author: Muhammad Yasir Imam
"""

import pandas as pd
import numpy as np
from visuai import ResearchAgent


def create_sample_dataset():
    """Create a realistic research dataset."""
    np.random.seed(42)
    n = 500

    return pd.DataFrame({
        'patient_id': range(1, n + 1),
        'age': np.random.randint(18, 85, n),
        'gender': np.random.choice(['Male', 'Female'], n),
        'blood_pressure_systolic': np.random.normal(120, 15, n).astype(int),
        'blood_pressure_diastolic': np.random.normal(80, 10, n).astype(int),
        'cholesterol': np.random.normal(200, 40, n).astype(int),
        'glucose': np.random.normal(100, 25, n).astype(int),
        'bmi': np.random.normal(25, 5, n).round(2),
        'smoking': np.random.choice(['Yes', 'No'], n, p=[0.3, 0.7]),
        'exercise_hours': np.random.exponential(3, n).round(2),
        'diet_quality': np.random.choice(['Poor', 'Average', 'Good', 'Excellent'], n),
        'stress_level': np.random.randint(1, 11, n),
        'sleep_hours': np.random.normal(7, 1.5, n).round(2),
        'risk_score': np.random.uniform(0, 100, n).round(2),
        'outcome': np.random.choice(['Healthy', 'At Risk', 'Critical'], n, p=[0.6, 0.3, 0.1])
    })


def main():
    print("=" * 70)
    print("🔬 VisuAI Research Agent - Interactive Demo")
    print("=" * 70)
    print("\n👤 Author: Muhammad Yasir Imam")
    print("📧 Email: imammuhammadyasir@gmail.com")
    print("🔗 GitHub: https://github.com/muhammadyasirimam")
    print("📚 Google Scholar: 19 Citations | ResearchGate: 1,710 Reads")
    print("=" * 70)

    # Create sample data
    print("\n📊 Creating sample healthcare research dataset...")
    data = create_sample_dataset()
    print(f"   ✓ Generated {data.shape[0]} patient records with {data.shape[1]} features")

    # Initialize agent
    print("\n🚀 Initializing VisuAI Research Agent...")
    agent = ResearchAgent(
        domain="healthcare",
        llm_provider="openai",  # Change to your preferred provider
        # api_key="your-api-key-here"  # Or set OPENAI_API_KEY env var
    )

    # Load data
    print("\n📁 Loading data into agent...")
    agent.load_data(data)

    # Run full analysis
    print("\n" + "=" * 70)
    print("🎯 RUNNING FULL VISUALIZATION PIPELINE")
    print("=" * 70)

    result = agent.run(
        query="Analyze patient risk factors, show distributions of vital signs, "
              "correlations between health metrics, and breakdown by outcome category. "
              "Include XAI explanations for feature importance.",
        export_formats=["html", "markdown", "png"],
        xai_enabled=True,
        statistical_tests=True,
        max_charts=8
    )

    # Display results
    print("\n" + "=" * 70)
    print("📊 RESULTS SUMMARY")
    print("=" * 70)
    result.show()

    # Save results
    print("\n💾 Saving results...")
    result.save("./visuai_demo_output")

    # Chat demo
    print("\n" + "=" * 70)
    print("💬 CHAT WITH YOUR DATA")
    print("=" * 70)

    questions = [
        "What is the average age of patients?",
        "How many patients are in the Critical outcome category?",
        "What is the correlation between BMI and risk score?"
    ]

    for question in questions:
        print(f"\n❓ Q: {question}")
        response = agent.chat(question)
        print(f"💡 A: {response}")

    # Quick chart demo
    print("\n" + "=" * 70)
    print("⚡ QUICK CHART GENERATION")
    print("=" * 70)

    chart = agent.quick_chart("histogram", x="age", title="Patient Age Distribution")
    print(f"\n📊 Quick chart generated: {chart.title}")
    print(f"   Type: {chart.chart_type}")
    print(f"   Insights: {chart.insights}")

    print("\n" + "=" * 70)
    print("✅ DEMO COMPLETE!")
    print("=" * 70)
    print("\n📁 All outputs saved to: ./visuai_demo_output/")
    print("\n🙏 Thank you for using VisuAI Research Agent!")
    print("   Built with ❤️ by Muhammad Yasir Imam")
    print("   From a mud house in Pakistan to the world of AI research 🌍")
    print("=" * 70)


if __name__ == "__main__":
    main()
