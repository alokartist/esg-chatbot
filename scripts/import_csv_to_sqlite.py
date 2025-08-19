# scripts/import_csv_to_sqlite.py
import sys
import pandas as pd
import sqlite3

def import_csv(csv_path, db_path, table_name="esg_records"):
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Imported {csv_path} to {db_path} as table {table_name}")
    print(f"Rows: {len(df)}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python import_csv_to_sqlite.py <csv_path> <db_path>")
        sys.exit(1)
    import_csv(sys.argv[1], sys.argv[2])
