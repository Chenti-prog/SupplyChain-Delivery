FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy dashboard code
COPY app_dashboard ./app_dashboard

ENV API_BASE_URL=http://api:8000

CMD ["streamlit", "run", "app_dashboard/dashboard.py","--server.port=8501", "--server.address=0.0.0.0"]
