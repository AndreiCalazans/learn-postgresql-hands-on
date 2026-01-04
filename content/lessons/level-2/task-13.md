---
title: "Task 13 — SELECT * Pitfalls"
weight: 13
level: "🟡 Level 2 — PostgreSQL Mistakes"
summary: "See how SELECT * inflates I/O when wide columns exist."
---

# Task 13 — SELECT * Pitfalls

Level:
🟡 Level 2 — PostgreSQL Mistakes

Estimated Time:
~5 minutes

Concept(s):
- Column bloat
- Network overhead
- Explain width

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson13;
SET search_path TO lesson13;

CREATE TABLE profiles (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL,
  bio TEXT,
  avatar BYTEA
);

INSERT INTO profiles (email, bio, avatar)
SELECT 'user' || g || '@example.com', repeat('about me ', 50), repeat(decode('ff','hex'), 500)
FROM generate_series(1, 2000) g;
```

## 🧠 Challenge

Compare EXPLAIN (BUFFERS) for SELECT * versus selecting only email. Observe row width and timing.

## 🧭 Hints (Progressive)

1. Use EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM profiles LIMIT 50;
2. Check the width column in the plan to see projected bytes per row.
3. Compare to selecting only the email column.

## ✅ Expected Observation / Outcome

- SELECT * pulled far more bytes per row than needed.
- Narrow selects reduced buffer hits and planning time.

## 🤔 Why This Matters

- Wide columns and binary data make SELECT * expensive in production APIs.
- Being intentional about projection keeps caches and network lean.
