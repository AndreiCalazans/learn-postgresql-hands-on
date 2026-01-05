---
title: "Task 23 — Ignoring EXPLAIN Is Costly"
weight: 23
level: "🟡 Level 2 — PostgreSQL Mistakes"
summary: "Use EXPLAIN ANALYZE to catch misestimates before shipping."
---

# Task 23 — Ignoring EXPLAIN Is Costly

Level:
🟡 Level 2 — PostgreSQL Mistakes

Estimated Time:
~5 minutes

Concept(s):
- Plan inspection
- Misestimates
- ANALYZE

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson23;
SET search_path TO lesson23;

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  price NUMERIC NOT NULL,
  featured BOOLEAN DEFAULT FALSE
);

INSERT INTO products (name, price, featured)
SELECT 'product ' || g, (10 + random()*90)::numeric, (g % 20 = 0)
FROM generate_series(1, 5000) g;

ANALYZE products;
```

## 🧠 Challenge

Write a query that filters featured products above a price threshold. Run EXPLAIN (ANALYZE, BUFFERS) and interpret whether the estimates match reality.

## 🧭 Hints (Progressive)

1. Try SELECT * FROM products WHERE featured AND price > 80;
2. Look at rows vs loops vs actual rows in the plan output.
3. ANALYZE updates stats; rerun EXPLAIN after ANALYZE if you change data.

## ✅ Expected Observation / Outcome

- You observed planner row estimates and compared them to actuals.
- You gained confidence reading node costs, loops, and rows columns.

## 🤔 Why This Matters

- Plan inspection catches performance issues before they hit users.
- Knowing what EXPLAIN says helps you decide between indexes, rewrites, or stats refreshes.
