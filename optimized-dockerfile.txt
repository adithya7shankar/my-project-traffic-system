# Use an official Python runtime as a parent image
FROM ubuntu:latest 

# Set environment variables
ENV TZ=US/Pacific \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Set arguments
ARG PYVER="3.9"
ARG GITUN="Adithya Shankar"
ARG GITEMAIL="adithya7shankar@gmail.com"

# Update and install dependencies in one layer to reduce image size
RUN apt-get update && apt-get install -y \
    software-properties-common \
    git-all \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y python${PYVER} \
    python3-pip \
    python3-cryptography \
    python3-matplotlib \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configure Git
RUN git config --global user.name "$GITUN" && \
    git config --global user.email "$GITEMAIL" && \
    git config --global init.defaultBranch main

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
CMD ["python3", "main.py"]
