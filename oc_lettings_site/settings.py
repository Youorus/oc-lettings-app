import os
from pathlib import Path
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# ===========================
# Sentry - Monitoring des erreurs
# ===========================
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),  # DSN récupéré dans .env
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,       # Performance monitoring (0.0 à 1.0)
    send_default_pii=True,        # Capture infos utilisateur (utile avec auth Django)
    environment=os.getenv("SENTRY_ENVIRONMENT", "development"),
)

# ===========================
# Paths
# ===========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ===========================
# Sécurité & Debug
# ===========================
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "insecure-key-change-me"  # valeur fallback en dev uniquement
)

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

"""
ALLOWED_HOSTS définit la liste des domaines que Django est autorisé à servir.
Il est chargé depuis .env et évite les attaques Host Header.
"""
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# ===========================
# Applications installées
# ===========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps locales
    "oc_lettings_site.apps.OCLettingsSiteConfig",
    "oc_lettings_site.lettings.apps.LettingsConfig",
    "oc_lettings_site.profiles.apps.ProfilesConfig",
]

# ===========================
# Middlewares
# ===========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "oc_lettings_site.urls"

# ===========================
# Templates
# ===========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "oc_lettings_site.wsgi.application"

# ===========================
# Base de données
# ===========================
"""
Par défaut, SQLite est utilisé.
⚠️ En production, préfère PostgreSQL ou MySQL pour la scalabilité.
"""
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("DB_PATH", str(BASE_DIR / "oc-lettings-site.sqlite3")),
    },
    # Ancienne base éventuelle (à retirer si inutile)
    "v2": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "v2.sqlite3"),
    },
}

# ===========================
# Validation des mots de passe
# ===========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ===========================
# Internationalisation
# ===========================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ===========================
# Fichiers statiques & médias
# ===========================
STATIC_URL = "/static/"
STATIC_ROOT = os.getenv("STATIC_ROOT", str(BASE_DIR / "staticfiles"))
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.getenv("MEDIA_ROOT", str(BASE_DIR / "media"))