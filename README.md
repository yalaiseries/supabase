# aihackathon.pro (Static site)

This repo is a simple multi-page static website.

## Deploy (Netlify)

1. In Netlify, connect this GitHub repo.
2. Build settings:
   - **Build command:** (leave blank)
   - **Publish directory:** `.`
   - **Functions directory:** `netlify/functions`
3. Add environment variables:
   - `OPENAI_API_KEY` (required for Q&A)
   - `OPENAI_MODEL` (optional, default: `gpt-4o-mini`)

## Members-only access

This site is the **participants learning hub** ("mother" hub) for the **AI (Hackathon) Series — Agentic AI (2026)**. Public pages cover what’s needed to understand and register; learning materials and detailed resources are for registered participants.

Public microsite (for anyone): <https://archihackathon.com>

Netlify Identity has been deprecated and may not be available for new sites. This repo now supports **Supabase Auth** for members-only access.

### Supabase Auth (recommended)

1. Create a Supabase project.
2. In Supabase Dashboard → Authentication → URL Configuration:
   - Site URL: `https://aihackathonpro.netlify.app`
   - Redirect URLs: add
     - `https://aihackathonpro.netlify.app/members.html`
     - `https://aihackathonpro.netlify.app/winners.html`
3. In Netlify Dashboard → Site configuration → Environment variables, set:
   - `SUPABASE_URL` (example: `https://<project-ref>.supabase.co`)
   - `SUPABASE_ANON_KEY` (your project's anon key)
4. Update [supabase-config.js](supabase-config.js) with:
   - `window.SUPABASE_URL`
   - `window.SUPABASE_ANON_KEY`

Members-only data is served via:

- `/.netlify/functions/members-resources`
- `/.netlify/functions/winners`

Both functions validate the Supabase access token (`Authorization: Bearer <token>`).

## Local preview

Open `index.html` directly in a browser, or run a static server.

PowerShell (Python installed):

```powershell
cd C:\2026_AI_Collaboration\aihackathon
python -m http.server 5173
```

Then open `http://localhost:5173/`.

## Domain cutover (Blogger → Netlify)

In Netlify: **Site configuration → Domain management**

- Add `aihackathon.pro` and `www.aihackathon.pro`
- Set a primary domain
- Enable HTTPS

Then update DNS at your registrar per Netlify instructions.

Recommended long-term setup:

- Main site: `aihackathon.pro` (Netlify)
- Blogger archive/news: `blog.aihackathon.pro`
