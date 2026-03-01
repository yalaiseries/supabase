-- Seed admin allowlist entry for production analytics access.

insert into public.admin_users (email, created_by)
values ('yal.aiseries@gmail.com', 'migration:20260301000004_seed_admin_user_yal')
on conflict (email) do update
set created_by = excluded.created_by;