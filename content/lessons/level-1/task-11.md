---
title: "Task 11 — Constraints as Application Logic"
weight: 11
level: "🟢 Level 1 — Just Use Postgres"
summary: "Encode a business rule directly in the table to avoid bad data."
---

# Task 11 — Constraints as Application Logic

Level:
🟢 Level 1 — Just Use Postgres

Estimated Time:
~5 minutes

Concept(s):
- CHECK constraints
- DEFAULTS
- Business rules

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson11;
SET search_path TO lesson11;

CREATE TABLE subscriptions (
  id SERIAL PRIMARY KEY,
  plan TEXT NOT NULL CHECK (plan IN ('free','pro','team')),
  seats INT NOT NULL DEFAULT 1 CHECK (seats > 0),
  expires_at DATE,
  CONSTRAINT paid_requires_expiry CHECK ((plan = 'free' AND expires_at IS NULL) OR (plan IN ('pro','team') AND expires_at IS NOT NULL))
);
```

## 🧠 Challenge

Attempt to insert a paid plan without expires_at and observe the failure. Then insert valid rows and query to confirm constraints hold.

## 🧭 Hints (Progressive)

1. INSERT INTO subscriptions(plan, seats) VALUES ('pro', 3);
2. Then insert with an expires_at date to satisfy the CHECK.
3. Use pg_constraint to read the check expression text.

## ✅ Expected Observation / Outcome

- Invalid data was rejected immediately by the CHECK.
- Valid paid rows stored their expiry date automatically.

## 🤔 Why This Matters

- Constraints keep invariants consistent across every code path.
- They make bulk imports and migrations safer by enforcing business rules at the edge.
