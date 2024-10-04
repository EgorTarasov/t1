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
	set -a && source local.env && set +a && fastapi dev src/main.py
