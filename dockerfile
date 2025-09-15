# Wine Quality Prediction System - Docker Configuration
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONPATH=/app
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs static/css static/js templates artifacts/model_trainer
RUN chmod -R 755 /app

RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose Render's dynamic PORT (documentational only)
EXPOSE ${PORT}

# Health check (must match dynamic PORT)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# Run with Gunicorn, bind to dynamic PORT
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 4 --threads 2 --timeout 120 app:app"]
