FROM python:3.13.7-slim-trixie AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /usr/src/ima-agent

COPY pyproject.toml uv.lock ./

RUN uv pip install --prerelease=allow --system --no-cache .

FROM python:3.13.7-slim-trixie

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/ima-agent

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

ENV PYTHONPATH="/usr/src/ima-agent"
ENV COLUMNS=80

CMD ["python", "/usr/src/ima-agent/agent/main.py"]