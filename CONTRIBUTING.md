# Guide contribution

Veuillez noter que l'équipe de l'Annuaire des Entreprises se réserve le droit de fermer toute issue ou pull request qui ne respecterait pas la feuille de route interne du produit.

## Comment tester en local

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
pytest app/tests/ -v
```

## Processus de CI/CD

### Github Actions

La CI utilise des workflows Github Actions et doit obligatoirement réussir :
* Tests Unitaires
* Tests End to End
* Le titre de la PR doit respecter les conventional commit

Par défaut les tests E2E visent l'index Elasticsearch `siren-reader` du serveur de staging.
Afin de viser dev-01 ou dev-02 il faut ajouter le label `test_on_dev_1` ou `test_on_dev_2` sur la PR avant de pousser les commits.

## Merger

Les commits mergés sur la branche `main` sont automatiquement déployés sur l'environnement de staging.
La stratégie squash and merge en étant à jour sur main est privilégiée.
Le nom du commit squashé doit respecter le titre de la Pull Request (en enlevant le numéro de PR).
L'approval d'un maintainer du dépôt de code est obligatoire.

## Déploiement

Les déploiements en production nécessitent une approbation manuelle de la part des maintainers du dépôt depuis la page actions.
