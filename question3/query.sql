WITH Digital_Clicks AS (
    -- Step 1: Filter the base data to include only high-intent (clicked) digital searches
    SELECT
        DQI.CATEGORY,
        U.THISDOMAIN,
        F.QUERYID
    FROM
        AOL_SCHEMA.FACTS F
    JOIN
        AOL_SCHEMA.URLDIM U ON F.URLID = U.ID
    JOIN
        AOL_SCHEMA.DIGITAL_QUERY_IDS DQI ON F.QUERYID = DQI.QUERYID
    WHERE
        F.CLICK = TRUE
),
Ranked_Domains AS (
    -- Step 2: Aggregate the data and calculate the RANK within each CATEGORY
    SELECT
        CATEGORY,
        THISDOMAIN,
        COUNT(QUERYID) AS Domain_Click_Count,
        -- Apply the RANK window function
        RANK() OVER (
            PARTITION BY CATEGORY -- Resets the rank for each Category (e.g., Music, Software)
            ORDER BY COUNT(QUERYID) DESC
        ) AS Domain_Rank_Within_Category
    FROM
        Digital_Clicks
    GROUP BY 1, 2
)
-- Step 3: Final SELECT statement filters the pre-calculated rank using a simple WHERE clause
SELECT
    CATEGORY,
    THISDOMAIN,
    Domain_Click_Count,
    Domain_Rank_Within_Category
FROM
    Ranked_Domains
WHERE
    Domain_Rank_Within_Category <= 5 -- Filter for the Top 5
ORDER BY CATEGORY, Domain_Rank_Within_Category;