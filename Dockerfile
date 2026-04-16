FROM python:3.10-slim

WORKDIR /app

# -------------------------------
# Install system dependencies (IMPORTANT for OpenCV + OCR)
# -------------------------------
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libxcb1 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Copy requirements first (cache optimization)
# -------------------------------

COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install \
    --no-cache-dir \
    --default-timeout=200 \
    --retries 10 \
    --resume-retries 10 \
    -r requirements.txt

# -------------------------------
# Copy full project
# -------------------------------
COPY . .

# -------------------------------
# Run app
# -------------------------------

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

