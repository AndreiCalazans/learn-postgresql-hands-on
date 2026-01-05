---
title: "Task 30 — WAL Growth from Writes"
weight: 30
level: "🔴 Level 3 — Postgres Internals"
summary: "Measure WAL position before and after a burst of writes."
---

# Task 30 — WAL Growth from Writes

Level:
🔴 Level 3 — Postgres Internals

Estimated Time:
~5 minutes

Concept(s):
- Write-Ahead Log
- LSN
- Durability

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson30;
SET search_path TO lesson30;

CREATE TABLE events (id SERIAL PRIMARY KEY, body TEXT);
SELECT pg_current_wal_lsn() AS lsn_before;
```

## 🧠 Challenge

Insert a few thousand rows, then compare pg_current_wal_lsn() to see WAL advancement. Optionally check pg_walfile_name(lsn).

## 🧭 Hints (Progressive)

1. INSERT INTO events (body) SELECT 'event ' || g FROM generate_series(1, 3000) g;
2. SELECT pg_current_wal_lsn() AS lsn_after;
3. Use pg_wal_lsn_diff to compute the byte difference between lsn_after and lsn_before.

## ✅ Expected Observation / Outcome

- WAL LSN advanced by several MB after the inserts.
- You saw how every write is logged for crash safety and replication.

## 🤔 Why This Matters

- WAL growth ties directly to write volume and replication lag.
- Measuring WAL churn helps plan disk capacity and replica bandwidth.
