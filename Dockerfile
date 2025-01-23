# Use the official Python image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Install necessary packages (add more if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python development dependencies
RUN pip install --upgrade pip

# Copy requirements if available
COPY requirements.txt ./
RUN pip install -r requirements.txt || true

# Default entry point
CMD ["bash"]

