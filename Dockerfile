FROM python:3.11-slim

# ── Metadata ────────────────────────────────────────────────────────────────
LABEL maintainer="Team NexAura <nexaura002@gmail.com>"
LABEL description="Drishti Chakra — Autonomous Industrial R&D Engine | AMD Developer Hackathon 2026"
LABEL version="1.0.0"

WORKDIR /app

# ── System dependencies (curl needed for HEALTHCHECK) ────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── Python dependencies ──────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Application source (including static/ splash video) ─────────────────────
COPY . .

# ── Streamlit config ─────────────────────────────────────────────────────────
EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", \
            "--server.port=8501", \
            "--server.address=0.0.0.0", \
            "--server.enableStaticServing=true", \
            "--server.headless=true"]
