# Google Apps Script (Sheet → Supabase allowlist)

Use this to automatically sync your registration sheet to Supabase `public.allowed_members`.

By default, this sync only sends **Email address** (and optionally **Full Name**) to Supabase.
That’s all you need for “recognized members” access control.

## Files

- `supabase-allowlist.gs` — Apps Script that posts emails to `/register-sync`

## Two-way / delete sync note ("mirror" mode)

Google Sheets does not reliably emit a "row deleted" event you can consume.
So if the spreadsheet is the **source of truth**, the practical way to sync deletes is to run a periodic **full mirror**.

This repo includes a second Edge Function:

- `/register-reconcile` — accepts the full set of sheet emails and makes Supabase match it (including removals)

In the Apps Script menu this appears as:

- **Supabase → Mirror ALL rows (reconcile deletes)**

Recommended setup:

- Keep `onFormSubmit` / `syncNewRows` for near real-time adds/updates
- Add a time-based trigger for `mirrorAllRows` every 1–5 minutes to handle deletes/revocations

## Quick steps

1) Open your Google Sheet → **Extensions → Apps Script**
2) Create a new script and paste in `supabase-allowlist.gs`
3) Set:

- Recommended: store `REGISTRATION_WEBHOOK_SECRET` in **Script Properties** (Project Settings → Script properties)
  - Or use **Supabase → Set webhook secret** from the Sheet menu
- Confirm the header name `Email address` matches your sheet’s column header exactly
- (Optional) Confirm the header name `Name` matches your sheet (or update `NAME_HEADER`)

4) Create an Apps Script trigger:

- If this is a Google Form responses sheet: `onFormSubmit` (near real-time)
- Otherwise: `syncNewRows` (time-driven)

## Required Supabase setup

- Table `public.allowed_members` exists
- Edge Function `register-sync` is deployed
- Edge Function `register-reconcile` is deployed
- Supabase Function Secrets include:
  - `SERVICE_ROLE_KEY`
  - `REGISTRATION_WEBHOOK_SECRET`

## Where to verify

- Supabase Dashboard → **Table Editor → allowed_members**
  - If emails appear here, your sheet → webhook sync is working.

## Important: allowlist vs login accounts

This sync only manages the **allowlist** (`allowed_members`). It does **not** create Supabase Auth accounts.
Each participant still needs to create an account once on the site (same email), confirm their email, then they can log in normally.
