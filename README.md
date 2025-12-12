<h1 align="center">
  <img src="https://github.com/annuaire-entreprises-data-gouv-fr/site/blob/main/public/images/annuaire-entreprises-paysage-large.gif" width="400px" />
</h1>

<a href="https://github.com/annuaire-entreprises-data-gouv-fr/search-api/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License Badge"></a>
[![Deploy cluster](https://github.com/annuaire-entreprises-data-gouv-fr/search-api/actions/workflows/deploy.yml/badge.svg)](https://github.com/annuaire-entreprises-data-gouv-fr/search-api/actions/workflows/deploy.yml)
[![Test Search API](https://github.com/annuaire-entreprises-data-gouv-fr/search-api/actions/workflows/workflow.yml/badge.svg)](https://github.com/annuaire-entreprises-data-gouv-fr/search-api/actions/workflows/workflow.yml)
<a href="https://recherche-entreprises.api.gouv.fr/docs/"><img src="https://img.shields.io/badge/API-documentation-yellow.svg" alt="Documentation Badge"></a>

Bienvenue sur le dépôt de données de [l’API de recherche d’Entreprises](https://recherche-entreprises.api.gouv.fr/). Cette API permet de chercher n’importe quelle entreprise de France. Elle fait partie du projet de [l'Annuaire des Entreprises](https://annuaire-entreprises.data.gouv.fr).


## À propos de l'API

L'API de Recherche des Entreprises est un service qui permet de rechercher et de récupérer des informations sur les entreprises françaises. Elle offre une interface unifiée pour accéder à des données provenant de diverses sources administratives.

### Fonctionnalités clés

- **Recherche avancée** : recherchez des entreprises par nom, SIREN, SIRET, adresse, code NAF, et bien plus encore
- **Filtrage** : filtrez les résultats par secteur d'activité, localisation géographique, taille d'entreprise, etc.
- **Données complètes** : accédez à des informations détaillées sur les entreprises, y compris leurs établissements, dirigeants, bilans financiers, etc.
- **Performance** : des temps de réponse rapides grâce à l'utilisation d'Elasticsearch
- **API RESTful** : une interface simple et bien documentée pour une intégration facile

### Exemples d'utilisation

```bash
# Recherche textuelle
curl "https://recherche-entreprises.api.gouv.fr/search?q=DINUM"

# Recherche par SIREN
curl "https://recherche-entreprises.api.gouv.fr/search?q=siren:130025265"

# Recherche avec filtres
curl "https://recherche-entreprises.api.gouv.fr/search?q=Boulangerie&code_postal=13001&code_naf=56.10A"
```

## Architecture du service

Ce dépôt fait partie [d'un ensemble de services qui constituent l'Annuaire des Entreprises](https://github.com/annuaire-entreprises-data-gouv-fr/site?tab=readme-ov-file#dépôts-liés-).


## Architecture technique

### Composants principaux

* `Elasticsearch` est le moteur de recherche utilisé pour indexer et requêter sur les données
* `FastAPI` est le HTTP framework utilisé pour construire l'API
* `Sentry` est utilisé pour le monitoring et le tracking des erreurs

### Flux de traitement

1. **Mise à jour des données** : mises à jours quotidiennes par l'import de l'index Elasticsearch construit par [l'infra data](https://github.com/annuaire-entreprises-data-gouv-fr/search-infra)
2. **Requête client** : un utilisateur envoie une requête HTTP à l'API FastAPI
3. **Traitement** : FastAPI valide et transforme la requête en une requête Elasticsearch
4. **Recherche** : Elasticsearch exécute la recherche et retourne les résultats
5. **Formatage** : FastAPI formate les résultats et les retourne au client
6. **Monitoring** : Les erreurs et les performances sont pilotées via Sentry et Kibana

## Sources de données

[👉 Liste des sources de données](https://github.com/annuaire-entreprises-data-gouv-fr/search-infra?tab=readme-ov-file#sources-de-données) utilisées pour construire l'index utilisé par l'API de Recherche des Entreprises.

Plus d'informations sur les sources de données [par
ici 👉](https://annuaire-entreprises.data.gouv.fr/donnees/sources).


## Tester en local

### Installer l'environment

1. Installer `mise`: [documentation](https://mise.jdx.dev/installing-mise.html).

2. Copier et compléter le fichier de variables d'environnements :
```bash
cp mise.local.toml.example mise.local.toml
```

3. Initialiser l'environnement :
```bash
mise install
uv sync --extra dev
```

### Lancer le service

```bash
uv run fastapi dev main.py
```

### Exécuter les tests

```bash
pytest app/tests/e2e_tests -v
```


## Déploiement

Les commits mergés sur la branche `main` sont automatiquement déployés sur l'environnement de staging.

Les déploiements en production nécessitent une approbation manuelle de la part des
maintainers du dépôt depuis la page actions.


## Contact

Channel Tchap : `https://tchap.gouv.fr/#/room/#annuaire-entreprises:agent.dinum.tchap.gouv.fr`
