# ecommerce_dbt

Transformations SQL du pipeline e-commerce (staging + star schema).

## Prerequis

- PostgreSQL avec la base `ecommerce_db`
- Table `raw_orders` remplie via `python ingestion/load_raw.py` (depuis la racine du repo)
- Profil dbt : copier `profiles.yml.example` vers `~/.dbt/profiles.yml`

## Commandes

Depuis ce dossier (`ecommerce_dbt/`), avec le venv active a la racine :

```powershell
..\venv\Scripts\dbt.exe debug
..\venv\Scripts\dbt.exe run
..\venv\Scripts\dbt.exe test
..\venv\Scripts\dbt.exe docs generate
..\venv\Scripts\dbt.exe docs serve
```

## Modeles

| Couche | Modele | Role |
|--------|--------|------|
| Source | `raw.raw_orders` | Donnees brutes CSV |
| Staging | `stg_orders` | Nettoyage, filtres metier |
| Mart | `dim_products` | SKUs uniques |
| Mart | `dim_locations` | Lieux de livraison |
| Mart | `dim_dates` | Calendrier |
| Mart | `fact_sales` | Lignes de vente + cles etrangeres |

Les transformations Python dans `transformation/build_star_schema.py` ne sont plus utilisees : **dbt est la source de verite**.
