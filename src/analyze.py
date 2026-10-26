from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)
df = pd.read_csv(BASE / "data" / "retail_transactions.csv", parse_dates=["transaction_date"])
required = ["transaction_id", "order_id", "transaction_date", "store_format", "region", "category", "units", "unit_price", "discount_pct", "returned"]
assert df[required].notna().all().all(), "Unexpected missing values"
assert df.transaction_id.is_unique, "Duplicate transaction IDs"
assert (df.units > 0).all() and (df.unit_price >= 0).all()
assert df.discount_pct.between(0, 1).all()
assert df.returned.isin([0, 1]).all()

df["gross_sales"] = df.units * df.unit_price
df["net_sales"] = (df.gross_sales * (1 - df.discount_pct) * (1 - df.returned)).round(2)
df["month"] = df.transaction_date.dt.to_period("M").astype(str)
monthly = df.groupby("month", as_index=False).agg(net_sales=("net_sales", "sum"), orders=("order_id", "nunique"), units=("units", "sum"))
monthly["aov"] = (monthly.net_sales / monthly.orders).round(2)
monthly.to_csv(OUT / "monthly_kpis.csv", index=False)
category = df.groupby("category", as_index=False).agg(net_sales=("net_sales", "sum"), returned_lines=("returned", "sum"), lines=("transaction_id", "count"))
category["return_rate_pct"] = (100 * category.returned_lines / category.lines).round(1)
category = category.sort_values("net_sales", ascending=False)
category.to_csv(OUT / "category_performance.csv", index=False)
by_format = df.groupby("store_format", as_index=False).agg(net_sales=("net_sales", "sum"), orders=("order_id", "nunique"))
by_format.sort_values("net_sales", ascending=False).to_csv(OUT / "format_performance.csv", index=False)
summary = (f"Transactions: {len(df):,}\nUnique orders: {df.order_id.nunique():,}\n"
           f"Gross sales (fictional USD): {df.gross_sales.sum():,.2f}\n"
           f"Net sales (fictional USD): {df.net_sales.sum():,.2f}\n"
           f"Average order value: {df.net_sales.sum() / df.order_id.nunique():,.2f}\n"
           f"Returned line rate: {100 * df.returned.mean():.1f}%\n")
(OUT / "summary.txt").write_text(summary, encoding="utf-8")
print(summary)
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(monthly.month, monthly.net_sales, marker="o")
ax.set(title="Monthly net sales — synthetic dataset", ylabel="Fictional USD", xlabel="Month")
ax.tick_params(axis="x", labelrotation=45)
fig.tight_layout(); fig.savefig(OUT / "monthly_sales.png", dpi=160); plt.close(fig)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(category.category, category.net_sales)
ax.set(title="Net sales by category — synthetic dataset", ylabel="Fictional USD")
ax.tick_params(axis="x", labelrotation=25)
fig.tight_layout(); fig.savefig(OUT / "category_sales.png", dpi=160); plt.close(fig)
