---
title: "Task 33 — Sequential vs Index Scan"
weight: 33
level: "🔴 Level 3 — Postgres Internals"
summary: "Toggle planner preferences to see how scan types change."
---

# Task 33 — Sequential vs Index Scan

Level:
🔴 Level 3 — Postgres Internals

Estimated Time:
~5 minutes

Concept(s):
- Planner toggles
- enable_seqscan
- Cost comparison

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson33;
SET search_path TO lesson33;

CREATE TABLE inventory_items (
  id SERIAL PRIMARY KEY,
  name TEXT,
  quantity INT
);

INSERT INTO inventory_items (name, quantity)
SELECT 'item ' || g, (random()*100)::int FROM generate_series(1, 15000) g;
CREATE INDEX ON inventory_items (quantity);
ANALYZE inventory_items;
```

## 🧠 Challenge

Run the same predicate with and without enable_seqscan to see plan shifts for a selective filter.

## 🧭 Hints (Progressive)

1. SET enable_seqscan = on; EXPLAIN SELECT * FROM inventory_items WHERE quantity = 99;
2. SET enable_seqscan = off; run the EXPLAIN again.
3. Reset the GUC with RESET enable_seqscan when done.

## ✅ Expected Observation / Outcome

- Planner chose sequential scan when allowed, index scan when forced.
- You saw how planner cost parameters influence decisions.

## 🤔 Why This Matters

- Tuning planner settings can highlight missing stats or index usefulness.
- Understanding why the planner chooses a scan type helps justify indexes or rewrites.
