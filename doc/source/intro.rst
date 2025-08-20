Description du projet
=====================

**OC-Lettings** est une application Django modulaire qui gère :
- les annonces de locations (app ``lettings``),
- les profils utilisateurs (app ``profiles``),
- la configuration et l’orchestration du site (app ``oc_lettings_site``).

Objectifs
---------
- Refactor d’une architecture monolithique vers une structure modulaire.
- Qualité de code (flake8), tests unitaires & d’intégration (>95%).
- CI/CD GitHub Actions (tests, build, release, Docker push).
- Conteneurisation Docker, exécution avec Gunicorn.
- Monitoring des erreurs avec Sentry.