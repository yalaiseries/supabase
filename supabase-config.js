// Centralized Supabase config for the static site.
// Fill these in from Supabase Dashboard → Project Settings → API.
//
// Example URL format:
//   https://<project-ref>.supabase.co
//
// IMPORTANT:
// - The anon key is safe to expose in a browser (it is a public key), but still treat it carefully.
// - Access control is enforced by your serverless functions verifying the user's JWT.

window.SUPABASE_URL = 'https://xcctqbamimafkkamuwly.supabase.co';
window.SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjY3RxYmFtaW1hZmtrYW11d2x5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY3MjYyNzQsImV4cCI6MjA4MjMwMjI3NH0.CG0AoRd6nwmEtKKx88l8_srJyZB_sypbcUbL27hA94Y';
// Optional: set this if Supabase Auth CAPTCHA is enabled (Auth -> Bot/Abuse Protection).
// For Cloudflare Turnstile, use the Turnstile site key (public).
window.SUPABASE_CAPTCHA_SITE_KEY = '';

// Derived helper for Supabase Edge Functions.
// Example: https://<project-ref>.functions.supabase.co
(() => {
	if (window.SUPABASE_FUNCTIONS_URL) return;
	try {
		const supabaseUrl = String(window.SUPABASE_URL || '').trim();
		if (!supabaseUrl) return;
		const host = new URL(supabaseUrl).hostname;
		const projectRef = host.split('.')[0];
		if (!projectRef) return;
		window.SUPABASE_FUNCTIONS_URL = `https://${projectRef}.functions.supabase.co`;
	} catch {
		// ignore
	}
})();
