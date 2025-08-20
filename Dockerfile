# syntax=docker/dockerfile:1
################################################################################
# Dockerfile — Application Django (oc_lettings_site) + SQLite seed
################################################################################

########## STAGE 1 : BUILDER (dépendances Python) ##############################
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Outils build (si wheels natives)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

########## STAGE 2 : RUNTIME (image finale) ###################################
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=oc_lettings_site.settings \
    PORT=8000

# Utilisateur non-root + répertoires
RUN adduser --disabled-password --gecos "" appuser \
 && mkdir -p /app /data /seed /docker \
 && chown -R appuser:appuser /app /data /seed /docker

USER appuser
WORKDIR /app

# Dépendances du builder
COPY --from=builder /install /usr/local

# Code source
COPY --chown=appuser:appuser . .

# DB locale (seed) -> /seed/db.sqlite3
# Ton fichier est: data/oc-lettings-site.sqlite3
COPY --chown=appuser:appuser data/oc-lettings-site.sqlite3 /seed/db.sqlite3

# Entrypoint
COPY --chown=appuser:appuser docker/entrypoint.sh /docker/entrypoint.sh
RUN chmod +x /docker/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/docker/entrypoint.sh"]