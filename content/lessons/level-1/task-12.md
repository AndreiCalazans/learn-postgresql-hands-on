---
title: "Task 12 — Geospatial Awareness Without PostGIS"
weight: 12
level: "🟢 Level 1 — Just Use Postgres"
summary: "Use built-in point math to sort and filter locations without extensions."
---

# Task 12 — Geospatial Awareness Without PostGIS

Level:
🟢 Level 1 — Just Use Postgres

Estimated Time:
~5 minutes

Concept(s):
- Point type
- Distance ordering
- Bounding boxes

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson12;
SET search_path TO lesson12;

CREATE TABLE places (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  location POINT NOT NULL
);

INSERT INTO places (name, location) VALUES
  ('office', POINT(-73.99, 40.75)),
  ('park', POINT(-73.97, 40.78)),
  ('cafe', POINT(-73.98, 40.76)),
  ('museum', POINT(-73.96, 40.78));
```

## 🧠 Challenge

Find the three closest places to POINT(-73.98, 40.77) and filter only those inside a bounding box of latitude 40.74–40.79.

## 🧭 Hints (Progressive)

1. Use the <-> operator between points to order by distance.
2. Bounding box: WHERE location[0] BETWEEN -74.0 AND -73.95 AND location[1] BETWEEN 40.74 AND 40.79.
3. Add a BTREE index on location to explore its effect (it works lexicographically).

## ✅ Expected Observation / Outcome

- You listed the nearest neighbors without PostGIS.
- Bounding box filters kept only plausible nearby results.

## 🤔 Why This Matters

- Even without extensions, PostgreSQL can do simple spatial reasoning.
- A bounding box pre-filter is a common production optimization before precise distance checks.
