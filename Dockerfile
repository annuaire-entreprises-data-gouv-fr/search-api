ARG BUILD_DATE
ARG BUILD_VERSION=main
ARG BUILD_REVISION

FROM python:3.12.8-alpine AS base
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.authors="https://github.com/annuaire-entreprises-data-gouv-fr/search-api/graphs/contributors"
LABEL org.opencontainers.image.url="https://github.com/annuaire-entreprises-data-gouv-fr/search-api"
LABEL org.opencontainers.image.documentation="https://github.com/annuaire-entreprises-data-gouv-fr/search-api/blob/main/README.md"
LABEL org.opencontainers.image.source="https://github.com/annuaire-entreprises-data-gouv-fr/search-api"
LABEL org.opencontainers.image.version="${BUILD_VERSION}"
LABEL org.opencontainers.image.revision="${BUILD_REVISION}"
LABEL org.opencontainers.image.vendor="annuaire-entreprises-data-gouv-fr"
LABEL org.opencontainers.image.licenses="MIT License"
LABEL org.opencontainers.image.title="API Recherche Annuaire des Entreprises"
LABEL org.opencontainers.image.description="Image Docker de l'API de recherche de l'Annuaire des Entreprises"
LABEL org.opencontainers.image.base.name="python:3.12.8-alpine"
LABEL org.opencontainers.image.base.digest=""
# https://docs.astral.sh/uv/guides/integration/docker/
COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /uvx /bin/
ENV UV_PYTHON_DOWNLOADS=never \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev

FROM base AS release
COPY ./app ./app
EXPOSE 8000

FROM base AS dev
RUN apk add make
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked
