import { serve } from 'https://deno.land/std@0.224.0/http/server.ts';
import { corsHeaders } from '../_shared/cors.ts';
import { requireRegisteredMember } from '../_shared/membership.ts';

type TrackPayload = {
  slide_id?: string;
  slide_url?: string;
  target?: string;
  access_token?: string;
  accessToken?: string;
};

const ALLOWED_SLIDE_HOSTS = new Set(['drive.google.com', 'docs.google.com']);

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

function getSupabaseUrl(): string {
  return normalizeSupabaseUrl(String(Deno.env.get('SUPABASE_URL') || Deno.env.get('URL') || '').trim());
}

function getServiceRoleKey(): string {
  return String(Deno.env.get('SERVICE_ROLE_KEY') || Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') || '').trim();
}

function parseBearerToken(req: Request): string {
  const auth = String(req.headers.get('authorization') || '').trim();
  if (!auth.toLowerCase().startsWith('bearer ')) return '';
  return auth.slice(7).trim();
}

function parseQueryPayload(req: Request): TrackPayload {
  const url = new URL(req.url);
  return {
    slide_id: String(url.searchParams.get('slide_id') || '').trim(),
    slide_url: String(url.searchParams.get('slide_url') || '').trim(),
    target: String(url.searchParams.get('target') || '').trim(),
    access_token: String(url.searchParams.get('access_token') || '').trim()
  };
}

async function parseBodyPayload(req: Request): Promise<TrackPayload> {
  const contentType = String(req.headers.get('content-type') || '').toLowerCase();

  if (contentType.includes('application/json')) {
    const body = (await req.json().catch(() => null)) as TrackPayload | null;
    return body || {};
  }

  const formData = await req.formData().catch(() => null);
  if (!formData) return {};

  const get = (key: string): string => String(formData.get(key) || '').trim();
  return {
    slide_id: get('slide_id'),
    slide_url: get('slide_url'),
    target: get('target'),
    access_token: get('access_token') || get('accessToken')
  };
}

function toValidSlideUrl(input: string): string {
  const raw = String(input || '').trim();
  if (!raw) return '';

  try {
    const parsed = new URL(raw);
    if (parsed.protocol !== 'https:') return '';
    if (!ALLOWED_SLIDE_HOSTS.has(parsed.hostname.toLowerCase())) return '';
    return parsed.toString();
  } catch {
    return '';
  }
}

function buildMembershipRequest(req: Request, token: string): Request {
  const headers = new Headers(req.headers);
  headers.set('authorization', `Bearer ${token}`);
  return new Request(req.url, { method: req.method, headers });
}

async function insertEvent(row: {
  email: string;
  slideId: string;
  slideUrl: string;
  userAgent: string;
  referrer: string;
  requestMethod: string;
}): Promise<{ ok: true } | { ok: false; status: number; error: string }> {
  const supabaseUrl = getSupabaseUrl();
  const serviceRoleKey = getServiceRoleKey();
  if (!supabaseUrl || !serviceRoleKey) {
    return { ok: false, status: 500, error: 'Server not configured.' };
  }

  const payload = {
    email: row.email,
    slide_id: row.slideId,
    slide_url: row.slideUrl,
    user_agent: row.userAgent || null,
    referrer: row.referrer || null,
    request_method: row.requestMethod || null,
    metadata: null
  };

  const resp = await fetch(`${supabaseUrl}/rest/v1/slide_download_events`, {
    method: 'POST',
    headers: {
      apikey: serviceRoleKey,
      authorization: `Bearer ${serviceRoleKey}`,
      'content-type': 'application/json',
      prefer: 'return=minimal'
    },
    body: JSON.stringify(payload)
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    return { ok: false, status: resp.status, error: text || 'Failed to insert event.' };
  }

  return { ok: true };
}

function redirectTo(target: string): Response {
  return new Response(null, {
    status: 302,
    headers: {
      ...corsHeaders,
      location: target,
      'cache-control': 'no-store'
    }
  });
}

serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  if (req.method !== 'GET' && req.method !== 'POST') {
    return json({ error: 'Method not allowed.' }, 405);
  }

  const payload = req.method === 'POST' ? await parseBodyPayload(req) : parseQueryPayload(req);
  const slideId = String(payload.slide_id || '').trim() || 'unknown-slide';
  const slideUrl = toValidSlideUrl(String(payload.slide_url || payload.target || '').trim());

  if (!slideUrl) {
    return json({ error: 'Invalid or unsupported slide_url. Only drive.google.com/docs.google.com HTTPS URLs are allowed.' }, 400);
  }

  const accessToken = parseBearerToken(req) || String(payload.access_token || payload.accessToken || '').trim();
  if (!accessToken) {
    return json({ error: 'Unauthorized. Missing access token.' }, 401);
  }

  const membership = await requireRegisteredMember(buildMembershipRequest(req, accessToken));
  if (!membership.ok) {
    return json(membership.body, membership.status);
  }

  const insert = await insertEvent({
    email: membership.email,
    slideId,
    slideUrl,
    userAgent: String(req.headers.get('user-agent') || ''),
    referrer: String(req.headers.get('referer') || ''),
    requestMethod: req.method
  });

  if (!insert.ok) {
    console.error('slide-download-track insert failed', {
      status: insert.status,
      error: insert.error,
      email: membership.email,
      slideId
    });
  }

  return redirectTo(slideUrl);
});
