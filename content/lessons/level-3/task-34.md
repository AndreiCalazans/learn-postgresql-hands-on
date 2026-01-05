---
title: "Task 34 — Planner Cost Tweaks"
weight: 34
level: "🔴 Level 3 — Postgres Internals"
summary: "Adjust cost settings to watch plan choices flip."
---

# Task 34 — Planner Cost Tweaks

Level:
🔴 Level 3 — Postgres Internals

Estimated Time:
~5 minutes

Concept(s):
- random_page_cost
- seq_page_cost
- Plan selection

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson34;
SET search_path TO lesson34;

CREATE TABLE readings (
  id SERIAL PRIMARY KEY,
  sensor TEXT,
  value NUMERIC
);

INSERT INTO readings (sensor, value)
SELECT 's' || (g % 3), (random()*100)::numeric FROM generate_series(1, 20000) g;
CREATE INDEX ON readings (sensor);
ANALYZE readings;
```

## 🧠 Challenge

Check the plan for a common sensor filter, then lower random_page_cost to make index access more attractive and compare.

## 🧭 Hints (Progressive)

1. EXPLAIN SELECT * FROM readings WHERE sensor = 's1';
2. SET random_page_cost = 1.0; run the EXPLAIN again.
3. RESET random_page_cost afterward to avoid affecting other sessions.

## ✅ Expected Observation / Outcome

- Lowering random_page_cost nudged the planner toward index scans if not already using them.
- You saw how cost parameters influence plan selection without schema changes.

## 🤔 Why This Matters

- Cost settings are a tuning lever when storage or caching changes.
- Understanding them helps interpret plans on fast disks vs slower media.
