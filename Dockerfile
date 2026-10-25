# =====================================================================
# Dockerfile para Django + MySQL (modelo e-gerenteservicos)
# App: e-gerenteservicos  —  Django 5.2, MySQL via mysqlclient
# Settings: core.settings  |  WSGI: core.wsgi:application
# =====================================================================

# ---------------------- Estágio de BUILD (compila o mysqlclient) -----
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

# Dependências de compilação do mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --prefix=/install -r requirements.txt

# ---------------------- Estágio FINAL (leve) ------------------------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Runtime do mysqlclient + whitenoise
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

COPY . .

RUN mkdir -p media staticfiles

EXPOSE 8000

CMD ["sh", "-c", "\
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn core.wsgi:application \
      --bind 0.0.0.0:8000 \
      --workers ${GUNICORN_WORKERS:-2} \
      --timeout ${GUNICORN_TIMEOUT:-120} \
      --access-logfile - \
      --error-logfile -"]