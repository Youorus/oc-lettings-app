SHELL := /bin/bash
# Charge .env si présent
ifneq (,$(wildcard ./.env))
include .env
export
endif

# --------- Variables principales ----------
VERSION_FILE     ?= VERSION
CUR_VERSION := $(shell cat $(VERSION_FILE))
NEXT_VERSION := $(shell awk -F. '{maj=$$1; min=$$2; if (min=="") min=0; min+=1; if (min>10){maj+=1; min=0} printf "%d.%d", maj, min}' $(VERSION_FILE))
IMAGE_REPO       := $(DOCKERHUB_USER)/$(DOCKERHUB_IMAGE)
PLATFORMS        := linux/amd64,linux/arm64
GIT_SHA          := $(shell git rev-parse --short HEAD 2>/dev/null || echo "nogit")
AUTO_GIT_TAG    ?= 0   # mets 1 si tu veux commit+tag git auto après release
CONTAINER_NAME   := oc_lettings_web

# --------- Aide ----------
.PHONY: help
help:
	@echo "Cibles Make pro:"
	@echo "  login        - docker login (Docker Hub)"
	@echo "  init-builder - crée/init buildx multi-arch"
	@echo "  release      - calcule la prochaine version, build multi-arch, push; MAJ VERSION (v$(CUR_VERSION) -> v$(NEXT_VERSION))"
	@echo "  run          - lance le conteneur local avec la version courante (v$(CUR_VERSION))"
	@echo "  stop         - arrête + supprime le conteneur"
	@echo "  release-run  - release puis lance la nouvelle version"
	@echo "  pull         - pull l'image v$(CUR_VERSION) depuis Docker Hub"
	@echo "  down         - alias de stop"

# --------- Buildx / Login ----------
.PHONY: init-builder
init-builder:
	@if ! docker buildx inspect multiarch >/dev/null 2>&1; then \
	  docker buildx create --name multiarch --use; \
	else \
	  docker buildx use multiarch; \
	fi
	@docker buildx inspect --bootstrap

.PHONY: login
login:
	@docker login -u "$(DOCKERHUB_USER)"

# --------- Release (auto-versioning) ----------
.PHONY: release
release: init-builder
	@echo "🚀 Release: $(IMAGE_REPO):v$(NEXT_VERSION) (depuis v$(CUR_VERSION))"
	@echo "🔨 Build + Push multi-arch vers Docker Hub..."
	docker buildx build . \
		--platform $(PLATFORMS) \
		--tag $(IMAGE_REPO):v$(NEXT_VERSION) \
		--tag $(IMAGE_REPO):latest \
		--label org.opencontainers.image.version=v$(NEXT_VERSION) \
		--label org.opencontainers.image.revision=$(GIT_SHA) \
		--provenance=false \
		--sbom=false \
		--push
	@echo "$(NEXT_VERSION)" > $(VERSION_FILE)
	@echo "✅ VERSION mise à jour -> $(NEXT_VERSION)"
ifneq ($(AUTO_GIT_TAG),0)
	@if git rev-parse --git-dir >/dev/null 2>&1; then \
	  if git diff --quiet && git diff --cached --quiet; then \
	    git add $(VERSION_FILE) && \
	    git commit -m "chore: release v$(NEXT_VERSION)" && \
	    git tag "v$(NEXT_VERSION)" && \
	    echo "✅ Git tag v$(NEXT_VERSION) créé"; \
	  else \
	    echo "⚠️  Repo non clean : pas de commit/tag auto."; \
	  fi; \
	else \
	  echo "ℹ️  Pas de repo git détecté, skip tag."; \
	fi
endif

# --------- Déploiement local (sans Compose) ----------
.PHONY: run
run:
	@echo "⬆️  Run local v$(CUR_VERSION)"
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p 8080:8000 \
		--env-file .env \
		-v oc_lettings_data:/data \
		$(IMAGE_REPO):v$(CUR_VERSION)

.PHONY: stop
stop:
	@echo "🛑 Stop + remove container $(CONTAINER_NAME)"
	-docker stop $(CONTAINER_NAME) || true
	-docker rm $(CONTAINER_NAME) || true

.PHONY: release-run
release-run: release stop run

.PHONY: pull
pull:
	@echo "⬇️  Pull image v$(CUR_VERSION)"
	docker pull $(IMAGE_REPO):v$(CUR_VERSION)

.PHONY: down
down: stop