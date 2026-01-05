---
title: "Task 18 — Inefficient Pagination"
weight: 18
level: "🟡 Level 2 — PostgreSQL Mistakes"
summary: "Feel OFFSET cost and switch to keyset pagination."
---

# Task 18 — Inefficient Pagination

Level:
🟡 Level 2 — PostgreSQL Mistakes

Estimated Time:
~5 minutes

Concept(s):
- OFFSET/LIMIT
- Keyset pagination
- Index usage

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson18;
SET search_path TO lesson18;

CREATE TABLE feed_items (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  body TEXT
);

INSERT INTO feed_items (created_at, body)
SELECT now() - (g || ' seconds')::interval, 'post ' || g
FROM generate_series(1, 5000) g;
```

## 🧠 Challenge

Compare OFFSET/LIMIT pagination to keyset pagination using the created_at and id columns.

## 🧭 Hints (Progressive)

1. 	iming ON; then run SELECT * FROM feed_items ORDER BY created_at DESC OFFSET 3000 LIMIT 20;
2. Use WHERE created_at < (SELECT created_at FROM feed_items ORDER BY created_at DESC OFFSET 100 LIMIT 1) ORDER BY created_at DESC LIMIT 20;
3. Create an index on created_at to speed both approaches.

## ✅ Expected Observation / Outcome

- OFFSET scanned thousands of rows only to discard them.
- Keyset pagination jumped directly to the next page using an index.

## 🤔 Why This Matters

- OFFSET grows linearly with page number and hurts user-facing latency.
- Keyset pagination is predictable and index-friendly for infinite scrolls.
