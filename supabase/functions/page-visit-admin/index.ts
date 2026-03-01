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

function normalizeEmail(value: string): string {
  return String(value || '').trim().toLowerCase();
}

function normalizeSupabaseUrl(raw: string): string {
  const value = String(raw || '').trim();
  if (!value) return '';
  try {
    const url = new URL(value);
    const host = url.hostname;
    if (host.includes('.functions.supabase.co')) {
      const projectRef = host.split('.')[0];
      if (projectRef) return `https://${projectRef}.supabase.co`;
    }
  } catch {
    // ignore
  }
  return value;
}

function getSupabaseUrl(): string {
  const raw = Deno.env.get('SUPABASE_URL') || Deno.env.get('URL') || '';
  return normalizeSupabaseUrl(raw);
}

function getAnonKey(): string {
  return String(Deno.env.get('ANON_KEY') || Deno.env.get('SUPABASE_ANON_KEY') || '').trim();
}

function getServiceRoleKey(): string {
  return String(Deno.env.get('SERVICE_ROLE_KEY') || Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') || '').trim();
}

function parseBearerToken(req: Request): string {
  const auth = String(req.headers.get('authorization') || '').trim();
  if (!auth.toLowerCase().startsWith('bearer ')) return '';
  return auth.slice(7).trim();
}

function getAllowedOrigins(): string[] {
  const raw = String(Deno.env.get('ADMIN_ALLOWED_ORIGINS') || '').trim();
  if (!raw) return [];
  return raw
    .split(',')
    .map((value) => String(value || '').trim().toLowerCase())
    .filter(Boolean);
}

function isAllowedOrigin(req: Request): boolean {
  const allowlist = getAllowedOrigins();
  if (!allowlist.length) return true;

  const origin = String(req.headers.get('origin') || '').trim().toLowerCase();
  if (!origin) return true;
  return allowlist.includes(origin);
}

function parseIntInRange(value: string, fallback: number, min: number, max: number): number {
  const n = Number(value);
  if (!Number.isFinite(n)) return fallback;
  const i = Math.floor(n);
  if (i < min) return min;
  if (i > max) return max;
  return i;
}

async function getSignedInEmail(input: {
  supabaseUrl: string;
  anonKey: string;
  accessToken: string;
}): Promise<{ ok: true; email: string } | { ok: false; status: number; error: string }> {
  const resp = await fetch(`${input.supabaseUrl}/auth/v1/user`, {
    headers: {
      apikey: input.anonKey,
      authorization: `Bearer ${input.accessToken}`
    }
  });

  if (!resp.ok) {
    return { ok: false, status: 401, error: 'Unauthorized. Please sign in.' };
  }

  const body = await resp.json().catch(() => ({} as any));
  const email = normalizeEmail(body?.email || body?.user_metadata?.email || '');
  if (!email) {
    return { ok: false, status: 401, error: 'Unauthorized. Email not found in session.' };
  }

  return { ok: true, email };
}

async function isAdminEmail(input: {
  supabaseUrl: string;
  serviceRoleKey: string;
  email: string;
}): Promise<{ ok: true } | { ok: false; status: number; error: string }> {
  const url = new URL(`${input.supabaseUrl}/rest/v1/admin_users`);
  url.searchParams.set('select', 'email');
  url.searchParams.set('email', `eq.${input.email}`);
  url.searchParams.set('limit', '1');

  const resp = await fetch(url.toString(), {
    headers: {
      apikey: input.serviceRoleKey,
      authorization: `Bearer ${input.serviceRoleKey}`
    }
  });

  if (!resp.ok) {
    return { ok: false, status: 500, error: 'Could not verify admin access.' };
  }

  const rows = (await resp.json().catch(() => [])) as Array<{ email?: string }>;
  if (!Array.isArray(rows) || rows.length === 0) {
    return { ok: false, status: 403, error: 'Forbidden. Admin access required.' };
  }

  return { ok: true };
}

async function loadVisitEvents(input: {
  req: Request;
  supabaseUrl: string;
  serviceRoleKey: string;
}): Promise<
  | {
      ok: true;
      rows: Array<Record<string, unknown>>;
      total: number | null;
      pagination: { limit: number; offset: number };
      filters: Record<string, string>;
    }
  | { ok: false; status: number; error: string }
> {
  const requestUrl = new URL(input.req.url);

  const limit = parseIntInRange(String(requestUrl.searchParams.get('limit') || ''), 200, 1, 20000);
  const offset = parseIntInRange(String(requestUrl.searchParams.get('offset') || ''), 0, 0, 1000000);

  const email = normalizeEmail(String(requestUrl.searchParams.get('email') || ''));
  const path = String(requestUrl.searchParams.get('path') || '').trim();
  const from = String(requestUrl.searchParams.get('from') || '').trim();
  const to = String(requestUrl.searchParams.get('to') || '').trim();

  const url = new URL(`${input.supabaseUrl}/rest/v1/page_visit_events`);
  url.searchParams.set('select', 'id,email,path,page_title,referrer,session_id,event_at,user_agent,metadata');
  url.searchParams.set('order', 'event_at.desc');
  url.searchParams.set('limit', String(limit));
  url.searchParams.set('offset', String(offset));

  const filters: Record<string, string> = {};

  if (email) {
    url.searchParams.set('email', `eq.${email}`);
    filters.email = email;
  }

  if (path) {
    url.searchParams.set('path', `eq.${path}`);
    filters.path = path;
  }

  if (from) {
    url.searchParams.append('event_at', `gte.${from}`);
    filters.from = from;
  }

  if (to) {
    url.searchParams.append('event_at', `lte.${to}`);
    filters.to = to;
  }

  const resp = await fetch(url.toString(), {
    headers: {
      apikey: input.serviceRoleKey,
      authorization: `Bearer ${input.serviceRoleKey}`,
      prefer: 'count=exact'
    }
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    return { ok: false, status: 500, error: text || 'Failed to load page visit events.' };
  }

  const rows = (await resp.json().catch(() => [])) as Array<Record<string, unknown>>;

  const contentRange = String(resp.headers.get('content-range') || '').trim();
  let total: number | null = null;
  const slashIndex = contentRange.lastIndexOf('/');
  if (slashIndex >= 0) {
    const totalStr = contentRange.slice(slashIndex + 1).trim();
    const parsed = Number(totalStr);
    if (Number.isFinite(parsed) && parsed >= 0) total = parsed;
  }

  return {
    ok: true,
    rows,
    total,
    pagination: { limit, offset },
    filters
  };
}

serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  if (req.method !== 'GET') {
    return json({ error: 'Method not allowed.' }, 405);
  }

  const supabaseUrl = getSupabaseUrl();
  const anonKey = getAnonKey();
  const serviceRoleKey = getServiceRoleKey();
  if (!supabaseUrl || !anonKey || !serviceRoleKey) {
    return json({ error: 'Server not configured.' }, 500);
  }

  if (!isAllowedOrigin(req)) {
    return json({ error: 'Forbidden.' }, 403);
  }

  const accessToken = parseBearerToken(req);
  if (!accessToken) {
    return json({ error: 'Unauthorized. Missing access token.' }, 401);
  }

  const user = await getSignedInEmail({ supabaseUrl, anonKey, accessToken });
  if (!user.ok) return json({ error: user.error }, user.status);

  const admin = await isAdminEmail({
    supabaseUrl,
    serviceRoleKey,
    email: user.email
  });
  if (!admin.ok) return json({ error: admin.error }, admin.status);

  const visits = await loadVisitEvents({ req, supabaseUrl, serviceRoleKey });
  if (!visits.ok) return json({ error: visits.error }, visits.status);

  return json({
    ok: true,
    admin_email: user.email,
    total: visits.total,
    limit: visits.pagination.limit,
    offset: visits.pagination.offset,
    filters: visits.filters,
    visits: visits.rows
  });
});
