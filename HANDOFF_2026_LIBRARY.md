# 2026 in the Winners Library — done

**Status:** Shipped 1 Aug 2026. 2026 now renders alongside 2024 and 2025.

---

## What the blocker was, and how it was resolved

`public.winners_payload` is keyed by year, and `year = 2026` was already taken by
the *AI/AECO Resources* payload — a row deliberately made **anon-readable** by RLS
so `resources.html` could fetch it without a login. Putting members-only winners
content in that row would have published it to the open internet.

Resolved with Option 1 from the original investigation: the resources payload was
re-keyed onto a non-year sentinel, `year = 9999`, and the public policy moved with
it. Every real calendar year is now free for winners.

Migration: `supabase/migrations/20260801000001_rekey_resources_sentinel.sql`
(idempotent). Applied to the remote project on 1 Aug 2026.

| Location | Change |
|---|---|
| `supabase/sql/schema.sql` | policy renamed `winners_payload_public_resources`, predicate `year = 9999` |
| `resources.html` | public fetch now `.eq('year', 9999)` |
| `winners.html` | `RESOURCES_YEAR = 9999` constant replaces the inline 2026 checks |
| `supabase/functions/winners/index.ts` | year filter is now `neq.9999` instead of an allow-list — **future years need no code change here** |

### Verified after deploy

- anon can read **only** `year = 9999`; a direct anon probe of `year=eq.2026` returns `[]`
- the service-role query the Edge Function runs returns 2026, 2025, 2024
- `functions/v1/winners` without a member JWT returns 401, not a 500

---

## Front-end changes

- `winners.html` used to pick exactly two categories per year via `.find()`, so any
  third category was silently dropped. It now renders **all** categories, ordered by
  `CATEGORY_RANK` with unranked ones following in payload order. 2026 needs this —
  it has three tiers.
- Year titles moved into a `YEAR_TITLES` map; 2026 is "2026 AI (Hackathon) Challenge".
- Copy updated: `winners.html` meta description, `members.html` (two places),
  `index.html` past-winners link.

---

## The 2026 data

Built by `scripts/build_2026_payload.py` (git-ignored — it reads PII sources).
Output `local/winners_2026.json`, upserted to `winners_payload` year 2026.

**Awards come from the signed certificates** in `C:\2026_AI_Collaboration\Certificates\2026\`,
which are the only authoritative record of who won what:

| Award | Team |
|---|---|
| First Prize | Agent A.i.D. (Agent A) |
| Second Prize | Metatron |
| Third Prize | AI Digital Reviewer |
| Innovation Award | Agent D, Agent i, BIM Reaper, PoC-05, Team 16, WIP |
| Rising Innovator Award | Building Bytes, Iteration Zero |

Agent A, Agent D and Agent i are three submissions from the **same** team
(Wynn Lei PHYU et al.) — confirmed against the form responses, not a cert copy-paste.

### ⚠️ Data trap — the assessment workbook is partly shuffled

In `2026 Submissions for JP.xlsx`:

- The four assessor sheets (`William`, `Immanuel`, `TF`, `KW`) contain **placeholder
  scores only** — every team has 25/25/25/75. There is no scored ranking anywhere.
- The `Summary` column (col 20) of the `Sub` sheet is **misaligned** with its rows:
  Building Bytes' summary describes Metatron's project and vice versa. The assessor
  sheets' summary column is shuffled the same way.
- Columns 2–19 of `Sub` **are** correctly aligned per team — verified by matching each
  row's slide URL against the form-response workbook.

So summaries in the payload are composed from each team's own objectives and outcomes
(cols 5 and 16), never from col 20. Do not "fix" this back to col 20.

---

## Still open

- **Prize amounts.** 2024/2025 awards read "First Prize Winner ($2500)" etc. The 2026
  certificates carry no amounts, so awards are stored without them. Add if wanted.
- **`challenge_topics` for 2026** is unset — 2025 has a "Topic Survey Ranking" block
  that 2026 will not render until that column is populated.
- **Lead position/company/LinkedIn** are absent for most 2026 leads (certificates list
  names only). The renderer degrades gracefully — it only shows the role line when
  both position and company are present. `Particiapnts Contact.xlsx` has contact data
  if you want to enrich this, but it is PII: keep it out of git.

---

## How winners data gets published

DB-only by design so this repo can stay public — see the note in
`supabase/functions/_shared/winners-data.ts`. The in-repo CSV/JSON constants are
deliberately empty placeholders and `admin.html` has no winners editor, so payloads
go in via SQL or a local script using the service-role key. Never commit the payload.

Payload shape actually consumed by `renderLibrary()`:

```jsonc
{ "categories": [ { "category": "Top Winners", "useCases": [ {
  "award": "First Prize", "team": "...", "title": "...", "summary": "...",
  "people": { "lead": { "name": "...", "position": "...", "company": "...", "linkedin": "..." },
              "coLeads": [], "teamMembers": [] },
  "showcase": { "problem": "", "existingSolutions": "", "gap": "", "proposedSolution": "",
                "approach": "", "methods": "", "tools": "", "strategy": "", "impact": "" },
  "links": [ { "label": "Slides", "url": "https://..." } ]
} ] } ] }
```

Note this differs from the shape guessed in the original handoff: there is no
top-level `year` inside `payload`, and `team` sits beside `title`.

---

## Unrelated latent bug still present

`supabase/functions/winners/index.ts:163` returns `debug: dbDebug`, but `dbDebug` is
never declared → `ReferenceError` if the code-fallback path ever runs. Only reachable
when the DB returns zero entries, and the fallback data is empty placeholders, so it
stays harmless. Worth deleting the `debug` field when next in that file.
