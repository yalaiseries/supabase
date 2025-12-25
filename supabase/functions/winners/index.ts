import { serve } from 'https://deno.land/std@0.224.0/http/server.ts';
import { corsHeaders } from '../_shared/cors.ts';
import { buildFromTransposedCsv, mergeYearEntries, type YearEntry } from '../_shared/winners-lib.ts';
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

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  const auth = req.headers.get('authorization') || '';
  if (!auth.toLowerCase().startsWith('bearer ')) {
    return json({ error: 'Unauthorized. Please sign in.' }, 401);
  }

  // Supabase can enforce JWT verification at the edge (verify_jwt=true by default).
  // We keep the check above mainly for clearer errors and to avoid work.

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

  yearEntries.push(
    buildFromTransposedCsv({
      csvText: winnersData2024Csv,
      year: 2024,
      defaultCategory: 'Winners'
    })
  );

  let extras: YearEntry[] = [];
  try {
    const parsed = JSON.parse(winnersExtraJson);
    if (Array.isArray(parsed)) extras = parsed as YearEntry[];
  } catch (_e) {
    extras = [];
  }

  const winners = mergeYearEntries(yearEntries.concat(extras));

  return json({ winners });
});
