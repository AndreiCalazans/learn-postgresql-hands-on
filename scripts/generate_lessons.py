import textwrap
from pathlib import Path

base = Path(__file__).resolve().parent.parent / "content" / "lessons"
base.mkdir(parents=True, exist_ok=True)

levels = {
    "level-1": "🟢 Level 1 — Just Use Postgres",
    "level-2": "🟡 Level 2 — PostgreSQL Mistakes",
    "level-3": "🔴 Level 3 — Postgres Internals",
}


tasks = [
    {
        "number": 1,
        "slug": "jsonb-vs-text",
        "level_key": "level-1",
        "title": "JSONB vs TEXT: Store and Query",
        "concepts": ["JSONB vs TEXT", "GIN indexing", "Predicate performance"],
        "summary": "Contrast JSONB with TEXT storage and see how indexing changes query speed.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson01;\nSET search_path TO lesson01;\n\nCREATE TABLE events_json (\n  id SERIAL PRIMARY KEY,\n  payload_json JSONB,\n  payload_text TEXT\n);\n\nINSERT INTO events_json (payload_json, payload_text)\nSELECT jsonb_build_object('user', 'user' || g, 'flag', (g % 2 = 0)),\n       json_build_object('user', 'user' || g, 'flag', (g % 2 = 0))::text\nFROM generate_series(1, 5000) g;""",
        "challenge": "Compare filtering JSON data stored as JSONB versus TEXT. Make one query fast without changing the WHERE clause.",
        "hints": [
            "Run EXPLAIN ANALYZE on a filter like payload_json ->> 'user' = 'user4200'.",
            "Create a GIN index on the JSONB column and rerun the filter.",
            "Use pg_class to compare relation sizes after indexing.",
        ],
        "outcome": [
            "You saw a sequential scan on TEXT and a GIN index scan on JSONB after indexing.",
            "Execution time dropped noticeably once the GIN index existed.",
        ],
        "why": [
            "JSONB supports binary storage and indexing; TEXT requires parsing on every read.",
            "Choosing the right type makes semi-structured data fast without schema changes.",
        ],
    },
    {
        "number": 2,
        "slug": "arrays-and-unnest",
        "level_key": "level-1",
        "title": "Arrays, UNNEST, and Order",
        "concepts": ["Array columns", "UNNEST", "Order preservation"],
        "summary": "Work with array columns, explode them, and keep element order obvious.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson02;\nSET search_path TO lesson02;\n\nCREATE TABLE playlists (\n  id SERIAL PRIMARY KEY,\n  name TEXT NOT NULL,\n  tracks TEXT[] NOT NULL\n);\n\nINSERT INTO playlists (name, tracks) VALUES\n  ('focus', ARRAY['intro','beat','outro']),\n  ('party', ARRAY['warmup','drop','bridge','end']);""",
        "challenge": "Expand the tracks into rows with their original position, then re-aggregate them back into arrays sorted by that position.",
        "hints": [
            "UNNEST supports WITH ORDINALITY to keep positions.",
            "Use ORDER BY ordinality when aggregating back with array_agg.",
            "Compare the rebuilt arrays to the originals to confirm ordering stayed intact.",
        ],
        "outcome": [
            "You produced one row per track with an element index.",
            "Re-aggregating with ORDER BY kept the array sequence stable.",
        ],
        "why": [
            "Arrays are great for small ordered lists without join tables.",
            "WITH ORDINALITY prevents subtle ordering bugs when expanding arrays in production.",
        ],
    },
    {
        "number": 3,
        "slug": "enums-and-constraints",
        "level_key": "level-1",
        "title": "Enums with Guard Rails",
        "concepts": ["ENUM type", "CHECK constraints", "State transitions"],
        "summary": "Use ENUM plus CHECK constraints to encode allowed states and transitions.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson03;\nSET search_path TO lesson03;\n\nDO $$ BEGIN\n  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'order_status') THEN\n    CREATE TYPE order_status AS ENUM ('pending','paid','shipped','cancelled');\n  END IF;\nEND $$;\n\nCREATE TABLE orders (\n  id SERIAL PRIMARY KEY,\n  status order_status NOT NULL DEFAULT 'pending',\n  paid_at TIMESTAMPTZ,\n  shipped_at TIMESTAMPTZ,\n  CONSTRAINT status_flow CHECK (\n    (status = 'paid' AND paid_at IS NOT NULL) OR\n    (status = 'shipped' AND paid_at IS NOT NULL AND shipped_at IS NOT NULL) OR\n    status IN ('pending','cancelled')\n  )\n);\n\nINSERT INTO orders (status, paid_at, shipped_at) VALUES\n  ('pending', NULL, NULL),\n  ('paid', now(), NULL),\n  ('shipped', now() - interval '1 hour', now());""",
        "challenge": "Try inserting an impossible state (shipped without paid_at). Find the constraint failure, then fix the data and insert successfully.",
        "hints": [
            "INSERT a shipped row with NULL paid_at to see the CHECK fire.",
            "Update the row to set paid_at before shipped_at to satisfy the constraint.",
            "Use the ENUM to block typos like 'shippped' from ever being stored.",
        ],
        "outcome": [
            "You observed a constraint violation on invalid state transitions.",
            "Valid data flowed through without custom code.",
        ],
        "why": [
            "Constraints keep business rules close to the data.",
            "Encoding flows in the database reduces downstream data cleanup work.",
        ],
    },
    {
        "number": 4,
        "slug": "generated-columns",
        "level_key": "level-1",
        "title": "Generated Columns for Derived Data",
        "concepts": ["Generated columns", "Data consistency", "Computed projections"],
        "summary": "Create computed columns to avoid recalculating obvious derived values.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson04;\nSET search_path TO lesson04;\n\nCREATE TABLE invoice_lines (\n  id SERIAL PRIMARY KEY,\n  qty INT NOT NULL,\n  unit_price NUMERIC(10,2) NOT NULL,\n  discount NUMERIC(4,2) DEFAULT 0,\n  total NUMERIC(12,2) GENERATED ALWAYS AS ((qty * unit_price) - discount) STORED\n);\n\nINSERT INTO invoice_lines (qty, unit_price, discount) VALUES\n  (2, 19.99, 0),\n  (5, 4.00, 1.50);""",
        "challenge": "Insert a new row and check that total is auto-computed. Update qty and confirm total keeps pace without manual recalculation.",
        "hints": [
            "Use RETURNING to see generated columns after INSERT or UPDATE.",
            "Generated ALWAYS prevents direct writes—try to set total and watch it fail.",
            "Check pg_get_expr on pg_attrdef to see the stored expression.",
        ],
        "outcome": [
            "Totals updated automatically on writes.",
            "Direct writes to the generated column were rejected.",
        ],
        "why": [
            "Generated columns keep computed data consistent without triggers.",
            "They make read models cheap without duplicating business logic in multiple services.",
        ],
    },
    {
        "number": 5,
        "slug": "upsert-with-on-conflict",
        "level_key": "level-1",
        "title": "UPSERT Without Race Conditions",
        "concepts": ["ON CONFLICT", "Unique constraints", "Idempotent writes"],
        "summary": "Use INSERT ... ON CONFLICT to de-duplicate writes safely.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson05;\nSET search_path TO lesson05;\n\nCREATE TABLE profiles (\n  id SERIAL PRIMARY KEY,\n  email TEXT UNIQUE NOT NULL,\n  logins INT NOT NULL DEFAULT 0,\n  last_seen TIMESTAMPTZ\n);\n\nINSERT INTO profiles (email, logins, last_seen) VALUES\n  ('casey@example.com', 1, now() - interval '1 day');""",
        "challenge": "Upsert the same email twice: first to insert, second to increment logins and update last_seen in one statement.",
        "hints": [
            "Target the UNIQUE email column in the ON CONFLICT clause.",
            "Use EXCLUDED to reference incoming values when updating.",
            "RETURNING shows whether the row was inserted or updated.",
        ],
        "outcome": [
            "The first command inserted; the second reused the same email and updated counters.",
            "No duplicate emails were created even under repeated calls.",
        ],
        "why": [
            "UPSERTs remove race conditions that appear when you SELECT then INSERT in separate steps.",
            "Idempotent writes make retry logic and background jobs safe.",
        ],
    },
    {
        "number": 6,
        "slug": "btree-vs-gin-tags",
        "level_key": "level-1",
        "title": "BTREE vs GIN for Tag Filters",
        "concepts": ["BTREE indexes", "GIN indexes", "Containment queries"],
        "summary": "Compare BTREE and GIN behavior when filtering array tags.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson06;\nSET search_path TO lesson06;\n\nCREATE TABLE articles (\n  id SERIAL PRIMARY KEY,\n  title TEXT NOT NULL,\n  tags TEXT[] NOT NULL\n);\n\nINSERT INTO articles (title, tags)
SELECT 'post ' || g, ARRAY['pg', 'cli', CASE WHEN g % 2 = 0 THEN 'json' ELSE 'fts' END]
FROM generate_series(1, 3000) g;""",
        "challenge": "Filter articles containing both 'pg' and 'json'. Measure plan and timing before and after adding a GIN index on tags.",
        "hints": [
            "Start with EXPLAIN ANALYZE on WHERE tags @> ARRAY['pg','json'].",
            "Create a GIN index using the default array_ops operator class.",
            "Compare with a BTREE index on tags (and notice why it is ineffective).",
        ],
        "outcome": [
            "Sequential scan before indexing; GIN index scan after.",
            "BTREE index did not help the @> operator.",
        ],
        "why": [
            "Operator classes matter—containment needs GIN/GiST, not BTREE.",
            "Choosing the right index saves CPU and makes tag filters predictable in production.",
        ],
    },
    {
        "number": 7,
        "slug": "full-text-search-basics",
        "level_key": "level-1",
        "title": "Full-Text Search in Five Minutes",
        "concepts": ["to_tsvector", "plainto_tsquery", "GIN for FTS"],
        "summary": "Build a tiny full-text index and run ranked searches.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson07;\nSET search_path TO lesson07;\n\nCREATE TABLE docs (\n  id SERIAL PRIMARY KEY,\n  body TEXT NOT NULL,\n  tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', body)) STORED\n);\n\nINSERT INTO docs (body) VALUES\n  ('PostgreSQL ships with full text search built-in'),\n  ('Searching JSON and text together is powerful'),\n  ('GIN indexes make repeated searches fast'),\n  ('Ranking results helps users find the right doc');""",
        "challenge": "Search for 'search powerful' and sort by rank. Add a GIN index on tsv and compare plan and speed.",
        "hints": [
            "Use plainto_tsquery('english', 'search powerful').",
            "ORDER BY ts_rank(tsv, plainto_tsquery(...)) DESC to see ranking.",
            "GIN on the generated tsvector column accelerates the lookup.",
        ],
        "outcome": [
            "You produced ranked results with ts_rank.",
            "GIN index changed the plan from sequential scan to bitmap index scan.",
        ],
        "why": [
            "Postgres ships full-text primitives—no extra service required.",
            "GIN indexes keep search latency low as text grows.",
        ],
    },
    {
        "number": 8,
        "slug": "time-series-basics",
        "level_key": "level-1",
        "title": "Time-Series Patterns Without Extensions",
        "concepts": ["date_trunc", "Partial indexes", "Rolling windows"],
        "summary": "Slice event data by day and speed up recent lookups with a partial index.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson08;\nSET search_path TO lesson08;\n\nCREATE TABLE readings (\n  id SERIAL PRIMARY KEY,\n  recorded_at TIMESTAMPTZ NOT NULL DEFAULT now(),\n  value NUMERIC NOT NULL\n);\n\nINSERT INTO readings (recorded_at, value)
SELECT now() - (g || ' minutes')::interval, (random()*10)::numeric
FROM generate_series(0, 1440) g;""",
        "challenge": "Compute average value per hour for the past day, then create a partial index on recent data and rerun the query.",
        "hints": [
            "Use WHERE recorded_at >= now() - interval '1 day'.",
            "Group by date_trunc('hour', recorded_at).",
            "Create INDEX ON readings (recorded_at) WHERE recorded_at >= now() - interval '1 day'.",
        ],
        "outcome": [
            "You produced hourly aggregates over the last 24 hours.",
            "Partial index reduced the scanned rows for recent-only queries.",
        ],
        "why": [
            "Time filters dominate many dashboards—partial indexes keep them cheap.",
            "date_trunc is a lightweight tool before reaching for full time-series stacks.",
        ],
    },
    {
        "number": 9,
        "slug": "window-functions-first-steps",
        "level_key": "level-1",
        "title": "Window Functions for Rankings",
        "concepts": ["Window functions", "ROW_NUMBER", "Partitioning"],
        "summary": "Rank rows within groups without collapsing them.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson09;\nSET search_path TO lesson09;\n\nCREATE TABLE scores (\n  id SERIAL PRIMARY KEY,\n  region TEXT NOT NULL,\n  player TEXT NOT NULL,\n  points INT NOT NULL\n);\n\nINSERT INTO scores (region, player, points)
SELECT CASE WHEN g % 2 = 0 THEN 'NA' ELSE 'EU' END,
       'player' || g,
       (random()*100)::int
FROM generate_series(1, 40) g;""",
        "challenge": "List the top 3 players per region using ROW_NUMBER over a partition and filter on the window value.",
        "hints": [
            "Use ROW_NUMBER() OVER (PARTITION BY region ORDER BY points DESC).",
            "Wrap the window function in a subquery to filter row_number <= 3.",
            "Compare to a GROUP BY approach to see why window functions preserve detail.",
        ],
        "outcome": [
            "You produced per-region rankings without losing rows.",
            "Filtering on the window column delivered top-N per partition.",
        ],
        "why": [
            "Window functions avoid the N+1 of per-group subqueries for ranking.",
            "They enable leaderboard-style views without extra tables.",
        ],
    },
    {
        "number": 10,
        "slug": "cte-vs-subquery",
        "level_key": "level-1",
        "title": "CTE vs Subquery: Same Result, Different Intent",
        "concepts": ["CTEs", "Inlining vs materialization", "EXPLAIN"],
        "summary": "Compare a CTE and inline subquery to see how the planner treats them.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson10;\nSET search_path TO lesson10;\n\nCREATE TABLE purchases (\n  id SERIAL PRIMARY KEY,\n  customer_id INT NOT NULL,\n  total NUMERIC NOT NULL\n);\n\nINSERT INTO purchases (customer_id, total)
SELECT (random()*20)::int, (10 + random()*90)::numeric
FROM generate_series(1, 3000) g;""",
        "challenge": "Write a query that filters customers above average spend using a CTE, then rewrite it as an inline subquery. Compare EXPLAIN plans and timing.",
        "hints": [
            "WITH avg_spend AS (SELECT avg(total) AS avg_total FROM purchases) SELECT ...",
            "Use EXPLAIN (ANALYZE, VERBOSE) on both versions.",
            "Note whether the CTE is inlined (it often is in newer PostgreSQL).",
        ],
        "outcome": [
            "Both queries returned the same rows.",
            "Plans likely looked similar—inlining shows the planner can optimize CTEs.",
        ],
        "why": [
            "CTEs communicate intent and can be optimized; materialization is not guaranteed.",
            "Understanding when CTEs inline prevents surprises when refactoring complex queries.",
        ],
    },
    {
        "number": 11,
        "slug": "constraints-as-logic",
        "level_key": "level-1",
        "title": "Constraints as Application Logic",
        "concepts": ["CHECK constraints", "DEFAULTS", "Business rules"],
        "summary": "Encode a business rule directly in the table to avoid bad data.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson11;\nSET search_path TO lesson11;\n\nCREATE TABLE subscriptions (\n  id SERIAL PRIMARY KEY,\n  plan TEXT NOT NULL CHECK (plan IN ('free','pro','team')),\n  seats INT NOT NULL DEFAULT 1 CHECK (seats > 0),\n  expires_at DATE,\n  CONSTRAINT paid_requires_expiry CHECK ((plan = 'free' AND expires_at IS NULL) OR (plan IN ('pro','team') AND expires_at IS NOT NULL))\n);""",
        "challenge": "Attempt to insert a paid plan without expires_at and observe the failure. Then insert valid rows and query to confirm constraints hold.",
        "hints": [
            "INSERT INTO subscriptions(plan, seats) VALUES ('pro', 3);",
            "Then insert with an expires_at date to satisfy the CHECK.",
            "Use pg_constraint to read the check expression text.",
        ],
        "outcome": [
            "Invalid data was rejected immediately by the CHECK.",
            "Valid paid rows stored their expiry date automatically.",
        ],
        "why": [
            "Constraints keep invariants consistent across every code path.",
            "They make bulk imports and migrations safer by enforcing business rules at the edge.",
        ],
    },
    {
        "number": 12,
        "slug": "geospatial-basics-without-postgis",
        "level_key": "level-1",
        "title": "Geospatial Awareness Without PostGIS",
        "concepts": ["Point type", "Distance ordering", "Bounding boxes"],
        "summary": "Use built-in point math to sort and filter locations without extensions.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson12;\nSET search_path TO lesson12;\n\nCREATE TABLE places (\n  id SERIAL PRIMARY KEY,\n  name TEXT NOT NULL,\n  location POINT NOT NULL\n);\n\nINSERT INTO places (name, location) VALUES\n  ('office', POINT(-73.99, 40.75)),\n  ('park', POINT(-73.97, 40.78)),\n  ('cafe', POINT(-73.98, 40.76)),\n  ('museum', POINT(-73.96, 40.78));""",
        "challenge": "Find the three closest places to POINT(-73.98, 40.77) and filter only those inside a bounding box of latitude 40.74–40.79.",
        "hints": [
            "Use the <-> operator between points to order by distance.",
            "Bounding box: WHERE location[0] BETWEEN -74.0 AND -73.95 AND location[1] BETWEEN 40.74 AND 40.79.",
            "Add a BTREE index on location to explore its effect (it works lexicographically).",
        ],
        "outcome": [
            "You listed the nearest neighbors without PostGIS.",
            "Bounding box filters kept only plausible nearby results.",
        ],
        "why": [
            "Even without extensions, PostgreSQL can do simple spatial reasoning.",
            "A bounding box pre-filter is a common production optimization before precise distance checks.",
        ],
    },
    # Level 2 tasks
    {
        "number": 13,
        "slug": "select-star-pitfalls",
        "level_key": "level-2",
        "title": "SELECT * Pitfalls",
        "concepts": ["Column bloat", "Network overhead", "Explain width"],
        "summary": "See how SELECT * inflates I/O when wide columns exist.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson13;\nSET search_path TO lesson13;\n\nCREATE TABLE profiles (\n  id SERIAL PRIMARY KEY,\n  email TEXT NOT NULL,\n  bio TEXT,\n  avatar BYTEA\n);\n\nINSERT INTO profiles (email, bio, avatar)
SELECT 'user' || g || '@example.com', repeat('about me ', 50), repeat(decode('ff','hex'), 500)
FROM generate_series(1, 2000) g;""",
        "challenge": "Compare EXPLAIN (BUFFERS) for SELECT * versus selecting only email. Observe row width and timing.",
        "hints": [
            "Use EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM profiles LIMIT 50;",
            "Check the width column in the plan to see projected bytes per row.",
            "Compare to selecting only the email column.",
        ],
        "outcome": [
            "SELECT * pulled far more bytes per row than needed.",
            "Narrow selects reduced buffer hits and planning time.",
        ],
        "why": [
            "Wide columns and binary data make SELECT * expensive in production APIs.",
            "Being intentional about projection keeps caches and network lean.",
        ],
    },
    {
        "number": 14,
        "slug": "missing-index-slow-query",
        "level_key": "level-2",
        "title": "Missing Indexes Hurt",
        "concepts": ["Sequential scan", "Index creation", "Query speed"],
        "summary": "Feel the latency of a missing index then fix it.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson14;\nSET search_path TO lesson14;\n\nCREATE TABLE orders (\n  id SERIAL PRIMARY KEY,\n  customer_id INT NOT NULL,\n  total NUMERIC NOT NULL\n);\n\nINSERT INTO orders (customer_id, total)
SELECT (random()*500)::int, (10 + random()*190)::numeric
FROM generate_series(1, 20000) g;""",
        "challenge": "Run a filter on customer_id without an index, note timing, then add an index and re-run the same query.",
        "hints": [
            "Use EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 42;",
            "CREATE INDEX ON orders (customer_id);",
            "Compare row scans and total time before/after.",
        ],
        "outcome": [
            "The first run used a sequential scan and was slower.",
            "After indexing, the plan switched to an index scan with fewer blocks read.",
        ],
        "why": [
            "Most production slowdowns start with missing indexes on common filters.",
            "Measuring before and after builds intuition for when an index pays off.",
        ],
    },
    {
        "number": 15,
        "slug": "over-indexing-costs",
        "level_key": "level-2",
        "title": "Over-Indexing Adds Write Cost",
        "concepts": ["Index overhead", "pg_relation_size", "Write amplification"],
        "summary": "See how too many indexes slow inserts and consume space.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson15;\nSET search_path TO lesson15;\n\nCREATE TABLE audit_events (\n  id SERIAL PRIMARY KEY,\n  actor TEXT NOT NULL,\n  path TEXT NOT NULL,\n  created_at TIMESTAMPTZ NOT NULL DEFAULT now()\n);\n\nCREATE INDEX ON audit_events (actor);
CREATE INDEX ON audit_events (path);
CREATE INDEX ON audit_events (created_at);
CREATE INDEX ON audit_events (actor, created_at);

INSERT INTO audit_events (actor, path)
SELECT 'user' || (g % 10), '/v1/resource/' || g
FROM generate_series(1, 15000) g;""",
        "challenge": "Measure table vs index size, then drop one index and insert again to compare insert timing.",
        "hints": [
            "Use pg_relation_size and pg_indexes_size on audit_events.",
            "DROP INDEX audit_events_actor_created_at_idx; then insert another batch.",
            "Compare insertion timing with \\timing on before/after batches.",
        ],
        "outcome": [
            "Indexes consumed more disk than the table itself.",
            "Dropping an overlapping index improved insert speed slightly.",
        ],
        "why": [
            "Each extra index must be maintained on every write.",
            "Pruning redundant indexes reduces storage, cache churn, and lock time in production.",
        ],
    },
    {
        "number": 16,
        "slug": "wrong-data-types",
        "level_key": "level-2",
        "title": "Wrong Data Types Bite Later",
        "concepts": ["Type casting", "Sorting", "Query planner"] ,
        "summary": "Compare text vs numeric/timestamp columns for correctness and speed.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson16;\nSET search_path TO lesson16;\n\nCREATE TABLE metrics_text (\n  id SERIAL PRIMARY KEY,\n  metric_value TEXT\n);\n
CREATE TABLE metrics_num (
  id SERIAL PRIMARY KEY,
  metric_value NUMERIC
);

INSERT INTO metrics_text (metric_value) VALUES
  ('9.5'), ('10.2'), ('2.4'), ('30.0');
INSERT INTO metrics_num (metric_value) VALUES
  (9.5), (10.2), (2.4), (30.0);""",
        "challenge": "Order both tables by metric_value DESC and note differences. Add a WHERE metric_value > 10 filter to feel casting cost on TEXT.",
        "hints": [
            "EXPLAIN ANALYZE SELECT * FROM metrics_text WHERE metric_value > '10';",
            "Note the lexical ordering of TEXT vs numeric ordering.",
            "Casting text in a WHERE prevents index use later.",
        ],
        "outcome": [
            "Text-sorted values were lexicographic (30.0 before 9.5).",
            "Numeric column sorted correctly and filtered faster.",
        ],
        "why": [
            "Using the right type avoids subtle correctness bugs and unlocks index usage.",
            "Casting on the fly prevents the planner from using fast paths.",
        ],
    },
    {
        "number": 17,
        "slug": "null-semantics",
        "level_key": "level-2",
        "title": "NULL Semantics Surprise",
        "concepts": ["NULL comparisons", "IS DISTINCT FROM", "Three-valued logic"],
        "summary": "Explore how NULL behaves in filters and equality checks.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson17;\nSET search_path TO lesson17;\n\nCREATE TABLE flags (\n  id SERIAL PRIMARY KEY,\n  feature TEXT NOT NULL,\n  enabled_at TIMESTAMPTZ\n);\n\nINSERT INTO flags (feature, enabled_at) VALUES\n  ('checkout', now()),\n  ('search', NULL),\n  ('billing', NULL);""",
        "challenge": "Count rows where enabled_at != NULL and compare to IS NOT NULL. Use IS DISTINCT FROM to handle NULL safely.",
        "hints": [
            "SELECT COUNT(*) WHERE enabled_at != NULL will return 0.",
            "Use enabled_at IS NOT NULL to find set values.",
            "IS DISTINCT FROM treats NULL as a comparable value for equality semantics.",
        ],
        "outcome": [
            "enabled_at != NULL matched nothing because comparisons with NULL are unknown.",
            "IS DISTINCT FROM counted the rows you expected.",
        ],
        "why": [
            "NULL semantics differ from most programming languages.",
            "Getting this wrong leads to missing data and incorrect analytics in production.",
        ],
    },
    {
        "number": 18,
        "slug": "inefficient-pagination",
        "level_key": "level-2",
        "title": "Inefficient Pagination",
        "concepts": ["OFFSET/LIMIT", "Keyset pagination", "Index usage"],
        "summary": "Feel OFFSET cost and switch to keyset pagination.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson18;\nSET search_path TO lesson18;\n\nCREATE TABLE feed_items (\n  id SERIAL PRIMARY KEY,\n  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),\n  body TEXT\n);\n\nINSERT INTO feed_items (created_at, body)
SELECT now() - (g || ' seconds')::interval, 'post ' || g
FROM generate_series(1, 5000) g;""",
        "challenge": "Compare OFFSET/LIMIT pagination to keyset pagination using the created_at and id columns.",
        "hints": [
            "\timing ON; then run SELECT * FROM feed_items ORDER BY created_at DESC OFFSET 3000 LIMIT 20;",
            "Use WHERE created_at < (SELECT created_at FROM feed_items ORDER BY created_at DESC OFFSET 100 LIMIT 1) ORDER BY created_at DESC LIMIT 20;",
            "Create an index on created_at to speed both approaches.",
        ],
        "outcome": [
            "OFFSET scanned thousands of rows only to discard them.",
            "Keyset pagination jumped directly to the next page using an index.",
        ],
        "why": [
            "OFFSET grows linearly with page number and hurts user-facing latency.",
            "Keyset pagination is predictable and index-friendly for infinite scrolls.",
        ],
    },
    {
        "number": 19,
        "slug": "transaction-boundary-mistakes",
        "level_key": "level-2",
        "title": "Bad Transaction Boundaries",
        "concepts": ["Long transactions", "Locks", "Visibility"],
        "summary": "See how holding a transaction open blocks others.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson19;\nSET search_path TO lesson19;\n\nCREATE TABLE accounts (\n  id SERIAL PRIMARY KEY,\n  balance NUMERIC NOT NULL\n);\n\nINSERT INTO accounts (balance) VALUES (100), (200);""",
        "challenge": "Open two psql sessions on this schema. In session A, BEGIN; UPDATE accounts SET balance = balance + 10 WHERE id = 1; do not commit. In session B, try to update the same row and observe the wait using pg_locks.",
        "hints": [
            "In session B, run SELECT pid, relation::regclass, mode, granted FROM pg_locks WHERE relation::regclass = 'accounts'::regclass;",
            "Notice session B is blocked until session A commits or rolls back.",
            "End session A with COMMIT or ROLLBACK and watch session B proceed.",
        ],
        "outcome": [
            "The second update waited for the first transaction to finish.",
            "Releasing the transaction cleared the lock and let work continue.",
        ],
        "why": [
            "Long-running transactions hold locks and bloat tables.",
            "Keeping transaction scopes tight prevents cascading slowdowns in production.",
        ],
    },
    {
        "number": 20,
        "slug": "n-plus-one-pattern",
        "level_key": "level-2",
        "title": "N+1 Query Pattern",
        "concepts": ["Join vs loop", "Query counting", "EXPLAIN"] ,
        "summary": "Simulate an N+1 loop and replace it with a single join.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson20;\nSET search_path TO lesson20;\n\nCREATE TABLE authors (id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE posts (id SERIAL PRIMARY KEY, author_id INT NOT NULL REFERENCES authors(id), title TEXT);

INSERT INTO authors (name)
SELECT 'author ' || g FROM generate_series(1, 50) g;

INSERT INTO posts (author_id, title)
SELECT (random()*50)::int + 1, 'post ' || g FROM generate_series(1, 500) g;""",
        "challenge": "Count posts per author using two approaches: (1) loop-like pattern with repeated SELECTs, and (2) a single GROUP BY join. Compare timing.",
        "hints": [
            "Use \timing and run SELECT COUNT(*) FROM posts WHERE author_id = 1; repeatedly for a handful of authors.",
            "Then run SELECT a.name, COUNT(p.*) FROM authors a LEFT JOIN posts p ON p.author_id = a.id GROUP BY a.id;",
            "EXPLAIN shows why the grouped join is cheaper.",
        ],
        "outcome": [
            "Multiple single-row queries were slower and noisier.",
            "The grouped join returned all counts in one scan.",
        ],
        "why": [
            "N+1 patterns amplify latency and connection usage.",
            "Batching with joins keeps database load predictable under traffic spikes.",
        ],
    },
    {
        "number": 21,
        "slug": "jsonb-misuse",
        "level_key": "level-2",
        "title": "Misusing JSONB as a Bucket",
        "concepts": ["JSONB performance", "Functional indexes", "Normalization"],
        "summary": "See how deep JSONB filters can hurt without indexes or normalized columns.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson21;\nSET search_path TO lesson21;\n\nCREATE TABLE sessions (\n  id SERIAL PRIMARY KEY,\n  metadata JSONB NOT NULL\n);\n\nINSERT INTO sessions (metadata)
SELECT jsonb_build_object('user', 'user' || (g % 100), 'device', jsonb_build_object('os', CASE WHEN g % 2 = 0 THEN 'ios' ELSE 'android' END, 'version', g % 5))
FROM generate_series(1, 8000) g;""",
        "challenge": "Filter for ios devices with version 3 using a JSON path filter, then add a generated column for os and index it to compare speed.",
        "hints": [
            "SELECT * FROM sessions WHERE metadata -> 'device' ->> 'os' = 'ios' AND (metadata -> 'device' ->> 'version')::int = 3;",
            "ALTER TABLE sessions ADD COLUMN os TEXT GENERATED ALWAYS AS (metadata -> 'device' ->> 'os') STORED;",
            "Create an index on the generated os column and rerun the filter.",
        ],
        "outcome": [
            "JSON path filtering alone used a sequential scan.",
            "Generated column plus index made the same predicate faster and plan simpler.",
        ],
        "why": [
            "Not every field belongs inside JSONB—hot predicates deserve first-class columns.",
            "Functional or generated indexes keep flexible schemas fast as data grows.",
        ],
    },
    {
        "number": 22,
        "slug": "locking-surprises",
        "level_key": "level-2",
        "title": "Locking Surprises",
        "concepts": ["Row locks", "Lock modes", "Timeouts"],
        "summary": "Observe how SELECT ... FOR UPDATE blocks concurrent writes.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson22;\nSET search_path TO lesson22;\n\nCREATE TABLE inventory (\n  id SERIAL PRIMARY KEY,\n  sku TEXT NOT NULL UNIQUE,\n  quantity INT NOT NULL\n);\n\nINSERT INTO inventory (sku, quantity) VALUES ('sku-1', 5), ('sku-2', 10);""",
        "challenge": "Open two sessions. In session A, SELECT * FROM inventory WHERE sku='sku-1' FOR UPDATE; keep it open. In session B, try to update that row and watch it block until session A commits.",
        "hints": [
            "\watch pg_locks to see granted vs waiting locks.",
            "Session A finishes when you COMMIT or ROLLBACK.",
            "Session B will complete immediately after the lock is released.",
        ],
        "outcome": [
            "FOR UPDATE took a row-level lock visible in pg_locks.",
            "Concurrent UPDATE waited until the lock was released.",
        ],
        "why": [
            "Lock-heavy code paths can serialize traffic unexpectedly.",
            "Understanding row locks helps you design retry and backoff strategies.",
        ],
    },
    {
        "number": 23,
        "slug": "ignoring-explain",
        "level_key": "level-2",
        "title": "Ignoring EXPLAIN Is Costly",
        "concepts": ["Plan inspection", "Misestimates", "ANALYZE"],
        "summary": "Use EXPLAIN ANALYZE to catch misestimates before shipping.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson23;\nSET search_path TO lesson23;\n\nCREATE TABLE products (\n  id SERIAL PRIMARY KEY,\n  name TEXT NOT NULL,\n  price NUMERIC NOT NULL,\n  featured BOOLEAN DEFAULT FALSE\n);

INSERT INTO products (name, price, featured)
SELECT 'product ' || g, (10 + random()*90)::numeric, (g % 20 = 0)
FROM generate_series(1, 5000) g;

ANALYZE products;""",
        "challenge": "Write a query that filters featured products above a price threshold. Run EXPLAIN (ANALYZE, BUFFERS) and interpret whether the estimates match reality.",
        "hints": [
            "Try SELECT * FROM products WHERE featured AND price > 80;",
            "Look at rows vs loops vs actual rows in the plan output.",
            "ANALYZE updates stats; rerun EXPLAIN after ANALYZE if you change data.",
        ],
        "outcome": [
            "You observed planner row estimates and compared them to actuals.",
            "You gained confidence reading node costs, loops, and rows columns.",
        ],
        "why": [
            "Plan inspection catches performance issues before they hit users.",
            "Knowing what EXPLAIN says helps you decide between indexes, rewrites, or stats refreshes.",
        ],
    },
    {
        "number": 24,
        "slug": "security-basics",
        "level_key": "level-2",
        "title": "Roles and Privileges",
        "concepts": ["GRANT/REVOKE", "Least privilege", "Schemas"],
        "summary": "Practice creating roles and applying least-privilege grants.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson24;\nSET search_path TO lesson24;\n\nCREATE TABLE reports (\n  id SERIAL PRIMARY KEY,\n  body TEXT NOT NULL\n);

INSERT INTO reports (body) VALUES ('secret report');

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_reader') THEN
    CREATE ROLE app_reader NOLOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_writer') THEN
    CREATE ROLE app_writer NOLOGIN;
  END IF;
END $$;""",
        "challenge": "Grant read-only access on reports to app_reader and write access to app_writer. Verify privileges using SET ROLE and simple selects/inserts.",
        "hints": [
            "GRANT USAGE ON SCHEMA lesson24 TO app_reader; GRANT SELECT ON reports TO app_reader;",
            "GRANT INSERT, UPDATE, DELETE ON reports TO app_writer;",
            "SET ROLE app_reader; try an INSERT to see it fail; RESET ROLE when done.",
        ],
        "outcome": [
            "app_reader could read but not write; app_writer could modify rows.",
            "Schema usage and table privileges worked together to enforce access.",
        ],
        "why": [
            "Least privilege reduces blast radius of application bugs and SQL injection.",
            "Practicing grants helps you design safe default roles in production clusters.",
        ],
    },
    # Level 3 tasks
    {
        "number": 25,
        "slug": "mvcc-visibility",
        "level_key": "level-3",
        "title": "MVCC Visibility",
        "concepts": ["MVCC snapshots", "Transaction isolation", "Stale reads"],
        "summary": "Watch how two transactions see different row versions.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson25;\nSET search_path TO lesson25;\n\nCREATE TABLE notes (id SERIAL PRIMARY KEY, body TEXT);
INSERT INTO notes (body) VALUES ('original');""",
        "challenge": "Open two sessions. In session A, BEGIN; UPDATE notes SET body = 'updated in A' WHERE id = 1; do not commit. In session B, read the row in REPEATABLE READ and observe which version you see before and after A commits.",
        "hints": [
            "In session B: BEGIN ISOLATION LEVEL REPEATABLE READ; SELECT * FROM notes;",
            "Commit session A, then reread in session B and notice you still see the old value until you commit.",
            "After committing session B, read again to see the new version.",
        ],
        "outcome": [
            "Session B held a snapshot that hid A's uncommitted change until it ended.",
            "Committing B advanced its snapshot and revealed the new version.",
        ],
        "why": [
            "MVCC isolates readers from writers, but long snapshots can hide fresh data.",
            "Understanding visibility rules helps debug ""stale read"" reports in production.",
        ],
    },
    {
        "number": 26,
        "slug": "xmin-xmax",
        "level_key": "level-3",
        "title": "xmin/xmax Introspection",
        "concepts": ["Transaction IDs", "Tuple metadata", "Versioning"],
        "summary": "Inspect xmin/xmax to see which transactions touched a row.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson26;\nSET search_path TO lesson26;\n
CREATE TABLE ledger (id SERIAL PRIMARY KEY, amount INT);
INSERT INTO ledger (amount) VALUES (10);""",
        "challenge": "Select xmin/xmax before and after an update to see how tuple metadata changes.",
        "hints": [
            "SELECT xmin, xmax, * FROM ledger;",
            "UPDATE ledger SET amount = 20 WHERE id = 1; then select xmin/xmax again.",
            "Observe that xmax is 0 for live rows; xmin changes with each version.",
        ],
        "outcome": [
            "xmin updated to the transaction that performed the write.",
            "Old version became dead with a nonzero xmax visible only until vacuum removes it.",
        ],
        "why": [
            "xmin/xmax make MVCC tangible and debuggable.",
            "They help explain why bloat builds up when dead tuples stick around.",
        ],
    },
    {
        "number": 27,
        "slug": "dead-tuples",
        "level_key": "level-3",
        "title": "Dead Tuples After Deletes",
        "concepts": ["Dead tuples", "pg_stat_all_tables", "Bloat signals"],
        "summary": "Delete rows and watch dead tuple counters rise.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson27;\nSET search_path TO lesson27;\n\nCREATE TABLE clicks (id SERIAL PRIMARY KEY, path TEXT);

INSERT INTO clicks (path)
SELECT '/product/' || g FROM generate_series(1, 5000) g;

ANALYZE clicks;""",
        "challenge": "Delete half the rows, check pg_stat_all_tables for n_dead_tup, then vacuum and recheck.",
        "hints": [
            "DELETE FROM clicks WHERE id % 2 = 0;",
            "SELECT n_dead_tup FROM pg_stat_all_tables WHERE relname = 'clicks';",
            "VACUUM clicks; then query stats again.",
        ],
        "outcome": [
            "n_dead_tup increased after the delete.",
            "VACUUM cleared dead tuples and reset the counter.",
        ],
        "why": [
            "Deletes and updates leave behind dead tuples until vacuumed.",
            "Watching these counters helps you spot bloat before it hurts performance.",
        ],
    },
    {
        "number": 28,
        "slug": "vacuum-effects",
        "level_key": "level-3",
        "title": "VACUUM Effects",
        "concepts": ["VACUUM", "Visibility maps", "Table size"],
        "summary": "Run VACUUM VERBOSE to see what it reclaims and why.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson28;\nSET search_path TO lesson28;\n\nCREATE TABLE tasks (id SERIAL PRIMARY KEY, done BOOLEAN DEFAULT FALSE);
INSERT INTO tasks (done)
SELECT (g % 2 = 0) FROM generate_series(1, 4000) g;
DELETE FROM tasks WHERE done = TRUE;""",
        "challenge": "Run VACUUM VERBOSE on the table and read the output. Measure pg_class.reltuples before and after.",
        "hints": [
            "SELECT reltuples, relpages FROM pg_class WHERE relname = 'tasks';",
            "VACUUM (VERBOSE) tasks;",
            "Query pg_class again to compare reltuples estimate changes.",
        ],
        "outcome": [
            "VACUUM VERBOSE reported dead tuples removed and pages scanned.",
            "relpages or reltuples estimates adjusted after vacuuming.",
        ],
        "why": [
            "VACUUM keeps visibility maps accurate and tables lean.",
            "Reading its output demystifies what the maintainer process does automatically.",
        ],
    },
    {
        "number": 29,
        "slug": "autovacuum-observation",
        "level_key": "level-3",
        "title": "Observe Autovacuum",
        "concepts": ["autovacuum thresholds", "pg_stat_progress_vacuum", "Table settings"],
        "summary": "Force a small table to trigger autovacuum and watch its progress.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson29;\nSET search_path TO lesson29;\n\nCREATE TABLE msgs (id SERIAL PRIMARY KEY, body TEXT);
ALTER TABLE msgs SET (autovacuum_vacuum_scale_factor = 0.0, autovacuum_vacuum_threshold = 10);
INSERT INTO msgs (body)
SELECT 'msg ' || g FROM generate_series(1, 200) g;""",
        "challenge": "Delete enough rows to cross the autovacuum threshold, wait briefly, and query pg_stat_progress_vacuum or pg_stat_all_tables to see autovacuum activity.",
        "hints": [
            "DELETE FROM msgs WHERE id <= 120;",
            "Repeatedly query SELECT last_autovacuum, vacuum_count FROM pg_stat_all_tables WHERE relname = 'msgs';",
            "If autovacuum runs quickly, you may only catch the timestamp update rather than a live row in pg_stat_progress_vacuum.",
        ],
        "outcome": [
            "After deleting rows, autovacuum triggered and updated last_autovacuum/vacuum_count.",
            "You may briefly see a row in pg_stat_progress_vacuum while it runs.",
        ],
        "why": [
            "Autovacuum keeps the system healthy without manual work, but only if thresholds fit your workload.",
            "Knowing how to check its progress helps when diagnosing bloat or lock issues.",
        ],
    },
    {
        "number": 30,
        "slug": "wal-behavior",
        "level_key": "level-3",
        "title": "WAL Growth from Writes",
        "concepts": ["Write-Ahead Log", "LSN", "Durability"],
        "summary": "Measure WAL position before and after a burst of writes.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson30;\nSET search_path TO lesson30;\n\nCREATE TABLE events (id SERIAL PRIMARY KEY, body TEXT);
SELECT pg_current_wal_lsn() AS lsn_before;""",
        "challenge": "Insert a few thousand rows, then compare pg_current_wal_lsn() to see WAL advancement. Optionally check pg_walfile_name(lsn).",
        "hints": [
            "INSERT INTO events (body) SELECT 'event ' || g FROM generate_series(1, 3000) g;",
            "SELECT pg_current_wal_lsn() AS lsn_after;",
            "Use pg_wal_lsn_diff to compute the byte difference between lsn_after and lsn_before.",
        ],
        "outcome": [
            "WAL LSN advanced by several MB after the inserts.",
            "You saw how every write is logged for crash safety and replication.",
        ],
        "why": [
            "WAL growth ties directly to write volume and replication lag.",
            "Measuring WAL churn helps plan disk capacity and replica bandwidth.",
        ],
    },
    {
        "number": 31,
        "slug": "buffer-cache-effects",
        "level_key": "level-3",
        "title": "Buffer Cache Effects",
        "concepts": ["Shared buffers", "Cache hits", "EXPLAIN BUFFERS"],
        "summary": "Run the same query twice and compare buffer hits vs reads.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson31;\nSET search_path TO lesson31;\n\nCREATE TABLE sales (id SERIAL PRIMARY KEY, amount NUMERIC);
INSERT INTO sales (amount)
SELECT (random()*100)::numeric FROM generate_series(1, 20000) g;
ANALYZE sales;""",
        "challenge": "Enable timing and run a filtered query twice with EXPLAIN (ANALYZE, BUFFERS) to observe shared hit vs read counts.",
        "hints": [
            "\timing ON;",
            "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM sales WHERE amount > 90; run it twice.",
            "The second run should show more shared hits and fewer reads.",
        ],
        "outcome": [
            "First run hit more disk reads; second run showed mostly shared hits.",
            "Execution time improved once data was warm in cache.",
        ],
        "why": [
            "Cache warmth explains why first requests are slower after deploys or failovers.",
            "Observing buffers helps differentiate I/O waits from CPU-bound work.",
        ],
    },
    {
        "number": 32,
        "slug": "index-vs-heap",
        "level_key": "level-3",
        "title": "Index-Only vs Heap Fetch",
        "concepts": ["Index-only scans", "Visibility map", "INCLUDE columns"],
        "summary": "Contrast index-only scans with heap visits using an included column.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson32;\nSET search_path TO lesson32;\n\nCREATE TABLE emails (\n  id SERIAL PRIMARY KEY,\n  address TEXT NOT NULL,\n  last_opened TIMESTAMPTZ\n);

INSERT INTO emails (address, last_opened)
SELECT 'user' || g || '@example.com', now() - (g || ' minutes')::interval
FROM generate_series(1, 5000) g;

CREATE INDEX ON emails (address);
CREATE INDEX ON emails (address) INCLUDE (last_opened);
VACUUM ANALYZE emails;""",
        "challenge": "Compare EXPLAIN (ANALYZE, BUFFERS) for a query selecting address only versus selecting address and last_opened. Note when index-only scans appear.",
        "hints": [
            "Run EXPLAIN (ANALYZE, BUFFERS) SELECT address FROM emails WHERE address LIKE 'user1%';",
            "Then select address, last_opened with the same predicate.",
            "Index-only scans require pages to be marked all-visible; VACUUM helps.",
        ],
        "outcome": [
            "Address-only query could use an index-only scan.",
            "Including last_opened forced heap fetch unless the INCLUDE index satisfied it.",
        ],
        "why": [
            "Covering indexes cut heap visits and reduce I/O on hot paths.",
            "Knowing when index-only scans occur informs which columns to include for read-heavy workloads.",
        ],
    },
    {
        "number": 33,
        "slug": "sequential-vs-index-scan",
        "level_key": "level-3",
        "title": "Sequential vs Index Scan",
        "concepts": ["Planner toggles", "enable_seqscan", "Cost comparison"],
        "summary": "Toggle planner preferences to see how scan types change.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson33;\nSET search_path TO lesson33;\n\nCREATE TABLE inventory_items (\n  id SERIAL PRIMARY KEY,\n  name TEXT,
  quantity INT
);

INSERT INTO inventory_items (name, quantity)
SELECT 'item ' || g, (random()*100)::int FROM generate_series(1, 15000) g;
CREATE INDEX ON inventory_items (quantity);
ANALYZE inventory_items;""",
        "challenge": "Run the same predicate with and without enable_seqscan to see plan shifts for a selective filter.",
        "hints": [
            "SET enable_seqscan = on; EXPLAIN SELECT * FROM inventory_items WHERE quantity = 99;",
            "SET enable_seqscan = off; run the EXPLAIN again.",
            "Reset the GUC with RESET enable_seqscan when done.",
        ],
        "outcome": [
            "Planner chose sequential scan when allowed, index scan when forced.",
            "You saw how planner cost parameters influence decisions.",
        ],
        "why": [
            "Tuning planner settings can highlight missing stats or index usefulness.",
            "Understanding why the planner chooses a scan type helps justify indexes or rewrites.",
        ],
    },
    {
        "number": 34,
        "slug": "planner-costs",
        "level_key": "level-3",
        "title": "Planner Cost Tweaks",
        "concepts": ["random_page_cost", "seq_page_cost", "Plan selection"],
        "summary": "Adjust cost settings to watch plan choices flip.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson34;\nSET search_path TO lesson34;\n\nCREATE TABLE readings (\n  id SERIAL PRIMARY KEY,\n  sensor TEXT,
  value NUMERIC
);

INSERT INTO readings (sensor, value)
SELECT 's' || (g % 3), (random()*100)::numeric FROM generate_series(1, 20000) g;
CREATE INDEX ON readings (sensor);
ANALYZE readings;""",
        "challenge": "Check the plan for a common sensor filter, then lower random_page_cost to make index access more attractive and compare.",
        "hints": [
            "EXPLAIN SELECT * FROM readings WHERE sensor = 's1';",
            "SET random_page_cost = 1.0; run the EXPLAIN again.",
            "RESET random_page_cost afterward to avoid affecting other sessions.",
        ],
        "outcome": [
            "Lowering random_page_cost nudged the planner toward index scans if not already using them.",
            "You saw how cost parameters influence plan selection without schema changes.",
        ],
        "why": [
            "Cost settings are a tuning lever when storage or caching changes.",
            "Understanding them helps interpret plans on fast disks vs slower media.",
        ],
    },
    {
        "number": 35,
        "slug": "lock-modes",
        "level_key": "level-3",
        "title": "Locks and Lock Modes",
        "concepts": ["Lock levels", "pg_locks", "Blocking chains"],
        "summary": "Observe how table vs row locks interact.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson35;\nSET search_path TO lesson35;\n\nCREATE TABLE docs (id SERIAL PRIMARY KEY, body TEXT);
INSERT INTO docs (body) VALUES ('v1');""",
        "challenge": "Open two sessions. In session A, LOCK TABLE docs IN SHARE MODE; keep it open. In session B, try to ALTER TABLE docs ADD COLUMN note TEXT and watch the block, then check pg_locks.",
        "hints": [
            "Session A holds a lock that conflicts with the DDL session B wants.",
            "Query pg_locks in either session to see the waiting lock with granted = false.",
            "Release the lock in session A to let the DDL proceed.",
        ],
        "outcome": [
            "DDL waited behind an existing SHARE lock.",
            "pg_locks showed blocking relationships between sessions.",
        ],
        "why": [
            "Understanding lock modes prevents surprise outages during migrations.",
            "Inspecting pg_locks is a fast way to debug blocked sessions in production.",
        ],
    },
    {
        "number": 36,
        "slug": "explain-analyze-reading",
        "level_key": "level-3",
        "title": "Read EXPLAIN ANALYZE Like a Pro",
        "concepts": ["EXPLAIN ANALYZE", "Actual vs estimated", "Node timing"],
        "summary": "Practice reading plan output to identify hot spots.",
        "setup": """CREATE SCHEMA IF NOT EXISTS lesson36;\nSET search_path TO lesson36;\n\nCREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, total NUMERIC, created_at TIMESTAMPTZ DEFAULT now());
INSERT INTO orders (customer_id, total, created_at)
SELECT (random()*50)::int, (10 + random()*90)::numeric, now() - (g || ' minutes')::interval
FROM generate_series(1, 8000) g;
CREATE INDEX ON orders (customer_id);
ANALYZE orders;""",
        "challenge": "Run EXPLAIN (ANALYZE, BUFFERS, VERBOSE) on a query that filters customer_id and orders by created_at. Identify which node dominates time and where estimates differ.",
        "hints": [
            "Try SELECT * FROM orders WHERE customer_id = 10 ORDER BY created_at DESC LIMIT 20;",
            "Look for loops, rows, and timing columns to find the slowest node.",
            "Note if the LIMIT is applied after a sort or if an index provides order already.",
        ],
        "outcome": [
            "You identified the node consuming the most time (often the sort or index scan).",
            "You compared estimated vs actual rows to judge planner accuracy.",
        ],
        "why": [
            "Reading plans quickly is a superpower during incidents.",
            "Knowing where time goes guides whether to add indexes, change queries, or adjust parameters.",
        ],
    },
]


def render_task(task):
    level = levels[task["level_key"]]
    concepts = "\n".join(f"- {c}" for c in task["concepts"])
    hints = "\n".join(f"{i+1}. {hint}" for i, hint in enumerate(task["hints"]))
    outcome = "\n".join(f"- {o}" for o in task["outcome"])
    why = "\n".join(f"- {w}" for w in task["why"])
    content = f"""---
title: \"Task {task['number']:02d} — {task['title']}\"
weight: {task['number']}
level: \"{level}\"
summary: \"{task['summary']}\"
---

# Task {task['number']:02d} — {task['title']}

Level:
{level}

Estimated Time:
~5 minutes

Concept(s):
{concepts}

## ⚙️ Setup

```sql
{task['setup']}
```

## 🧠 Challenge

{task['challenge']}

## 🧭 Hints (Progressive)

{hints}

## ✅ Expected Observation / Outcome

{outcome}

## 🤔 Why This Matters

{why}
"""
    return content


for task in tasks:
    level_dir = base / task["level_key"]
    level_dir.mkdir(parents=True, exist_ok=True)
    path = level_dir / f"task-{task['number']:02d}.md"
    path.write_text(render_task(task))

print(f"Generated {len(tasks)} lessons.")
