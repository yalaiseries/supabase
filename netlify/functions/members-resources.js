exports.handler = async (event, context) => {
  async function requireSupabaseUser() {
    const headers = (event && event.headers) || {};
    const auth = headers.authorization || headers.Authorization || '';
    if (!auth || !String(auth).toLowerCase().startsWith('bearer ')) {
      return { ok: false, error: 'Unauthorized. Please sign in.' };
    }

    const supabaseUrl = process.env.SUPABASE_URL;
    const supabaseAnonKey = process.env.SUPABASE_ANON_KEY;
    if (!supabaseUrl || !supabaseAnonKey) {
      return { ok: false, error: 'Server auth is not configured (missing SUPABASE_URL/SUPABASE_ANON_KEY).' };
    }

    try {
      const res = await fetch(`${supabaseUrl.replace(/\/$/, '')}/auth/v1/user`, {
        headers: {
          apikey: supabaseAnonKey,
          authorization: auth
        }
      });
      if (!res.ok) {
        return { ok: false, error: 'Unauthorized. Please sign in.' };
      }
      const user = await res.json().catch(() => null);
      return { ok: true, user };
    } catch (e) {
      return { ok: false, error: 'Auth check failed.' };
    }
  }

  const auth = await requireSupabaseUser();
  if (!auth.ok) {
    return {
      statusCode: 401,
      headers: {
        'content-type': 'application/json; charset=utf-8',
        'cache-control': 'no-store'
      },
      body: JSON.stringify({
        error: auth.error
      })
    };
  }

  // Replace these with your real members-only resources (Drive folders, recordings, templates, etc.)
  const resources = [
    {
      title: 'Members handbook (placeholder)',
      url: 'https://aihackathon.pro/',
      note: 'Replace with a real link (e.g., Google Drive folder with restricted access).'
    },
    {
      title: 'Submission templates (placeholder)',
      url: 'https://aihackathon.pro/members.html',
      note: 'Add links to the 2-page write-up and 10-slide deck templates here.'
    },
    {
      title: 'Session recordings & slides (placeholder)',
      url: 'https://aihackathon.pro/members.html',
      note: 'Add Drive/YouTube unlisted links shared within the community.'
    },
    {
      title: 'Past submissions (2025) — reference spreadsheet',
      url: 'https://docs.google.com/spreadsheets/d/1reC3JTJfoq5IHD0N60uOTidVDLprC9lSDbRjGo_i3jo',
      note: 'Members-only reference link.'
    },
    {
      title: 'Past submissions (2024) — reference document',
      url: 'https://docs.google.com/document/d/15N1HCwghvmifW0rmJCiF28-HQKxT4vu5zwTHwYM4m48',
      note: 'Members-only reference link.'
    },
    {
      title: 'Curated learning paths (placeholder)',
      url: 'https://aihackathon.pro/members.html',
      note: 'Add curated tracks (e.g., Getting started, BIM automation, Agentic AI for practice management).'
    },
    {
      title: 'Past sharing & recordings (placeholder)',
      url: 'https://www.youtube.com/@SIAYAL',
      note: 'If you need this truly private, host behind a private link or Drive permission.'
    }
  ];

  return {
    statusCode: 200,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'no-store'
    },
    body: JSON.stringify({
      resources
    })
  };
};
