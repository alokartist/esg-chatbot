# backend/utils.py
import sqlite3
import os
from typing import Dict, List

def get_sqlite_connection(db_path: str):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def introspect_db_schema(conn) -> Dict[str, List[str]]:
    """
    Return dict: {table_name: [col1, col2, ...]}
    """
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cur.fetchall()]
    schema = {}
    for t in tables:
        cur.execute(f"PRAGMA table_info({t});")
        cols = [row[1] for row in cur.fetchall()]
        schema[t] = cols
    return schema

def pretty_samples(conn, table: str, limit: int = 5):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table} LIMIT {limit}")
    rows = cur.fetchall()
    return [dict(r) for r in rows]
