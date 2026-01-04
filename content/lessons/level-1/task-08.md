---
title: "Task 08 — Time-Series Patterns Without Extensions"
weight: 8
level: "🟢 Level 1 — Just Use Postgres"
summary: "Slice event data by day and speed up recent lookups with a partial index."
---

# Task 08 — Time-Series Patterns Without Extensions

Level:
🟢 Level 1 — Just Use Postgres

Estimated Time:
~5 minutes

Concept(s):
- date_trunc
- Partial indexes
- Rolling windows

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson08;
SET search_path TO lesson08;

CREATE TABLE readings (
  id SERIAL PRIMARY KEY,
  recorded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  value NUMERIC NOT NULL
);

INSERT INTO readings (recorded_at, value)
SELECT now() - (g || ' minutes')::interval, (random()*10)::numeric
FROM generate_series(0, 1440) g;
```

## 🧠 Challenge

Compute average value per hour for the past day, then create a partial index on recent data and rerun the query.

## 🧭 Hints (Progressive)

1. Use WHERE recorded_at >= now() - interval '1 day'.
2. Group by date_trunc('hour', recorded_at).
3. Create INDEX ON readings (recorded_at) WHERE recorded_at >= now() - interval '1 day'.

## ✅ Expected Observation / Outcome

- You produced hourly aggregates over the last 24 hours.
- Partial index reduced the scanned rows for recent-only queries.

## 🤔 Why This Matters

- Time filters dominate many dashboards—partial indexes keep them cheap.
- date_trunc is a lightweight tool before reaching for full time-series stacks.
