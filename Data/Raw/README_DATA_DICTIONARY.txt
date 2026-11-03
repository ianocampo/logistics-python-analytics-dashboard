PYTHON MASTERCLASS (RETAIL / E-COMMERCE) — TRAINING DATASET PACKAGE
==================================================================

Files included (7 CSVs)
----------------------
1) customers.csv
2) products.csv
3) orders.csv
4) order_items.csv
5) payments.csv
6) shipments.csv
7) returns.csv

Design goals
------------
- Thousands of records, realistic retail/e-commerce workflow
- INTENTIONAL data issues for cleaning practice:
  • missing values (nulls)
  • duplicates
  • invalid values (negative age, qty=0, malformed email)
  • inconsistent categories and text casing
  • mixed date/datetime formats
  • currency formatted as strings (₱, commas)
  • a small number of orphan keys (customer_id / product_id not found)

Recommended primary keys / join keys
-----------------------------------
- customers.customer_id  (PK)
- products.product_id    (PK)
- orders.order_id        (PK)  [NOTE: intentional duplicates exist]
- order_items.order_item_id (PK)

Joins:
- orders.customer_id  -> customers.customer_id
- order_items.order_id -> orders.order_id
- order_items.product_id -> products.product_id
- payments.order_id -> orders.order_id
- shipments.order_id -> orders.order_id
- returns.order_id -> orders.order_id

Column dictionary (high level)
-----------------------------
customers.csv
- customer_id: string (CUST000001...)
- gender: messy values (M/F/Male/Female/Unknown/blank)
- age: may contain null or invalid (-1)
- email: may contain null or malformed emails
- phone: may contain null or short numbers
- signup_date: mixed formats (YYYY-MM-DD, MM/DD/YYYY, dd-Mon-YYYY)
- loyalty_tier: Bronze/Silver/Gold/Platinum/blank

products.csv
- category: inconsistent labels/casing/spelling (clean & standardize)
- unit_cost: numeric OR numeric string with commas
- unit_price: numeric OR currency string like "₱1,234.56"
- stock_qty: may contain null

orders.csv
- order_datetime: mixed datetime formats
- discount_pct: numeric or null
- shipping_fee: numeric or null
- intentional duplicate rows for same order_id

order_items.csv
- quantity: may contain invalid 0
- unit_price_at_purchase: may contain null (you can backfill from products)
- small number of invalid product_id values for cleaning checks

payments.csv
- amount_paid: numeric, currency string, or null
  (INTENTIONALLY not consistent with computed order totals — trainees can compute true totals)

shipments.csv
- delivered_date: may contain null
- shipment_status: Delivered/In Transit/Lost/Returned to Sender

returns.csv
- refund_amount: may contain null
- refunded_flag: Yes/No/Partial/blank

Suggested Day-by-Day Use
------------------------
Day 1: Load CSVs, explore columns, inspect types, basic Python loops on small slices.
Day 2: Fix missing values, duplicates, text standardization (gender, category).
Day 3: Parse dates, fix currency strings, validate keys, create derived columns (revenue).
Day 4: Groupby KPIs, pivot tables, ranking top products/customers, joins via merge().
Day 5: Visualizations (monthly revenue trend, category performance, region comparison).
Day 6: Mini end-to-end notebook + capstone briefing.

Capstone-ready business questions
---------------------------------
- Monthly revenue trend (overall + by channel)
- Top 10 products by revenue and quantity
- Best performing categories (after standardizing category names)
- Customer segmentation by total spend
- Delivery performance: average delivery lead time, late deliveries, lost shipments
- Returns rate by category or courier

Notes
-----
This dataset is synthetic (generated for training) and safe to use publicly.
