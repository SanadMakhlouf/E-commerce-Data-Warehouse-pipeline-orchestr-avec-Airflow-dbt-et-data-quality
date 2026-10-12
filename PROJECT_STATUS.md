# État du projet — E-commerce Data Pipeline

> Dernière mise à jour : 2026-10-12  
> Source : audit du dépôt Git + exécutions locales (`dbt debug`, `dbt run`, `dbt test`, inspection PostgreSQL).

## Présentation

Projet d’apprentissage **Data Engineering** : pipeline batch **CSV ventes e-commerce → PostgreSQL → modélisation analytique (star schema)**.

**Vision cible** (trouvée en fin de `README.md`, encodage UTF-16) :  
*Data Warehouse orchestré avec **Airflow**, **dbt** et **data quality**.*

## Architecture actuelle

```
sales.csv (local, non versionné)
    │
    ▼
ingestion/load_raw.py  ──►  raw_orders (PostgreSQL, public)
    │
    ├──► transformation/build_star_schema.py  ──► dim_* + fact_sales (pandas, replace)
    │
    └──► ecommerce_dbt (dbt)
              stg_orders (view)
              dim_products, dim_locations, dim_dates (tables)
              fact_sales (table)
```

**Décision à trancher :** deux moteurs de transformation (Python et dbt) produisent les mêmes objets métier. Continuité recommandée : **dbt = transformations officielles**, Python = **ingestion uniquement**.

## Technologies

| Outil | Rôle | Dans le repo | Preuve d’exécution |
|-------|------|--------------|-------------------|
| Python 3.14 | Ingestion / script legacy transform | Oui | Dépendances OK dans `venv` |
| pandas, SQLAlchemy, psycopg2 | Chargement CSV / SQL | `requirements.txt` | — |
| PostgreSQL | Warehouse | `.env` / `.env.example` | `dbt debug` OK (2026-10-12) |
| dbt 1.12 | Transform SQL + tests | `ecommerce_dbt/` | `dbt run` + `dbt test` OK (2026-10-12) |
| Git | Versionnement | 5 commits sur `main` | Working tree clean |

**Non présents dans le repo :** Docker, Airflow, CI/CD, Great Expectations/Soda, BI (Metabase/Superset), cloud.

## État d’avancement par composant

| Composant | Statut | Notes |
|-----------|--------|-------|
| Ingestion CSV → `raw_orders` | Terminé (code) / À confirmer (routine) | Script simple, `if_exists="replace"` |
| Nettoyage & règles métier | Terminé | Python + `stg_orders.sql` (alignés) |
| Star schema (Python) | Terminé | `build_star_schema.py` |
| Star schema (dbt) | Terminé et vérifié | 5 modèles, run OK |
| Tests dbt | Partiel | 3 tests seulement |
| Profil dbt | Partiel | `~/.dbt/profiles.yml` local, pas d’exemple versionné |
| Documentation README | À corriger | Obsolète + corruption encodage (UTF-16 en queue) |
| Orchestration Airflow | À commencer | Objectif documenté |
| Data quality avancée | À commencer | — |
| Docker / reproductibilité | À commencer | — |
| CI/CD | À commencer | — |

## Données PostgreSQL (snapshot 2026-10-12)

Exécution locale après `dbt run` :

- `raw_orders` : 128 975 lignes
- `dim_products` : 7 082
- `fact_sales` : 107 160
- `stg_orders` : vue dbt (non listée comme table)
- **Dette :** table orpheline `my_first_dbt_model` (reste d’un `dbt init` antérieur, absent du repo)

## Problèmes identifiés

1. **README** ne reflète pas l’état réel (star schema + dbt faits).
2. **Double pipeline** Python/dbt — risque de confusion et d’écrasement des tables.
3. **`dbt_project.yml`** : section `example` inutilisée (warning dbt).
4. **`requirements.txt`** : ne liste pas `dbt-postgres` (installé manuellement dans le venv).
5. **`logs/dbt.log`** versionné alors qu’il ne contient que des `dbt init`.
6. **Schéma unique `public`** pour raw, staging et marts (acceptable en apprentissage, à améliorer plus tard).
7. **Chargements full replace** — pas d’incremental ni d’idempotence avancée.

## Décisions techniques à conserver

- PostgreSQL local + `DATABASE_URL` via `.env` : simple, standard, pertinent pour junior DE.
- Modèle **star schema** (dims + `fact_sales`) : bon choix pédagogique et pro.
- **dbt** pour les transformations SQL : aligné avec le marché.
- CSV gitignoré : bonne pratique (dataset volumineux / licence).

## Décisions à réévaluer (sans urgence)

- Garder ou retirer `build_star_schema.py` une fois dbt validé comme chemin unique.
- dbt 1.12.0-**b3** (beta) : envisager version stable pour CI plus tard.
- Séparer schémas `raw` / `staging` / `marts` via config dbt.

## Feuille de route priorisée

| Priorité | Phase | Tâche | Statut | Résultat attendu | Dépendances |
|----------|-------|-------|--------|------------------|-------------|
| P0 | Remise en état | Valider ingest → dbt run → dbt test | Terminé et vérifié (2026-10-12) | Pipeline dbt vert | PostgreSQL + CSV + profil dbt |
| P0 | Remise en état | Documenter commandes dans README + corriger encodage | À commencer | README à jour | — |
| P0 | Architecture | Choisir dbt comme transform officiel | À confirmer | Note dans doc / commentaire script Python | — |
| P1 | Config | Corriger `dbt_project.yml` (staging view, retirer example) | À commencer | Plus de warning dbt | — |
| P1 | Config | Ajouter `profiles.yml.example` + doc | À commencer | Reproducible pour autre machine | — |
| P1 | Dépendances | Pin `dbt-postgres` dans requirements ou `requirements-dev.txt` | À commencer | `pip install` suffit | — |
| P1 | Qualité | Enrichir `schema.yml` (relationships, not_null) | À commencer | ≥10 tests dbt | dbt run OK |
| P2 | Nettoyage | Supprimer table `my_first_dbt_model` | À commencer | DB sans artefacts | — |
| P2 | Orchestration | Docker Compose + DAG Airflow | À commencer | Run planifié ingest → dbt | Docker |
| P2 | Industrialisation | GitHub Actions `dbt test` | À commencer | CI verte | Repo GitHub |
| P3 | Analytics | Metabase/Superset + mart KPI | Facultatif | Dashboard portfolio | marts stables |
| P3 | Cloud | Snowflake/BigQuery (option) | Facultatif | Extension cloud | Budget / compte |

## Prochaine tâche

**P0 — Mettre à jour la documentation et figer le “golden path” :**

1. Corriger `README.md` (contenu + supprimer le bloc UTF-16).
2. Ajouter section : `load_raw.py` → `cd ecommerce_dbt && dbt run && dbt test`.
3. Noter explicitement : transformations = **dbt** ; `build_star_schema.py` = exercice historique (ou deprecated).

## Commandes utiles

```powershell
cd C:\Users\sanad\OneDrive\Desktop\ecommerce-data-pipeline
.\venv\Scripts\activate

# Ingestion
python ingestion/load_raw.py

# Transform + tests (depuis la racine du projet dbt)
cd ecommerce_dbt
..\venv\Scripts\dbt.exe debug
..\venv\Scripts\dbt.exe run
..\venv\Scripts\dbt.exe test
```

## Historique Git (plan reconstitué)

| Commit | Date | Intention |
|--------|------|-----------|
| `9ec1c47` | 2026-06-25 | Semaine 1 — ingestion, config, deps |
| `b86bb9e` | 2026-06-25 | Exploration / nettoyage colonnes (Python) |
| `be7b44d` | 2026-06-25 | Star schema en Python |
| `26e5ade` | 2026-06-30 | Équivalent star schema en dbt + commit logs init |

**Où tu t’es arrêté :** après le commit dbt (`26e5ade`), sans mise à jour README, sans orchestration ni phase data quality. Les modèles dbt étaient écrits ; l’exécution de bout en bout n’était pas documentée dans le repo (exécutée avec succès le 2026-10-12 en audit).

## Fichier TODO

Voir `TODO.md` pour le suivi opérationnel tâche par tâche.
