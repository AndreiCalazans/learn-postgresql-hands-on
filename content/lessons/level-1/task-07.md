---
title: "Task 07 — Full-Text Search in Five Minutes"
weight: 7
level: "🟢 Level 1 — Just Use Postgres"
summary: "Build a tiny full-text index and run ranked searches."
---

# Task 07 — Full-Text Search in Five Minutes

Level:
🟢 Level 1 — Just Use Postgres

Estimated Time:
~5 minutes

Concept(s):
- to_tsvector
- plainto_tsquery
- GIN for FTS

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson07;
SET search_path TO lesson07;

CREATE TABLE docs (
  id SERIAL PRIMARY KEY,
  body TEXT NOT NULL,
  tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', body)) STORED
);

INSERT INTO docs (body) VALUES
  ('PostgreSQL ships with full text search built-in'),
  ('Searching JSON and text together is powerful'),
  ('GIN indexes make repeated searches fast'),
  ('Ranking results helps users find the right doc');
```

## 🧠 Challenge

Search for 'search powerful' and sort by rank. Add a GIN index on tsv and compare plan and speed.

## 🧭 Hints (Progressive)

1. Use plainto_tsquery('english', 'search powerful').
2. ORDER BY ts_rank(tsv, plainto_tsquery(...)) DESC to see ranking.
3. GIN on the generated tsvector column accelerates the lookup.

## ✅ Expected Observation / Outcome

- You produced ranked results with ts_rank.
- GIN index changed the plan from sequential scan to bitmap index scan.

## 🤔 Why This Matters

- Postgres ships full-text primitives—no extra service required.
- GIN indexes keep search latency low as text grows.
