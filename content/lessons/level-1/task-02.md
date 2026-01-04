---
title: "Task 02 — Arrays, UNNEST, and Order"
weight: 2
level: "🟢 Level 1 — Just Use Postgres"
summary: "Work with array columns, explode them, and keep element order obvious."
---

# Task 02 — Arrays, UNNEST, and Order

Level:
🟢 Level 1 — Just Use Postgres

Estimated Time:
~5 minutes

Concept(s):
- Array columns
- UNNEST
- Order preservation

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson02;
SET search_path TO lesson02;

CREATE TABLE playlists (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  tracks TEXT[] NOT NULL
);

INSERT INTO playlists (name, tracks) VALUES
  ('focus', ARRAY['intro','beat','outro']),
  ('party', ARRAY['warmup','drop','bridge','end']);
```

## 🧠 Challenge

Expand the tracks into rows with their original position, then re-aggregate them back into arrays sorted by that position.

## 🧭 Hints (Progressive)

1. UNNEST supports WITH ORDINALITY to keep positions.
2. Use ORDER BY ordinality when aggregating back with array_agg.
3. Compare the rebuilt arrays to the originals to confirm ordering stayed intact.

## ✅ Expected Observation / Outcome

- You produced one row per track with an element index.
- Re-aggregating with ORDER BY kept the array sequence stable.

## 🤔 Why This Matters

- Arrays are great for small ordered lists without join tables.
- WITH ORDINALITY prevents subtle ordering bugs when expanding arrays in production.
