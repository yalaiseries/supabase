-- Update 2024 category name from "Merit Awards" to "Merit Prizes"
UPDATE winners_payload
SET category = 'Merit Prizes'
WHERE year = 2024 AND category = 'Merit Awards';

-- Verify the update
SELECT year, category, COUNT(*) as count
FROM winners_payload
GROUP BY year, category
ORDER BY year DESC, category;
