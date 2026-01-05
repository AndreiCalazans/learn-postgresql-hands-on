---
title: "PostgreSQL in 36 Lessons"
summary: "A five-minute-per-task curriculum to master PostgreSQL hands-on."
---

Welcome! This Hugo site contains 36 hands-on CLI tasks split into three levels. Each page is self-contained: copy the SQL from **Setup**, run it in `psql` on macOS, tackle the **Challenge**, and consult the **Hints** only if needed.

- **Level 1 — Just Use Postgres (Tasks 1–12):** Explore built-in capabilities such as JSONB, indexes, full-text search, time-series patterns, generated columns, and constraints as logic.
- **Level 2 — PostgreSQL Mistakes (Tasks 13–24):** Experience common performance and correctness pitfalls—missing indexes, NULL traps, inefficient pagination, locking issues, and privilege design.
- **Level 3 — Postgres Internals (Tasks 25–36):** Observe the engine itself: MVCC visibility, xmin/xmax, dead tuples, vacuum/autovacuum, WAL growth, buffer caches, planner decisions, and lock modes.

## How to use this curriculum

1. Use a disposable database or schema for each task—most setup blocks already do this with `CREATE SCHEMA lessonXX` and `SET search_path`.
2. Keep `\timing on` in `psql` to see performance differences quickly.
3. Open multiple `psql` sessions for locking and transaction exercises. Prefix prompts with session labels to avoid confusion.
4. Cleanup is simple: drop the lesson schema if you want a fresh start (e.g., `DROP SCHEMA lesson07 CASCADE;`).

## Level recap prompts

**After Level 1:** How would you combine generated columns, constraints, and UPSERT to keep a denormalized reporting table trustworthy under concurrent writes?

**After Level 2:** Which three mistakes from this level are most likely in your codebase today, and what lightweight guardrails (indexes, role grants, query rewrites) would mitigate them?

**After Level 3:** When a query regresses in production, how would you use EXPLAIN (ANALYZE, BUFFERS) plus pg_locks/pg_stat views to decide between index changes, vacuuming, or transaction boundary fixes?

Dive into the lessons below to get started.
