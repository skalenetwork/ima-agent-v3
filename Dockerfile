FROM python:3.14.0-slim-trixie AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /usr/src/ima-agent

COPY pyproject.toml uv.lock ./

RUN uv pip install --prerelease=allow --system --no-cache .

FROM python:3.14.0-slim-trixie

WORKDIR /usr/src/ima-agent

COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

ENV PYTHONPATH="/usr/src/ima-agent"
ENV COLUMNS=80

CMD ["python", "/usr/src/ima-agent/agent/main.py"]