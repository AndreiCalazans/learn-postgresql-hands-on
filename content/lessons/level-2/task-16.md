---
title: "Task 16 — Wrong Data Types Bite Later"
weight: 16
level: "🟡 Level 2 — PostgreSQL Mistakes"
summary: "Compare text vs numeric/timestamp columns for correctness and speed."
---

# Task 16 — Wrong Data Types Bite Later

Level:
🟡 Level 2 — PostgreSQL Mistakes

Estimated Time:
~5 minutes

Concept(s):
- Type casting
- Sorting
- Query planner

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson16;
SET search_path TO lesson16;

CREATE TABLE metrics_text (
  id SERIAL PRIMARY KEY,
  metric_value TEXT
);

CREATE TABLE metrics_num (
  id SERIAL PRIMARY KEY,
  metric_value NUMERIC
);

INSERT INTO metrics_text (metric_value) VALUES
  ('9.5'), ('10.2'), ('2.4'), ('30.0');
INSERT INTO metrics_num (metric_value) VALUES
  (9.5), (10.2), (2.4), (30.0);
```

## 🧠 Challenge

Order both tables by metric_value DESC and note differences. Add a WHERE metric_value > 10 filter to feel casting cost on TEXT.

## 🧭 Hints (Progressive)

1. EXPLAIN ANALYZE SELECT * FROM metrics_text WHERE metric_value > '10';
2. Note the lexical ordering of TEXT vs numeric ordering.
3. Casting text in a WHERE prevents index use later.

## ✅ Expected Observation / Outcome

- Text-sorted values were lexicographic (30.0 before 9.5).
- Numeric column sorted correctly and filtered faster.

## 🤔 Why This Matters

- Using the right type avoids subtle correctness bugs and unlocks index usage.
- Casting on the fly prevents the planner from using fast paths.
