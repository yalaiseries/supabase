# Security Hardening Checklist

This checklist is focused on your current stack: static website + Supabase Auth + Supabase Edge Functions.

## 0) Threat model (quick)

Primary risks:

- Credential stuffing / brute-force attempts on auth endpoints
- Abuse/scanning of admin endpoints
- Token/session theft from compromised client devices
- Misconfiguration leaks (service role key exposure, overly-broad CORS/origin)

## 1) Immediate actions (today)

1. Enable MFA for all admin accounts in Supabase Auth.
2. Ensure `SERVICE_ROLE_KEY` exists only in Supabase secrets (never in frontend files).
3. Add admin emails only to `public.admin_users` that actually need access.
4. Set optional origin restriction for admin endpoint:
   - Secret name: `ADMIN_ALLOWED_ORIGINS`
   - Example value: `https://aihackathon.pro,https://www.aihackathon.pro`

5. Configure Cloudflare/WAF rate limits on:
   - `/functions/v1/slide-download-admin`
   - `/functions/v1/slide-download-track`
   - `/auth/v1/*`

## 2) Supabase secrets to set

```powershell
supabase secrets set ADMIN_ALLOWED_ORIGINS="https://aihackathon.pro,https://www.aihackathon.pro"
```

Optional (for staging/local testing):

- Add `http://localhost:5173` temporarily, then remove after testing.

## 3) Access control verification

### Admin endpoint

- Endpoint: `slide-download-admin`
- Requires:
  - valid logged-in JWT
  - email exists in `public.admin_users`
  - origin in `ADMIN_ALLOWED_ORIGINS` (if configured)

### Quick SQL checks

```sql
-- Current admins
select email, created_at, created_by
from public.admin_users
order by created_at desc;

-- Add admin
insert into public.admin_users (email, created_by)
values ('your-admin-email@example.com', 'manual-setup')
on conflict (email) do nothing;

-- Remove admin
delete from public.admin_users
where lower(email) = lower('old-admin@example.com');
```

## 4) Cloudflare/WAF guidance

Recommended baseline:

- Managed WAF rules: ON
- Bot Fight Mode / Super Bot Fight Mode: ON
- Rate limit examples:
  - `slide-download-admin`: 30 requests / 1 min / IP
  - `slide-download-track`: 120 requests / 1 min / IP
  - `auth` endpoints: 60 requests / 1 min / IP
- Block obvious bad ASNs/countries only if you have a clear business need.

## 5) Monitoring and alerting

Daily checks:

- Supabase Auth logs: failed sign-ins, unusual spikes
- Supabase Edge Function logs: repeated 401/403/429 patterns
- WAF dashboard: top blocked paths/IPs

## 6) Session and auth hygiene

- Keep admin sessions short (enforced in auth settings where practical).
- Revoke sessions immediately when an admin leaves.
- Use unique, strong passwords + MFA.

## 7) Data retention

For analytics data minimization:

- Keep raw event logs only as long as needed (e.g., 90-180 days)
- Aggregate older data if long-term trends are needed

Example purge job query:

```sql
delete from public.slide_download_events
where event_at < now() - interval '180 days';
```

## 8) Deployment safety

Before deploying function changes:

1. `supabase db push`
2. `supabase functions deploy slide-download-track`
3. `supabase functions deploy slide-download-admin`
4. Verify with an admin account and a non-admin account.

## 9) Security baseline summary

If you only do five things, do these:

1. MFA for admins
2. Admin allowlist table maintenance
3. Origin allowlist via `ADMIN_ALLOWED_ORIGINS`
4. WAF + rate limiting
5. Daily log review + fast revoke playbook
