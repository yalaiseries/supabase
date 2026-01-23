-- Verify video_recordings data
-- Run this in Supabase SQL Editor to check if data was inserted

SELECT * FROM video_recordings ORDER BY year DESC, sort_order;

-- Expected result: 11 rows
-- 2025: 2 videos
-- 2024: 8 videos
-- 2023: 1 video

-- If you see 0 rows, run the INSERT_VIDEO_RECORDINGS.sql file again
