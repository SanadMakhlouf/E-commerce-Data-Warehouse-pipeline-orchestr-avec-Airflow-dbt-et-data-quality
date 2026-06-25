import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import get_database_url

TABLE_NAME = "raw_orders"

COLUMNS = [
    "Order ID",
    "Date",
    "Status",
    "SKU",
    "Category",
    "Style",
    "Size",
    "Qty",
    "Amount",
    "ship-city",
    "ship-state",
    "ship-country",
]

RENAME = {
    "Order ID": "order_id",
    "Date": "order_date",
    "Status": "status",
    "SKU": "sku",
    "Category": "category",
    "Style": "style",
    "Size": "size",
    "Qty": "qty",
    "Amount": "amount",
    "ship-city": "ship_city",
    "ship-state": "ship_state",
    "ship-country": "ship_country",
}

engine = create_engine(get_database_url())

# --- Etape 1 : lire ---
df = pd.read_sql_table(TABLE_NAME, engine)
print(f"{len(df)} lignes lues depuis {TABLE_NAME}")

# --- Etape 1 : explorer ---
print("\n--- Apercu ---")
print(df.head())

print("\n--- Infos ---")
print(df.info())

print("\n--- Statuts ---")
print(df["Status"].value_counts())

# --- Etape 1 : reduire les colonnes ---
df = df[COLUMNS]
df = df.rename(columns=RENAME)

# --- Etape 1 : nettoyer ---
rows_before = len(df)

df = df[df["status"].str.contains("Shipped", case=False, na=False)]
df = df.dropna(subset=["sku", "order_date", "qty", "amount"])
df = df[df["qty"] > 0]
df = df[df["amount"] > 0]

rows_after = len(df)

print(f"\n--- Nettoyage ---")
print(f"Lignes avant : {rows_before}")
print(f"Lignes apres  : {rows_after}")
print(f"Lignes supprimees : {rows_before - rows_after}")

print("\n--- Donnees propres (df_clean) ---")
print(df.head())
print(df.info())

df_clean = df
