# Handoff — Adding 2026 to the Winners Library

**Status:** Investigation only. No code changes made yet.
**Date:** 1 Aug 2026

Goal: add a 2026 section to the Winners Library (`winners.html`), alongside the
existing 2024 and 2025 sections.

---

## ⚠️ Blocker: year 2026 is already taken

`public.winners_payload` is keyed by year (`year int primary key`), and the row at
`year = 2026` is **not** a winners year — it holds the *AI/AECO Resources* payload.
Four places hard-code this:

| Location | What it does |
|---|---|
| `winners.html:192-193` | `winners.find(w => Number(w.year) === 2026)` → treated as resources; 2026 is filtered out of the years list |
| `supabase/functions/winners/index.ts:43` | `year=in.(2024,2025)` — 2026 explicitly excluded from the members-only fetch |
| `resources.html:114-116` | Public (anon) read of `winners_payload` where `year = 2026` |
| `supabase/sql/schema.sql:42-47` | RLS policy `winners_payload_public_resources_2026` grants **anon** select on `year = 2026` |

Same policy also in `supabase/migrations/20260226000001_enable_rls_public_tables.sql`.

### 🚨 Security consequence — read this before touching the DB

Do **not** insert 2026 winners content into the row at `year = 2026`. That row is
publicly readable by `anon` under the RLS policy above. Winners content is
members-only; writing it there would expose it to the open internet.

### Options

1. **Re-key the resources payload** to a non-year sentinel (e.g. `9999`), update the
   RLS policy, `resources.html`, and the `winners.html` resources branch. Then 2026
   is free for real winners data. *Cleanest; touches 4 files + a migration.*
2. **Move resources to its own table** (e.g. `public.resources_payload`) with its own
   public policy. More invasive but removes the year-sentinel hack for good.

Option 1 is the smaller change. Either way it needs a migration, because the RLS
policy predicate is literally `year = 2026`.

---

## Front-end changes also needed (`winners.html`)

- `:376-381` — category matcher only knows `Top Winners` / `Prize Winners` /
  `AI Programme Winners` (left) and `Innovation Awards` / `Merit Awards` /
  `Merit Prizes` (right). Add whatever 2026's award categories are called.
- `:390-394` — year → title map has 2025 and 2024 only; falls back to bare
  `String(year)`. Add the 2026 title (e.g. "2026 AI Collaboration").
- `members.html:166` and `:185` — copy says "2024 and 2025", needs updating.
- `winners.html:7` — meta description says "(2024–2025)".

---

## Source data (local only — not in the repo)

`C:\2026_AI_Collaboration\Submission\`

- **11 team submissions**, PDF + PPTX:
  BuildingBytes, Agent D, Metatron, AI Digital Reviewer, PoC-05, WIP,
  IterationsZero, Agent i, Agent A, BIM_Reaper, Team16
- `AI_assesment\2026 Submissions for JP.xlsx` — sheets: `Sub` (27 cols: full
  write-up + scores) plus assessor sheets `William`, `Immanuel`, `TF`, `KW`
- `AI Challenge 2026 - 13 May Write-up Submission (Responses).xlsx` — 11 form
  responses: team members' names, emails, mobiles, Google Slides links
- `Particiapnts Contact.xlsx` — participant contacts (PII)

**Scoring rubric:** Practicality & Impact 30% + Collaboration & Innovation 30% +
Documentation & Implementation 40% = Total 100%.

⚠️ These workbooks contain personal data (emails, mobile numbers). Keep them out of
git — `data/*.xlsx` is already gitignored; the `Submission` folder is outside the repo.

---

## Open decisions (need your input)

1. Which option above for freeing up the 2026 slot?
2. What are 2026's award categories, and which teams won what? The assessor sheets
   have raw scores but I have not seen a final ranking / award allocation.
3. Year section title for 2026 — "2026 AI Collaboration"? "2026 AI Challenge"?
4. Where will the 2026 slide decks be hosted? Prior years link to Google Slides /
   Drive URLs; the form responses do include per-team Google Slides links.

---

## How winners data gets published

Winners content is **DB-only by design** so this repo can stay public — see the note
in `supabase/functions/_shared/winners-data.ts`. The in-repo CSV/JSON constants are
deliberately empty placeholders. `admin.html` has **no** winners editor, so the 2026
payload has to be inserted into `public.winners_payload` via SQL or a local script
using the service-role key. Do not commit the payload.

Payload shape consumed by `renderLibrary()` (`winners.html:185`):

```jsonc
{
  "year": 2026,
  "categories": [
    {
      "category": "Top Winners",
      "useCases": [
        {
          "title": "...", "team": "...", "award": "...", "summary": "...",
          "people": {
            "lead": { "name": "...", "position": "...", "company": "...", "linkedin": "..." },
            "coLeads": [], "teamMembers": []
          },
          "showcase": {
            "problem": "", "existingSolutions": "", "gap": "", "proposedSolution": "",
            "approach": "", "methods": "", "tools": "", "strategy": "", "impact": ""
          },
          "links": [{ "label": "Slides", "url": "https://..." }]
        }
      ]
    }
  ]
}
```

The `showcase` keys map cleanly onto the write-up form columns.

---

## Unrelated latent bug spotted

`supabase/functions/winners/index.ts:163` returns `debug: dbDebug`, but `dbDebug` is
never declared → `ReferenceError` if the code-fallback path ever runs. Only reachable
when the DB returns zero entries, and the fallback data is empty placeholders anyway,
so it is currently harmless. Worth deleting the `debug` field when next in that file.
