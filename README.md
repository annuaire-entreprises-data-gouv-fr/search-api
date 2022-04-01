# Annuaire des Entreprises - [Infrastructure de recherche]

Ce site est disponible en ligne : [L’Annuaire des Entreprises](https://annuaire-entreprises.data.gouv.fr)

Ce repo met en place l'infrastructure Airflow permettant d'exécuter le workflow qui récupère, traite et indexe les données publiques d'entreprises.

L'infrastructure actuelle est basée sur du LocalExecutor (le scheduler, le webserver et worker sont hébergés sur le même container)

## Architecture du service 🏗

Ce repository fait partie d'un ensemble de services qui constituent l'[Annuaire des Entreprises](https://annuaire-entreprises.data.gouv.fr) :

| Description | Accès |
|-|-|
|Le site Web | [par ici 👉](https://github.com/etalab/annuaire-entreprises-site) |
|L’API du Moteur de recherche | [par ici 👉](https://github.com/etalab/annuaire-entreprises-search-api) |
|L‘API de redondance de Sirene | [par ici 👉](https://github.com/etalab/annuaire-entreprises-sirene-api) |
|L‘infra du moteur de recherche | [par ici 👉](https://github.com/etalab/annuaire-entreprises-search-infra) |

## A propos de l'infrastructure

L'architecture se base sur cette stack 👉 https://github.com/etalab/data-engineering-stack
