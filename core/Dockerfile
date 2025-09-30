# ---------- Build Stage ----------
FROM python:3.10-slim as builder

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir cython -r requirements.txt

COPY . .

# Compile all .py files in core/ into .so
RUN cythonize -i core/*.py

# Remove raw source .py files
RUN rm -f core/*.py

# ---------- Final Stage ----------
FROM python:3.10-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

# Copy compiled app only (no build deps)
COPY --from=builder /app /app

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
