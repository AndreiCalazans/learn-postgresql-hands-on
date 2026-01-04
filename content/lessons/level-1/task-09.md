---
title: "Task 09 — Window Functions for Rankings"
weight: 9
level: "🟢 Level 1 — Just Use Postgres"
summary: "Rank rows within groups without collapsing them."
---

# Task 09 — Window Functions for Rankings

Level:
🟢 Level 1 — Just Use Postgres

Estimated Time:
~5 minutes

Concept(s):
- Window functions
- ROW_NUMBER
- Partitioning

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson09;
SET search_path TO lesson09;

CREATE TABLE scores (
  id SERIAL PRIMARY KEY,
  region TEXT NOT NULL,
  player TEXT NOT NULL,
  points INT NOT NULL
);

INSERT INTO scores (region, player, points)
SELECT CASE WHEN g % 2 = 0 THEN 'NA' ELSE 'EU' END,
       'player' || g,
       (random()*100)::int
FROM generate_series(1, 40) g;
```

## 🧠 Challenge

List the top 3 players per region using ROW_NUMBER over a partition and filter on the window value.

## 🧭 Hints (Progressive)

1. Use ROW_NUMBER() OVER (PARTITION BY region ORDER BY points DESC).
2. Wrap the window function in a subquery to filter row_number <= 3.
3. Compare to a GROUP BY approach to see why window functions preserve detail.

## ✅ Expected Observation / Outcome

- You produced per-region rankings without losing rows.
- Filtering on the window column delivered top-N per partition.

## 🤔 Why This Matters

- Window functions avoid the N+1 of per-group subqueries for ranking.
- They enable leaderboard-style views without extra tables.
