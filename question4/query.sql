-- 1. DROP the table if it exists to ensure a clean slate and avoid conflicts
DROP TABLE IF EXISTS AOL_SCHEMA.ECOM_EVENTS CASCADE;

CREATE TABLE AOL_SCHEMA.ECOM_EVENTS (
    EVENT_ID DECIMAL(18,0) NOT NULL PRIMARY KEY,
    EVENT_DATE DATE, -- Retained for original source date of the event
    EVENT_KEYWORD VARCHAR(100) UTF8,
    EVENT_TYPE VARCHAR(50) UTF8,
    DESCRIPTION VARCHAR(500) UTF8
);


INSERT INTO AOL_SCHEMA.ECOM_EVENTS (EVENT_ID, EVENT_DATE, EVENT_KEYWORD, EVENT_TYPE, DESCRIPTION) VALUES
-- 1. Infrastructure Launch (Mid-March)
(1, '2006-03-14', 'AMAZON S3', 'Service Launch', 'Amazon Web Services S3 launched, signaling a major shift in digital infrastructure.'),

-- 2. Core Digital Media Update (Late March)
(2, '2006-03-29', 'EBAY ACQUISITION', 'Marketplace News', 'eBay acquired Skype (finalized later), signaling major expansion into digital communication.'),

-- 3. Digital Music Regulation/Pressure (Early April)
(3, '2006-04-10', 'RIAA LAWSUITS', 'Legal Action', 'RIAA escalated lawsuits against file-sharing, driving searches for legal music.'),

-- 4. Digital Media Competitor (Mid-April)
(4, '2006-04-16', 'NETFLIX', 'Service Update', 'Netflix began offering a monetary prize for the best video recommendation algorithm.'),

-- 5. Major Platform Launch (Late April)
(5, '2006-04-23', 'SPOTIFY', 'Platform Launch', 'Spotify was founded, suggesting early searches for the concept/brand.'),

-- 6. Social Commerce Growth (Early May)
(6, '2006-05-01', 'FACEBOOK', 'Feature Launch', 'Facebook opened its platform beyond college networks, potentially increasing general e-commerce search reach.'),

-- 7. Digital Music Competitor (Early May)
(7, '2006-05-09', 'YAHOO MUSIC', 'Service Update', 'Yahoo! Music Unlimited launched new features, increasing competition for digital music.'),

-- 8. Payment Infrastructure (Mid-May)
(8, '2006-05-18', 'GOOGLE CHECKOUT', 'Infrastructure Launch', 'Google announced early plans for its checkout service, impacting general e-commerce payment searches.'),

-- 9. Core Digital Media Update (Late May)
(9, '2006-05-30', 'ITUNES VIDEO', 'Product Update', 'Major update to iTunes video capabilities, stimulating video-related digital searches.'),

-- 10. E-commerce Platform Startup (June - for Q2 closure)
(10, '2006-06-01', 'SHOPIFY', 'Platform Launch', 'Shopify officially launched its first iteration as an e-commerce platform.');



-- Maps the events date to the TIMEDIM
CREATE OR REPLACE TABLE AOL_SCHEMA.ECOM_EVENT_TIME AS
-- Selects the EVENT_ID and ALL corresponding TIMEID values for that day
SELECT
    E.EVENT_ID,
    T.ID AS TIMEID -- The granular Time ID (e.g., 77,294 records for one day)
FROM
    AOL_SCHEMA.ECOM_EVENTS E
JOIN
    AOL_SCHEMA.TIMEDIM T ON 
        -- 1. Match on Year (TO_CHAR is used to extract components from the DATE type)
        T."year" = TO_CHAR(E.EVENT_DATE, 'YYYY')
        
        -- 2. Match on Month Name (Requires careful handling of padding and case)
        -- We convert the date's month name to lowercase and TRIM it, matching the format in TIMEDIM
        AND TRIM(T."month") = LOWER(TRIM(TO_CHAR(E.EVENT_DATE, 'Month')))
        
        -- 3. Match on Day of the Month (Requires conversion to string/char format)
        -- We convert the DATE's day to a string/char format to match TIMEDIM."day of the month"
        AND T."day of the month" = TO_CHAR(E.EVENT_DATE, 'DD');

        
        
-- For Q4 visualization
WITH Daily_Searches AS (
    -- Get the total digital search volume for every day in the quarter
    SELECT
        -- Convert month name to number (MM) for a consistent YYYY-MM-DD format
        T."year" || '-' || 
        CASE TRIM(T."month")
            WHEN 'march' THEN '03'
            WHEN 'april' THEN '04'
            WHEN 'may' THEN '05'
            ELSE 'XX' -- Fallback for error checking
        END || '-' || 
        T."day of the month" AS Event_Date_String,
        COUNT(F.QUERYID) AS Total_Daily_Digital_Searches,
        COUNT(DISTINCT F.ANONID) AS Unique_Daily_Digital_Users -- NEW METRIC
    FROM
        AOL_SCHEMA.FACTS F
    JOIN
        AOL_SCHEMA.TIMEDIM T ON F.TIMEID = T.ID
    JOIN
        AOL_SCHEMA.DIGITAL_QUERY_IDS DQI ON F.QUERYID = DQI.QUERYID
    GROUP BY 1
)
SELECT * FROM Daily_Searches
ORDER BY Event_Date_String;

        
        
SELECT
    E.EVENT_DATE,
    E.EVENT_KEYWORD,
    COUNT(F.QUERYID) AS High_Intent_Search_Count,
    -- Get the total number of unique users involved in this event's search spike
--    COUNT(DISTINCT F.ANONID) AS Unique_Users_Involved
FROM
    AOL_SCHEMA.FACTS F
-- 1. Join to the bridge table to filter FACTS by the event dates
JOIN
    AOL_SCHEMA.ECOM_EVENT_TIME EET ON F.TIMEID = EET.TIMEID
-- 2. Join to the event definition table to retrieve the event details
JOIN
    AOL_SCHEMA.ECOM_EVENTS E ON EET.EVENT_ID = E.EVENT_ID
-- 3. Join to the digital query staging table to ensure only digital commerce searches are counted
JOIN
    AOL_SCHEMA.DIGITAL_QUERY_IDS DQI ON F.QUERYID = DQI.QUERYID
WHERE
    F.CLICK = TRUE -- Crucial: Focus only on high-intent user activity (clicks)
GROUP BY 1, 2
ORDER BY E.EVENT_DATE;