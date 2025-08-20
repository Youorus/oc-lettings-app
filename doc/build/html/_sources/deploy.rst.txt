Procédures de déploiement et gestion
====================================

CI/CD (GitHub Actions)
----------------------
- Pipeline sur merge ``develop → main`` :
  1) tests (pytest, checks Django)
  2) build Docker (validation)
  3) release (tag vX.Y)
  4) build & push Docker Hub (``latest`` et ``vX.Y``)

Secrets requis (Actions)
------------------------
- ``DOCKERHUB_USERNAME``, ``DOCKERHUB_TOKEN``

Déploiement Render (image Docker)
---------------------------------
1. Service Web → **Docker Image**
2. Image: ``docker.io/marctakoumba/oc-lettings-site:latest``
3. Port interne: **8000**
4. Variables d’env:
   - ``DJANGO_SETTINGS_MODULE=oc_lettings_site.settings``
   - ``SECRET_KEY=<value>``
   - ``ALLOWED_HOSTS=<ton-service>.onrender.com,localhost,127.0.0.1``
   - ``CSRF_TRUSTED_ORIGINS=https://<ton-service>.onrender.com``
   - (SQLite) ``SQLITE_PATH=/data/oc-lettings-site.sqlite3`` ou (Postgres) ``DATABASE_URL=postgres://...``
5. Start command: vide (ENTRYPOINT gère migrate, collectstatic, gunicorn)

Déploiement Koyeb (image Docker)
--------------------------------
- Service depuis image Container
- Port exposé: **8000**
- Env: identiques à Render
- Persistance: utiliser Postgres gratuite et ``DATABASE_URL``

Sauvegarde & persistance
------------------------
- SQLite avec volume: ``-v oc_lettings_data:/data``
- Production: préférer **Postgres** + ``DATABASE_URL``

Opérations courantes
--------------------
.. code-block:: bash

   # Migrations
   python manage.py makemigrations
   python manage.py migrate

   # Collecte des fichiers statiques
   python manage.py collectstatic --noinput

   # Lancement local
   python manage.py runserver