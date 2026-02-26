-- Schema required for the members-only allowlist + (optional) members resources.
-- Run this in Supabase Dashboard → SQL Editor.

-- 1) Allowlist table used to decide whether a signed-in user is "registered".
create table if not exists public.allowed_members (
  email text primary key,
  name text,
  source text,
  metadata jsonb,
  created_at timestamptz not null default now()
);

alter table public.allowed_members enable row level security;

revoke all on table public.allowed_members from anon;
grant select on table public.allowed_members to authenticated;

drop policy if exists allowed_members_select_own_email on public.allowed_members;
create policy allowed_members_select_own_email
  on public.allowed_members
  for select
  to authenticated
  using (lower(email) = lower(coalesce(auth.jwt() ->> 'email', '')));

-- Helpful for case-insensitive lookups if you ever switch to ilike queries.
-- (The Edge Functions normalize emails to lowercase already.)
create index if not exists allowed_members_created_at
  on public.allowed_members (created_at);

-- 2) Optional: store members-only winners content in the database (instead of committing it to git).
-- The `winners` Edge Function can read this table using the service role key after verifying membership.
create table if not exists public.winners_payload (
  year int primary key,
  payload jsonb not null,
  updated_at timestamptz not null default now()
);

alter table public.winners_payload enable row level security;

grant select on table public.winners_payload to anon, authenticated;

drop policy if exists winners_payload_public_resources_2026 on public.winners_payload;
create policy winners_payload_public_resources_2026
  on public.winners_payload
  for select
  to anon, authenticated
  using (year = 2026);

create index if not exists winners_payload_updated_at
  on public.winners_payload (updated_at);
