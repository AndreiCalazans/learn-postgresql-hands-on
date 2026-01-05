---
title: "Task 26 — xmin/xmax Introspection"
weight: 26
level: "🔴 Level 3 — Postgres Internals"
summary: "Inspect xmin/xmax to see which transactions touched a row."
---

# Task 26 — xmin/xmax Introspection

Level:
🔴 Level 3 — Postgres Internals

Estimated Time:
~5 minutes

Concept(s):
- Transaction IDs
- Tuple metadata
- Versioning

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson26;
SET search_path TO lesson26;

CREATE TABLE ledger (id SERIAL PRIMARY KEY, amount INT);
INSERT INTO ledger (amount) VALUES (10);
```

## 🧠 Challenge

Select xmin/xmax before and after an update to see how tuple metadata changes.

## 🧭 Hints (Progressive)

1. SELECT xmin, xmax, * FROM ledger;
2. UPDATE ledger SET amount = 20 WHERE id = 1; then select xmin/xmax again.
3. Observe that xmax is 0 for live rows; xmin changes with each version.

## ✅ Expected Observation / Outcome

- xmin updated to the transaction that performed the write.
- Old version became dead with a nonzero xmax visible only until vacuum removes it.

## 🤔 Why This Matters

- xmin/xmax make MVCC tangible and debuggable.
- They help explain why bloat builds up when dead tuples stick around.
