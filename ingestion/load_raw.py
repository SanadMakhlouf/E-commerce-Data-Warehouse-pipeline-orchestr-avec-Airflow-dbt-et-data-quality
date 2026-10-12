import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, inspect, text

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import get_database_url

CSV_PATH = PROJECT_ROOT / "data" / "raw" / "sales.csv"
TABLE_NAME = "raw_orders"

# Etape 1 : lire le CSV
df = pd.read_csv(CSV_PATH, low_memory=False)
print(f"{len(df)} lignes lues")
print(df.head())

# Etape 2 : connexion PostgreSQL
engine = create_engine(get_database_url())

# Etape 3 : charger dans raw_orders (TRUNCATE + append : ne pas DROP, les vues dbt en dependent)
if inspect(engine).has_table(TABLE_NAME):
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {TABLE_NAME}"))
    if_exists = "append"
else:
    if_exists = "replace"

df.to_sql(TABLE_NAME, engine, if_exists=if_exists, index=False)

print(f"Table {TABLE_NAME} chargee dans PostgreSQL ({len(df)} lignes)")
