---
title: "Task 24 — Roles and Privileges"
weight: 24
level: "🟡 Level 2 — PostgreSQL Mistakes"
summary: "Practice creating roles and applying least-privilege grants."
---

# Task 24 — Roles and Privileges

Level:
🟡 Level 2 — PostgreSQL Mistakes

Estimated Time:
~5 minutes

Concept(s):
- GRANT/REVOKE
- Least privilege
- Schemas

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson24;
SET search_path TO lesson24;

CREATE TABLE reports (
  id SERIAL PRIMARY KEY,
  body TEXT NOT NULL
);

INSERT INTO reports (body) VALUES ('secret report');

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_reader') THEN
    CREATE ROLE app_reader NOLOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_writer') THEN
    CREATE ROLE app_writer NOLOGIN;
  END IF;
END $$;
```

## 🧠 Challenge

Grant read-only access on reports to app_reader and write access to app_writer. Verify privileges using SET ROLE and simple selects/inserts.

## 🧭 Hints (Progressive)

1. GRANT USAGE ON SCHEMA lesson24 TO app_reader; GRANT SELECT ON reports TO app_reader;
2. GRANT INSERT, UPDATE, DELETE ON reports TO app_writer;
3. SET ROLE app_reader; try an INSERT to see it fail; RESET ROLE when done.

## ✅ Expected Observation / Outcome

- app_reader could read but not write; app_writer could modify rows.
- Schema usage and table privileges worked together to enforce access.

## 🤔 Why This Matters

- Least privilege reduces blast radius of application bugs and SQL injection.
- Practicing grants helps you design safe default roles in production clusters.
