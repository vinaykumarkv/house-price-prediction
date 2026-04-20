# Use official Python slim image
FROM python:3.11-slim

# Install system dependencies first (critical for LightGBM)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgomp1 && \
    rm -rf /var/lib/apt/lists/*  # Clean up to keep image small

# Set working directory
WORKDIR /app

# Copy and install Python dependencies (caching layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

RUN chmod +x start.sh
# Expose the port Hugging Face expects (Streamlit on 7860)
EXPOSE 7860

# Use our start script to run both services
CMD ["bash", "start.sh"]