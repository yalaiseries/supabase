-- Admin allowlist for private analytics endpoints.

create table if not exists public.admin_users (
  email text primary key,
  created_at timestamptz not null default now(),
  created_by text
);

alter table public.admin_users enable row level security;

revoke all on table public.admin_users from anon, authenticated;

create index if not exists admin_users_created_at
  on public.admin_users (created_at desc);
