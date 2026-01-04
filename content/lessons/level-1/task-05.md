---
title: "Task 05 — UPSERT Without Race Conditions"
weight: 5
level: "🟢 Level 1 — Just Use Postgres"
summary: "Use INSERT ... ON CONFLICT to de-duplicate writes safely."
---

# Task 05 — UPSERT Without Race Conditions

Level:
🟢 Level 1 — Just Use Postgres

Estimated Time:
~5 minutes

Concept(s):
- ON CONFLICT
- Unique constraints
- Idempotent writes

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson05;
SET search_path TO lesson05;

CREATE TABLE profiles (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  logins INT NOT NULL DEFAULT 0,
  last_seen TIMESTAMPTZ
);

INSERT INTO profiles (email, logins, last_seen) VALUES
  ('casey@example.com', 1, now() - interval '1 day');
```

## 🧠 Challenge

Upsert the same email twice: first to insert, second to increment logins and update last_seen in one statement.

## 🧭 Hints (Progressive)

1. Target the UNIQUE email column in the ON CONFLICT clause.
2. Use EXCLUDED to reference incoming values when updating.
3. RETURNING shows whether the row was inserted or updated.

## ✅ Expected Observation / Outcome

- The first command inserted; the second reused the same email and updated counters.
- No duplicate emails were created even under repeated calls.

## 🤔 Why This Matters

- UPSERTs remove race conditions that appear when you SELECT then INSERT in separate steps.
- Idempotent writes make retry logic and background jobs safe.
