-- =========================================================
-- 01_data_validation.sql
-- Purpose: Validate raw A/B test data before any analysis
-- =========================================================

-- 1. Quick inspection of raw assignment data
SELECT *
FROM ab_test_assignments
LIMIT 5;

-- 2. Verify schema and datatypes
SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'ab_test_assignments';

-- 3. Check for duplicate user assignments
-- Each user should ideally appear once
SELECT
    user_id,
    COUNT(*) AS record_count
FROM ab_test_assignments
GROUP BY user_id
HAVING COUNT(*) > 1;

-- 4. Check for nulls or incomplete rows
-- Critical fields must never be NULL
SELECT *
FROM ab_test_assignments
WHERE user_id IS NULL
   OR "group" IS NULL
   OR landing_page IS NULL
   OR converted IS NULL;

-- 5. Validate country mapping table
SELECT COUNT(*) AS total_rows,
       COUNT(DISTINCT user_id) AS unique_users
FROM user_countries;

-- 6. Sanity check conversion distribution
SELECT
    COUNT(DISTINCT user_id) AS users,
    SUM(converted) AS total_conversions
FROM ab_test_assignments;
