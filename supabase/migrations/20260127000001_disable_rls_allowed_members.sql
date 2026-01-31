-- Disable RLS on allowed_members table to allow Edge Functions to write
-- The register-sync Edge Function uses the service role key to upsert members
ALTER TABLE public.allowed_members DISABLE ROW LEVEL SECURITY;

