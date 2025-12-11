FROM python:3.12
WORKDIR /usr/local/app

RUN pip install uv
COPY pyproject.toml ./
RUN uv sync
COPY . .
EXPOSE 8080

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]