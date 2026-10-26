-- SQLite dialect; transaction lines, not distinct baskets unless COUNT(DISTINCT order_id) used.
-- 1. Sales KPIs
SELECT ROUND(SUM(units * unit_price), 2) AS gross_sales,
       ROUND(SUM(units * unit_price * (1 - discount_pct) * (1 - returned)), 2) AS net_sales,
       COUNT(DISTINCT order_id) AS orders,
       ROUND(SUM(units * unit_price * (1 - discount_pct) * (1 - returned)) / COUNT(DISTINCT order_id), 2) AS aov
FROM retail_transactions;

-- 2. Monthly net sales and orders
SELECT SUBSTR(transaction_date, 1, 7) AS month,
       ROUND(SUM(units * unit_price * (1 - discount_pct) * (1 - returned)), 2) AS net_sales,
       COUNT(DISTINCT order_id) AS orders
FROM retail_transactions
GROUP BY SUBSTR(transaction_date, 1, 7)
ORDER BY month;

-- 3. Category share with window function
WITH category_sales AS (
 SELECT category, SUM(units * unit_price * (1 - discount_pct) * (1 - returned)) AS net_sales
 FROM retail_transactions GROUP BY category
)
SELECT category, ROUND(net_sales, 2) AS net_sales,
       ROUND(100.0 * net_sales / SUM(net_sales) OVER (), 1) AS sales_share_pct
FROM category_sales ORDER BY net_sales DESC;

-- 4. Return line rates by format
SELECT store_format, COUNT(*) AS transaction_lines, SUM(returned) AS returned_lines,
       ROUND(100.0 * SUM(returned) / COUNT(*), 1) AS return_rate_pct
FROM retail_transactions GROUP BY store_format ORDER BY return_rate_pct DESC;
