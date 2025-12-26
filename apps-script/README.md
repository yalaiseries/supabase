# Google Apps Script (Sheet → Supabase allowlist)

Use this to automatically sync your registration sheet to Supabase `public.allowed_members`.

## Files

- `supabase-allowlist.gs` — Apps Script that posts emails to `/register-sync`

## Quick steps

1) Open your Google Sheet → **Extensions → Apps Script**
2) Create a new script and paste in `supabase-allowlist.gs`
3) Set:

- `WEBHOOK_SECRET` to match your Supabase secret `REGISTRATION_WEBHOOK_SECRET`
- Confirm the header name `Email address` matches your sheet’s column header exactly

4) Create an Apps Script trigger:

- If this is a Google Form responses sheet: `onFormSubmit` (near real-time)
- Otherwise: `syncNewRows` (time-driven)

## Required Supabase setup

- Table `public.allowed_members` exists
- Edge Function `register-sync` is deployed
- Supabase Function Secrets include:
  - `SERVICE_ROLE_KEY`
  - `REGISTRATION_WEBHOOK_SECRET`
