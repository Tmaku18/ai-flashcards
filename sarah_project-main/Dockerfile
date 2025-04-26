FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY app/ ./app/
COPY run.py .

# Copy frontend static files
RUN mkdir -p /app/frontend
COPY frontend/index.html /app/frontend/
COPY frontend/dashboard.html /app/frontend/
COPY frontend/public /app/frontend/public

# Create uploads directory
RUN mkdir -p uploads

# Set environment variables
ENV PORT=8080
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8080

# Start the application
CMD ["python", "run.py"]
