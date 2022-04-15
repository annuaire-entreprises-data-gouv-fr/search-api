# Annuaire des Entreprises - [API de recherche]

Ce site est disponible en ligne : [L’Annuaire des Entreprises](https://annuaire-entreprises.data.gouv.fr)

Ce repository met en place l'infrastructure de l'API de recherche sur les données d'entreprises.

## Architecture du service 🏗

Ce repository fait partie d'un ensemble de services qui constituent l'[Annuaire des Entreprises](https://annuaire-entreprises.data.gouv.fr) :

| Description | Accès |
|-|-|
|Le site Web | [par ici 👉](https://github.com/etalab/annuaire-entreprises-site) |
|L’API du Moteur de recherche | [par ici 👉](https://github.com/etalab/annuaire-entreprises-search-api) |
|L‘API de redondance de Sirene | [par ici 👉](https://github.com/etalab/annuaire-entreprises-sirene-api) |
|Le traitement permettant la génération de données à ingérer dans le moteur de recherche | [par ici 👉](https://github.com/etalab/annuaire-entreprises-search-infra) |

## A propos de l'architecture

* `Elasticsearh` est le moteur de recherche utilisé pour indexer et requêter sur les données
* `aiohttp` est le HTTP client/server framework utilisé
* `Sentry` est utilisé pour le monitoring et le tracking des erreurs

## Sources de données

👉 [Base Sirene des entreprises et de leurs établissements](https://www.data.gouv.fr/fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/)
