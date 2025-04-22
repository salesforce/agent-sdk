# Dockerfile for integration tests
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project
COPY . .

# Install Python dependencies using requirements.txt
COPY requirements.txt .
COPY requirements-test.txt .
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-test.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

# Create directories for test results and assets
RUN mkdir -p examples/test_results examples/assets

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "-u", "examples/integration_tests/run_integration_tests.py"]