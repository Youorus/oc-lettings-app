# OC‑Lettings — README professionnel

> Application Django modulaire (\`lettings\`, \`profiles\`, \`oc\_lettings\_site\`) avec tests, CI/CD GitHub Actions, conteneurisation Docker et déploiement sur Render.

---

## 🧭 Sommaire

* [Aperçu](#aperçu)
* [Architecture & arborescence](#architecture--arborescence)
* [Stack technique](#stack-technique)
* [Installation & démarrage rapide](#installation--démarrage-rapide)
* [Configuration (ENV)](#configuration-env)
* [Base de données & modèles](#base-de-données--modèles)
* [Lancer l’application](#lancer-lapplication)
* [Tests, qualité & couverture](#tests-qualité--couverture)
* [Documentation (Sphinx & Read the Docs)](#documentation-sphinx--read-the-docs)
* [CI/CD GitHub Actions](#cicd-github-actions)
* [Releases & images Docker](#releases--images-docker)
* [Déploiement sur Render (image Docker)](#déploiement-sur-render-image-docker)
* [Exploitation & commandes utiles](#exploitation--commandes-utiles)
* [Dépannage](#dépannage)

---

## Aperçu

OC‑Lettings est une application Django refactorée d’une architecture monolithique vers **trois apps** découpées :

* **\`lettings\`** : gestion des annonces/locations
* **\`profiles\`** : gestion des profils utilisateurs
* **\`oc\_lettings\_site\`** : configuration globale (settings/urls/wsgi)

Objectifs clés : qualité de code (flake8), **tests unitaires & d’intégration (>95 %)**, conteneurisation, pipeline CI/CD, monitoring Sentry et **déploiement automatisé**.

---

## Architecture & arborescence

```
.
├─ oc_lettings_site/
│  ├─ __init__.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  ├─ views.py
│  ├─ tests/                      # tests projet (optionnel)
│  ├─ lettings/
│  │  ├─ __init__.py
│  │  ├─ admin.py
│  │  ├─ apps.py
│  │  ├─ migrations/
│  │  ├─ models.py
│  │  ├─ urls.py
│  │  └─ views.py
│  └─ profiles/
│     ├─ __init__.py
│     ├─ admin.py
│     ├─ apps.py
│     ├─ migrations/
│     ├─ models.py
│     ├─ urls.py
│     └─ views.py
├─ templates/
│  ├─ base.html
│  ├─ 404.html
│  ├─ 500.html
│  ├─ oc_lettings_site/
│  │  └─ index.html
│  ├─ lettings/
│  │  ├─ index.html
│  │  └─ letting.html
│  └─ profiles/
│     └─ ...
├─ static/                        # tes fichiers statiques source
├─ data/                          # base SQLite (ex: /data/oc-lettings-site.sqlite3)
├─ doc/
│  ├─ source/
│  │  ├─ conf.py
│  │  ├─ index.rst
│  │  ├─ intro.rst
│  │  ├─ installation.rst
│  │  ├─ quickstart.rst
│  │  ├─ tech_stack.rst
│  │  ├─ data_models.rst
│  │  ├─ api.rst
│  │  └─ deploy.rst
│  └─ build/
├─ .readthedocs.yaml
├─ Dockerfile
├─ Makefile
├─ manage.py
├─ requirements.txt
├─ pytest.ini
├─ .gitignore
└─ README.md
```

---

## Stack technique

* **Django** (Python 3.11)
* **Gunicorn** (WSGI)
* **Docker** (multi‑stage, image finale Python slim)
* **GitHub Actions** (tests → build → release → push Docker)
* **Render** (hébergement Web Service à partir d’une image Docker Hub)
* **pytest**, **flake8**, **coverage**
* **Sentry** (journalisation des erreurs)
* **Sphinx** + **Read the Docs** (documentation)

---

## Installation & démarrage rapide

### Option A — Docker (le plus simple)

```bash
# depuis Docker Hub (port hôte 8080 → conteneur 8000)
docker run -it --rm \
  -p 8080:8000 \
  -v oc_lettings_data:/data \
  docker.io/marctakoumba/oc-lettings-site:latest
```

Ouvre : [http://localhost:8080](http://localhost:8080)

### Option B — Local (venv)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=oc_lettings_site.settings
python manage.py migrate
python manage.py runserver
```

---

## Configuration (ENV)

> ⚠️ **Ne commitez jamais** votre `.env`. Conservez un `.env.example`.

Variables usuelles :

```ini
# Django
SECRET_KEY=change_me
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,mon-service.onrender.com
CSRF_TRUSTED_ORIGINS=https://mon-service.onrender.com

# Base de données
# Par défaut SQLite
SQLITE_PATH=/data/oc-lettings-site.sqlite3
# ou Postgres
# DATABASE_URL=postgres://user:pass@host:5432/dbname

# Gunicorn / app
PORT=8000
GUNICORN_WORKERS=3
GUNICORN_TIMEOUT=60

# Sentry (optionnel)
# SENTRY_DSN=...
```

Django peut être configuré pour utiliser automatiquement `DATABASE_URL` (via `dj-database-url`) avec repli **SQLite** par défaut.

---

## Base de données & modèles

* **SQLite** en local (fichier persistant monté sur `/data`).
* **PostgreSQL** recommandé en production (`DATABASE_URL`).

Modèles principaux (extrait) :

* `profiles.Profile(user OneToOne auth.User, favorite_city)`
* `lettings.Address(number, street, city, state, zip_code, country_iso_code)`
* `lettings.Letting(title, address → Address)`

Migrations :

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Lancer l’application

### Via Makefile (automatisation sans docker‑compose)

```bash
make run         # lance l’image locale/Docker Hub (port 8080)
make stop        # stoppe et supprime le conteneur
make release     # buildx multi‑arch + push :latest et :vX.Y
make pull        # pull l’image taggée vVERSION puis run
```

### Commandes manuelles Docker

```bash
# Build + push multi‑arch (exemple sans Makefile)
docker buildx build . \
  --platform linux/amd64,linux/arm64 \
  -t marctakoumba/oc-lettings-site:latest \
  -t marctakoumba/oc-lettings-site:v1.2 \
  --push
```

---

## Tests, qualité & couverture

```bash
flake8
pytest -q --cov=.
coverage html  # rapport HTML dans htmlcov/
```

Dans la CI, on compile d’abord les fichiers Python (détection d’erreurs de syntaxe), puis `manage.py check`, puis `pytest`.

---

## Documentation (Sphinx & Read the Docs)

* Sources dans **`doc/source/`** (point d’entrée : `index.rst`).
* Build local :

```bash
make -C doc html
# ouvre doc/build/html/index.html
```

* Publication automatique : fichier **`.readthedocs.yaml`** (à la racine) + `doc/requirements.txt` → Read the Docs construit et héberge la doc.

---

## CI/CD GitHub Actions

Deux workflows recommandés :

1. **CI (develop)** — se déclenche sur **Pull Request vers `develop`**

   * Installe les deps
   * `python -m py_compile` (syntaxe)
   * `python manage.py check`
   * `pytest`

2. **Main Pipeline (tests → build → release → docker)** — se déclenche sur **push vers `main`**, **uniquement si** le commit de `main` **inclut** `origin/develop` (merge local ou via PR). Chaîne :

   * **tests** → mêmes vérifications que ci‑dessus
   * **build** Docker (validation **sans push**)
   * **release** → calcule `vX.Y`, **crée le tag** et la **GitHub Release**
   * **docker** → build multi‑arch et **push** vers Docker Hub (`:vX.Y` + `:latest`)

Secrets requis (Settings → Secrets and variables → Actions) :

* `DOCKERHUB_USERNAME`
* `DOCKERHUB_TOKEN` (Access Token Docker Hub)

---

## Releases & images Docker

* Versionning automatisé : incrément **minor** (`v1.0 → v1.1 → … → v1.10 → v2.0`).
* À chaque release :

  * tag Git **`vX.Y`** + **GitHub Release**
  * build/push images Docker :

    * `docker.io/marctakoumba/oc-lettings-site:vX.Y`
    * `docker.io/marctakoumba/oc-lettings-site:latest`

Commandes manuelles (alternative) :

```bash
git checkout main && git pull
# (optionnel) merge develop → main
# git merge --no-ff develop && git push

git tag v1.4 -m "release v1.4"
git push origin v1.4
# (si un workflow "on tag" est configuré, il se déclenchera ici)
```

---

## Déploiement sur Render (image Docker)

> **Scénario supporté** : Render consomme l’image Docker publiée sur Docker Hub.

### Création du service

1. **New → Web Service** → *Deploy an existing image*
2. **Image URL** : `docker.io/marctakoumba/oc-lettings-site:latest`
3. **Port interne** : `8000`
4. **Start command** : **laisser vide** (l’ENTRYPOINT exécute `migrate`, `collectstatic`, puis `gunicorn`)
5. **Variables d’environnement** (Settings → Environment) :

```ini
DJANGO_SETTINGS_MODULE=oc_lettings_site.settings
SECRET_KEY=<valeur>
DEBUG=False
PORT=8000
ALLOWED_HOSTS=mon-service.onrender.com,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://mon-service.onrender.com
# SQLite (éphémère)
SQLITE_PATH=/data/oc-lettings-site.sqlite3
# ou Postgres (persistance)
# DATABASE_URL=postgres://user:pass@host:5432/dbname
```

> **Important** : pour éviter les erreurs **400 Bad Request**, ajoute bien le domaine Render à `ALLOWED_HOSTS` et `CSRF_TRUSTED_ORIGINS`.

### Déploiements automatiques (nouvelle image)

* Render ne suit pas toujours `latest` automatiquement. Utilisez le **Deploy Hook** (Settings → Deploy → *Deploy Hook*).
* Appelez‑le **après** chaque push d’image :

```bash
# URL fournie par Render (garde‑la secrète)
curl -X POST "https://api.render.com/deploy/srv-XXXXXXXX?key=YYYYYYYY"
```

> Astuce : ajoute une cible `make deploy` qui appelle ce hook juste après `make release`.

### Notes persistance

* **SQLite** dans le conteneur free = **éphémère**. Pour conserver les données, passez à **Postgres** et définissez `DATABASE_URL`.

---

## Exploitation & commandes utiles

Migrations & statiques :

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

Sentry (test) : exposez une route de test (ex. `/sentry-debug/`) qui déclenche une exception volontaire pour valider la remontée des erreurs.

Docker local :

```bash
docker ps
docker logs -f oc_lettings_web
```

---

## Dépannage

* **400 Bad Request sur Render** : vérifier `ALLOWED_HOSTS` et `CSRF_TRUSTED_ORIGINS` (https), `SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https")`, `USE_X_FORWARDED_HOST=True`.
* **Avertissement « Your models have changes… »** : exécuter `manage.py makemigrations`, commiter, redéployer.
* **La CI ne part pas** :

  * le workflow doit être présent sur **`main`**;
  * pour le mode *push + gate*, il faut **merger `develop` dans `main`** puis pousser ;
  * secrets Docker Hub manquants.

---

> **Licence** : à compléter (MIT/GPL/Apache…).

---

### Badges (exemple)

```md
![CI](https://github.com/<owner>/<repo>/actions/workflows/main-pipeline.yml/badge.svg)
![Docs](https://readthedocs.org/projects/<slug>/badge/?version=latest)
![Docker Pulls](https://img.shields.io/docker/pulls/marctakoumba/oc-lettings-site)
```

---

### Auteurs

* Marc Takoumba 
