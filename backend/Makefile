.PHONY: migration-create
migration-create:
	alembic revision --autogenerate -m "$(name)"

.PHONY: migration-up
migration-up:
	alembic upgrade head

.PHONY: migration-down
migration-down:
	alembic downgrade -1

.PHONY: dev
dev:
	fastapi dev src/main.py


.PHONY: docker-build-amd64
docker-build-amd64:
	docker build \
		--tag ghcr.io/egortarasov/t1/api:dev \
		--platform linux/amd64 .

.PHONY: docker-push-amd64
docker-push-amd64:
	docker push ghcr.io/egortarasov/t1/api:dev


.PHONY: docker-publish-amd64
docker-publish-amd64: docker-build-amd64 docker-push-amd64
