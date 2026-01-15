-- =========================================================
-- 03_final_metrics.sql
-- Purpose: Compute final A/B test metrics for analysis
-- =========================================================

WITH cleaned_users AS (
    -- Reuse the cleaned, deduplicated dataset
    SELECT
        user_id,
        "group",
        MAX(converted) AS converted_status
    FROM (
        SELECT
            a.user_id,
            a."group",
            a.landing_page,
            a.converted
        FROM ab_test_assignments AS a
        WHERE ("group" = 'control' AND landing_page = 'old_page')
           OR ("group" = 'treatment' AND landing_page = 'new_page')
    ) t
    GROUP BY user_id, "group"
)

-- Final aggregation used for z-test and dashboard
SELECT
    "group",
    COUNT(user_id) AS total_users,
    SUM(converted_status) AS converted_users,
    SUM(converted_status) * 1.0 / COUNT(user_id) AS conversion_rate
FROM cleaned_users
GROUP BY "group";
