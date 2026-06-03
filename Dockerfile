# Use a lightweight and high-performance Python 3.12 image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=True
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# --- Critical modification: changed from gunicorn to uvicorn ---
# ADK/FastAPI must be started using uvicorn
# Use sh -c to ensure the $PORT environment variable is parsed
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
#CMD ["python", "main.py"]