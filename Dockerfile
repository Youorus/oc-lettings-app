# syntax=docker/dockerfile:1
################################################################################
# Dockerfile — Application Django (oc_lettings_site)
#
# Points clés :
# - Build multi-étapes : on installe les dépendances dans une étape "builder"
#   puis on ne copie que le strict nécessaire dans l'image finale (plus légère).
# - Variables d'environnement pour la config (DEBUG, SECRET_KEY, ALLOWED_HOSTS,
#   SENTRY_DSN, DB_PATH, PORT, etc.) : elles sont injectées au runtime.
# - Démarrage sain : migrate -> collectstatic -> Gunicorn.
# - Utilisateur non-root pour de meilleures pratiques de sécurité.
################################################################################


########## STAGE 1 : BUILDER (installe les dépendances Python) #################
FROM python:3.11-slim AS builder

# Bonnes pratiques Python
ENV PYTHONDONTWRITEBYTECODE=1 \        # ne pas créer de .pyc
    PYTHONUNBUFFERED=1 \               # logs non-bufferisés (stdout)
    PIP_NO_CACHE_DIR=1                 # ne pas garder le cache pip (image + légère)

# Dossier de travail
WORKDIR /app

# (Optionnel) Outils de compilation si certaines libs Python compilent des wheels
# - build-essential : gcc, make, etc.
# Si tu n'en as pas besoin, tu peux supprimer ce RUN pour réduire encore l'image.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# On copie uniquement le fichier des dépendances pour profiter du cache Docker :
# tant que requirements.txt ne change pas, cette couche reste en cache.
COPY requirements.txt ./

# On installe les dépendances dans /install (chemin "propre" qu'on copiera ensuite)
RUN python -m pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt
# Note : assure-toi que gunicorn (et éventuellement whitenoise, sentry-sdk) figurent dans requirements.txt


########## STAGE 2 : RUNTIME (image finale minimale) ###########################
FROM python:3.11-slim

# Valeurs par défaut "raisonnables", surchargées par -e / --env-file au runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=oc_lettings_site.settings \
    PORT=8000

# Créer un utilisateur non-root (sécurité) et basculer dessus
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Dossier de travail
WORKDIR /app

# Copier les dépendances Python installées à l'étape builder
# - On met le contenu dans /usr/local (chemin standard où Python cherchera les libs)
COPY --from=builder /install /usr/local

# Copier le code de l’application (propriétaire = appuser)
COPY --chown=appuser:appuser . .

# Exposer le port interne sur lequel Gunicorn écoute (documentaire)
EXPOSE 8000

# (Optionnel) Healthcheck basique : vérifie que le port est ouvert.
# Tu peux le retirer ou adapter à un endpoint /health si tu en exposes un.
# HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
#   CMD python -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('127.0.0.1', int('${PORT:-8000}'))); s.close()" || exit 1

# Commande de démarrage :
# 1) Applique les migrations : assure le schéma DB (SQLite ou autre)
# 2) collectstatic : rassemble les fichiers statiques vers STATIC_ROOT
# 3) lance Gunicorn : serveur WSGI de prod
#
# Variables surchargables :
# - PORT                : port interne d’écoute
# - GUNICORN_WORKERS    : nb. de workers (CPU-bound vs I/O-bound à ajuster)
# - GUNICORN_TIMEOUT    : timeout de requête (secondes)
CMD sh -c "\
  python manage.py migrate --noinput && \
  python manage.py collectstatic --noinput && \
  gunicorn oc_lettings_site.wsgi:application \
    -b 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-3} \
    --timeout ${GUNICORN_TIMEOUT:-60}"