---
title: "Task 36 — Read EXPLAIN ANALYZE Like a Pro"
weight: 36
level: "🔴 Level 3 — Postgres Internals"
summary: "Practice reading plan output to identify hot spots."
---

# Task 36 — Read EXPLAIN ANALYZE Like a Pro

Level:
🔴 Level 3 — Postgres Internals

Estimated Time:
~5 minutes

Concept(s):
- EXPLAIN ANALYZE
- Actual vs estimated
- Node timing

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson36;
SET search_path TO lesson36;

CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, total NUMERIC, created_at TIMESTAMPTZ DEFAULT now());
INSERT INTO orders (customer_id, total, created_at)
SELECT (random()*50)::int, (10 + random()*90)::numeric, now() - (g || ' minutes')::interval
FROM generate_series(1, 8000) g;
CREATE INDEX ON orders (customer_id);
ANALYZE orders;
```

## 🧠 Challenge

Run EXPLAIN (ANALYZE, BUFFERS, VERBOSE) on a query that filters customer_id and orders by created_at. Identify which node dominates time and where estimates differ.

## 🧭 Hints (Progressive)

1. Try SELECT * FROM orders WHERE customer_id = 10 ORDER BY created_at DESC LIMIT 20;
2. Look for loops, rows, and timing columns to find the slowest node.
3. Note if the LIMIT is applied after a sort or if an index provides order already.

## ✅ Expected Observation / Outcome

- You identified the node consuming the most time (often the sort or index scan).
- You compared estimated vs actual rows to judge planner accuracy.

## 🤔 Why This Matters

- Reading plans quickly is a superpower during incidents.
- Knowing where time goes guides whether to add indexes, change queries, or adjust parameters.
