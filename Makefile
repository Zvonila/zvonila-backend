dev-up:
	docker compose up -d
	fastapi dev main.py --host 0.0.0.0

mig-up:
	alembic upgrade +1