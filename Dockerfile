# ---------- Base ----------
FROM python:3.10-slim

# ---------- Env ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------- Workdir ----------
WORKDIR /app

# ---------- System deps (minimal) ----------
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---------- Install Python deps (cache optimized) ----------
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---------- Copy only code ----------
COPY . .

# ---------- Streamlit config (optional but clean) ----------
RUN mkdir -p ~/.streamlit && \
    echo "[server]\n\
headless = true\n\
port = 8501\n\
enableCORS = false\n\
" > ~/.streamlit/config.toml

# ---------- Expose ----------
EXPOSE 8501

# ---------- Run ----------
CMD ["streamlit", "run", "app.py"]