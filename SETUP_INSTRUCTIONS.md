# 🚀 VisuAI Research Agent — Complete Setup Guide

**Author:** Muhammad Yasir Imam | **ORCID:** 0000-0002-7495-4179 | **GitHub:** [muhammadyasirimam](https://github.com/muhammadyasirimam)

> *"From a mud house in Pakistan to the world of open-source AI research tools."*

---

## 📋 Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Installation](#2-installation)
3. [Configuration](#3-configuration)
4. [Running the Project](#4-running-the-project)
5. [Adding to GitHub Pages](#5-adding-to-github-pages)
6. [Adding to Your GitHub Profile](#6-adding-to-your-github-profile)
7. [Docker Deployment](#7-docker-deployment)
8. [API Usage](#8-api-usage)
9. [Troubleshooting](#9-troubleshooting)
10. [Next Steps](#10-next-steps)

---

## 1. Prerequisites

Before starting, ensure you have:

- **Python 3.9+** installed ([Download](https://python.org/downloads))
- **Git** installed ([Download](https://git-scm.com/downloads))
- A **GitHub account** ([Sign up](https://github.com/join))
- (Optional) An **OpenAI API key** for AI features ([Get one](https://platform.openai.com/api-keys))
- (Optional) **Docker** for containerized deployment

### Check your Python version:
```bash
python --version  # Should be 3.9 or higher
```

---

## 2. Installation

### Step 2.1: Clone the Repository

```bash
# Clone your repository
git clone https://github.com/muhammadyasirimam/visuai-research-agent.git
cd visuai-research-agent
```

### Step 2.2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 2.3: Install Dependencies

```bash
# Install in development mode
pip install -e .

# Or install with all extras
pip install -e ".[dev,docs]"
```

### Step 2.4: Verify Installation

```bash
# Check if visuai CLI is available
visuai --help

# Run tests
pytest tests/ -v
```

---

## 3. Configuration

### Step 3.1: Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

### Step 3.2: Configure Your API Key

Add your API key to the `.env` file:

```env
VISUAI_LLM_PROVIDER=openai
VISUAI_LLM_API_KEY=sk-your-api-key-here
VISUAI_LLM_MODEL=gpt-4o
VISUAI_DOMAIN=general
```

**Alternative:** Set directly in environment:
```bash
# Windows (PowerShell)
$env:VISUAI_LLM_API_KEY="sk-your-api-key-here"

# macOS/Linux
export VISUAI_LLM_API_KEY="sk-your-api-key-here"
```

### Step 3.3: Verify Configuration

```bash
# Test the configuration
python -c "from visuai.core.config import Config; c = Config.from_env(); print(f'Config loaded: {c.llm.provider}')"
```

---

## 4. Running the Project

### Option A: Python Script

```bash
# Run the demo
python examples/demo.py

# Run quickstart
python examples/quickstart.py
```

### Option B: CLI Commands

```bash
# Analyze a dataset
visuai analyze data.csv --domain healthcare --query "Show me distributions and correlations"

# Chat with data
visuai chat data.csv --query "What is the average age?"

# Generate report
visuai report data.csv --template ieee --output report.pdf

# List supported domains
visuai domains
```

### Option C: Web Interface (Streamlit)

```bash
# Launch the web app
visuai web --port 8501

# Or directly with streamlit
streamlit run src/visuai/web/app.py
```

Then open your browser to: **http://localhost:8501**

### Option D: Jupyter Notebook

```bash
# Start Jupyter
jupyter notebook examples/notebooks/tutorial.ipynb
```

---

## 5. Adding to GitHub Pages

### Step 5.1: Enable GitHub Pages

1. Go to your repository on GitHub: `https://github.com/muhammadyasirimam/visuai-research-agent`
2. Click **Settings** tab
3. Scroll down to **Pages** section (left sidebar)
4. Under **Source**, select **Deploy from a branch**
5. Select **main** branch and **/ (root)** folder
6. Click **Save**

### Step 5.2: Ensure pages/ Folder Exists

Your repository should have:
```
visuai-research-agent/
├── pages/
│   └── index.html          ← This is your GitHub Pages site
├── src/
├── README.md
└── ...
```

The `pages/index.html` file is already created and ready.

### Step 5.3: Wait for Deployment

- GitHub Pages will deploy automatically
- Visit: `https://muhammadyasirimam.github.io/visuai-research-agent`
- Deployment may take 1-5 minutes

### Step 5.4: Custom Domain (Optional)

1. In repository Settings > Pages
2. Under **Custom domain**, enter your domain (e.g., `visuai.yourdomain.com`)
3. Add a CNAME file in the `pages/` folder:
   ```bash
   echo "visuai.yourdomain.com" > pages/CNAME
   ```
4. Configure DNS with your provider

---

## 6. Adding to Your GitHub Profile

### Step 6.1: Pin the Repository

1. Go to your GitHub profile: `https://github.com/muhammadyasirimam`
2. Click **Customize your pins**
3. Select **visuai-research-agent** from the list
4. Click **Save pins**

### Step 6.2: Update Your GitHub Profile README

Edit your profile repository (`muhammadyasirimam/muhammadyasirimam`):

```markdown
### 🔬 Featured Project: VisuAI Research Agent

[![VisuAI](https://img.shields.io/badge/VisuAI-Research%20Agent-2563eb)](https://github.com/muhammadyasirimam/visuai-research-agent)

AI-powered research data visualization tool. Transform datasets into publication-ready charts with natural language.

- 🎯 50+ chart types | 5 research domains | 7 export formats
- 🧠 SHAP, LIME, Permutation Importance XAI support
- 📄 LaTeX, PDF, HTML, Jupyter, PowerPoint export
- 🌐 Live demo: [muhammadyasirimam.github.io/visuai-research-agent](https://muhammadyasirimam.github.io/visuai-research-agent)
```

### Step 6.3: Add to Your Portfolio Website

On `muhammadyasirimam.github.io`, add a project card:

```html
<div class="project-card">
    <h3>🔬 VisuAI Research Agent</h3>
    <p>AI-powered research data visualization</p>
    <a href="https://github.com/muhammadyasirimam/visuai-research-agent">GitHub</a>
    <a href="https://muhammadyasirimam.github.io/visuai-research-agent">Live Demo</a>
</div>
```

---

## 7. Docker Deployment

### Step 7.1: Build Docker Image

```bash
# Build the image
docker build -f docker/Dockerfile -t visuai:latest .

# Or use docker-compose
cd docker
docker-compose up --build
```

### Step 7.2: Run Container

```bash
# Run web interface
docker run -p 8501:8501 -e VISUAI_LLM_API_KEY=$VISUAI_LLM_API_KEY visuai:latest

# Run with volume for data
docker run -p 8501:8501 -v $(pwd)/data:/app/data -v $(pwd)/output:/app/visuai_output visuai:latest
```

### Step 7.3: Deploy to Cloud

**AWS:**
```bash
# Push to ECR and deploy to ECS
docker tag visuai:latest YOUR_AWS_ACCOUNT.dkr.ecr.region.amazonaws.com/visuai:latest
docker push YOUR_AWS_ACCOUNT.dkr.ecr.region.amazonaws.com/visuai:latest
```

**Google Cloud Run:**
```bash
gcloud run deploy visuai --image visuai:latest --port 8501
```

**Heroku:**
```bash
heroku container:push web -a your-app-name
heroku container:release web -a your-app-name
```

---

## 8. API Usage

### Step 8.1: Start API Server

```bash
# Start FastAPI server
uvicorn visuai.api:app --host 0.0.0.0 --port 8000
```

### Step 8.2: API Endpoints

```bash
# Upload data and analyze
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data.csv" \
  -F "query=Show distributions" \
  -F "domain=healthcare"

# Chat with data
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the average age?", "session_id": "abc123"}'
```

### Step 8.3: API Documentation

Visit: **http://localhost:8000/docs** for interactive Swagger UI

---

## 9. Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'visuai'`

**Solution:**
```bash
# Make sure you're in the project root
cd visuai-research-agent

# Install in editable mode
pip install -e .

# Verify
python -c "import visuai; print(visuai.__version__)"
```

### Issue: `ImportError: cannot import name 'ResearchAgent'`

**Solution:**
```bash
# Check if src/visuai/__init__.py exports it
cat src/visuai/__init__.py

# Should contain: from .core.agent import ResearchAgent
```

### Issue: `API key not found`

**Solution:**
```bash
# Check environment variable
echo $VISUAI_LLM_API_KEY

# Or set it explicitly
export VISUAI_LLM_API_KEY="sk-your-key"

# Or pass to agent directly
agent = ResearchAgent(api_key="sk-your-key")
```

### Issue: `matplotlib backend error`

**Solution:**
```bash
# Install GUI backend
pip install PyQt5

# Or use non-interactive backend (already configured in code)
```

### Issue: GitHub Pages not showing

**Solution:**
1. Check that `pages/index.html` exists in the main branch
2. Go to Settings > Pages and verify the source branch
3. Wait 5 minutes for deployment
4. Clear browser cache and try again

---

## 10. Next Steps

### ✅ Immediate Actions

1. **Star the repo** on GitHub to show support
2. **Share on social media** — Twitter, LinkedIn, ResearchGate
3. **Write a blog post** about your experience using VisuAI
4. **Submit to conferences** — showcase as a research tool

### 🔮 Future Enhancements

- [ ] Add more chart types (3D plots, animated charts)
- [ ] Integrate with Google Colab
- [ ] Add multi-language support
- [ ] Create video tutorials
- [ ] Submit to PyPI for `pip install visuai`
- [ ] Add CI/CD badges and coverage reports
- [ ] Write academic paper about the tool

### 🤝 Community

- **Report issues:** [GitHub Issues](https://github.com/muhammadyasirimam/visuai-research-agent/issues)
- **Contribute:** See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Discuss:** Open a GitHub Discussion

---

## 📬 Contact

- **Email:** imammuhammadyasir@gmail.com
- **GitHub:** [@muhammadyasirimam](https://github.com/muhammadyasirimam)
- **Google Scholar:** [Profile](https://scholar.google.com/citations?user=b80oc1UAAAAJ)
- **ResearchGate:** [Profile](https://www.researchgate.net/profile/Muhammad-Yasir-Imam)
- **ORCID:** [0000-0002-7495-4179](https://orcid.org/0000-0002-7495-4179)
- **LinkedIn:** [muhammadyasirimam](https://linkedin.com/in/muhammadyasirimam)
- **MYI News World:** [myinewsworld.com](https://myinewsworld.com)

---

<div align="center">

**Built with ❤️ by Muhammad Yasir Imam**

*Gold Medalist | Award-Winning Researcher | Published Author*

*From a mud house in Pakistan to the world of open-source AI research tools 🌍*

</div>
