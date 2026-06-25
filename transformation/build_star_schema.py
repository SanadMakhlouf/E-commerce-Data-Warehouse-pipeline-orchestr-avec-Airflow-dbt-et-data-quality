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

df_clean = df.copy()
df_clean["order_date"] = pd.to_datetime(df_clean["order_date"])

# --- Etape 2 : dim_product ---
df_products = df_clean[["sku", "category", "style", "size"]].drop_duplicates()
df_products = df_products.reset_index(drop=True)
df_products["product_id"] = df_products.index + 1
df_products.to_sql("dim_products", engine, if_exists="replace", index=False)
print(f"Table dim_products creee ({len(df_products)} lignes)")

# --- Etape 3 : dim_location ---
df_locations = df_clean[["ship_city", "ship_state", "ship_country"]].drop_duplicates()
df_locations = df_locations.reset_index(drop=True)
df_locations["location_id"] = df_locations.index + 1
df_locations.to_sql("dim_locations", engine, if_exists="replace", index=False)
print(f"Table dim_locations creee ({len(df_locations)} lignes)")

# --- Etape 4 : dim_date ---
df_dates = df_clean[["order_date"]].drop_duplicates()
df_dates["year"] = df_dates["order_date"].dt.year
df_dates["month"] = df_dates["order_date"].dt.month
df_dates["day"] = df_dates["order_date"].dt.day
df_dates["day_name"] = df_dates["order_date"].dt.day_name()
df_dates = df_dates.reset_index(drop=True)
df_dates["date_id"] = df_dates.index + 1
df_dates.to_sql("dim_dates", engine, if_exists="replace", index=False)
print(f"Table dim_dates creee ({len(df_dates)} lignes)")

# --- Etape 5 : fact_sales ---
fact_sales = df_clean.merge(
    df_products[["sku", "product_id"]],
    on="sku",
    how="left",
)
fact_sales = fact_sales.merge(
    df_locations[["ship_city", "ship_state", "ship_country", "location_id"]],
    on=["ship_city", "ship_state", "ship_country"],
    how="left",
)
fact_sales = fact_sales.merge(
    df_dates[["order_date", "date_id"]],
    on="order_date",
    how="left",
)

fact_sales = fact_sales[
    [
        "order_id",
        "product_id",
        "location_id",
        "date_id",
        "qty",
        "amount",
        "status",
    ]
]

fact_sales.to_sql("fact_sales", engine, if_exists="replace", index=False)
print(f"Table fact_sales creee ({len(fact_sales)} lignes)")