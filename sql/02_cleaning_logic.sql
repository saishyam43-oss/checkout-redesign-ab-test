-- =========================================================
-- 02_cleaning_logic.sql
-- Purpose: Enforce experimental integrity and deduplicate users
-- =========================================================

WITH full_data AS (
    -- 1. Join assignment data with country metadata
    SELECT
        a.user_id,
        a."group",
        a.landing_page,
        a.converted
    FROM ab_test_assignments AS a
    LEFT JOIN user_countries AS c
        ON a.user_id = c.user_id
),

valid_users AS (
    -- 2. Remove incorrect group–page combinations
    -- This ensures users only see the page they were assigned to
    SELECT
        user_id,
        "group",
        converted
    FROM full_data
    WHERE ("group" = 'control' AND landing_page = 'old_page')
       OR ("group" = 'treatment' AND landing_page = 'new_page')
),

deduplicated_users AS (
    -- 3. Deduplicate users
    -- If a user appears multiple times, treat conversion as binary:
    -- if they converted once, they are a converter
    SELECT
        user_id,
        "group",
        MAX(converted) AS converted_status
    FROM valid_users
    GROUP BY user_id, "group"
)

SELECT *
FROM deduplicated_users;
