FROM python:3.14-slim
WORKDIR /usr/local/app

ARG APP_ENV=dev

RUN pip install uv
COPY pyproject.toml ./
RUN uv sync
COPY . .
COPY .env.${APP_ENV} .env
RUN echo "BUILT WITH APP_ENV=${APP_ENV}"
EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]