FROM python:3.11-slim

WORKDIR /app

COPY api_service/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared code
COPY shared /app/shared

# Copy service code
COPY api_service /app/api_service

# Set python path
ENV PYTHONPATH=/app

CMD ["uvicorn", "api_service.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
