# Use a slim Python 3.9 image
FROM python:3.9-slim

# Prevent Python from writing .pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory in the container
WORKDIR /app

# Install system-level dependencies (required for moviepy and faster-whisper)
RUN apt-get update && apt-get install -y --no-install-recommends 
    ffmpeg 
    build-essential 
    && apt-get clean 
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Ensure instance directory exists for SQLite
RUN mkdir -p instance

# Expose port
EXPOSE 5000

# Start the application
CMD ["python", "run_app.py"]
