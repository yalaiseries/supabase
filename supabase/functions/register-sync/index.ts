import { serve } from 'https://deno.land/std@0.224.0/http/server.ts';
import { corsHeaders } from '../_shared/cors.ts';
import { upsertAllowedMember } from '../_shared/membership.ts';

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

type WebhookBody = {
  email?: string;
  name?: string;
  source?: string;
  [k: string]: unknown;
};

serve(async (req) => {
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

  let payload: WebhookBody;
  try {
    payload = (await req.json()) as WebhookBody;
  } catch (_e) {
    return json({ error: 'Invalid JSON' }, 400);
  }

  const email = String(payload.email || '').trim();
  if (!email) return json({ error: 'Missing email' }, 400);

  const result = await upsertAllowedMember({
    email,
    name: payload.name ? String(payload.name) : undefined,
    source: payload.source ? String(payload.source) : 'google_form',
    payload
  });

  if (!result.ok) {
    return json({ error: result.error }, result.status);
  }

  return json({ ok: true });
});
