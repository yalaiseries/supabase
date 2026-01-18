type MembershipCheckResult =
  | { ok: true; email: string }
  | { ok: false; status: number; body: { error: string; code?: string } };

function normalizeEmail(value: string): string {
  return String(value || '').trim().toLowerCase();
}

function parseBearerToken(req: Request): string {
  const auth = req.headers.get('authorization') || '';
  if (!auth.toLowerCase().startsWith('bearer ')) return '';
  return auth.slice(7).trim();
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
  // Prefer project-level SUPABASE_URL. If URL points to functions host, normalize it.
  const raw = Deno.env.get('SUPABASE_URL') || Deno.env.get('URL') || '';
  return normalizeSupabaseUrl(raw);
}

function getAnonKey(): string {
  // Prefer function-level secret "ANON_KEY", fall back to SUPABASE_ANON_KEY
  return String(Deno.env.get('ANON_KEY') || Deno.env.get('SUPABASE_ANON_KEY') || '').trim();
}

function getServiceRoleKey(): string {
  // Prefer function-level secret "SERVICE_ROLE_KEY", fall back to SUPABASE_SERVICE_ROLE_KEY
  return String(Deno.env.get('SERVICE_ROLE_KEY') || Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') || '').trim();
}

export async function requireRegisteredMember(req: Request): Promise<MembershipCheckResult> {
  const accessToken = parseBearerToken(req);
  if (!accessToken) {
    return { ok: false, status: 401, body: { error: 'Unauthorized. Please sign in.', code: 'unauthorized' } };
  }

  const supabaseUrl = getSupabaseUrl();
  const anonKey = getAnonKey();
  const serviceRoleKey = getServiceRoleKey();

  if (!supabaseUrl || !anonKey || !serviceRoleKey) {
    return { ok: false, status: 500, body: { error: 'Server not configured.', code: 'server_not_configured' } };
  }

  // 1) Get the signed-in user's email via Auth API.
  const userResp = await fetch(`${supabaseUrl}/auth/v1/user`, {
    headers: {
      apikey: anonKey,
      authorization: `Bearer ${accessToken}`
    }
  });

  if (!userResp.ok) {
    return { ok: false, status: 401, body: { error: 'Unauthorized. Please sign in.', code: 'unauthorized' } };
  }

  const userData = await userResp.json().catch(() => ({} as any));
  const email = normalizeEmail(userData?.email || userData?.user_metadata?.email || '');
  if (!email) {
    return { ok: false, status: 401, body: { error: 'Unauthorized. Please sign in.', code: 'unauthorized' } };
  }

  // 2) Check allowlist in DB using service role key.
  const allowUrl = new URL(`${supabaseUrl}/rest/v1/allowed_members`);
  allowUrl.searchParams.set('select', 'email');
  allowUrl.searchParams.set('email', `eq.${email}`);
  allowUrl.searchParams.set('limit', '1');

  const allowResp = await fetch(allowUrl.toString(), {
    headers: {
      apikey: serviceRoleKey,
      authorization: `Bearer ${serviceRoleKey}`
    }
  });

  if (allowResp.status === 404) {
    return {
      ok: false,
      status: 500,
      body: {
        error: 'Server not configured. Database table "public.allowed_members" was not found.',
        code: 'allowlist_table_missing'
      }
    };
  }

  if (!allowResp.ok) {
    return { ok: false, status: 500, body: { error: 'Could not verify registration.', code: 'membership_check_failed' } };
  }

  const rows = (await allowResp.json().catch(() => [])) as Array<{ email?: string }>;
  if (!Array.isArray(rows) || rows.length === 0) {
    return {
      ok: false,
      status: 403,
      body: {
        error: 'You are signed in, but not registered yet. Please submit the registration form and try again.',
        code: 'not_registered'
      }
    };
  }

  return { ok: true, email };
}

export async function upsertAllowedMember(input: {
  email: string;
  name?: string;
  source?: string;
  payload?: unknown;
}): Promise<{ ok: true } | { ok: false; status: number; error: string }> {
  const supabaseUrl = getSupabaseUrl();
  const serviceRoleKey = getServiceRoleKey();
  if (!supabaseUrl || !serviceRoleKey) {
    return { ok: false, status: 500, error: 'Server not configured.' };
  }

  const email = normalizeEmail(input.email);
  if (!email) return { ok: false, status: 400, error: 'Missing email.' };

  const body = {
    email,
    name: input.name || null,
    source: input.source || 'google_form',
    metadata: input.payload ?? null
  };

  const resp = await fetch(`${supabaseUrl}/rest/v1/allowed_members`, {
    method: 'POST',
    headers: {
      apikey: serviceRoleKey,
      authorization: `Bearer ${serviceRoleKey}`,
      'content-type': 'application/json',
      prefer: 'resolution=merge-duplicates'
    },
    body: JSON.stringify(body)
  });

  if (resp.status === 404) {
    return { ok: false, status: 500, error: 'Server not configured. Database table "public.allowed_members" was not found.' };
  }

  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    return { ok: false, status: 502, error: `Upsert failed: ${text}` };
  }

  return { ok: true };
}