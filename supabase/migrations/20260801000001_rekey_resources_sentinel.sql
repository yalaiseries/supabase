-- Free up year 2026 in public.winners_payload so it can hold real 2026 winners.
--
-- Until now the row at year = 2026 held the public AI/AECO Resources payload,
-- and the RLS policy granted anon SELECT on that literal year. Winners content
-- is members-only, so 2026 could not be used for winners while that was true --
-- inserting winners there would have exposed them to the open internet.
--
-- Re-key the resources payload onto a non-year sentinel (9999) and move the
-- public policy with it. Idempotent: re-running is a no-op.

-- 1) Move the resources payload off the 2026 slot.
UPDATE public.winners_payload SET year = 9999 WHERE year = 2026;

-- 2) Point the anon-readable policy at the new sentinel.
DROP POLICY IF EXISTS winners_payload_public_resources_2026 ON public.winners_payload;
DROP POLICY IF EXISTS winners_payload_public_resources ON public.winners_payload;
CREATE POLICY winners_payload_public_resources
  ON public.winners_payload
  FOR SELECT
  TO anon, authenticated
  USING (year = 9999);
