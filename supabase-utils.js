/**
 * Shared utilities for AI (Hackathon) Series website
 * Reduces code duplication across HTML pages
 */

(function() {
  'use strict';

  // Shared Supabase configuration
  const SUPABASE_URL = String(window.SUPABASE_URL || '').trim();
  const SUPABASE_ANON_KEY = String(window.SUPABASE_ANON_KEY || '').trim();
  const hasSupabaseConfig = !!SUPABASE_URL && !!SUPABASE_ANON_KEY;

  let supabaseClient = null;

  /**
   * Sleep utility for async waiting
   */
  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  /**
   * Get or create Supabase client with caching
   * @param {Object} options - Additional Supabase client options
   * @returns {Promise<Object|null>} Supabase client or null
   */
  async function getSupabaseClient(options = {}) {
    if (supabaseClient) return supabaseClient;
    if (!hasSupabaseConfig) return null;

    // Wait for loader to complete
    for (let i = 0; i < 40; i++) {
      if (window.__createSupabaseClient) break;
      await sleep(50);
    }

    if (!window.__createSupabaseClient) return null;

    try {
      const defaultOptions = {
        auth: {
          persistSession: true,
          autoRefreshToken: true,
          detectSessionInUrl: true,
          flowType: 'pkce'
        }
      };

      const mergedOptions = { ...defaultOptions, ...options };
      supabaseClient = window.__createSupabaseClient(SUPABASE_URL, SUPABASE_ANON_KEY, mergedOptions);
      return supabaseClient;
    } catch (e) {
      console.error('Failed to create Supabase client:', e);
      supabaseClient = null;
      return null;
    }
  }

  /**
   * HTML escape utility
   */
  function escapeHtml(value) {
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  /**
   * Get site base URL
   */
  function siteBaseUrl() {
    const origin = window.location.origin;
    const path = window.location.pathname;
    const basePath = path.endsWith('/') ? path : path.substring(0, path.lastIndexOf('/') + 1);
    return origin + basePath;
  }

  // Expose utilities globally
  window.__supabaseUtils = {
    SUPABASE_URL,
    SUPABASE_ANON_KEY,
    hasSupabaseConfig,
    getSupabaseClient,
    escapeHtml,
    siteBaseUrl,
    sleep
  };
})();
