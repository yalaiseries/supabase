# AI (Hackathon) Series (Static site)

This repo is a simple multi-page static website intended for **GitHub Pages** hosting, with **Supabase Auth** + **Supabase Edge Functions** providing members-only data.

## Hosting (GitHub Pages)

- GitHub repo: <https://github.com/yalaiseries/supabase>
- Pages URL (default): `https://yalaiseries.github.io/supabase/`

In GitHub: **Settings → Pages**

- Source: `Deploy from a branch`
- Branch: `main` / folder: `/ (root)`

## Supabase setup

### 1) Frontend config

Update [supabase-config.js](supabase-config.js) with:

- `window.SUPABASE_URL` (example: `https://<project-ref>.supabase.co`)
- `window.SUPABASE_ANON_KEY` (publishable/anon key)

`window.SUPABASE_FUNCTIONS_URL` is derived automatically.

### 2) Auth redirect URLs

In Supabase Dashboard → Authentication → URL Configuration:

- Site URL: `https://yalaiseries.github.io/supabase`
- Redirect URLs:
  - `https://yalaiseries.github.io/supabase/members.html`
  - `https://yalaiseries.github.io/supabase/winners.html`

### 3) Deploy Edge Functions

Install Supabase CLI, then from this repo root:

```powershell
cd C:\2026_AI_Collaboration\aiseries
supabase login
supabase link --project-ref <your-project-ref>

# Secrets (needed for registration enforcement + automation)
supabase secrets set SERVICE_ROLE_KEY=<your-service-role-key>
supabase secrets set REGISTRATION_WEBHOOK_SECRET=<make-a-long-random-secret>

# Deploy
supabase functions deploy winners
supabase functions deploy members-resources
supabase functions deploy register-sync
supabase functions deploy register-reconcile
supabase functions deploy request-access
supabase functions deploy slide-download-track
supabase functions deploy slide-download-admin
```

Members-only data endpoints (require `Authorization: Bearer <access_token>`):

- `https://<project-ref>.functions.supabase.co/winners`
- `https://<project-ref>.functions.supabase.co/members-resources`
- `https://<project-ref>.functions.supabase.co/slide-download-track`
- `https://<project-ref>.functions.supabase.co/slide-download-admin` (admin only)

## Slide download tracking

`members.html` routes tagged slide links through `slide-download-track`.

- Function flow: verify logged-in registered member → insert event row in `public.slide_download_events` → `302` redirect to the Google Drive/Slides URL.
- Captured fields: `email`, `slide_id`, `slide_url`, `event_at`, `user_agent`, `referrer`.

Run these analytics queries in Supabase SQL editor:

```sql
-- 1) Frequency by user
select email, count(*) as downloads
from public.slide_download_events
group by email
order by downloads desc;

-- 2) Frequency by slide
select slide_id, slide_url, count(*) as downloads
from public.slide_download_events
group by slide_id, slide_url
order by downloads desc;

-- 3) Daily frequency trend
select date_trunc('day', event_at) as day, count(*) as downloads
from public.slide_download_events
group by 1
order by 1 desc;

-- 4) Weekly frequency per user and slide
select date_trunc('week', event_at) as week, email, slide_id, count(*) as downloads
from public.slide_download_events
group by 1, 2, 3
order by week desc, downloads desc;
```

### Admin-only access to who/when data

To ensure only admins can view who downloaded and when:

```sql
-- Add admin emails allowed to query private download logs
insert into public.admin_users (email, created_by)
values
  ('your-admin-email@example.com', 'setup')
on conflict (email) do nothing;
```

Then call:

`GET https://<project-ref>.functions.supabase.co/slide-download-admin`

Headers:

- `apikey: <anon-key>`
- `authorization: Bearer <user-access-token>`

Optional query params:

- `limit` (default 200, max 1000)
- `offset` (default 0)
- `email` (filter by downloader)
- `slide_id` (filter by file)
- `from` / `to` (ISO timestamp window)

Non-admin users receive `403 Forbidden`.

Optional hardening (recommended):

```powershell
supabase secrets set ADMIN_ALLOWED_ORIGINS="https://aihackathon.pro,https://www.aihackathon.pro"
```

This restricts browser-origin access for `slide-download-admin` when configured.

### Admin analytics page

Open `admin.html` after signing in.

It shows:

- Total download count
- Unique users and unique files
- Time period and frequency (`downloads/day`, `downloads/week`)
- Graphical bars for top files, top users, and daily frequency trend
- Detailed who/when/file event table with CSV export

## Security operations docs

- [SECURITY_HARDENING.md](SECURITY_HARDENING.md)
- [INCIDENT_RESPONSE_RUNBOOK.md](INCIDENT_RESPONSE_RUNBOOK.md)



## Password setup (user-friendly)

This site uses a **registration allowlist** (from your spreadsheet) plus **Supabase Auth**.

- Participants register via your registration form (their email appears in `public.allowed_members`).
- On the members page, participants click **Request access / set password**.
  - If allowlisted, they receive an email to set their password.
  - After that, they log in normally with email + password.

If a user forgets their password, **Forgot password** on the members page will send a reset email.

## Fully automated registration (Google Form → members-only access)

This repo enforces **registered-only** access using an allowlist table in Supabase. Registration is automated by sending each new Google Form submission to a Supabase Edge Function webhook.

### 1) Create allowlist table

In Supabase SQL editor, run (or use [supabase/sql/schema.sql](supabase/sql/schema.sql)):

```sql
create table if not exists public.allowed_members (
  email text primary key,
  name text,
  source text,
  metadata jsonb,
  created_at timestamptz not null default now()
);
```

### (Optional) Members-only resources table

The `members-resources` Edge Function can load links from a table (recommended), so you can update the library without redeploying.

```sql
create table if not exists public.members_resources (
  id bigint generated by default as identity primary key,
  title text not null,
  url text not null,
  note text,
  sort_order int,
  active boolean not null default true,
  created_at timestamptz not null default now()
);

create index if not exists members_resources_active_sort
  on public.members_resources (active, sort_order, created_at);
```

Example insert:

```sql
insert into public.members_resources (title, url, note, sort_order)
values
  ('2026 session recordings (Drive)', 'https://example.com', 'Replace with your real link.', 10),
  ('Submission templates', 'https://example.com', '2-page write-up + 10-slide deck.', 20);
```

### 2) Add a Google Apps Script trigger

In the Google Form responses sheet:

- Extensions → Apps Script
- Paste this script (edit the email field name to match your form):

```javascript
function onFormSubmit(e) {
  var values = e.namedValues || {};
  var email = (values['Email'] && values['Email'][0]) ? values['Email'][0].trim() : '';
  var name = (values['Name'] && values['Name'][0]) ? values['Name'][0].trim() : '';
  if (!email) return;

  var url = 'https://<project-ref>.functions.supabase.co/register-sync';
  var secret = '<REGISTRATION_WEBHOOK_SECRET>'; // must match Supabase secret

  var payload = {
    email: email,
    name: name,
    source: 'google_form',
    submittedAt: new Date().toISOString(),
    raw: values
  };

  UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'x-webhook-secret': secret
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });
}
```

- Triggers (clock icon) → Add Trigger
  - Choose function: `onFormSubmit`
  - Event source: `From spreadsheet`
  - Event type: `On form submit`

### 3) How access works

- Users sign in on `members.html` using email + password, and must use the same email they registered with.
- First time, they use **Create account** (they may need to confirm their email once).
- If they don’t have a password yet (or forgot it), they use **Forgot / set password** (this sends a password reset email).
- The protected APIs (`winners`, `members-resources`) return **403** if the email is not in `allowed_members`.

## Local preview

```powershell
cd C:\2026_AI_Collaboration\aiseries
python -m http.server 5173
```

Then open `http://localhost:5173/`.
