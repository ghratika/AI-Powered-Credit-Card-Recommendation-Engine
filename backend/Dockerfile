# Railway backend image: FastAPI API + data files
# Build context: backend/ directory
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CARDS_DATA_PATH=/app/data/processed/cards.json \
    AA_DATA_PATH=/app/data/synthetic/aa_transactions.json

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY data/ ./data/

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
