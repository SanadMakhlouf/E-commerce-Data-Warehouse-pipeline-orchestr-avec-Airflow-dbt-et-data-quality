# TODO — Reprise du projet

Légende : `[x]` terminé · `[~]` partiel · `[ ]` à faire

## P0 — Reprise immédiate

- [x] Vérifier `dbt debug` (connexion PostgreSQL)
- [x] Exécuter `dbt run` (5 modèles)
- [x] Exécuter `dbt test` (28 tests — tous PASS)
- [x] Corriger `README.md` (pipeline complet + encodage)
- [x] Décision écrite : dbt = transform principal
- [ ] Exécuter `python ingestion/load_raw.py` puis re-`dbt run` (validation ingest → transform — à refaire si besoin)

## P1 — Consolidation (dbt)

- [x] Corriger `ecommerce_dbt/dbt_project.yml` (staging + retirer `example`)
- [x] Ajouter `profiles.yml.example`
- [ ] Documenter dataset `data/raw/sales.csv` (source, téléchargement)
- [x] Ajouter dbt au fichier de dépendances (`requirements-dev.txt`)
- [x] Enrichir tests dans `schema.yml` + test singulier
- [x] Retirer `logs/dbt.log` du suivi Git
- [x] Supprimer objets orphelins `my_first_dbt_model` / `my_second_dbt_model`

## P2 — Industrialisation

- [ ] Docker Compose (Postgres + option Airflow)
- [ ] DAG Airflow : ingest → dbt run → dbt test
- [ ] GitHub Actions : dbt parse / test

## P3 — Portfolio (facultatif)

- [ ] `dbt docs generate`
- [ ] Dashboard BI (Metabase/Superset)
- [ ] Modèle mart agrégé (ex. ventes journalières)
