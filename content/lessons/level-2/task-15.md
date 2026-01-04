---
title: "Task 15 — Over-Indexing Adds Write Cost"
weight: 15
level: "🟡 Level 2 — PostgreSQL Mistakes"
summary: "See how too many indexes slow inserts and consume space."
---

# Task 15 — Over-Indexing Adds Write Cost

Level:
🟡 Level 2 — PostgreSQL Mistakes

Estimated Time:
~5 minutes

Concept(s):
- Index overhead
- pg_relation_size
- Write amplification

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson15;
SET search_path TO lesson15;

CREATE TABLE audit_events (
  id SERIAL PRIMARY KEY,
  actor TEXT NOT NULL,
  path TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ON audit_events (actor);
CREATE INDEX ON audit_events (path);
CREATE INDEX ON audit_events (created_at);
CREATE INDEX ON audit_events (actor, created_at);

INSERT INTO audit_events (actor, path)
SELECT 'user' || (g % 10), '/v1/resource/' || g
FROM generate_series(1, 15000) g;
```

## 🧠 Challenge

Measure table vs index size, then drop one index and insert again to compare insert timing.

## 🧭 Hints (Progressive)

1. Use pg_relation_size and pg_indexes_size on audit_events.
2. DROP INDEX audit_events_actor_created_at_idx; then insert another batch.
3. Compare insertion timing with \timing on before/after batches.

## ✅ Expected Observation / Outcome

- Indexes consumed more disk than the table itself.
- Dropping an overlapping index improved insert speed slightly.

## 🤔 Why This Matters

- Each extra index must be maintained on every write.
- Pruning redundant indexes reduces storage, cache churn, and lock time in production.
