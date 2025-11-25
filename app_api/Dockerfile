FROM python:3.11-slim

WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy API code
COPY app_api ./app_api

# Default DB inside Docker
ENV DB_URL=postgresql+psycopg2://postgres:postgres@db:5432/supply_chain

CMD ["uvicorn", "app_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
