import { serve } from 'https://deno.land/std@0.224.0/http/server.ts';
import { corsHeaders } from '../_shared/cors.ts';
import { requireRegisteredMember } from '../_shared/membership.ts';
import { buildFromTransposedCsv, enrichYearEntryByTitle, mergeYearEntries, type YearEntry } from '../_shared/winners-lib.ts';
import {
  winnersData2024Csv,
  winnersData2025Csv,
  winnersData2025InnovationCsv,
  winnersExtraJson
} from '../_shared/winners-data.ts';

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      ...corsHeaders,
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'no-store'
    }
  });
}

function getSupabaseUrl(): string {
  // Prefer SUPABASE_URL. Some runtimes set URL to the function URL.
  return String(Deno.env.get('SUPABASE_URL') || Deno.env.get('URL') || '').trim();
}

function getServiceRoleKey(): string {
  return String(Deno.env.get('SERVICE_ROLE_KEY') || Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') || '').trim();
}

async function loadWinnersFromDb(): Promise<{ ok: true; entries: YearEntry[]; challengeTopics?: Record<number, unknown> } | { ok: false; status: number; error: string }> {
  const supabaseUrl = getSupabaseUrl();
  const serviceRoleKey = getServiceRoleKey();
  
  if (!supabaseUrl || !serviceRoleKey) {
    return { ok: false, status: 500, error: 'Server not configured.' };
  }

  const url = new URL(`${supabaseUrl}/rest/v1/winners_payload`);
  url.searchParams.set('select', 'year,payload,challenge_topics');
  url.searchParams.set('year', 'in.(2024,2025)');  // Only fetch winners years, not resources (2026)
  url.searchParams.set('order', 'year.desc');

  const resp = await fetch(url.toString(), {
    headers: {
      apikey: serviceRoleKey,
      authorization: `Bearer ${serviceRoleKey}`
    }
  });

  if (resp.status === 404) {
    return { ok: false, status: 404, error: 'Table public.winners_payload not found.' };
  }
  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    return { ok: false, status: resp.status, error: text || 'Failed to load winners from DB.' };
  }

  const rows = (await resp.json().catch(() => [])) as Array<{ year?: number; payload?: unknown; challenge_topics?: unknown }>;
  const entries: YearEntry[] = [];
  const challengeTopics: Record<number, unknown> = {};
  
  for (const row of rows) {
    const payload = (row as any)?.payload;
    const dbYear = Number(row.year);
    
    // Store challenge_topics for this year if available
    if (row.challenge_topics && Number.isFinite(dbYear)) {
      challengeTopics[dbYear] = row.challenge_topics;
    }
    
    if (!payload) continue;
    
    // If payload is an array, iterate through it
    if (Array.isArray(payload)) {
      for (const item of payload) {
        if (item && typeof item === 'object' && Number((item as any).year)) {
          entries.push(item as YearEntry);
        }
      }
      continue;
    }
    
    // If payload is an object, use the row's year if payload doesn't have it
    if (payload && typeof payload === 'object') {
      const yearEntry: YearEntry = {
        year: (payload as any).year || dbYear,  // Use payload.year if exists, otherwise use row.year
        categories: Array.isArray((payload as any).categories) ? (payload as any).categories : []
      };
      
      if (Number.isFinite(yearEntry.year) && yearEntry.year > 0) {
        entries.push(yearEntry);
      }
    }
  }

  return { ok: true, entries, challengeTopics: Object.keys(challengeTopics).length > 0 ? challengeTopics : undefined };
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  const membership = await requireRegisteredMember(req);
  if (!membership.ok) return json(membership.body, membership.status);

  // Prefer DB-backed winners content (keeps sensitive content out of git).
  const db = await loadWinnersFromDb();
  
  if (db.ok && db.entries.length > 0) {
    const winners = mergeYearEntries(db.entries);
    const response: { winners: YearEntry[]; source: string; challengeTopics?: Record<number, unknown> } = { winners, source: 'db' };
    if (db.challengeTopics) {
      response.challengeTopics = db.challengeTopics;
    }
    return json(response);
  }

  const yearEntries: Array<YearEntry | null> = [];

  yearEntries.push(
    buildFromTransposedCsv({
      csvText: winnersData2025Csv,
      year: 2025,
      defaultCategory: 'Top Winners'
    })
  );

  yearEntries.push(
    buildFromTransposedCsv({
      csvText: winnersData2025InnovationCsv,
      year: 2025,
      defaultCategory: 'Innovation Awards'
    })
  );

  const winners2024FromCsv = buildFromTransposedCsv({
    csvText: winnersData2024Csv,
    year: 2024,
    defaultCategory: 'Winners'
  });

  let extras: YearEntry[] = [];
  try {
    const parsed = JSON.parse(winnersExtraJson);
    if (Array.isArray(parsed)) extras = parsed as YearEntry[];
  } catch (_e) {
    extras = [];
  }

  if (winners2024FromCsv) {
    extras = extras.map((e) => {
      if (Number(e?.year) !== 2024) return e;
      return enrichYearEntryByTitle(e, winners2024FromCsv);
    });
  }

  const winners = mergeYearEntries(yearEntries.concat(extras));

  return json({ winners, source: 'code', debug: dbDebug });
});
