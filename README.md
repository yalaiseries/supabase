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

# Deploy
supabase functions deploy winners
supabase functions deploy members-resources
supabase functions deploy chat
```

Members-only data endpoints (require `Authorization: Bearer <access_token>`):

- `https://<project-ref>.functions.supabase.co/winners`
- `https://<project-ref>.functions.supabase.co/members-resources`

Homepage Q&A endpoint (public):

- `https://<project-ref>.functions.supabase.co/chat`

## Local preview

```powershell
cd C:\2026_AI_Collaboration\aiseries
python -m http.server 5173
```

Then open `http://localhost:5173/`.
