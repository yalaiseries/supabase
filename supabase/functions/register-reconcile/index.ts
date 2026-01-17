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
  // Prefer function-level secret "URL", fall back to project-level SUPABASE_URL
  return String(Deno.env.get('URL') || Deno.env.get('SUPABASE_URL') || '').trim();
}

function getServiceRoleKey(): string {
  // Prefer function-level secret "SERVICE_ROLE_KEY", fall back to SUPABASE_SERVICE_ROLE_KEY
  return String(Deno.env.get('SERVICE_ROLE_KEY') || Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') || '').trim();
}

type IncomingRow = {
  email?: unknown;
  name?: unknown;
  source?: unknown;
  metadata?: unknown;
  [k: string]: unknown;
};

type ReconcileRequest = {
  rows?: IncomingRow[];
  allowEmptyDelete?: boolean;
  source?: string;
  [k: string]: unknown;
};

async function fetchJson<T>(url: string, init: RequestInit): Promise<{ ok: true; data: T } | { ok: false; status: number; text: string }> {
  const resp = await fetch(url, init);
  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    return { ok: false, status: resp.status, text };
  }
  const data = (await resp.json().catch(() => null)) as T;
  return { ok: true, data };
}

async function listAllEmails(supabaseUrl: string, serviceRoleKey: string): Promise<{ ok: true; emails: string[] } | { ok: false; status: number; error: string }> {
  const pageSize = 1000;
  let offset = 0;
  const emails: string[] = [];

  while (true) {
    const url = new URL(`${supabaseUrl}/rest/v1/allowed_members`);
    url.searchParams.set('select', 'email');
    url.searchParams.set('order', 'email.asc');
    url.searchParams.set('limit', String(pageSize));
    url.searchParams.set('offset', String(offset));

    const resp = await fetchJson<Array<{ email?: string }>>(url.toString(), {
      headers: {
        apikey: serviceRoleKey,
        authorization: `Bearer ${serviceRoleKey}`
      }
    });

    if (!resp.ok) {
      if (resp.status === 404) {
        return { ok: false, status: 500, error: 'Server not configured. Database table "public.allowed_members" was not found.' };
      }
      return { ok: false, status: 502, error: `Failed to list allowed_members: HTTP ${resp.status} ${resp.text}` };
    }

    const rows = Array.isArray(resp.data) ? resp.data : [];
    for (const row of rows) {
      if (row?.email) emails.push(normalizeEmail(row.email));
    }

    if (rows.length < pageSize) break;
    offset += pageSize;
  }

  return { ok: true, emails };
}

async function upsertRows(supabaseUrl: string, serviceRoleKey: string, rows: Array<{ email: string; name: string | null; source: string; metadata: unknown }>): Promise<{ ok: true } | { ok: false; status: number; error: string }> {
  if (rows.length === 0) return { ok: true };

  const resp = await fetch(`${supabaseUrl}/rest/v1/allowed_members?on_conflict=email`, {
    method: 'POST',
    headers: {
      apikey: serviceRoleKey,
      authorization: `Bearer ${serviceRoleKey}`,
      'content-type': 'application/json',
      prefer: 'resolution=merge-duplicates'
    },
    body: JSON.stringify(rows)
  });

  if (resp.status === 404) {
    return { ok: false, status: 500, error: 'Server not configured. Database table "public.allowed_members" was not found.' };
  }

  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    return { ok: false, status: 502, error: `Upsert failed: HTTP ${resp.status} ${text}` };
  }

  return { ok: true };
}

async function deleteEmails(supabaseUrl: string, serviceRoleKey: string, emails: string[]): Promise<{ ok: true } | { ok: false; status: number; error: string }> {
  if (emails.length === 0) return { ok: true };

  // Chunk to avoid URL length limits.
  const chunkSize = 50;
  for (let i = 0; i < emails.length; i += chunkSize) {
    const chunk = emails.slice(i, i + chunkSize);
    const url = new URL(`${supabaseUrl}/rest/v1/allowed_members`);
    url.searchParams.set('email', `in.(${chunk.join(',')})`);

    const resp = await fetch(url.toString(), {
      method: 'DELETE',
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
      return { ok: false, status: 502, error: `Delete failed: HTTP ${resp.status} ${text}` };
    }
  }

  return { ok: true };
}

serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  if (req.method !== 'POST') {
    return json({ error: 'Method not allowed' }, 405);
  }

  const expected = String(Deno.env.get('REGISTRATION_WEBHOOK_SECRET') || '').trim();
  const provided = String(req.headers.get('x-webhook-secret') || '').trim();
  if (!expected || provided !== expected) {
    return json({ error: 'Unauthorized' }, 401);
  }

  const supabaseUrl = getSupabaseUrl();
  const serviceRoleKey = getServiceRoleKey();
  if (!supabaseUrl || !serviceRoleKey) {
    return json({ error: 'Server not configured.' }, 500);
  }

  let payloadRaw: unknown;
  try {
    payloadRaw = await req.json();
  } catch (_e) {
    return json({ error: 'Invalid JSON' }, 400);
  }

  let payload: ReconcileRequest;
  if (Array.isArray(payloadRaw)) {
    payload = { rows: payloadRaw as IncomingRow[] };
  } else {
    payload = (payloadRaw || {}) as ReconcileRequest;
  }

  const source = String(payload.source || 'google_sheet_reconcile');
  const allowEmptyDelete = Boolean(payload.allowEmptyDelete);

  const incomingRows = Array.isArray(payload.rows) ? payload.rows : [];

  // Build a deduped map by email.
  const rowByEmail = new Map<string, { email: string; name: string | null; source: string; metadata: unknown }>();
  for (const r of incomingRows) {
    const email = normalizeEmail(r?.email);
    if (!email) continue;

    const name = r?.name != null ? String(r.name).trim() : '';

    // Last write wins if sheet contains duplicates.
    rowByEmail.set(email, {
      email,
      name: name ? name : null,
      source: String(r?.source || source),
      metadata: r?.metadata ?? null
    });
  }

  const sheetEmails = Array.from(rowByEmail.keys());
  if (sheetEmails.length === 0 && !allowEmptyDelete) {
    return json(
      {
        error: 'No valid emails provided. If you really intend to wipe allowed_members, set allowEmptyDelete=true.'
      },
      400
    );
  }

  // 1) List current DB emails.
  const list = await listAllEmails(supabaseUrl, serviceRoleKey);
  if (!list.ok) {
    return json({ error: list.error }, list.status);
  }

  const currentEmailSet = new Set(list.emails);
  const sheetEmailSet = new Set(sheetEmails);

  // 2) Upsert all provided rows.
  const upsertAll = Array.from(rowByEmail.values());
  const upsertChunkSize = 500;
  for (let i = 0; i < upsertAll.length; i += upsertChunkSize) {
    const chunk = upsertAll.slice(i, i + upsertChunkSize);
    const up = await upsertRows(supabaseUrl, serviceRoleKey, chunk);
    if (!up.ok) return json({ error: up.error }, up.status);
  }

  // 3) Delete any DB email not in sheet.
  const toDelete: string[] = [];
  for (const email of currentEmailSet) {
    if (!sheetEmailSet.has(email)) toDelete.push(email);
  }

  const del = await deleteEmails(supabaseUrl, serviceRoleKey, toDelete);
  if (!del.ok) return json({ error: del.error }, del.status);

  return json({
    ok: true,
    sheetCount: sheetEmails.length,
    currentCount: list.emails.length,
    upserted: upsertAll.length,
    deleted: toDelete.length
  });
});

// Deployed via GitHub Actions (CI).
