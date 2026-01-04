---
title: "Task 14 — Missing Indexes Hurt"
weight: 14
level: "🟡 Level 2 — PostgreSQL Mistakes"
summary: "Feel the latency of a missing index then fix it."
---

# Task 14 — Missing Indexes Hurt

Level:
🟡 Level 2 — PostgreSQL Mistakes

Estimated Time:
~5 minutes

Concept(s):
- Sequential scan
- Index creation
- Query speed

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson14;
SET search_path TO lesson14;

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INT NOT NULL,
  total NUMERIC NOT NULL
);

INSERT INTO orders (customer_id, total)
SELECT (random()*500)::int, (10 + random()*190)::numeric
FROM generate_series(1, 20000) g;
```

## 🧠 Challenge

Run a filter on customer_id without an index, note timing, then add an index and re-run the same query.

## 🧭 Hints (Progressive)

1. Use EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 42;
2. CREATE INDEX ON orders (customer_id);
3. Compare row scans and total time before/after.

## ✅ Expected Observation / Outcome

- The first run used a sequential scan and was slower.
- After indexing, the plan switched to an index scan with fewer blocks read.

## 🤔 Why This Matters

- Most production slowdowns start with missing indexes on common filters.
- Measuring before and after builds intuition for when an index pays off.
