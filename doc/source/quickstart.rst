Guide de démarrage rapide
=========================

Lancer avec Docker (image publiée)
----------------------------------
.. code-block:: bash

   docker run -it --rm \
     -p 8080:8000 \
     -v oc_lettings_data:/data \
     docker.io/marctakoumba/oc-lettings-site:latest

Application accessible sur http://localhost:8080

Build & run local (Dockerfile du repo)
--------------------------------------
.. code-block:: bash

   docker build -t oc-lettings-site:local .
   docker run -it --rm -p 8080:8000 -v oc_lettings_data:/data oc-lettings-site:local

Makefile (si présent)
---------------------
.. code-block:: bash

   make release      # buildx + push Docker
   make run          # lance le conteneur local
   make stop         # stoppe le conteneur