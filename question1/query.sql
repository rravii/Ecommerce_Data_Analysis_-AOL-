-- adding search key word table
-- 1. DROP the table if it exists to ensure a clean slate and avoid conflicts
DROP TABLE IF EXISTS AOL_SCHEMA.DIGITAL_KEYWORD_DIM CASCADE;

-- 2. CREATE the table structure
CREATE TABLE AOL_SCHEMA.DIGITAL_KEYWORD_DIM (
    KEYWORD_ID DECIMAL(18,0) NOT NULL PRIMARY KEY,
    SEARCH_TERM VARCHAR(100) UTF8,
    CATEGORY VARCHAR(50) UTF8
);

-- 3. INSERT the focused, high-confidence digital commerce terms
INSERT INTO AOL_SCHEMA.DIGITAL_KEYWORD_DIM (KEYWORD_ID, SEARCH_TERM, CATEGORY) VALUES
-- ====================================================================================
-- HIGH-CONFIDENCE DIGITAL MEDIA & CONTENT
-- ====================================================================================
(200, 'download',        'Media/Digital'),
(201, 'mp3',             'Media/Music'),
(202, 'ringtone',        'Media/Music'),
(205, 'ebook',           'Media/Reading'),

-- ====================================================================================
-- CORE SOFTWARE & TECH
-- ====================================================================================
(300, 'software',        'Software/Tech'),
(308, 'antivirus',       'Software/Tech'),

-- ====================================================================================
-- KEY E-COMMERCE BRANDS (Focusing on Digital/High-Volume Ecom)
-- ====================================================================================
(400, 'itunes',          'Brand/Music'),
(402, 'spotify',         'Brand/Music'),
(404, 'steam',           'Brand/Games'),
(401, 'audible',         'Brand/Reading'),
(407, 'amazon',          'Brand/General'),
(406, 'ebay',            'Brand/General');


-- ====================================================================================
-- MATERIALIZE VIEW (STAGING TABLE) DIGITAL_QUERY_IDS
-- ====================================================================================   
CREATE OR REPLACE TABLE AOL_SCHEMA.DIGITAL_QUERY_IDS AS
-- Select all unique Query IDs that match any of our extensive list of search terms
SELECT DISTINCT
    Q.ID AS QUERYID,
    Q.QUERY AS QUERY,
    K.CATEGORY AS CATEGORY
FROM
    AOL_SCHEMA.QUERYDIM Q
JOIN
    AOL_SCHEMA.DIGITAL_KEYWORD_DIM K
    -- Join using the slow, but necessary, case-insensitive string match
    ON LOWER(Q.QUERY) LIKE '%' || K.SEARCH_TERM || '%';
   
 
-- ====================================================================================
-- QUESTION 1 SQL TO GET DATA
-- ====================================================================================   
   
    SELECT
    TRIM(T."month") AS Sales_Month,
    T."calender week",
    -- COUNT all records that exist in the staging table
    COUNT(F.QUERYID) AS Digital_Search_Count
FROM
    AOL_SCHEMA.FACTS F
JOIN
    AOL_SCHEMA.TIMEDIM T ON F.TIMEID = T.ID
JOIN
    AOL_SCHEMA.DIGITAL_QUERY_IDS DQI ON F.QUERYID = DQI.QUERYID -- FAST INTEGER JOIN HERE!
GROUP BY ROLLUP(TRIM(T."month"), T."calender week")
ORDER BY 
    -- Custom sort order for month: March (1), April (2), May (3)
    CASE TRIM(T."month") 
        WHEN 'march' THEN 1
        WHEN 'april' THEN 2
        WHEN 'may' THEN 3
        ELSE 4 
    END,
    T."calender week";