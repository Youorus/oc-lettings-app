Interfaces de programmation (API)
=================================

Endpoints publics (exemples)
----------------------------
- ``GET /`` : page d’accueil
- ``GET /lettings/`` : liste des locations
- ``GET /lettings/<id>/`` : détail d’une location
- ``GET /profiles/`` : liste des profils
- ``GET /profiles/<username>/`` : détail d’un profil

Si vous exposez une API REST (DRF)
----------------------------------
- ``GET /api/lettings/`` : liste JSON
- ``GET /api/lettings/<id>/`` : détail JSON
- ``GET /api/profiles/``
- ``GET /api/profiles/<id>/``

Authentification
----------------
- Par défaut, endpoints publics en lecture.
- Pour des opérations d’écriture, activez l’auth Django/DRF.

Format & codes de statut
------------------------
- **200** OK, **201** Created, **400** Bad Request, **404** Not Found, **500** Server Error