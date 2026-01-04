---
title: "Task 17 — NULL Semantics Surprise"
weight: 17
level: "🟡 Level 2 — PostgreSQL Mistakes"
summary: "Explore how NULL behaves in filters and equality checks."
---

# Task 17 — NULL Semantics Surprise

Level:
🟡 Level 2 — PostgreSQL Mistakes

Estimated Time:
~5 minutes

Concept(s):
- NULL comparisons
- IS DISTINCT FROM
- Three-valued logic

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson17;
SET search_path TO lesson17;

CREATE TABLE flags (
  id SERIAL PRIMARY KEY,
  feature TEXT NOT NULL,
  enabled_at TIMESTAMPTZ
);

INSERT INTO flags (feature, enabled_at) VALUES
  ('checkout', now()),
  ('search', NULL),
  ('billing', NULL);
```

## 🧠 Challenge

Count rows where enabled_at != NULL and compare to IS NOT NULL. Use IS DISTINCT FROM to handle NULL safely.

## 🧭 Hints (Progressive)

1. SELECT COUNT(*) WHERE enabled_at != NULL will return 0.
2. Use enabled_at IS NOT NULL to find set values.
3. IS DISTINCT FROM treats NULL as a comparable value for equality semantics.

## ✅ Expected Observation / Outcome

- enabled_at != NULL matched nothing because comparisons with NULL are unknown.
- IS DISTINCT FROM counted the rows you expected.

## 🤔 Why This Matters

- NULL semantics differ from most programming languages.
- Getting this wrong leads to missing data and incorrect analytics in production.
