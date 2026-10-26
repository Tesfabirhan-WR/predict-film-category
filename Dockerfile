FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TF_CPP_MIN_LOG_LEVEL=2

WORKDIR /app

# Dependencies first: this layer is cached until requirements-api.txt changes
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt \
 && python -m spacy download en_core_web_sm

# Application code and trained model (notebook/model from the notebook stage 8)
COPY src/ ./src/
COPY model/ ./model/

# Commit id shown by /health (placed late so a new commit does not rebuild the layers above)
ARG GIT_COMMIT=unknown
ENV GIT_COMMIT=${GIT_COMMIT} \
    MODEL_DIR=/app/model

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=90s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
