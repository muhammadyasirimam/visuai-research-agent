"""
Streamlit Web Interface for VisuAI Research Agent.
Author: Muhammad Yasir Imam
"""

import os
import sys
import tempfile
import streamlit as st
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from visuai.core.agent import ResearchAgent

st.set_page_config(page_title="VisuAI Research Agent", page_icon="🔬", layout="wide")

def init_session_state():
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "data" not in st.session_state:
        st.session_state.data = None
    if "results" not in st.session_state:
        st.session_state.results = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def sidebar():
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        domain = st.selectbox("Research Domain", ["general", "machine_learning", "healthcare", "finance", "social_science", "engineering"])
        llm_provider = st.selectbox("LLM Provider", ["openai", "anthropic", "google", "local"])
        api_key = st.text_input("API Key", type="password")
        export_formats = st.multiselect("Export Formats", ["html", "pdf", "png", "jupyter", "latex", "pptx", "markdown"], default=["html", "png"])
        st.markdown("---")
        st.markdown("[GitHub](https://github.com/muhammadyasirimam)")
        st.markdown("[Google Scholar](https://scholar.google.com/citations?user=b80oc1UAAAAJ)")
        return {"domain": domain, "llm_provider": llm_provider, "api_key": api_key, "export_formats": export_formats}

def data_upload_section():
    st.markdown("### 📁 Upload Your Data")
    uploaded_file = st.file_uploader("Upload dataset", type=["csv", "xlsx", "xls", "json", "parquet"])
    if uploaded_file is not None:
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f2:
            f2.write(uploaded_file.getvalue())
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif uploaded_file.name.endswith((".xlsx", ".xls")):
                df = pd.read_excel(file_path)
            elif uploaded_file.name.endswith(".json"):
                df = pd.read_json(file_path)
            elif uploaded_file.name.endswith(".parquet"):
                df = pd.read_parquet(file_path)
            else:
                st.error("Unsupported file format")
                return None
            st.session_state.data = df
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Rows", df.shape[0])
            with col2: st.metric("Columns", df.shape[1])
            with col3: st.metric("Missing Values", df.isnull().sum().sum())
            with st.expander("🔍 Data Preview"):
                st.dataframe(df.head(20), use_container_width=True)
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None
    return None

def visualization_section(config):
    st.markdown("### 🎨 Generate Visualizations")
    query = st.text_area("Describe what you want to visualize", placeholder="e.g., Show me distributions and correlations")
    col1, col2 = st.columns(2)
    with col1: xai_enabled = st.checkbox("Enable XAI Explanations", value=True)
    with col2: max_charts = st.slider("Max Charts", 1, 20, 5)
    if st.button("🚀 Generate Visualizations", use_container_width=True):
        if st.session_state.data is None:
            st.warning("Please upload data first!")
            return
        if not query:
            st.warning("Please enter a visualization query!")
            return
        with st.spinner("🤖 AI Agent is analyzing your data..."):
            try:
                agent = ResearchAgent(domain=config["domain"], llm_provider=config["llm_provider"], api_key=config["api_key"] or None)
                agent.load_data(st.session_state.data)
                result = agent.run(query=query, export_formats=config["export_formats"], xai_enabled=xai_enabled, max_charts=max_charts)
                st.session_state.results = result
                st.session_state.agent = agent
                st.success(f"✅ Generated {len(result.charts)} visualizations in {result.execution_time:.2f}s!")
            except Exception as e:
                st.error(f"❌ Error: {e}")

def results_section():
    if st.session_state.results is None: return
    result = st.session_state.results
    if result.narrative:
        st.markdown("### 📖 AI Narrative")
        st.markdown(result.narrative)
    st.markdown("### 📊 Generated Visualizations")
    for i, chart in enumerate(result.charts):
        st.markdown(f"#### {i+1}. {chart.title} ({chart.chart_type})")
        col1, col2 = st.columns([3, 1])
        with col1:
            if chart.figure_path and os.path.exists(chart.figure_path):
                st.image(chart.figure_path, use_container_width=True)
        with col2:
            st.markdown("**Insights:**")
            for insight in chart.insights:
                st.markdown(f"- {insight}")
        st.divider()
    if result.xai_results:
        st.markdown("### 🔍 XAI Explanations")
        for xai in result.xai_results:
            with st.expander(f"{xai.method} Analysis"):
                st.markdown(f"**{xai.global_explanation}**")
                if xai.feature_importance:
                    feat_df = pd.DataFrame({"Feature": list(xai.feature_importance.keys())[:10], "Importance": list(xai.feature_importance.values())[:10]})
                    st.bar_chart(feat_df.set_index("Feature"))
    if result.statistical_results:
        st.markdown("### 📈 Statistical Tests")
        test_data = []
        for test in result.statistical_results:
            test_data.append({"Test": test.test_name, "Statistic": f"{test.statistic:.4f}", "P-Value": f"{test.p_value:.4f}", "Interpretation": test.interpretation})
        st.dataframe(pd.DataFrame(test_data), use_container_width=True)
    if result.export_paths:
        st.markdown("### 📤 Export Results")
        for fmt, path in result.export_paths.items():
            if path and os.path.exists(path):
                with open(path, "rb") as f2:
                    st.download_button(label=f"📥 {fmt.upper()}", data=f2.read(), file_name=os.path.basename(path))

def chat_section():
    st.markdown("### 💬 Chat with Your Data")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if prompt := st.chat_input("Ask about your data..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            if st.session_state.agent and st.session_state.data is not None:
                with st.spinner("Thinking..."):
                    response = st.session_state.agent.chat(prompt)
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            else:
                response = "Please upload data and generate visualizations first!"
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

def main():
    init_session_state()
    st.title("🔬 VisuAI Research Agent")
    st.caption("Transform Research Data Into Stunning Visual Intelligence — Powered by AI")
    config = sidebar()
    tab1, tab2, tab3 = st.tabs(["📁 Data & Visualize", "📊 Results", "💬 Chat"])
    with tab1:
        data_upload_section()
        if st.session_state.data is not None:
            visualization_section(config)
    with tab2: results_section()
    with tab3: chat_section()
    st.divider()
    st.caption("Built with ❤️ by Muhammad Yasir Imam | Gold Medalist | Award-Winning Researcher | Published Author")
    st.caption("From a mud house in Pakistan to the world of open-source AI research tools")

if __name__ == "__main__":
    main()