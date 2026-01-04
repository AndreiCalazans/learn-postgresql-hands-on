---
title: "Task 22 — Locking Surprises"
weight: 22
level: "🟡 Level 2 — PostgreSQL Mistakes"
summary: "Observe how SELECT ... FOR UPDATE blocks concurrent writes."
---

# Task 22 — Locking Surprises

Level:
🟡 Level 2 — PostgreSQL Mistakes

Estimated Time:
~5 minutes

Concept(s):
- Row locks
- Lock modes
- Timeouts

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson22;
SET search_path TO lesson22;

CREATE TABLE inventory (
  id SERIAL PRIMARY KEY,
  sku TEXT NOT NULL UNIQUE,
  quantity INT NOT NULL
);

INSERT INTO inventory (sku, quantity) VALUES ('sku-1', 5), ('sku-2', 10);
```

## 🧠 Challenge

Open two sessions. In session A, SELECT * FROM inventory WHERE sku='sku-1' FOR UPDATE; keep it open. In session B, try to update that row and watch it block until session A commits.

## 🧭 Hints (Progressive)

1. \watch pg_locks to see granted vs waiting locks.
2. Session A finishes when you COMMIT or ROLLBACK.
3. Session B will complete immediately after the lock is released.

## ✅ Expected Observation / Outcome

- FOR UPDATE took a row-level lock visible in pg_locks.
- Concurrent UPDATE waited until the lock was released.

## 🤔 Why This Matters

- Lock-heavy code paths can serialize traffic unexpectedly.
- Understanding row locks helps you design retry and backoff strategies.
