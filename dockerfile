# Wine Quality Prediction System - Docker Configuration
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Environment variables
ENV PYTHONPATH=/app \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p logs static/css static/js templates artifacts/model_trainer

# Set permissions
RUN chmod -R 755 /app

# Add non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port (Render ignores this, but it's good documentation)
EXPOSE 8080

# Health check (make sure /health exists in app.py ✅)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8080}/health || exit 1

# Run Gunicorn with dynamic PORT
ENTRYPOINT ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 4 --threads 2 --timeout 120 app:app"]
