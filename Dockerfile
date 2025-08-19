# syntax=docker/dockerfile:1
################################################################################
# Dockerfile — Application Django (oc_lettings_site)
################################################################################

########## STAGE 1 : BUILDER (installe les dépendances Python) #################
FROM python:3.11-slim AS builder

# Bonnes pratiques Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Dossier de travail
WORKDIR /app

# (Optionnel) Outils de compilation si certaines libs Python compilent des wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copier les dépendances en premier (cache Docker)
COPY requirements.txt ./

RUN python -m pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt


########## STAGE 2 : RUNTIME (image finale minimale) ###########################
FROM python:3.11-slim

# Variables par défaut (surchargées au runtime via --env-file ou -e)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=oc_lettings_site.settings \
    PORT=8000 \
    GUNICORN_WORKERS=3 \
    GUNICORN_TIMEOUT=60 \
    STATIC_ROOT=/app/staticfiles \
    MEDIA_ROOT=/app/media

# Créer un utilisateur non-root et préparer les répertoires
RUN adduser --disabled-password --gecos "" appuser \
 && mkdir -p /app /data ${STATIC_ROOT} ${MEDIA_ROOT} \
 && chown -R appuser:appuser /app /data ${STATIC_ROOT} ${MEDIA_ROOT}

# Passer à l’utilisateur non-root
USER appuser

# Dossier de travail
WORKDIR /app

# Copier les dépendances Python depuis builder
COPY --from=builder /install /usr/local

# Copier le code source (propriétaire = appuser)
COPY --chown=appuser:appuser . .

# Ajouter l'entrypoint (exécution en JSON pour éviter les warnings de CMD shell)
COPY --chown=appuser:appuser docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Exposer le port interne
EXPOSE 8000

# Démarrage via entrypoint (migrate -> collectstatic -> gunicorn)
ENTRYPOINT ["/app/entrypoint.sh"]