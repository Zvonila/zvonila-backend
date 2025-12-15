dev-up:
	uv sync
	docker compose -f docker-compose.dev.yaml up -d --build
	alembic upgrade head
	uvicorn main:app --host 0.0.0.0 --port 8000

mig-up:
	alembic upgrade +1

prod-up: 
	docker compose --env-file .env.prod up -d --build

gen-keys:
	openssl genrsa -out private.pem 2048
	openssl rsa -in private.pem -pubout -out public.pem
