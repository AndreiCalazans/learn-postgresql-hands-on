---
title: "Task 20 — N+1 Query Pattern"
weight: 20
level: "🟡 Level 2 — PostgreSQL Mistakes"
summary: "Simulate an N+1 loop and replace it with a single join."
---

# Task 20 — N+1 Query Pattern

Level:
🟡 Level 2 — PostgreSQL Mistakes

Estimated Time:
~5 minutes

Concept(s):
- Join vs loop
- Query counting
- EXPLAIN

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson20;
SET search_path TO lesson20;

CREATE TABLE authors (id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE posts (id SERIAL PRIMARY KEY, author_id INT NOT NULL REFERENCES authors(id), title TEXT);

INSERT INTO authors (name)
SELECT 'author ' || g FROM generate_series(1, 50) g;

INSERT INTO posts (author_id, title)
SELECT (random()*50)::int + 1, 'post ' || g FROM generate_series(1, 500) g;
```

## 🧠 Challenge

Count posts per author using two approaches: (1) loop-like pattern with repeated SELECTs, and (2) a single GROUP BY join. Compare timing.

## 🧭 Hints (Progressive)

1. Use 	iming and run SELECT COUNT(*) FROM posts WHERE author_id = 1; repeatedly for a handful of authors.
2. Then run SELECT a.name, COUNT(p.*) FROM authors a LEFT JOIN posts p ON p.author_id = a.id GROUP BY a.id;
3. EXPLAIN shows why the grouped join is cheaper.

## ✅ Expected Observation / Outcome

- Multiple single-row queries were slower and noisier.
- The grouped join returned all counts in one scan.

## 🤔 Why This Matters

- N+1 patterns amplify latency and connection usage.
- Batching with joins keeps database load predictable under traffic spikes.
