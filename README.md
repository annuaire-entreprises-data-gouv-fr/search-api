<h1 align="center">
  <img src="https://github.com/etalab/annuaire-entreprises-site/blob/main/public/images/annuaire-entreprises-paysage-large.gif" width="400px" />
</h1>

<a href="https://github.com/etalab/annuaire-entreprises-search-api/blob/main/LICENSE"><img src="https://img.shields.io/github/license/etalab/annuaire-entreprises-search-api.svg?color=green" alt="License Badge"></a>
[![Deploy cluster](https://github.com/etalab/annuaire-entreprises-search-api/actions/workflows/deploy.yml/badge.svg)](https://github.com/etalab/annuaire-entreprises-search-api/actions/workflows/deploy.yml)
[![Test Search API](https://github.com/etalab/annuaire-entreprises-search-api/actions/workflows/workflow.yml/badge.svg)](https://github.com/etalab/annuaire-entreprises-search-api/actions/workflows/workflow.yml)
<a href="https://recherche-entreprises.api.gouv.fr/docs/"><img src="https://img.shields.io/badge/API-documentation-yellow.svg" alt="Documentation Badge"></a>

Bienvenue sur le repository de [l’API de recherche d’Entreprises](https://recherche.api.gouv.fr). Cette API permet de chercher n’importe quelle entreprise de france. Elle fait partie du projet [Annuaire des Entreprises](https://annuaire-entreprises.data.gouv.fr).

## Architecture du service 🏗

Ce repository fait partie [d'un ensemble de services qui constituent l'Annuaire des Entreprises](https://github.com/etalab/annuaire-entreprises-site?tab=readme-ov-file#dépôts-liés-).

## A propos de l'architecture

* `Elasticsearh` est le moteur de recherche utilisé pour indexer et requêter sur les données
* `aiohttp` est le HTTP client/server framework utilisé
* `Sentry` est utilisé pour le monitoring et le tracking des erreurs

## Sources de données

👉 [Base Sirene des entreprises et de leurs établissements](https://www.data.gouv.fr/fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/)
