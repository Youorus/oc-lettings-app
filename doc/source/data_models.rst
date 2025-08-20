Structure de la base de données et modèles
==========================================

Vue d'ensemble
--------------
La base s’appuie sur Django ORM. Par défaut, SQLite est utilisée en local, et Postgres est recommandé en production.

Modèles principaux
------------------

App ``profiles``
~~~~~~~~~~~~~~~~
- **Profile**
  - ``user`` (OneToOne vers ``auth.User``)
  - ``favorite_city`` (CharField, nullable)

App ``lettings``
~~~~~~~~~~~~~~~~
- **Address**
  - ``number`` (PositiveIntegerField)
  - ``street`` (CharField)
  - ``city`` (CharField)
  - ``state`` (CharField)
  - ``zip_code`` (PositiveIntegerField)
  - ``country_iso_code`` (CharField, optionnel)

- **Letting**
  - ``title`` (CharField)
  - ``address`` (ForeignKey vers ``Address``)
  - (ajouter vos champs spécifiques si besoin)

Migrations & schéma
-------------------
.. code-block:: bash

   python manage.py makemigrations
   python manage.py migrate

Schéma (indicatif)
------------------
.. code-block:: text

   Profile (1–1)──User
   Letting (*–1)──Address