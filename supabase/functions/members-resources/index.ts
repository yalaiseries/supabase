import { serve } from 'https://deno.land/std@0.224.0/http/server.ts';
import { corsHeaders } from '../_shared/cors.ts';
import { requireRegisteredMember } from '../_shared/membership.ts';

type ResourceItem = {
  title: string;
  url: string;
  note?: string | null;
};

const fallbackResources: ResourceItem[] = [
  {
    title: 'Members handbook (placeholder)',
    url: 'https://yalaiseries.github.io/supabase/',
    note: 'Replace with a real link (e.g., Google Drive folder with restricted access).'
  },
  {
    title: 'Submission templates (placeholder)',
    url: 'https://yalaiseries.github.io/supabase/members.html',
    note: 'Add links to the 2-page write-up and 10-slide deck templates here.'
  },
  {
    title: 'Session recordings & slides (placeholder)',
    url: 'https://yalaiseries.github.io/supabase/members.html',
    note: 'Add Drive/YouTube unlisted links shared within the community.'
  },
  {
    title: 'Curated learning paths (placeholder)',
    url: 'https://yalaiseries.github.io/supabase/members.html',
    note: 'Add curated tracks (e.g., Getting started, BIM automation, Agentic AI for practice management).'
  }
];

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

function normalizeResourceRow(row: Record<string, unknown>): ResourceItem | null {
  const title = String(row.title || '').trim();
  const url = String(row.url || '').trim();
  if (!title || !url) return null;
  const noteRaw = row.note;
  const note = noteRaw === null || noteRaw === undefined ? null : String(noteRaw);
  return { title, url, note };
}

async function loadResourcesFromDb(): Promise<{ ok: true; resources: ResourceItem[] } | { ok: false; status: number; error: string }> {
  const supabaseUrl = String(Deno.env.get('SUPABASE_URL') || '').trim();
  const serviceRoleKey = String(
    Deno.env.get('SERVICE_ROLE_KEY') || Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') || ''
  ).trim();
  if (!supabaseUrl || !serviceRoleKey) {
    return { ok: false, status: 500, error: 'Server not configured.' };
  }

  const url = new URL(`${supabaseUrl}/rest/v1/members_resources`);
  url.searchParams.set('select', 'title,url,note,sort_order,created_at');
  url.searchParams.set('active', 'eq.true');
  url.searchParams.set('order', 'sort_order.asc.nullslast,created_at.asc');

  const resp = await fetch(url.toString(), {
    headers: {
      apikey: serviceRoleKey,
      authorization: `Bearer ${serviceRoleKey}`
    }
  });

  if (resp.status === 404) {
    return { ok: false, status: 404, error: 'Resources table not found.' };
  }
  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    return { ok: false, status: 502, error: text || 'Could not load resources.' };
  }

  const rows = (await resp.json().catch(() => [])) as Array<Record<string, unknown>>;
  const resources = (Array.isArray(rows) ? rows : [])
    .map((r) => normalizeResourceRow(r))
    .filter((r): r is ResourceItem => !!r);

  return { ok: true, resources };
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  const membership = await requireRegisteredMember(req);
  if (!membership.ok) return json(membership.body, membership.status);

  const fromDb = await loadResourcesFromDb();
  if (fromDb.ok) {
    if (fromDb.resources.length > 0) return json({ resources: fromDb.resources });
    return json({ resources: [] });
  }

  // If the DB table isn't set up yet, return safe placeholders.
  if (fromDb.status === 404) {
    return json({ resources: fallbackResources });
  }

  // For transient DB errors, also fall back (keeps members page usable), but expose a hint.
  return json({ resources: fallbackResources, warning: fromDb.error }, 200);
});
