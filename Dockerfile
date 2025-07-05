FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get -y install vim
RUN python3 -m pip install uv

WORKDIR /app

COPY src/* .

CMD ["uv", "run", "entrypoint.py"]
