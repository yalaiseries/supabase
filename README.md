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

# Secrets (needed for the homepage Q&A)
supabase secrets set OPENAI_API_KEY=<your-key>
supabase secrets set OPENAI_MODEL=gpt-4o-mini

# Secrets (needed for registration enforcement + automation)
supabase secrets set SUPABASE_URL=https://<project-ref>.supabase.co
supabase secrets set SUPABASE_ANON_KEY=<your-anon-key>
supabase secrets set SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>
supabase secrets set REGISTRATION_WEBHOOK_SECRET=<make-a-long-random-secret>

# Deploy
supabase functions deploy winners
supabase functions deploy members-resources
supabase functions deploy chat
supabase functions deploy register-sync
```

Members-only data endpoints (require `Authorization: Bearer <access_token>`):

- `https://<project-ref>.functions.supabase.co/winners`
- `https://<project-ref>.functions.supabase.co/members-resources`

Homepage Q&A endpoint (public):

- `https://<project-ref>.functions.supabase.co/chat`

## Fully automated registration (Google Form → members-only access)

This repo enforces **registered-only** access using an allowlist table in Supabase. Registration is automated by sending each new Google Form submission to a Supabase Edge Function webhook.

### 1) Create allowlist table

In Supabase SQL editor, run:

```sql
create table if not exists public.allowed_members (
  email text primary key,
  name text,
  source text,
  metadata jsonb,
  created_at timestamptz not null default now()
);
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

- Users must sign in on `members.html` using the same email they registered with.
- The protected APIs (`winners`, `members-resources`) return **403** if the email is not in `allowed_members`.

## Local preview

```powershell
cd C:\2026_AI_Collaboration\aiseries
python -m http.server 5173
```

Then open `http://localhost:5173/`.
