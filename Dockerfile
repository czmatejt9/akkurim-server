FROM ghcr.io/astral-sh/uv:0.5.13-python3.12-bookworm
# keep that to 0.5.13 now as 0.5.14 failed

WORKDIR /app

ENV ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y \ 
    gcc python3-dev \ 
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

# Make port 8000 available to the world outside this container
ENTRYPOINT []

RUN chmod +x /app/app/scripts/*.sh
EXPOSE 8000
CMD ["/app/app/scripts/run.sh"]
