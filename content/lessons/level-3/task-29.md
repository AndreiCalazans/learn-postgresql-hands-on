---
title: "Task 29 — Observe Autovacuum"
weight: 29
level: "🔴 Level 3 — Postgres Internals"
summary: "Force a small table to trigger autovacuum and watch its progress."
---

# Task 29 — Observe Autovacuum

Level:
🔴 Level 3 — Postgres Internals

Estimated Time:
~5 minutes

Concept(s):
- autovacuum thresholds
- pg_stat_progress_vacuum
- Table settings

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson29;
SET search_path TO lesson29;

CREATE TABLE msgs (id SERIAL PRIMARY KEY, body TEXT);
ALTER TABLE msgs SET (autovacuum_vacuum_scale_factor = 0.0, autovacuum_vacuum_threshold = 10);
INSERT INTO msgs (body)
SELECT 'msg ' || g FROM generate_series(1, 200) g;
```

## 🧠 Challenge

Delete enough rows to cross the autovacuum threshold, wait briefly, and query pg_stat_progress_vacuum or pg_stat_all_tables to see autovacuum activity.

## 🧭 Hints (Progressive)

1. DELETE FROM msgs WHERE id <= 120;
2. Repeatedly query SELECT last_autovacuum, vacuum_count FROM pg_stat_all_tables WHERE relname = 'msgs';
3. If autovacuum runs quickly, you may only catch the timestamp update rather than a live row in pg_stat_progress_vacuum.

## ✅ Expected Observation / Outcome

- After deleting rows, autovacuum triggered and updated last_autovacuum/vacuum_count.
- You may briefly see a row in pg_stat_progress_vacuum while it runs.

## 🤔 Why This Matters

- Autovacuum keeps the system healthy without manual work, but only if thresholds fit your workload.
- Knowing how to check its progress helps when diagnosing bloat or lock issues.
