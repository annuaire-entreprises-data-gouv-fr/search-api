### Dag permettant l'alimentation d'un datalake sirene

Le notebook `generate-data-before-indexation` permet de formater les données de la base sirene pour optimiser son indexation et faciliter le requêtage elasticsearch.

Le notebook `generate-kpi-sirene` permet de générer des KPI autour des codes NAFs et activités juridiques des entreprises. Ce notebook n'entre pas dans le cadre de l'annuaire des entreprises.

Le script `dag-insert-elk.py` est un DAG airflow orchestrant un ensemble de tâche permettant :
- de formatter les données de la base sirene
- de générer des indicateurs sur la base sirene
- de créer des index elasticsearch
- d'insérer des données dans un index elasticsearch (index siren et index siret)