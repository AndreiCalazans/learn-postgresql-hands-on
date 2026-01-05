---
title: "Task 32 — Index-Only vs Heap Fetch"
weight: 32
level: "🔴 Level 3 — Postgres Internals"
summary: "Contrast index-only scans with heap visits using an included column."
---

# Task 32 — Index-Only vs Heap Fetch

Level:
🔴 Level 3 — Postgres Internals

Estimated Time:
~5 minutes

Concept(s):
- Index-only scans
- Visibility map
- INCLUDE columns

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson32;
SET search_path TO lesson32;

CREATE TABLE emails (
  id SERIAL PRIMARY KEY,
  address TEXT NOT NULL,
  last_opened TIMESTAMPTZ
);

INSERT INTO emails (address, last_opened)
SELECT 'user' || g || '@example.com', now() - (g || ' minutes')::interval
FROM generate_series(1, 5000) g;

CREATE INDEX ON emails (address);
CREATE INDEX ON emails (address) INCLUDE (last_opened);
VACUUM ANALYZE emails;
```

## 🧠 Challenge

Compare EXPLAIN (ANALYZE, BUFFERS) for a query selecting address only versus selecting address and last_opened. Note when index-only scans appear.

## 🧭 Hints (Progressive)

1. Run EXPLAIN (ANALYZE, BUFFERS) SELECT address FROM emails WHERE address LIKE 'user1%';
2. Then select address, last_opened with the same predicate.
3. Index-only scans require pages to be marked all-visible; VACUUM helps.

## ✅ Expected Observation / Outcome

- Address-only query could use an index-only scan.
- Including last_opened forced heap fetch unless the INCLUDE index satisfied it.

## 🤔 Why This Matters

- Covering indexes cut heap visits and reduce I/O on hot paths.
- Knowing when index-only scans occur informs which columns to include for read-heavy workloads.
