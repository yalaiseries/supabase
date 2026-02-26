-- Re-enable RLS on tables exposed to PostgREST and add explicit policies.
-- Security Advisor flagged these tables because RLS had been disabled.

-- 1) allowed_members: authenticated users can only read their own email row.
ALTER TABLE public.allowed_members ENABLE ROW LEVEL SECURITY;

REVOKE ALL ON TABLE public.allowed_members FROM anon;
GRANT SELECT ON TABLE public.allowed_members TO authenticated;

DROP POLICY IF EXISTS allowed_members_select_own_email ON public.allowed_members;
CREATE POLICY allowed_members_select_own_email
  ON public.allowed_members
  FOR SELECT
  TO authenticated
  USING (lower(email) = lower(coalesce(auth.jwt() ->> 'email', '')));

-- 2) winners_payload: keep 2026 resources publicly readable for resources.html.
ALTER TABLE public.winners_payload ENABLE ROW LEVEL SECURITY;

GRANT SELECT ON TABLE public.winners_payload TO anon, authenticated;

DROP POLICY IF EXISTS winners_payload_public_resources_2026 ON public.winners_payload;
CREATE POLICY winners_payload_public_resources_2026
  ON public.winners_payload
  FOR SELECT
  TO anon, authenticated
  USING (year = 2026);
