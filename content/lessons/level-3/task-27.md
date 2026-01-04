---
title: "Task 27 — Dead Tuples After Deletes"
weight: 27
level: "🔴 Level 3 — Postgres Internals"
summary: "Delete rows and watch dead tuple counters rise."
---

# Task 27 — Dead Tuples After Deletes

Level:
🔴 Level 3 — Postgres Internals

Estimated Time:
~5 minutes

Concept(s):
- Dead tuples
- pg_stat_all_tables
- Bloat signals

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson27;
SET search_path TO lesson27;

CREATE TABLE clicks (id SERIAL PRIMARY KEY, path TEXT);

INSERT INTO clicks (path)
SELECT '/product/' || g FROM generate_series(1, 5000) g;

ANALYZE clicks;
```

## 🧠 Challenge

Delete half the rows, check pg_stat_all_tables for n_dead_tup, then vacuum and recheck.

## 🧭 Hints (Progressive)

1. DELETE FROM clicks WHERE id % 2 = 0;
2. SELECT n_dead_tup FROM pg_stat_all_tables WHERE relname = 'clicks';
3. VACUUM clicks; then query stats again.

## ✅ Expected Observation / Outcome

- n_dead_tup increased after the delete.
- VACUUM cleared dead tuples and reset the counter.

## 🤔 Why This Matters

- Deletes and updates leave behind dead tuples until vacuumed.
- Watching these counters helps you spot bloat before it hurts performance.
