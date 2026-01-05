---
title: "Task 06 — BTREE vs GIN for Tag Filters"
weight: 6
level: "🟢 Level 1 — Just Use Postgres"
summary: "Compare BTREE and GIN behavior when filtering array tags."
---

# Task 06 — BTREE vs GIN for Tag Filters

Level:
🟢 Level 1 — Just Use Postgres

Estimated Time:
~5 minutes

Concept(s):
- BTREE indexes
- GIN indexes
- Containment queries

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson06;
SET search_path TO lesson06;

CREATE TABLE articles (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  tags TEXT[] NOT NULL
);

INSERT INTO articles (title, tags)
SELECT 'post ' || g, ARRAY['pg', 'cli', CASE WHEN g % 2 = 0 THEN 'json' ELSE 'fts' END]
FROM generate_series(1, 3000) g;
```

## 🧠 Challenge

Filter articles containing both 'pg' and 'json'. Measure plan and timing before and after adding a GIN index on tags.

## 🧭 Hints (Progressive)

1. Start with EXPLAIN ANALYZE on WHERE tags @> ARRAY['pg','json'].
2. Create a GIN index using the default array_ops operator class.
3. Compare with a BTREE index on tags (and notice why it is ineffective).

## ✅ Expected Observation / Outcome

- Sequential scan before indexing; GIN index scan after.
- BTREE index did not help the @> operator.

## 🤔 Why This Matters

- Operator classes matter—containment needs GIN/GiST, not BTREE.
- Choosing the right index saves CPU and makes tag filters predictable in production.
