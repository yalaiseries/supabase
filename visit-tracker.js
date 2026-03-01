(function () {
  'use strict';

  const functionsBase = String(window.SUPABASE_FUNCTIONS_URL || '').trim();
  const anonKey = String(window.SUPABASE_ANON_KEY || '').trim();
  const supabaseUrl = String(window.SUPABASE_URL || '').trim();

  if (!functionsBase || !anonKey) return;

  const sentFlag = '__visitTracked';
  if (window[sentFlag]) return;
  window[sentFlag] = true;

  const sessionStorageKey = 'aih_visit_session_id';

  function getOrCreateSessionId() {
    try {
      const existing = sessionStorage.getItem(sessionStorageKey);
      if (existing) return existing;
      const created = `s_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 10)}`;
      sessionStorage.setItem(sessionStorageKey, created);
      return created;
    } catch {
      return `s_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 10)}`;
    }
  }

  function buildPath() {
    const pathname = String(window.location.pathname || '/').trim() || '/';
    return pathname.startsWith('/') ? pathname : `/${pathname}`;
  }

  function buildClientMetadata() {
    const metadata = {
      href: String(window.location.href || '').slice(0, 1200)
    };

    try {
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      if (timezone) metadata.timezone = String(timezone).slice(0, 120);
    } catch {
      // ignore
    }

    const language = String((navigator && navigator.language) || '').trim();
    if (language) metadata.language = language.slice(0, 40);

    return metadata;
  }

  async function resolveAccessToken() {
    try {
      if (window.__supabaseUtils && typeof window.__supabaseUtils.getSupabaseClient === 'function') {
        const client = await window.__supabaseUtils.getSupabaseClient();
        if (client && client.auth && typeof client.auth.getSession === 'function') {
          const { data } = await client.auth.getSession();
          return String(data && data.session && data.session.access_token ? data.session.access_token : '').trim();
        }
      }

      if (window.__createSupabaseClient && supabaseUrl && anonKey) {
        if (!window.__visitTrackerClient) {
          window.__visitTrackerClient = window.__createSupabaseClient(supabaseUrl, anonKey, {
            auth: {
              persistSession: true,
              autoRefreshToken: false,
              detectSessionInUrl: false
            }
          });
        }

        const client = window.__visitTrackerClient;
        if (client && client.auth && typeof client.auth.getSession === 'function') {
          const { data } = await client.auth.getSession();
          return String(data && data.session && data.session.access_token ? data.session.access_token : '').trim();
        }
      }
    } catch {
      return '';
    }

    return '';
  }

  async function sendVisit() {
    const accessToken = await resolveAccessToken();

    const payload = {
      path: buildPath(),
      page_title: String(document.title || '').trim().slice(0, 200),
      referrer: String(document.referrer || '').trim().slice(0, 1000),
      session_id: getOrCreateSessionId(),
      metadata: buildClientMetadata(),
      access_token: accessToken || undefined
    };

    fetch(`${functionsBase}/page-visit-track`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        apikey: anonKey
      },
      body: JSON.stringify(payload),
      keepalive: true
    }).catch(() => {
      // ignore tracking errors
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      sendVisit();
    }, { once: true });
  } else {
    sendVisit();
  }
})();
