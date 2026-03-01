import { serve } from 'https://deno.land/std@0.224.0/http/server.ts';
import { corsHeaders } from '../_shared/cors.ts';

type VisitPayload = {
  path?: string;
  page_title?: string;
  referrer?: string;
  session_id?: string;
  metadata?: Record<string, unknown> | null;
  access_token?: string;
  accessToken?: string;
};

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

function normalizeEmail(value: string): string {
  return String(value || '').trim().toLowerCase();
}

function getSupabaseUrl(): string {
  return normalizeSupabaseUrl(String(Deno.env.get('SUPABASE_URL') || Deno.env.get('URL') || '').trim());
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

function cleanText(value: string, maxLen = 500): string {
  return String(value || '').trim().slice(0, maxLen);
}

function parseQueryPayload(req: Request): VisitPayload {
  const url = new URL(req.url);
  return {
    path: cleanText(String(url.searchParams.get('path') || ''), 300),
    page_title: cleanText(String(url.searchParams.get('page_title') || ''), 200),
    referrer: cleanText(String(url.searchParams.get('referrer') || ''), 1000),
    session_id: cleanText(String(url.searchParams.get('session_id') || ''), 100),
    access_token: cleanText(String(url.searchParams.get('access_token') || ''), 4000)
  };
}

async function parseBodyPayload(req: Request): Promise<VisitPayload> {
  const contentType = String(req.headers.get('content-type') || '').toLowerCase();

  if (contentType.includes('application/json')) {
    const body = (await req.json().catch(() => null)) as VisitPayload | null;
    return body || {};
  }

  const formData = await req.formData().catch(() => null);
  if (!formData) return {};

  const get = (key: string, maxLen = 500): string => cleanText(String(formData.get(key) || ''), maxLen);
  return {
    path: get('path', 300),
    page_title: get('page_title', 200),
    referrer: get('referrer', 1000),
    session_id: get('session_id', 100),
    access_token: get('access_token', 4000) || get('accessToken', 4000)
  };
}

async function getSignedInEmail(input: {
  supabaseUrl: string;
  anonKey: string;
  accessToken: string;
}): Promise<string> {
  const token = String(input.accessToken || '').trim();
  if (!token || !input.supabaseUrl || !input.anonKey) return '';

  const resp = await fetch(`${input.supabaseUrl}/auth/v1/user`, {
    headers: {
      apikey: input.anonKey,
      authorization: `Bearer ${token}`
    }
  }).catch(() => null);

  if (!resp || !resp.ok) return '';

  const body = await resp.json().catch(() => ({} as any));
  return normalizeEmail(body?.email || body?.user_metadata?.email || '');
}

async function insertEvent(input: {
  supabaseUrl: string;
  serviceRoleKey: string;
  email: string;
  path: string;
  pageTitle: string;
  referrer: string;
  sessionId: string;
  userAgent: string;
  metadata: Record<string, unknown> | null;
}): Promise<{ ok: true } | { ok: false; status: number; error: string }> {
  const payload = {
    email: input.email || null,
    path: input.path,
    page_title: input.pageTitle || null,
    referrer: input.referrer || null,
    session_id: input.sessionId || null,
    user_agent: input.userAgent || null,
    metadata: input.metadata || null
  };

  const resp = await fetch(`${input.supabaseUrl}/rest/v1/page_visit_events`, {
    method: 'POST',
    headers: {
      apikey: input.serviceRoleKey,
      authorization: `Bearer ${input.serviceRoleKey}`,
      'content-type': 'application/json',
      prefer: 'return=minimal'
    },
    body: JSON.stringify(payload)
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    return { ok: false, status: resp.status, error: text || 'Failed to insert visit event.' };
  }

  return { ok: true };
}

serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  if (req.method !== 'GET' && req.method !== 'POST') {
    return json({ error: 'Method not allowed.' }, 405);
  }

  const supabaseUrl = getSupabaseUrl();
  const anonKey = getAnonKey();
  const serviceRoleKey = getServiceRoleKey();
  if (!supabaseUrl || !serviceRoleKey) {
    return json({ error: 'Server not configured.' }, 500);
  }

  const payload = req.method === 'POST' ? await parseBodyPayload(req) : parseQueryPayload(req);
  const path = cleanText(String(payload.path || ''), 300);
  if (!path || !path.startsWith('/')) {
    return json({ error: 'Invalid path.' }, 400);
  }

  const accessToken = parseBearerToken(req) || cleanText(String(payload.access_token || payload.accessToken || ''), 4000);
  const email = accessToken && anonKey
    ? await getSignedInEmail({ supabaseUrl, anonKey, accessToken })
    : '';

  const insert = await insertEvent({
    supabaseUrl,
    serviceRoleKey,
    email,
    path,
    pageTitle: cleanText(String(payload.page_title || ''), 200),
    referrer: cleanText(String(payload.referrer || req.headers.get('referer') || ''), 1000),
    sessionId: cleanText(String(payload.session_id || ''), 100),
    userAgent: cleanText(String(req.headers.get('user-agent') || ''), 500),
    metadata: payload.metadata && typeof payload.metadata === 'object' ? payload.metadata : null
  });

  if (!insert.ok) {
    console.error('page-visit-track insert failed', {
      status: insert.status,
      error: insert.error,
      path,
      email
    });
    return json({ ok: false }, 202);
  }

  return json({ ok: true });
});
