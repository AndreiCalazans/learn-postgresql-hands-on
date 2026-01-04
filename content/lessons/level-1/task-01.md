---
title: "Task 01 — JSONB vs TEXT: Store and Query"
weight: 1
level: "🟢 Level 1 — Just Use Postgres"
summary: "Contrast JSONB with TEXT storage and see how indexing changes query speed."
---

# Task 01 — JSONB vs TEXT: Store and Query

Level:
🟢 Level 1 — Just Use Postgres

Estimated Time:
~5 minutes

Concept(s):
- JSONB vs TEXT
- GIN indexing
- Predicate performance

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson01;
SET search_path TO lesson01;

CREATE TABLE events_json (
  id SERIAL PRIMARY KEY,
  payload_json JSONB,
  payload_text TEXT
);

INSERT INTO events_json (payload_json, payload_text)
SELECT jsonb_build_object('user', 'user' || g, 'flag', (g % 2 = 0)),
       json_build_object('user', 'user' || g, 'flag', (g % 2 = 0))::text
FROM generate_series(1, 5000) g;
```

## 🧠 Challenge

Compare filtering JSON data stored as JSONB versus TEXT. Make one query fast without changing the WHERE clause.

## 🧭 Hints (Progressive)

1. Run EXPLAIN ANALYZE on a filter like payload_json ->> 'user' = 'user4200'.
2. Create a GIN index on the JSONB column and rerun the filter.
3. Use pg_class to compare relation sizes after indexing.

## ✅ Expected Observation / Outcome

- You saw a sequential scan on TEXT and a GIN index scan on JSONB after indexing.
- Execution time dropped noticeably once the GIN index existed.

## 🤔 Why This Matters

- JSONB supports binary storage and indexing; TEXT requires parsing on every read.
- Choosing the right type makes semi-structured data fast without schema changes.
