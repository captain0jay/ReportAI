# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Default command is overridden by docker-compose
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}