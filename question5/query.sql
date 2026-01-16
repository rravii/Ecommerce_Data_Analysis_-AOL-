-- 1. Create the table structure for FINANCIAL_TRENDS_DIM
DROP TABLE IF EXISTS AOL_SCHEMA.FINANCIAL_TRENDS_DIM CASCADE;
CREATE TABLE AOL_SCHEMA.FINANCIAL_TRENDS_DIM (
    STOCK_DATE DATE,
    TICKER VARCHAR(10) UTF8,
    OPEN_PRICE DECIMAL(18,4),
    HIGH_PRICE DECIMAL(18,4),
    LOW_PRICE DECIMAL(18,4),
    CLOSE_PRICE DECIMAL(18,4),
    ADJ_CLOSE_PRICE DECIMAL(18,4), -- Crucial for analysis
    VOLUME DECIMAL(20,0)
);

-- 2. Set the Primary Key to the Composite Key of Date and Ticker
-- This ensures each stock (AAPL, EBAY) has only one price entry per day.
ALTER TABLE AOL_SCHEMA.FINANCIAL_TRENDS_DIM
ADD CONSTRAINT FINANCIAL_TRENDS_DIM_PK PRIMARY KEY (STOCK_DATE, TICKER) ENABLE;


-- ==========================================================
-- 3. Populate the FINANCIAL_TRENDS_DIM table using the data/FINANCIAL_TRENDS_DIM.csv file
-- ==========================================================


-- ==========================================================
-- 4. Query the data for the plot
-- ==========================================================
WITH Daily_Digital_Searches AS (
    -- 1. Aggregate the daily count of high-intent digital searches
    SELECT
        T."year" || '-' || 
        CASE TRIM(T."month") WHEN 'march' THEN '03' WHEN 'april' THEN '04' WHEN 'may' THEN '05' END || '-' || 
        T."day of the month" AS Date_Key,
        COUNT(F.QUERYID) AS Total_Daily_Digital_Searches
    FROM
        AOL_SCHEMA.FACTS F
    JOIN
        AOL_SCHEMA.TIMEDIM T ON F.TIMEID = T.ID
    JOIN
        AOL_SCHEMA.DIGITAL_QUERY_IDS DQI ON F.QUERYID = DQI.QUERYID
    WHERE
        F.CLICK = TRUE 
    GROUP BY 1
),
Cumulative_AOL_Trend AS (
    -- 2. FIX: Calculate the Cumulative Average (fully supported advanced window function)
    SELECT
        DDS.Date_Key,
        DDS.Total_Daily_Digital_Searches,
        -- CRITICAL FIX: Use the supported UNBOUNDED PRECEDING frame
        AVG(DDS.Total_Daily_Digital_Searches) 
        OVER (
            ORDER BY DDS.Date_Key ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS Cumulative_Search_Avg -- Renamed metric
    FROM
        Daily_Digital_Searches DDS
)
-- 3. Final Join: Correlate the internal AOL trend with the external financial trend
SELECT
    CAT.Date_Key,
    CAT.Total_Daily_Digital_Searches,
    ROUND(CAT.Cumulative_Search_Avg, 3) AS Cumulative_Search_Avg,
    FTD.ADJ_CLOSE_PRICE,
    FTD.TICKER
FROM
    Cumulative_AOL_Trend CAT
JOIN
    AOL_SCHEMA.FINANCIAL_TRENDS_DIM FTD 
    ON CAT.Date_Key = TO_CHAR(FTD.STOCK_DATE, 'YYYY-MM-DD')
WHERE
    FTD.TICKER = 'AAPL'
--    FTD.TICKER = 'EBAY'
ORDER BY CAT.Date_Key;