# Retail Sales & Market Analysis

A reproducible **Data Analyst portfolio project** demonstrating Python-based data cleaning, retail KPI analysis, SQL aggregation and visual storytelling.

> **Data disclaimer:** All records are artificially generated for portfolio demonstration. Results are illustrative, not real company performance or market benchmarks.

## Business questions
1. How do monthly net sales and order volume change over time?
2. Which store formats and product categories generate the most revenue?
3. What are the net sales, gross sales, units and average order value (AOV)?
4. Which categories have the highest returns?

## Tech stack
**Python 3.10+**, pandas, matplotlib, SQLite (standard Python library), SQL.

## Data dictionary
`data/retail_transactions.csv` contains one row per transaction line:
- `transaction_id`: unique line identifier
- `order_id`: basket identifier (an order may contain several lines)
- `transaction_date`: date (YYYY-MM-DD)
- `store_format`: Supermarket, Convenience or Hypermarket
- `region`: geographic market
- `category`: product family
- `units`: units sold, positive integer
- `unit_price`: selling price per unit (fictional USD)
- `discount_pct`: decimal discount rate, 0–0.20
- `returned`: 1 if the entire line was returned; otherwise 0

**Net sales** = `units × unit_price × (1 − discount_pct) × (1 − returned)`. **Gross sales** = `units × unit_price`. **AOV** = net sales / distinct order IDs. Returned lines contribute zero net sales. This is a simplified analysis without tax, shipping or cost of goods sold.

## Run locally
```bash
python -m pip install -r requirements.txt
python src/analyze.py
```

Outputs are saved to `outputs/`:
- `monthly_kpis.csv`
- `category_performance.csv`
- `format_performance.csv`
- `summary.txt`
- `monthly_sales.png`
- `category_sales.png`

## SQL analysis
Run the script to load the CSV into SQLite and execute the SQL file:
```bash
python src/run_sql.py
```
Or open `sql/retail_analysis.sql` to review the queries (SQLite dialect).

## Portfolio discussion points
- Validate schema, missing values, duplicate transaction IDs and business-rule constraints before analysis.
- Report gross and net sales separately, and clarify the treatment of returned items.
- Highlight revenue mix across categories and formats, alongside monthly trends.
- Distinguish descriptive metrics from causal conclusions.

## Limitations
This dataset is synthetically generated and not a realistic demand forecast. No real customer or retailer data is included. Add actual business insights only after reviewing the generated results.
