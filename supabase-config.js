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
window.SUPABASE_ANON_KEY = 'REPLACE_WITH_SUPABASE_ANON_KEY';
// Optional: set this if Supabase Auth CAPTCHA is enabled (Auth -> Bot/Abuse Protection).
// For Cloudflare Turnstile, use the Turnstile site key (public).
window.SUPABASE_CAPTCHA_SITE_KEY = 'REPLACE_WITH_SUPABASE_CAPTCHA_SITE_KEY';

// Guardrail: if key was pasted with an accidental duplicate prefix (e.g. 0x...0x...),
// keep only the last valid-looking segment.
(() => {
	const rawKey = String(window.SUPABASE_CAPTCHA_SITE_KEY || '').trim();
	if (!rawKey) return;
	const secondPrefix = rawKey.indexOf('0x', 2);
	if (secondPrefix > 0) {
		window.SUPABASE_CAPTCHA_SITE_KEY = rawKey.slice(secondPrefix);
	}
})();

// Derived helper for Supabase Edge Functions.
// Example: https://<project-ref>.supabase.co/functions/v1
(() => {
	if (window.SUPABASE_FUNCTIONS_URL) return;
	try {
		const supabaseUrl = String(window.SUPABASE_URL || '').trim();
		if (!supabaseUrl) return;
		const base = supabaseUrl.replace(/\/+$/, '');
		window.SUPABASE_FUNCTIONS_URL = `${base}/functions/v1`;
	} catch {
		// ignore
	}
})();

(() => {
	if (window.SUPABASE_ANON_KEY === 'REPLACE_WITH_SUPABASE_ANON_KEY') {
		console.warn('Supabase anon key is not configured. Set window.SUPABASE_ANON_KEY in supabase-config.js.');
	}
})();
