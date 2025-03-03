# Use an official Python slim image as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=US/Pacific

# Set the working directory in the container
WORKDIR /app

# Create a non-root user to run the application
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && mkdir -p /app/output /app/logs \
    && chown -R appuser:appuser /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create output and logs directories and set permissions
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Make port 80 available to the world outside this container
EXPOSE 80

# Create volumes for persistent data
VOLUME ["/app/output", "/app/logs"]

# Run main.py when the container launches
CMD ["python", "main.py"]
