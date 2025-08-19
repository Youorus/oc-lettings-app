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

# --------- Aide ----------
.PHONY: help
help:
	@echo "Cibles Make pro:"
	@echo "  login           - docker login (Docker Hub)"
	@echo "  init-builder    - crée/init buildx multi-arch"
	@echo "  release         - calcule la prochaine version, build multi-arch, push; MAJ VERSION (v$(CUR_VERSION) -> v$(NEXT_VERSION))"
	@echo "  up              - lance compose avec la version COURANTE (v$(CUR_VERSION))"
	@echo "  release-up      - release puis déploiement compose de la NOUVELLE version (v$(NEXT_VERSION))"
	@echo "  env-sync        - recopie la version courante dans .env (VERSION=...)"
	@echo "  pull            - pull l'image v$(CUR_VERSION) puis up"
	@echo "  down            - arrête compose"

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

# --------- Sync .env avec VERSION ----------
.PHONY: env-sync
env-sync:
	@awk 'BEGIN{IGNORECASE=1} !/^VERSION=/' .env > .env.tmp 2>/dev/null || true
	@echo "VERSION=$(CUR_VERSION)" >> .env.tmp
	@mv .env.tmp .env
	@echo "✅ .env sync -> VERSION=$(CUR_VERSION)"

# --------- Release (auto-versioning) ----------
# Logique :
# 1) calcule NEXT_VERSION
# 2) buildx multi-arch + push tags : vNEXT et latest
# 3) seulement si push OK -> écrit NEXT_VERSION dans VERSION
# 4) optionnel: commit + tag git
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

# --------- Déploiement ----------
.PHONY: up
up: env-sync
	@echo "⬆️  Déploiement compose v$(CUR_VERSION)"
	VERSION=$(CUR_VERSION) docker compose --env-file .env up -d

.PHONY: release-up
release-up: release
	@$(MAKE) up

.PHONY: pull
pull: env-sync
	@echo "⬇️  Pull image v$(CUR_VERSION)"
	VERSION=$(CUR_VERSION) docker compose --env-file .env pull
	@$(MAKE) up

.PHONY: down
down:
	@docker compose down