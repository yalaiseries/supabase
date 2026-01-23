-- Check for duplicate entries in video_recordings
SELECT year, date_text, title, COUNT(*) as count
FROM video_recordings
GROUP BY year, date_text, title
HAVING COUNT(*) > 1;

-- If you see duplicates, run this to delete them:
-- Keep only the first entry of each duplicate
DELETE FROM video_recordings
WHERE id NOT IN (
  SELECT MIN(id)
  FROM video_recordings
  GROUP BY year, date_text, title, url
);

-- Verify the data after cleanup
SELECT * FROM video_recordings ORDER BY year DESC, sort_order;
