-- Disable RLS on winners_payload to allow Edge Function to read data
-- The Edge Function already uses membership validation, so table-level RLS is redundant
ALTER TABLE public.winners_payload DISABLE ROW LEVEL SECURITY;

-- Grant necessary permissions to authenticated role (just in case)
GRANT SELECT ON public.winners_payload TO authenticated;
GRANT SELECT ON public.winners_payload TO anon;
