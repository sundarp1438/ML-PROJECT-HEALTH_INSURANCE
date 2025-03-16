FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for MLflow
ENV MLFLOW_TRACKING_URI=http://127.0.0.1:5000

# Expose API port
EXPOSE 8000

# Run FastAPI server
CMD ["uvicorn", "fastapi_service:app", "--host", "0.0.0.0", "--port", "8000"]
