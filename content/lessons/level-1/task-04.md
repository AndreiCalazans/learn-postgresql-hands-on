---
title: "Task 04 — Generated Columns for Derived Data"
weight: 4
level: "🟢 Level 1 — Just Use Postgres"
summary: "Create computed columns to avoid recalculating obvious derived values."
---

# Task 04 — Generated Columns for Derived Data

Level:
🟢 Level 1 — Just Use Postgres

Estimated Time:
~5 minutes

Concept(s):
- Generated columns
- Data consistency
- Computed projections

## ⚙️ Setup

```sql
CREATE SCHEMA IF NOT EXISTS lesson04;
SET search_path TO lesson04;

CREATE TABLE invoice_lines (
  id SERIAL PRIMARY KEY,
  qty INT NOT NULL,
  unit_price NUMERIC(10,2) NOT NULL,
  discount NUMERIC(4,2) DEFAULT 0,
  total NUMERIC(12,2) GENERATED ALWAYS AS ((qty * unit_price) - discount) STORED
);

INSERT INTO invoice_lines (qty, unit_price, discount) VALUES
  (2, 19.99, 0),
  (5, 4.00, 1.50);
```

## 🧠 Challenge

Insert a new row and check that total is auto-computed. Update qty and confirm total keeps pace without manual recalculation.

## 🧭 Hints (Progressive)

1. Use RETURNING to see generated columns after INSERT or UPDATE.
2. Generated ALWAYS prevents direct writes—try to set total and watch it fail.
3. Check pg_get_expr on pg_attrdef to see the stored expression.

## ✅ Expected Observation / Outcome

- Totals updated automatically on writes.
- Direct writes to the generated column were rejected.

## 🤔 Why This Matters

- Generated columns keep computed data consistent without triggers.
- They make read models cheap without duplicating business logic in multiple services.
