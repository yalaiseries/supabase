import { serve } from 'https://deno.land/std@0.224.0/http/server.ts';
import { corsHeaders } from '../_shared/cors.ts';

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
  return String(Deno.env.get('URL') || Deno.env.get('SUPABASE_URL') || '').trim();
}

function getServiceRoleKey(): string {
  return String(Deno.env.get('SERVICE_ROLE_KEY') || Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') || '').trim();
}

function getAdminToken(): string {
  return String(Deno.env.get('WINNERS_ADMIN_TOKEN') || '').trim();
}

function safeEquals(a: string, b: string): boolean {
  // Constant-time-ish compare for same-length strings.
  if (a.length !== b.length) return false;
  let out = 0;
  for (let i = 0; i < a.length; i++) out |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return out === 0;
}

function requireAdmin(req: Request): { ok: true } | { ok: false; status: number; body: any } {
  const token = getAdminToken();
  if (!token) {
    return { ok: false, status: 500, body: { error: 'Server not configured. Missing WINNERS_ADMIN_TOKEN.' } };
  }

  const got = String(req.headers.get('x-admin-token') || '').trim();
  if (!got || !safeEquals(got, token)) {
    return { ok: false, status: 401, body: { error: 'Unauthorized.' } };
  }

  return { ok: true };
}

type UpsertRequest =
  | { year: number; payload: unknown }
  | { entries: Array<{ year: number; categories: unknown }> };

async function upsertYearPayload(year: number, payload: unknown): Promise<{ ok: true } | { ok: false; status: number; error: string }> {
  const supabaseUrl = getSupabaseUrl();
  const serviceRoleKey = getServiceRoleKey();
  if (!supabaseUrl || !serviceRoleKey) {
    return { ok: false, status: 500, error: 'Server not configured.' };
  }

  const y = Number(year);
  if (!Number.isFinite(y) || y < 1900 || y > 3000) {
    return { ok: false, status: 400, error: 'Invalid year.' };
  }

  const resp = await fetch(`${supabaseUrl}/rest/v1/winners_payload`, {
    method: 'POST',
    headers: {
      apikey: serviceRoleKey,
      authorization: `Bearer ${serviceRoleKey}`,
      'content-type': 'application/json',
      prefer: 'resolution=merge-duplicates'
    },
    body: JSON.stringify({ year: y, payload, updated_at: new Date().toISOString() })
  });

  if (resp.status === 404) {
    return { ok: false, status: 500, error: 'Database table public.winners_payload was not found.' };
  }

  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    return { ok: false, status: 502, error: `Upsert failed: ${text}` };
  }

  return { ok: true };
}

serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  const admin = requireAdmin(req);
  if (!admin.ok) return json(admin.body, admin.status);

  if (req.method !== 'POST') {
    return json({ error: 'Method not allowed.' }, 405);
  }

  const body = (await req.json().catch(() => null)) as UpsertRequest | null;
  if (!body) return json({ error: 'Invalid JSON body.' }, 400);

  // Mode A: upsert one year
  if ('year' in body) {
    const res = await upsertYearPayload(Number((body as any).year), (body as any).payload);
    if (!res.ok) return json({ error: res.error }, res.status);
    return json({ ok: true });
  }

  // Mode B: upsert multiple entries, split by year
  if (Array.isArray((body as any).entries)) {
    const entries = (body as any).entries as Array<any>;
    const byYear = new Map<number, any[]>();
    for (const e of entries) {
      const y = Number(e?.year);
      if (!Number.isFinite(y)) continue;
      const list = byYear.get(y) ?? [];
      list.push(e);
      byYear.set(y, list);
    }

    const results: Array<{ year: number; ok: boolean; error?: string }> = [];
    for (const [year, list] of byYear.entries()) {
      // Store the single YearEntry if only one, else store array.
      const payload = list.length === 1 ? list[0] : list;
      const res = await upsertYearPayload(year, payload);
      results.push({ year, ok: res.ok, ...(res.ok ? {} : { error: (res as any).error }) });
    }

    return json({ ok: true, results });
  }

  return json({ error: 'Invalid body. Expected {year,payload} or {entries:[...]}' }, 400);
});
