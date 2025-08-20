Installation
============

Prérequis
---------
- Python 3.11
- pip
- (optionnel) virtualenv
- (optionnel) Docker

Installation locale (sans Docker)
---------------------------------
.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate     # Windows: .venv\\Scripts\\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   export DJANGO_SETTINGS_MODULE=oc_lettings_site.settings
   python manage.py migrate
   python manage.py runserver

Variables d'environnement (exemples)
------------------------------------
.. code-block:: ini

   SECRET_KEY=change_me
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   CSRF_TRUSTED_ORIGINS=https://example.com
   # SQLite par défaut, sinon:
   # DATABASE_URL=postgres://user:pass@host:5432/dbname
   PORT=8000
   GUNICORN_WORKERS=3
   GUNICORN_TIMEOUT=60