# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install OS packages required to build SciPy (and similar compiled libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gfortran \
    gcc \
    g++ \
    libopenblas-dev \
    liblapack-dev \
    pkg-config \
    cmake \
    git \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage docker cache
COPY requirements.txt .

# Upgrade pip and install numpy first to avoid ABI issues
RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install numpy==2.0.2

# Install remaining Python deps
RUN python -m pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port and start the app (change app:app if needed)
ENV PORT=10000
EXPOSE 10000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000", "--workers", "2"]
