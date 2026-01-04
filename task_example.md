---
task_id: 07
level: 2
title: "Why This Query Is Slow Without an Index"
estimated_time_minutes: 5
completion_weight: 1
status: "not_started" # not_started | in_progress | completed
prev_task_id: 06
next_task_id: 08
---

# Task 07 — Why This Query Is Slow Without an Index

**Level:** 🟡 Level 2 — PostgreSQL Mistakes
**Estimated time:** ⏱️ ~5 minutes
**Completion:** ⬜ Not completed (0%)

---

## 🎯 Concepts
- Missing indexes
- Sequential scan vs index scan
- `EXPLAIN ANALYZE`

---

## 🧰 Prerequisites
- PostgreSQL running locally
- Access to `psql`
- Permission to create a schema/table

---

## ⚙️ Setup

Run in `psql`:

```sql
CREATE SCHEMA IF NOT EXISTS challenge_07;
SET search_path TO challenge_07;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);

INSERT INTO users (email)
SELECT 'user' || g || '@example.com'
FROM generate_series(1, 10000) g;
```
---

## 🧠 Challenge

Your goal is to **understand why the following query is slow** and make it faster **without changing the query itself**.

1. Run the query and note how long it takes:
```sql
SELECT *
FROM users
WHERE email = 'user9000@example.com';
```

2. Inspect how PostgreSQL executes it.

3. Improve its performance.

⛔ Do **not** modify the `SELECT` statement itself.

---

## 🔍 What To Observe

Before changing anything, pay attention to:
- Total execution time
- Whether it uses a sequential scan or index scan
- How many rows were examined vs returned

---

## 🧭 Hints

Reveal hints progressively (jump to the bottom):

- [Hint 1 →](#hint-1)
- [Hint 2 →](#hint-2)
- [Hint 3 →](#hint-3)

---

## ✅ Expected Outcome

After completing this task, you should be able to:
- Explain **why** the original query was slow
- Show a measurable improvement
- Describe what changed in the execution plan

---

## 🤔 Why This Matters

In real systems, missing indexes are a top cause of slow endpoints and timeouts.

If you can quickly confirm “this is a missing-index problem,” you can:
- fix it safely,
- validate the improvement with `EXPLAIN ANALYZE`,
- and avoid guessing in production.

---

## 🧩 Completion Check

Mark complete when:
- [ ] You ran `EXPLAIN ANALYZE` before and after
- [ ] The scan strategy changed
- [ ] You can explain the difference in one sentence

---

## 🔗 Navigation

⬅️ **Previous Task:** [Task 06 — Title](./task-06.md)
➡️ **Next Task:** [Task 08 — Title](./task-08.md)

---

## 🧠 Hints Section

### <a id="hint-1"></a>Hint 1
Use `EXPLAIN ANALYZE` on the query.
Look for the scan type.

```sql
EXPLAIN ANALYZE
SELECT *
FROM users
WHERE email = 'user9000@example.com';
```

---

### <a id="hint-2"></a>Hint 2
If PostgreSQL has no efficient way to find a row by `email`, it may scan the whole table.

What structure helps PostgreSQL jump directly to matching rows?

---

### <a id="hint-3"></a>Hint 3
Create an index on the `email` column, then rerun the query and compare plans.

```sql
CREATE INDEX users_email_idx ON users (email);
```

```sql
EXPLAIN ANALYZE
SELECT *
FROM users
WHERE email = 'user9000@example.com';
```
