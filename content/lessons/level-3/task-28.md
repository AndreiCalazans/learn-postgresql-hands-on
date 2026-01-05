---
title: "Task 28 — VACUUM Effects"
weight: 28
level: "🔴 Level 3 — Postgres Internals"
summary: "Run VACUUM VERBOSE to see what it reclaims and why."
---

# Task 28 — VACUUM Effects

Level:
🔴 Level 3 — Postgres Internals

Estimated Time:
~5 minutes

Concept(s):
- VACUUM
- Visibility maps
- Table size

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson28;
SET search_path TO lesson28;

CREATE TABLE tasks (id SERIAL PRIMARY KEY, done BOOLEAN DEFAULT FALSE);
INSERT INTO tasks (done)
SELECT (g % 2 = 0) FROM generate_series(1, 4000) g;
DELETE FROM tasks WHERE done = TRUE;
```

## 🧠 Challenge

Run VACUUM VERBOSE on the table and read the output. Measure pg_class.reltuples before and after.

## 🧭 Hints (Progressive)

1. SELECT reltuples, relpages FROM pg_class WHERE relname = 'tasks';
2. VACUUM (VERBOSE) tasks;
3. Query pg_class again to compare reltuples estimate changes.

## ✅ Expected Observation / Outcome

- VACUUM VERBOSE reported dead tuples removed and pages scanned.
- relpages or reltuples estimates adjusted after vacuuming.

## 🤔 Why This Matters

- VACUUM keeps visibility maps accurate and tables lean.
- Reading its output demystifies what the maintainer process does automatically.
