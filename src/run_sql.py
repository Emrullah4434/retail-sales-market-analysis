import csv
import sqlite3
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
with sqlite3.connect(":memory:") as con:
    con.execute("""CREATE TABLE retail_transactions (
    transaction_id TEXT, order_id TEXT, transaction_date TEXT, store_format TEXT,
    region TEXT, category TEXT, units INTEGER, unit_price REAL, discount_pct REAL, returned INTEGER)""")
    with (BASE / "data" / "retail_transactions.csv").open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        con.executemany("INSERT INTO retail_transactions VALUES (?,?,?,?,?,?,?,?,?,?)",
            ([row[c] for c in columns] for row in reader))
    script = (BASE / "sql" / "retail_analysis.sql").read_text(encoding="utf-8")
    script = "\n".join(line for line in script.splitlines() if not line.lstrip().startswith("--"))
    for i, statement in enumerate(script.split(";"), start=1):
        # Keep SQL comments attached to each statement; skip empty segments.
        if not statement.strip():
            continue
        cur = con.execute(statement)
        print(f"\nQUERY {i}")
        print(' | '.join(col[0] for col in cur.description))
        for row in cur.fetchall():
            print(' | '.join(str(value) for value in row))
