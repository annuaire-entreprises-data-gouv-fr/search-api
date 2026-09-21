# Guide contribution

Veuillez noter que l'équipe de l'Annuaire des Entreprises se réserve le droit de fermer toute issue ou pull request qui ne respecterait pas la feuille de route interne du produit.

## Comment tester en local

### Installer l'environment

1. Installer `uv` : [documentation](https://docs.astral.sh/uv/getting-started/installation/).
   C'est le seul prérequis, il fournit lui-même l'interpréteur Python.

2. Copier et compléter le fichier de variables d'environnements :
```bash
cp .env.example .env
```

3. Initialiser l'environnement :
```bash
uv sync --extra dev
```

4. Installer `pre-commit` et ses hooks git :
```bash
uv tool install pre-commit
pre-commit install --install-hooks
```

Les hooks lancent `ruff` et `mypy` avant chaque commit.
Pour les lancer à la main sur l'ensemble du dépôt :
```bash
pre-commit run --all-files
```

### Lancer le service

```bash
uv run fastapi dev app/main.py
```

### Exécuter les tests

```bash
uv run pytest app/tests/unit_tests -v     # rapides, sans réseau
uv run pytest app/tests/e2e_tests -v      # l'API doit tourner sur localhost:8000
uv run pytest app/tests/search_tests -v   # idem, tests de l'algorithme de recherche
```

Les tests de `search_tests` verrouillent le classement et les champs interrogés
sur des entités réelles de l'index (voir `BUGS.md`). Ils dépendent des données
et peuvent casser à chaque reconstruction de l'index.

## Processus de CI/CD

### Github Actions

La CI utilise des workflows Github Actions et doit obligatoirement réussir :
* Tests Unitaires
* Tests End to End
* Le titre de la PR doit respecter les conventional commit

Les tests sur la recherche ne sont pas obligatoire : un échec peut juste signaler un changement naturel des résultats sans régression. Dans ce cas mettre à jour le test en question.

Par défaut les tests E2E visent l'index Elasticsearch `siren-reader` du serveur de staging.
Afin de viser dev-01 ou dev-02 il faut ajouter le label `test_on_dev_1` ou `test_on_dev_2` sur la PR avant de pousser les commits.

## Merger

Les commits mergés sur la branche `main` sont automatiquement déployés sur l'environnement de staging.
La stratégie squash and merge en étant à jour sur main est privilégiée.
Le nom du commit squashé doit respecter le titre de la Pull Request (en enlevant le numéro de PR).
L'approval d'un maintainer du dépôt de code est obligatoire.

## Déploiement

Les déploiements en production nécessitent une approbation manuelle de la part des maintainers du dépôt depuis la page actions.
