"""
FastAPI backend for VisuAI Research Agent.

Provides REST API endpoints for programmatic access.

Author: Muhammad Yasir Imam
"""

import os
import tempfile
from typing import List, Optional, Dict, Any
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import pandas as pd

from .core.agent import ResearchAgent
from .core.config import Config


app = FastAPI(
    title="VisuAI Research Agent API",
    description="AI-Powered Research Data Visualization API",
    version="1.0.0",
    contact={
        "name": "Muhammad Yasir Imam",
        "email": "imammuhammadyasir@gmail.com",
        "url": "https://github.com/muhammadyasirimam"
    }
)


class AnalyzeRequest(BaseModel):
    query: str = "Analyze and visualize this data"
    domain: str = "general"
    chart_types: Optional[List[str]] = None
    export_formats: List[str] = ["html"]
    xai_enabled: bool = True
    statistical_tests: bool = True
    max_charts: int = 10
    llm_provider: str = "openai"
    api_key: Optional[str] = None


class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None


@app.get("/")
def root():
    return {
        "name": "VisuAI Research Agent API",
        "version": "1.0.0",
        "author": "Muhammad Yasir Imam",
        "endpoints": [
            "/analyze",
            "/chat",
            "/domains",
            "/health"
        ]
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "visuai-api"}


@app.get("/domains")
def get_domains():
    from .core.config import DOMAIN_PRESETS
    return {
        "domains": list(DOMAIN_PRESETS.keys()),
        "details": DOMAIN_PRESETS
    }


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    request: str = Form(...)
):
    """Analyze uploaded data and return visualizations."""
    try:
        import json
        req = json.loads(request)

        # Save uploaded file
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Initialize agent
        agent = ResearchAgent(
            domain=req.get("domain", "general"),
            llm_provider=req.get("llm_provider", "openai"),
            api_key=req.get("api_key")
        )

        # Load and analyze
        agent.load_data(file_path)
        result = agent.run(
            query=req.get("query", "Analyze this data"),
            chart_types=req.get("chart_types"),
            export_formats=req.get("export_formats", ["html"]),
            xai_enabled=req.get("xai_enabled", True),
            statistical_tests=req.get("statistical_tests", True),
            max_charts=req.get("max_charts", 10)
        )

        # Prepare response
        response = {
            "session_id": result.session_id,
            "query": result.query,
            "domain": result.domain,
            "charts_generated": len(result.charts),
            "xai_analyses": len(result.xai_results),
            "statistical_tests": len(result.statistical_results),
            "execution_time": result.execution_time,
            "narrative": result.narrative,
            "charts": [
                {
                    "id": c.chart_id,
                    "type": c.chart_type,
                    "title": c.title,
                    "insights": c.insights,
                    "figure_path": c.figure_path
                }
                for c in result.charts
            ],
            "export_paths": result.export_paths
        }

        return JSONResponse(content=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
async def chat(request: ChatRequest):
    """Chat with data (requires existing session)."""
    return {
        "response": "Chat functionality requires session management. Use /analyze first.",
        "query": request.query
    }


@app.get("/download/{session_id}/{filename}")
def download_file(session_id: str, filename: str):
    """Download generated file."""
    file_path = f"./visuai_output/{session_id}/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")
