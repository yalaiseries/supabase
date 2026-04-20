-- Drop public.members_resources.
--
-- The table was created as scaffolding for a members-only resources Edge
-- Function that was never built. No code references it, it has no rows,
-- and session recordings are served from winners_payload instead.
-- Removing it eliminates the rls_disabled_in_public Security Advisor
-- alert and reduces unused attack surface.

DROP TABLE IF EXISTS public.members_resources;
