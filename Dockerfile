# Use Python 3.11
FROM python:3.11-slim

# Install system dependencies for Playwright browsers
RUN apt-get update && apt-get install -y     wget     gnupg     && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY main.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (Essential for the Scout Agent)
RUN playwright install --with-deps chromium

# Expose the port Railway gives us
ENV PORT=8000
EXPOSE 8000

# Run the server
CMD ["python", "main.py"]
