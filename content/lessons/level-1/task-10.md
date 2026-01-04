---
title: "Task 10 — CTE vs Subquery: Same Result, Different Intent"
weight: 10
level: "🟢 Level 1 — Just Use Postgres"
summary: "Compare a CTE and inline subquery to see how the planner treats them."
---

# Task 10 — CTE vs Subquery: Same Result, Different Intent

Level:
🟢 Level 1 — Just Use Postgres

Estimated Time:
~5 minutes

Concept(s):
- CTEs
- Inlining vs materialization
- EXPLAIN

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson10;
SET search_path TO lesson10;

CREATE TABLE purchases (
  id SERIAL PRIMARY KEY,
  customer_id INT NOT NULL,
  total NUMERIC NOT NULL
);

INSERT INTO purchases (customer_id, total)
SELECT (random()*20)::int, (10 + random()*90)::numeric
FROM generate_series(1, 3000) g;
```

## 🧠 Challenge

Write a query that filters customers above average spend using a CTE, then rewrite it as an inline subquery. Compare EXPLAIN plans and timing.

## 🧭 Hints (Progressive)

1. WITH avg_spend AS (SELECT avg(total) AS avg_total FROM purchases) SELECT ...
2. Use EXPLAIN (ANALYZE, VERBOSE) on both versions.
3. Note whether the CTE is inlined (it often is in newer PostgreSQL).

## ✅ Expected Observation / Outcome

- Both queries returned the same rows.
- Plans likely looked similar—inlining shows the planner can optimize CTEs.

## 🤔 Why This Matters

- CTEs communicate intent and can be optimized; materialization is not guaranteed.
- Understanding when CTEs inline prevents surprises when refactoring complex queries.
