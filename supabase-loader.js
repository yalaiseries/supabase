/**
 * Shared Supabase client loader for AI (Hackathon) Series
 * Attempts to load Supabase JS client from multiple CDNs with smart caching
 */

(async function initSupabaseLoader() {
  const CDN_URLS = [
    'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm',
    'https://esm.sh/@supabase/supabase-js@2',
    'https://unpkg.com/@supabase/supabase-js@2/dist/esm/supabase.js'
  ];

  const CACHE_KEY = 'supabase_cdn_preference';

  /**
   * Try to load Supabase from a specific CDN URL
   */
  async function tryLoadFromCDN(url) {
    try {
      const mod = await import(url);
      if (mod && typeof mod.createClient === 'function') {
        return { createClient: mod.createClient, url, success: true };
      }
      return { success: false, error: `Loaded ${url} but createClient was not found.` };
    } catch (e) {
      return { success: false, error: String(e && e.message ? e.message : e) };
    }
  }

  /**
   * Load Supabase client with smart CDN fallback
   */
  async function loadSupabase() {
    // Try cached CDN first if available
    let preferredCDN = null;
    try {
      preferredCDN = localStorage.getItem(CACHE_KEY);
    } catch {}

    if (preferredCDN && CDN_URLS.includes(preferredCDN)) {
      const result = await tryLoadFromCDN(preferredCDN);
      if (result.success) {
        return result;
      }
    }

    // Try all CDNs in parallel for faster failover
    const results = await Promise.allSettled(
      CDN_URLS.map(url => tryLoadFromCDN(url))
    );

    // Find first successful load
    for (const result of results) {
      if (result.status === 'fulfilled' && result.value.success) {
        const { createClient, url } = result.value;
        // Cache the successful CDN for next time
        try {
          localStorage.setItem(CACHE_KEY, url);
        } catch {}
        return { createClient, url };
      }
    }

    // All failed - collect errors
    const errors = results
      .filter(r => r.status === 'fulfilled' && !r.value.success)
      .map(r => r.value.error)
      .join('; ');

    return {
      createClient: null,
      error: errors || 'Failed to load Supabase client from all CDNs.'
    };
  }

  // Load and expose to window
  const loaded = await loadSupabase();
  if (loaded.createClient) {
    window.__createSupabaseClient = loaded.createClient;
    window.__supabaseClientSource = loaded.url;
    window.__supabaseLoadError = '';
  } else {
    window.__createSupabaseClient = null;
    window.__supabaseClientSource = '';
    window.__supabaseLoadError = loaded.error || 'Failed to load Supabase client.';
  }
})();
