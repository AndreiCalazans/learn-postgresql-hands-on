---
title: "Task 25 — MVCC Visibility"
weight: 25
level: "🔴 Level 3 — Postgres Internals"
summary: "Watch how two transactions see different row versions."
---

# Task 25 — MVCC Visibility

Level:
🔴 Level 3 — Postgres Internals

Estimated Time:
~5 minutes

Concept(s):
- MVCC snapshots
- Transaction isolation
- Stale reads

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson25;
SET search_path TO lesson25;

CREATE TABLE notes (id SERIAL PRIMARY KEY, body TEXT);
INSERT INTO notes (body) VALUES ('original');
```

## 🧠 Challenge

Open two sessions. In session A, BEGIN; UPDATE notes SET body = 'updated in A' WHERE id = 1; do not commit. In session B, read the row in REPEATABLE READ and observe which version you see before and after A commits.

## 🧭 Hints (Progressive)

1. In session B: BEGIN ISOLATION LEVEL REPEATABLE READ; SELECT * FROM notes;
2. Commit session A, then reread in session B and notice you still see the old value until you commit.
3. After committing session B, read again to see the new version.

## ✅ Expected Observation / Outcome

- Session B held a snapshot that hid A's uncommitted change until it ended.
- Committing B advanced its snapshot and revealed the new version.

## 🤔 Why This Matters

- MVCC isolates readers from writers, but long snapshots can hide fresh data.
- Understanding visibility rules helps debug stale read reports in production.
