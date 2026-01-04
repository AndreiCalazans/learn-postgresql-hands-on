---
title: "Task 35 — Locks and Lock Modes"
weight: 35
level: "🔴 Level 3 — Postgres Internals"
summary: "Observe how table vs row locks interact."
---

# Task 35 — Locks and Lock Modes

Level:
🔴 Level 3 — Postgres Internals

Estimated Time:
~5 minutes

Concept(s):
- Lock levels
- pg_locks
- Blocking chains

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson35;
SET search_path TO lesson35;

CREATE TABLE docs (id SERIAL PRIMARY KEY, body TEXT);
INSERT INTO docs (body) VALUES ('v1');
```

## 🧠 Challenge

Open two sessions. In session A, LOCK TABLE docs IN SHARE MODE; keep it open. In session B, try to ALTER TABLE docs ADD COLUMN note TEXT and watch the block, then check pg_locks.

## 🧭 Hints (Progressive)

1. Session A holds a lock that conflicts with the DDL session B wants.
2. Query pg_locks in either session to see the waiting lock with granted = false.
3. Release the lock in session A to let the DDL proceed.

## ✅ Expected Observation / Outcome

- DDL waited behind an existing SHARE lock.
- pg_locks showed blocking relationships between sessions.

## 🤔 Why This Matters

- Understanding lock modes prevents surprise outages during migrations.
- Inspecting pg_locks is a fast way to debug blocked sessions in production.
