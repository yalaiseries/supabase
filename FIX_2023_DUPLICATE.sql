-- First, check how many 2023 entries exist
SELECT * FROM video_recordings WHERE year = 2023;

-- Delete all 2023 entries first
DELETE FROM video_recordings WHERE year = 2023;

-- Re-insert just ONE 2023 entry
INSERT INTO video_recordings (year, date_text, title, url, sort_order) VALUES
(2023, '2023 and earlier', 'YAL AI Talks and earlier computational BIM workshops', 'https://www.integrations.space/p/past-workshops.html', 1);

-- Verify - should show exactly 1 row for 2023
SELECT * FROM video_recordings WHERE year = 2023;
