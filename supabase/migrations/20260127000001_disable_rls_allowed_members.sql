-- Disable RLS on allowed_members table to allow Edge Functions to write
-- The register-sync Edge Function uses the service role key to upsert members
ALTER TABLE public.allowed_members DISABLE ROW LEVEL SECURITY;

-- Similarly, ensure members_resources can be managed by Edge Functions
ALTER TABLE public.members_resources DISABLE ROW LEVEL SECURITY;
