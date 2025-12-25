// Centralized Supabase config for the static site.
// Fill these in from Supabase Dashboard → Project Settings → API.
//
// Example URL format:
//   https://<project-ref>.supabase.co
//
// IMPORTANT:
// - The anon key is safe to expose in a browser (it is a public key), but still treat it carefully.
// - Access control is enforced by your serverless functions verifying the user's JWT.

window.SUPABASE_URL = 'https://mckgmiofqxuwfwlszrkc.supabase.co';
window.SUPABASE_ANON_KEY = 'sb_publishable_MTy4H7a5lmVCVs6c2oMQSw_zAzgNzrm';

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
