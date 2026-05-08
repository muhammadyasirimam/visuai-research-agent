FROM python:3.11-slim

LABEL maintainer="Muhammad Yasir Imam <imammuhammadyasir@gmail.com>"
LABEL description="VisuAI Research Agent - AI-Powered Research Data Visualization"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .
RUN pip install -e .

# Create output directory
RUN mkdir -p /app/visuai_output

# Expose ports
EXPOSE 8501 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import visuai; print('OK')" || exit 1

# Default command
CMD ["visuai", "web", "--port", "8501", "--host", "0.0.0.0"]
