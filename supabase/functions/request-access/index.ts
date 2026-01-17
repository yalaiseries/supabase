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

function normalizeEmail(value: unknown): string {
  return String(value || '').trim().toLowerCase();
}

function getSupabaseUrl(): string {
  return String(Deno.env.get('URL') || Deno.env.get('SUPABASE_URL') || '').trim();
}

function getServiceRoleKey(): string {
  return String(Deno.env.get('SERVICE_ROLE_KEY') || Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') || '').trim();
}

type RequestAccessBody = {
  email?: string;
};

async function isAllowlisted(supabaseUrl: string, serviceRoleKey: string, email: string): Promise<
  | { ok: true; allowlisted: boolean }
  | { ok: false; status: number; error: string }
> {
  const url = new URL(`${supabaseUrl}/rest/v1/allowed_members`);
  url.searchParams.set('select', 'email');
  url.searchParams.set('email', `eq.${email}`);
  url.searchParams.set('limit', '1');

  const resp = await fetch(url.toString(), {
    headers: {
      apikey: serviceRoleKey,
      authorization: `Bearer ${serviceRoleKey}`
    }
  });

  if (resp.status === 404) {
    return { ok: false, status: 500, error: 'Server not configured. Database table "public.allowed_members" was not found.' };
  }

  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    return { ok: false, status: 502, error: `Allowlist check failed: HTTP ${resp.status} ${text}` };
  }

  const rows = (await resp.json().catch(() => [])) as Array<{ email?: string }>;
  return { ok: true, allowlisted: Array.isArray(rows) && rows.length > 0 };
}

async function sendInvite(supabaseUrl: string, serviceRoleKey: string, email: string): Promise<void> {
  const redirectTo = String(Deno.env.get('INVITE_REDIRECT_URL') || '').trim();
  const url = new URL(`${supabaseUrl}/auth/v1/admin/invite`);
  if (redirectTo) url.searchParams.set('redirect_to', redirectTo);

  await fetch(url.toString(), {
    method: 'POST',
    headers: {
      apikey: serviceRoleKey,
      authorization: `Bearer ${serviceRoleKey}`,
      'content-type': 'application/json'
    },
    body: JSON.stringify({ email })
  });
}

serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  if (req.method !== 'POST') {
    return json({ error: 'Method not allowed' }, 405);
  }

  const supabaseUrl = getSupabaseUrl();
  const serviceRoleKey = getServiceRoleKey();
  if (!supabaseUrl || !serviceRoleKey) {
    return json({ error: 'Server not configured.' }, 500);
  }

  let payload: RequestAccessBody;
  try {
    payload = (await req.json()) as RequestAccessBody;
  } catch {
    return json({ error: 'Invalid JSON' }, 400);
  }

  const email = normalizeEmail(payload?.email);
  if (!email) {
    // Generic response to avoid leaking.
    return json({ ok: true });
  }

  const allow = await isAllowlisted(supabaseUrl, serviceRoleKey, email);
  if (!allow.ok) {
    return json({ error: allow.error }, allow.status);
  }

  // Privacy: do NOT reveal allowlist status to the caller.
  // Only send the invite email when allowlisted.
  if (allow.allowlisted) {
    try {
      await sendInvite(supabaseUrl, serviceRoleKey, email);
    } catch {
      // Intentionally swallow errors to avoid allowlist enumeration.
      // Check Supabase Function logs if you need to debug invite sending.
    }
  }

  return json({ ok: true });
});

// Deployed via GitHub Actions (CI).
