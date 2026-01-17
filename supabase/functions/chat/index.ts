import { serve } from 'https://deno.land/std@0.224.0/http/server.ts';
import { corsHeaders } from '../_shared/cors.ts';
import { websiteKb } from '../_shared/kb.ts';
import { requireRegisteredMember } from '../_shared/membership.ts';

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

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  if (req.method !== 'POST') {
    return json({ error: 'Method not allowed' }, 405);
  }

  const member = await requireRegisteredMember(req);
  if (!member.ok) {
    return json(member.body, member.status);
  }

  const apiKey = Deno.env.get('OPENAI_API_KEY') || '';
  if (!apiKey) {
    return json(
      {
        error:
          'Missing OPENAI_API_KEY. Set it with `supabase secrets set OPENAI_API_KEY=...` and redeploy the function.'
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

  const model = Deno.env.get('OPENAI_MODEL') || 'gpt-4o-mini';

  const messages = [
    {
      role: 'system',
      content:
        'You are the website assistant for AI (Hackathon) Series — Agentic AI Learning Hub (2026). Answer using the provided website knowledge. If the answer is not available, say you do not have that info and suggest the contact email. Keep answers concise and factual.'
    },
    {
      role: 'user',
      content: `Website knowledge:\n${websiteKb}\n\nQuestion: ${question}`
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
      temperature: 0.2
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
