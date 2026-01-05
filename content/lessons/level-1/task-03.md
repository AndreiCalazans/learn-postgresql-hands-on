---
title: "Task 03 — Enums with Guard Rails"
weight: 3
level: "🟢 Level 1 — Just Use Postgres"
summary: "Use ENUM plus CHECK constraints to encode allowed states and transitions."
---

# Task 03 — Enums with Guard Rails

Level:
🟢 Level 1 — Just Use Postgres

Estimated Time:
~5 minutes

Concept(s):
- ENUM type
- CHECK constraints
- State transitions

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson03;
SET search_path TO lesson03;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'order_status') THEN
    CREATE TYPE order_status AS ENUM ('pending','paid','shipped','cancelled');
  END IF;
END $$;

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  status order_status NOT NULL DEFAULT 'pending',
  paid_at TIMESTAMPTZ,
  shipped_at TIMESTAMPTZ,
  CONSTRAINT status_flow CHECK (
    (status = 'paid' AND paid_at IS NOT NULL) OR
    (status = 'shipped' AND paid_at IS NOT NULL AND shipped_at IS NOT NULL) OR
    status IN ('pending','cancelled')
  )
);

INSERT INTO orders (status, paid_at, shipped_at) VALUES
  ('pending', NULL, NULL),
  ('paid', now(), NULL),
  ('shipped', now() - interval '1 hour', now());
```

## 🧠 Challenge

Try inserting an impossible state (shipped without paid_at). Find the constraint failure, then fix the data and insert successfully.

## 🧭 Hints (Progressive)

1. INSERT a shipped row with NULL paid_at to see the CHECK fire.
2. Update the row to set paid_at before shipped_at to satisfy the constraint.
3. Use the ENUM to block typos like 'shippped' from ever being stored.

## ✅ Expected Observation / Outcome

- You observed a constraint violation on invalid state transitions.
- Valid data flowed through without custom code.

## 🤔 Why This Matters

- Constraints keep business rules close to the data.
- Encoding flows in the database reduces downstream data cleanup work.
