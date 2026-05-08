"""
Command Line Interface for VisuAI Research Agent.

Author: Muhammad Yasir Imam
"""

import os
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from .core.agent import ResearchAgent
from .core.config import Config

app = typer.Typer(
    name="visuai",
    help="VisuAI Research Agent - AI-Powered Research Data Visualization",
    add_completion=False
)
console = Console()


@app.command()
def analyze(
    data_path: str = typer.Argument(..., help="Path to data file"),
    domain: str = typer.Option("general", "--domain", "-d", help="Research domain"),
    query: str = typer.Option("Analyze and visualize this data", "--query", "-q", help="Analysis query"),
    output: str = typer.Option("./visuai_output", "--output", "-o", help="Output directory"),
    formats: str = typer.Option("html,pdf", "--formats", "-f", help="Export formats (comma-separated)"),
    xai: bool = typer.Option(True, "--xai/--no-xai", help="Enable XAI explanations"),
    llm: str = typer.Option("openai", "--llm", help="LLM provider"),
    api_key: Optional[str] = typer.Option(None, "--api-key", help="API key for LLM"),
):
    """Analyze data and generate visualizations."""
    console.print(Panel.fit(
        "[bold cyan]🔬 VisuAI Research Agent[/bold cyan]\n"
        "[dim]AI-Powered Research Data Visualization[/dim]",
        border_style="cyan"
    ))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Initializing agent...", total=None)

        agent = ResearchAgent(
            domain=domain,
            llm_provider=llm,
            api_key=api_key
        )

        progress.update(task, description="Loading data...")
        agent.load_data(data_path)

        progress.update(task, description="Running analysis...")
        result = agent.run(
            query=query,
            export_formats=formats.split(","),
            xai_enabled=xai
        )

        progress.update(task, description="Saving results...")
        result.save(output)

    console.print(f"\n[green]✅ Analysis complete![/green]")
    console.print(f"📊 Charts generated: {len(result.charts)}")
    console.print(f"📁 Output saved to: {output}")

    # Display results table
    table = Table(title="Generated Visualizations")
    table.add_column("#", style="cyan")
    table.add_column("Chart", style="green")
    table.add_column("Type", style="yellow")
    table.add_column("Insights", style="white")

    for i, chart in enumerate(result.charts, 1):
        insights = "; ".join(chart.insights[:2]) if chart.insights else "N/A"
        table.add_row(str(i), chart.title, chart.chart_type, insights)

    console.print(table)


@app.command()
def chat(
    data_path: str = typer.Argument(..., help="Path to data file"),
    query: str = typer.Option(..., "--query", "-q", help="Question about the data"),
    domain: str = typer.Option("general", "--domain", "-d", help="Research domain"),
    llm: str = typer.Option("openai", "--llm", help="LLM provider"),
    api_key: Optional[str] = typer.Option(None, "--api-key", help="API key for LLM"),
):
    """Chat with your data using natural language."""
    console.print(Panel.fit(
        "[bold cyan]💬 VisuAI Data Chat[/bold cyan]",
        border_style="cyan"
    ))

    agent = ResearchAgent(domain=domain, llm_provider=llm, api_key=api_key)
    agent.load_data(data_path)

    response = agent.chat(query)
    console.print(f"\n[bold green]Response:[/bold green]")
    console.print(Panel(response, border_style="green"))


@app.command()
def report(
    data_path: str = typer.Argument(..., help="Path to data file"),
    template: str = typer.Option("ieee", "--template", "-t", help="Report template (ieee, acm, nature)"),
    output: str = typer.Option("./report.pdf", "--output", "-o", help="Output file path"),
    domain: str = typer.Option("general", "--domain", "-d", help="Research domain"),
):
    """Generate full research report."""
    console.print(Panel.fit(
        "[bold cyan]📄 VisuAI Report Generator[/bold cyan]",
        border_style="cyan"
    ))

    agent = ResearchAgent(domain=domain)
    agent.load_data(data_path)

    result = agent.run(
        query=f"Generate comprehensive research report using {template} template",
        export_formats=["pdf", "latex", "html"]
    )
    result.save(os.path.dirname(output))

    console.print(f"[green]✅ Report generated![/green]")


@app.command()
def web(
    port: int = typer.Option(8501, "--port", "-p", help="Port number"),
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host address"),
):
    """Launch web interface."""
    console.print(Panel.fit(
        "[bold cyan]🌐 VisuAI Web Interface[/bold cyan]\n"
        f"[dim]Starting on http://{host}:{port}[/dim]",
        border_style="cyan"
    ))

    try:
        import streamlit.web.cli as stcli
        import sys

        web_app_path = os.path.join(os.path.dirname(__file__), "..", "web", "app.py")
        sys.argv = ["streamlit", "run", web_app_path, "--server.port", str(port), "--server.address", host]
        stcli.main()
    except Exception as e:
        console.print(f"[red]❌ Failed to start web interface: {e}[/red]")
        console.print("[yellow]Make sure streamlit is installed: pip install streamlit[/yellow]")


@app.command()
def domains():
    """List supported research domains."""
    from .core.config import DOMAIN_PRESETS

    table = Table(title="Supported Research Domains")
    table.add_column("Domain", style="cyan")
    table.add_column("Specialized Charts", style="green")
    table.add_column("Statistical Tests", style="yellow")

    for domain, preset in DOMAIN_PRESETS.items():
        charts = ", ".join(preset.get("specialized_charts", [])[:5]) + "..."
        tests = ", ".join(preset.get("statistical_tests", [])[:3]) + "..."
        table.add_row(domain, charts, tests)

    console.print(table)


def main():
    app()


if __name__ == "__main__":
    main()
