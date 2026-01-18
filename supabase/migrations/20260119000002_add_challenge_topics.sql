-- Add challenge_topics column to winners_payload table
ALTER TABLE public.winners_payload 
ADD COLUMN IF NOT EXISTS challenge_topics jsonb;

COMMENT ON COLUMN public.winners_payload.challenge_topics IS 'Challenge topics and themes for each year';
