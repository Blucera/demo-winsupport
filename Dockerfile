FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your already-built app (with .so files)
COPY . .

CMD ["streamlit", "run", "Chat.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false"]
