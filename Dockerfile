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
    PORT=8000

# Créer un utilisateur non-root et préparer les répertoires
RUN adduser --disabled-password --gecos "" appuser \
 && mkdir -p /app /data \
 && chown -R appuser:appuser /app /data

# Passer à l’utilisateur non-root
USER appuser

# Dossier de travail
WORKDIR /app

# Copier les dépendances Python depuis builder
COPY --from=builder /install /usr/local

# Copier le code source (propriétaire = appuser)
COPY --chown=appuser:appuser . .

# Exposer le port interne
EXPOSE 8000

# Commande de démarrage :
# - migrate : applique les migrations
# - collectstatic : rassemble les fichiers statiques
# - gunicorn : serveur WSGI
CMD sh -c "\
  python manage.py migrate --noinput && \
  python manage.py collectstatic --noinput && \
  gunicorn oc_lettings_site.wsgi:application \
    -b 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-3} \
    --timeout ${GUNICORN_TIMEOUT:-60}"