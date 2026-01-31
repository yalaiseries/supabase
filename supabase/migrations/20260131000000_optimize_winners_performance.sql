-- Optimize winners_payload table for better query performance
-- Add index on year column for faster filtering
CREATE INDEX IF NOT EXISTS idx_winners_payload_year ON public.winners_payload(year);

-- Add index on updated_at for cache invalidation queries
CREATE INDEX IF NOT EXISTS idx_winners_payload_updated_at ON public.winners_payload(updated_at DESC);

-- Add GIN index on payload JSONB for faster JSON queries (if needed in future)
CREATE INDEX IF NOT EXISTS idx_winners_payload_payload_gin ON public.winners_payload USING GIN(payload);

-- Analyze table to update query planner statistics
ANALYZE public.winners_payload;

-- Optional: Add materialized view for faster repeated queries
-- This would be useful if you query the same data frequently
-- Uncomment if you want to use this approach:
/*
CREATE MATERIALIZED VIEW IF NOT EXISTS winners_library_cache AS
SELECT 
  year,
  payload,
  challenge_topics,
  updated_at
FROM public.winners_payload
WHERE year IN (2024, 2025)
ORDER BY year DESC;

-- Create index on the materialized view
CREATE INDEX IF NOT EXISTS idx_winners_library_cache_year ON winners_library_cache(year);

-- Refresh the view (needs to be run after each data update)
-- REFRESH MATERIALIZED VIEW winners_library_cache;
*/
