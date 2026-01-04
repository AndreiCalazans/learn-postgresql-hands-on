---
title: "Task 31 — Buffer Cache Effects"
weight: 31
level: "🔴 Level 3 — Postgres Internals"
summary: "Run the same query twice and compare buffer hits vs reads."
---

# Task 31 — Buffer Cache Effects

Level:
🔴 Level 3 — Postgres Internals

Estimated Time:
~5 minutes

Concept(s):
- Shared buffers
- Cache hits
- EXPLAIN BUFFERS

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson31;
SET search_path TO lesson31;

CREATE TABLE sales (id SERIAL PRIMARY KEY, amount NUMERIC);
INSERT INTO sales (amount)
SELECT (random()*100)::numeric FROM generate_series(1, 20000) g;
ANALYZE sales;
```

## 🧠 Challenge

Enable timing and run a filtered query twice with EXPLAIN (ANALYZE, BUFFERS) to observe shared hit vs read counts.

## 🧭 Hints (Progressive)

1. 	iming ON;
2. EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM sales WHERE amount > 90; run it twice.
3. The second run should show more shared hits and fewer reads.

## ✅ Expected Observation / Outcome

- First run hit more disk reads; second run showed mostly shared hits.
- Execution time improved once data was warm in cache.

## 🤔 Why This Matters

- Cache warmth explains why first requests are slower after deploys or failovers.
- Observing buffers helps differentiate I/O waits from CPU-bound work.
