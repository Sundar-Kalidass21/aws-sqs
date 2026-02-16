FROM python:3.11-slim

WORKDIR /app

COPY worker_service/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared code
COPY shared /app/shared

# Copy service code
COPY worker_service /app/worker_service

# Set python path
ENV PYTHONPATH=/app

CMD ["python", "-m", "worker_service.app.worker"]
