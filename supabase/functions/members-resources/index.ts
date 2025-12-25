import { serve } from 'https://deno.land/std@0.224.0/http/server.ts';
import { corsHeaders } from '../_shared/cors.ts';
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

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  const membership = await requireRegisteredMember(req);
  if (!membership.ok) return json(membership.body, membership.status);

  // Replace these with your real members-only resources.
  const resources = [
    {
      title: 'Members handbook (placeholder)',
      url: 'https://yalaiseries.github.io/supabase/',
      note: 'Replace with a real link (e.g., Google Drive folder with restricted access).'
    },
    {
      title: 'Submission templates (placeholder)',
      url: 'https://yalaiseries.github.io/supabase/members.html',
      note: 'Add links to the 2-page write-up and 10-slide deck templates here.'
    },
    {
      title: 'Session recordings & slides (placeholder)',
      url: 'https://yalaiseries.github.io/supabase/members.html',
      note: 'Add Drive/YouTube unlisted links shared within the community.'
    },
    {
      title: 'Curated learning paths (placeholder)',
      url: 'https://yalaiseries.github.io/supabase/members.html',
      note: 'Add curated tracks (e.g., Getting started, BIM automation, Agentic AI for practice management).'
    }
  ];

  return json({ resources });
});
