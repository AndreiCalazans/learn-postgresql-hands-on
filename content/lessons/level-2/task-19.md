---
title: "Task 19 — Bad Transaction Boundaries"
weight: 19
level: "🟡 Level 2 — PostgreSQL Mistakes"
summary: "See how holding a transaction open blocks others."
---

# Task 19 — Bad Transaction Boundaries

Level:
🟡 Level 2 — PostgreSQL Mistakes

Estimated Time:
~5 minutes

Concept(s):
- Long transactions
- Locks
- Visibility

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson19;
SET search_path TO lesson19;

CREATE TABLE accounts (
  id SERIAL PRIMARY KEY,
  balance NUMERIC NOT NULL
);

INSERT INTO accounts (balance) VALUES (100), (200);
```

## 🧠 Challenge

Open two psql sessions on this schema. In session A, BEGIN; UPDATE accounts SET balance = balance + 10 WHERE id = 1; do not commit. In session B, try to update the same row and observe the wait using pg_locks.

## 🧭 Hints (Progressive)

1. In session B, run SELECT pid, relation::regclass, mode, granted FROM pg_locks WHERE relation::regclass = 'accounts'::regclass;
2. Notice session B is blocked until session A commits or rolls back.
3. End session A with COMMIT or ROLLBACK and watch session B proceed.

## ✅ Expected Observation / Outcome

- The second update waited for the first transaction to finish.
- Releasing the transaction cleared the lock and let work continue.

## 🤔 Why This Matters

- Long-running transactions hold locks and bloat tables.
- Keeping transaction scopes tight prevents cascading slowdowns in production.
