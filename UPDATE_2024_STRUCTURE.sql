-- Split 2024 "AI Programme Winners" into "Top Winners" and "Merit Prizes"
-- This SQL updates the winners_payload JSON structure for 2024

-- First, let's see what we're working with
SELECT id, year, category, payload->'categories'->0->>'category' as current_category
FROM winners_payload 
WHERE year = 2024;

-- NOTE: This update needs to be done via a Python script since we need to:
-- 1. Parse the JSON payload
-- 2. Split useCases array based on award field
-- 3. Create two separate category objects
-- 4. Update the payload back to the database

-- The logic should be:
-- - Top Winners: awards containing "Prize Winner" (First/Second/Third)
-- - Merit Prizes: awards containing "Merit Prize"
