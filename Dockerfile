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
RUN pip install --upgrade pip
WORKDIR /app
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS release
COPY ./app ./app
EXPOSE 8000

FROM base AS dev
RUN apk add make
