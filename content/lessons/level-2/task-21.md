---
title: "Task 21 — Misusing JSONB as a Bucket"
weight: 21
level: "🟡 Level 2 — PostgreSQL Mistakes"
summary: "See how deep JSONB filters can hurt without indexes or normalized columns."
---

# Task 21 — Misusing JSONB as a Bucket

Level:
🟡 Level 2 — PostgreSQL Mistakes

Estimated Time:
~5 minutes

Concept(s):
- JSONB performance
- Functional indexes
- Normalization

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson21;
SET search_path TO lesson21;

CREATE TABLE sessions (
  id SERIAL PRIMARY KEY,
  metadata JSONB NOT NULL
);

INSERT INTO sessions (metadata)
SELECT jsonb_build_object('user', 'user' || (g % 100), 'device', jsonb_build_object('os', CASE WHEN g % 2 = 0 THEN 'ios' ELSE 'android' END, 'version', g % 5))
FROM generate_series(1, 8000) g;
```

## 🧠 Challenge

Filter for ios devices with version 3 using a JSON path filter, then add a generated column for os and index it to compare speed.

## 🧭 Hints (Progressive)

1. SELECT * FROM sessions WHERE metadata -> 'device' ->> 'os' = 'ios' AND (metadata -> 'device' ->> 'version')::int = 3;
2. ALTER TABLE sessions ADD COLUMN os TEXT GENERATED ALWAYS AS (metadata -> 'device' ->> 'os') STORED;
3. Create an index on the generated os column and rerun the filter.

## ✅ Expected Observation / Outcome

- JSON path filtering alone used a sequential scan.
- Generated column plus index made the same predicate faster and plan simpler.

## 🤔 Why This Matters

- Not every field belongs inside JSONB—hot predicates deserve first-class columns.
- Functional or generated indexes keep flexible schemas fast as data grows.
