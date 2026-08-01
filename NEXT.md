# Next actions

Last updated: 1 Aug 2026. Background detail for the 2026 library work lives in
[HANDOFF_2026_LIBRARY.md](HANDOFF_2026_LIBRARY.md).

---

## 🔴 Do first

### 1. Revoke the GitHub personal access token

A classic PAT (`ghp_…`, `repo` scope) was pasted into a chat transcript on 1 Aug 2026
and used for four pushes to `yalaiseries/supabase`. It is still valid.

- Revoke: <https://github.com/settings/tokens>
- Then set up credentials properly so it never needs pasting again:
  ```
  gh auth login          # as yal.aiseries@gmail.com
  gh auth setup-git
  ```
  The `gh` accounts currently on this machine (`integrations-space`, `justfifty`) have
  **read-only** access to `yalaiseries/supabase`, which is why the push failed initially.

### 2. Confirm the 2026 prize amounts

Awards currently render without figures — "First Prize", "Innovation Award", etc.
2024 and 2025 include them ("First Prize Winner ($2500)").

`index.html` lists them under **"Cash prizes (to be confirmed)"**: First $3,000,
Second $2,000, Third $1,000, Innovation Awards $500 ×5. Two problems:

- still marked *to be confirmed*
- **6** Innovation Awards were actually given, plus **2** Rising Innovator Awards —
  so "×5" does not match the outcome

The 2026 certificates carry no amounts, so there is no authoritative source on disk.
Once confirmed, append them to each `award` string in the 2026 payload and re-upsert.

---

## 🟡 Worth doing

### 3. `yalaiseries/aihackathon` has ~7 months of uncommitted work

Separate repo from this one (`c:\2026_AI_Collaboration\aihackathon`). Its last commit is
26 Dec 2025; the working tree holds 15 modified files, 2 deletions, and untracked
`collaboration.html`, `winners.html`, `supabase/`, `scripts/`, `supabase-config.js`.

Before committing any of it:

- `supabase-config.js` may hold keys — check what is in it
- `assets/webpage/` holds `.xlsx`, `For Judges.docx`, and `data.csv` that are **untracked
  but not gitignored**, so a plain `git add .` would sweep them into a public repo.
  Add ignore rules first.

### 4. Enrich the 2026 team leads

Most 2026 leads have a name only. The renderer shows the role line only when **both**
`position` and `company` are present, so entries degrade gracefully — but 2025 entries
look richer. `Particiapnts Contact.xlsx` has the data and is **PII**: keep it out of git.

### 5. Delete the dead `debug` field

`supabase/functions/winners/index.ts:165` returns `debug: dbDebug`, and `dbDebug` is
never declared → `ReferenceError` if the code-fallback path ever runs. Only reachable
when the DB returns zero entries, and the fallback data is empty placeholders, so it is
currently harmless. Remove the field next time that file is open.

---

## ✅ Done on 1 Aug 2026

- **2026 added to the Winners Library** — 11 teams, 3 categories (Top Winners 3,
  Innovation Awards 6, Rising Innovator Awards 2). Award tiers taken from the signed
  certificates, the only authoritative record.
- **Year sentinel untangled** — `year = 2026` used to hold the *public* AI/AECO Resources
  payload with an anon-readable RLS policy. Re-keyed to `9999`
  (migration `20260801000001`). Verified: anon reads only 9999, and a direct anon probe
  of `year=eq.2026` returns `[]`, so winners stay members-only.
- **Renderer fixed** — it previously picked exactly two categories per year via `.find()`,
  silently dropping a third. Now renders all categories via `CATEGORY_RANK`.
- **Slide links point at the shared PDFs** in the organiser's Drive folder, replacing the
  teams' own `.pptx` / Google Slides links. 11 links, 0 pptx remaining.
- **2026 Topic Survey Ranking published** from
  `data/AI Hackathon Collaboration 2026 (Responses).xlsx` (132 responses, Jan–Jul 2026):
  Compliance Checking 107, BIM Coordination 88, Design Optimisation 85, Site Inspection 53,
  Contract Admin Assistant 47, then the self-defined option.
- **Cache made stale-while-revalidate** — `winners.html` used to treat its localStorage
  copy as authoritative for 5 minutes and serve it stale for an hour. Data-only changes
  were invisible and a browser refresh could not clear it, since reloads do not touch
  localStorage. The key is now versioned *and* the page always revalidates in the
  background. This was the real reason each of the three changes above appeared missing
  after a correct deploy.

### Traps recorded for whoever works on this next

- `2026 Submissions for JP.xlsx`: the assessor sheets hold **placeholder scores only**
  (25/25/25/75 for every team) — there is no scored ranking anywhere.
- The same workbook's `Summary` column is **misaligned** with its rows (Building Bytes'
  summary describes Metatron's project). Columns 2–19 are correct; summaries in the
  payload are composed from those, never from the Summary column.
- `Copy of AI Challenge Survey Form (Responses).xlsx` is the **2025** survey, not 2026 —
  its tally reproduces the published 2025 ranking exactly.
