import { serve } from 'https://deno.land/std@0.224.0/http/server.ts';
import { corsHeaders } from '../_shared/cors.ts';
import { websiteKb } from '../_shared/kb.ts';
import { requireRegisteredMember } from '../_shared/membership.ts';

function getBoolEnv(name: string, fallback = false): boolean {
  const raw = String(Deno.env.get(name) || '').trim().toLowerCase();
  if (!raw) return fallback;
  return raw === '1' || raw === 'true' || raw === 'yes' || raw === 'y' || raw === 'on';
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

function getServiceRoleKey(): string {
  return String(Deno.env.get('SERVICE_ROLE_KEY') || Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') || '').trim();
}

function getIntEnv(name: string, fallback: number): number {
  const raw = String(Deno.env.get(name) || '').trim();
  const n = Number.parseInt(raw, 10);
  return Number.isFinite(n) && n > 0 ? n : fallback;
}

function getClientIp(req: Request): string {
  const cf = String(req.headers.get('cf-connecting-ip') || '').trim();
  if (cf) return cf;

  const real = String(req.headers.get('x-real-ip') || '').trim();
  if (real) return real;

  const xff = String(req.headers.get('x-forwarded-for') || '').trim();
  if (!xff) return '';
  return xff.split(',')[0]?.trim() || '';
}

async function sha256Hex(input: string): Promise<string> {
  const data = new TextEncoder().encode(input);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
}

function htmlToText(html: string): string {
  let v = String(html || '');
  v = v.replace(/<script[\s\S]*?<\/script>/gi, ' ');
  v = v.replace(/<style[\s\S]*?<\/style>/gi, ' ');
  v = v.replace(/<br\s*\/?\s*>/gi, '\n');
  v = v.replace(/<\/(p|div|li|h1|h2|h3|h4|h5|h6|section|article|ul|ol)>/gi, '\n');
  v = v.replace(/<[^>]+>/g, ' ');
  v = v
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
  v = v.replace(/[ \t\f\v]+/g, ' ');
  v = v.replace(/\n\s+/g, '\n');
  v = v.replace(/\n{3,}/g, '\n\n');
  return v.trim();
}

async function loadKb(): Promise<{ source: string; text: string }> {
  const kbUrl = String(Deno.env.get('CHAT_KB_URL') || '').trim();
  const maxChars = getIntEnv('CHAT_KB_MAX_CHARS', 8000);
  if (!kbUrl) return { source: 'embedded', text: websiteKb.slice(0, maxChars) };

  try {
    const resp = await fetch(kbUrl, {
      headers: {
        'user-agent': 'aihackathon-pro-chat/1.0'
      }
    });
    if (!resp.ok) throw new Error(`kb fetch failed: ${resp.status}`);
    const html = await resp.text();
    const text = htmlToText(html);
    return { source: kbUrl, text: text.slice(0, maxChars) };
  } catch {
    return { source: 'embedded-fallback', text: websiteKb.slice(0, maxChars) };
  }
}

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

type ChatBody = {
  question?: string;
};

function getByokKey(req: Request): string {
  // Optional: user provides their own OpenAI key. Do not store it.
  return String(req.headers.get('x-openai-key') || '').trim();
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  if (req.method !== 'POST') {
    return json({ error: 'Method not allowed' }, 405);
  }

  const requireAuth = getBoolEnv('CHAT_REQUIRE_AUTH', true);
  const publicMode = getBoolEnv('CHAT_PUBLIC', false);

  let memberEmail = '';
  if (requireAuth && !publicMode) {
    const member = await requireRegisteredMember(req);
    if (!member.ok) {
      return json(member.body, member.status);
    }
    memberEmail = member.email;
  }

  // If public mode is enabled, apply a privacy-preserving IP-based rate limit.
  if (publicMode) {
    const ipDailyLimit = getIntEnv('CHAT_IP_DAILY_LIMIT', 60);
    const supabaseUrl = getSupabaseUrl();
    const serviceRoleKey = getServiceRoleKey();
    const ip = getClientIp(req);
    if (supabaseUrl && serviceRoleKey && ip) {
      const ipHash = (await sha256Hex(ip)).slice(0, 32);
      const rpcResp = await fetch(`${supabaseUrl}/rest/v1/rpc/chat_usage_ip_increment`, {
        method: 'POST',
        headers: {
          apikey: serviceRoleKey,
          authorization: `Bearer ${serviceRoleKey}`,
          'content-type': 'application/json'
        },
        body: JSON.stringify({ p_ip_hash: ipHash })
      });

      if (rpcResp.ok) {
        const count = Number(await rpcResp.json().catch(() => 0));
        if (Number.isFinite(count) && count > ipDailyLimit) {
          return json({ error: `Too many requests. Please try again tomorrow.` }, 429);
        }
      }
    }
  }

  // Cost control: enforce per-member daily quota using an atomic DB counter.
  // Uses service role key server-side (never exposed to the browser).
  const dailyLimit = getIntEnv('CHAT_DAILY_LIMIT', 20);
  const supabaseUrl = getSupabaseUrl();
  const serviceRoleKey = getServiceRoleKey();
  if (memberEmail && supabaseUrl && serviceRoleKey) {
    const rpcResp = await fetch(`${supabaseUrl}/rest/v1/rpc/chat_usage_increment`, {
      method: 'POST',
      headers: {
        apikey: serviceRoleKey,
        authorization: `Bearer ${serviceRoleKey}`,
        'content-type': 'application/json'
      },
      body: JSON.stringify({ p_email: memberEmail })
    });

    if (rpcResp.ok) {
      const count = Number(await rpcResp.json().catch(() => 0));
      if (Number.isFinite(count) && count > dailyLimit) {
        return json(
          {
            error: `Daily chat limit reached (${dailyLimit}/day). Please try again tomorrow or contact the organisers if you need more access.`
          },
          429
        );
      }
    }
    // If quota tracking fails, we allow the request (fail-open) to avoid breaking the site.
    // You can inspect function logs to debug.
  }

  const byokOnly = getBoolEnv('CHAT_BYOK_ONLY', false);
  const byokKey = getByokKey(req);
  const apiKey = (byokOnly ? byokKey : byokKey || (Deno.env.get('OPENAI_API_KEY') || '')).trim();
  if (!apiKey) {
    return json(
      {
        error:
          byokOnly
            ? 'BYOK is required. Please provide your API key in the “Bring your own API key” field.'
            : 'Chat is not configured. Set OPENAI_API_KEY on the server, or enable BYOK by providing your own API key in the prompt.'
      },
      500
    );
  }

  let payload: ChatBody;
  try {
    payload = (await req.json()) as ChatBody;
  } catch (_e) {
    return json({ error: 'Invalid JSON' }, 400);
  }

  const question = String(payload.question || '').trim();
  if (!question) return json({ error: 'Missing question' }, 400);
  if (question.length > 800) return json({ error: 'Question too long (max 800 characters).' }, 400);

  const model = Deno.env.get('OPENAI_MODEL') || 'gpt-4o-mini';
  const maxTokens = getIntEnv('OPENAI_MAX_TOKENS', 256);

  const kb = await loadKb();
  const kbHint = kb.source === 'embedded' || kb.source === 'embedded-fallback' ? 'Website knowledge base' : `Source page: ${kb.source}`;

  const messages = [
    {
      role: 'system',
      content:
        'You are the website assistant for AI (Hackathon) Series. Answer strictly using the provided page content/knowledge. If the answer is not present, say you do not have that info and suggest the contact email. Keep answers concise and factual.'
    },
    {
      role: 'user',
      content: `${kbHint}\n\n${kb.text}\n\nQuestion: ${question}`
    }
  ];

  const resp = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      authorization: `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model,
      messages,
      temperature: 0.2,
      max_tokens: maxTokens
    })
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    return json({ error: `Upstream error (${resp.status}): ${text}` }, 502);
  }

  const data = await resp.json().catch(() => ({} as any));
  const answer = String(data?.choices?.[0]?.message?.content || '').trim();
  return json({ answer });
});
