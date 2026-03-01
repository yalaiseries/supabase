# Incident Response Runbook

Use this runbook when suspicious access/abuse is detected.

## Severity levels

- **SEV-1**: confirmed admin compromise, data exposure, active abuse
- **SEV-2**: repeated suspicious attempts, possible misconfiguration
- **SEV-3**: low-confidence alerts/no confirmed impact

## 1) First 15 minutes (containment)

1. Identify impacted surface:
   - Auth (`/auth/v1/*`)
   - Admin analytics (`slide-download-admin`)
   - Tracking endpoint (`slide-download-track`)
2. Apply temporary WAF block/rate limit tightening.
3. Remove suspicious admin email(s) from `public.admin_users`.
4. Revoke active sessions for affected accounts.

SQL quick action:

```sql
delete from public.admin_users
where lower(email) in (
  lower('compromised-admin@example.com')
);
```

## 2) Credential and key response

If compromise suspected:

1. Rotate `SERVICE_ROLE_KEY` and relevant secrets.
2. Re-deploy functions after secret rotation.
3. Force admin password reset + MFA re-enrollment if needed.

## 3) Investigation checklist

- Pull timeline from:
  - Supabase Auth logs
  - Supabase Edge Function logs
  - Cloudflare WAF logs
- Determine:
  - first suspicious timestamp
  - source IP ranges
  - affected endpoint(s)
  - whether admin endpoint returned real data

## 4) Recovery

1. Confirm patched config (WAF/rate limits/origin allowlist).
2. Restore only required admin users.
3. Run validation tests:
   - Admin account can access analytics
   - Non-admin account receives `403`
   - Normal member flows still work

## 5) Communication

For internal stakeholders include:

- What happened
- Time window
- Scope/impact
- Actions taken
- Follow-up prevention tasks

## 6) Post-incident hardening tasks

- Tighten `ADMIN_ALLOWED_ORIGINS`
- Review admin roster and least privilege
- Add/adjust alert thresholds
- Confirm data retention and purge schedule
