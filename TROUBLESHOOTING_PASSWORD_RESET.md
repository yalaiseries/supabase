# Troubleshooting Password Reset Email Issues

## Problem
Email `youngpong@gmail.com` is in the allowlist but not receiving password reset emails when clicking "Email me a link to set/reset my password" button.

## Common Causes

### 1. Supabase Auth Email Not Configured
**Check in Supabase Dashboard:**
- Go to: https://supabase.com/dashboard/project/xcctqbamimafkkamuwly/auth/templates
- Verify "Confirm signup" and "Reset password" email templates are enabled
- Check if emails are being sent from Supabase (check "Auth Logs")

### 2. SMTP Settings Required
Supabase's default email service has rate limits and may not deliver to all addresses.

**Solution:** Configure custom SMTP
- Go to: https://supabase.com/dashboard/project/xcctqbamimafkkamuwly/settings/auth
- Scroll to "SMTP Settings"
- Configure your own SMTP provider (SendGrid, AWS SES, etc.)

### 3. Redirect URL Not Whitelisted
The password reset email contains a redirect back to your site.

**Check:**
- Go to: https://supabase.com/dashboard/project/xcctqbamimafkkamuwly/auth/url-configuration
- Ensure these URLs are in "Redirect URLs" list:
  - `https://aihackathon.pro/members.html`
  - `https://www.aihackathon.pro/members.html`

### 4. Email in Spam/Junk Folder
- Check spam folder in Gmail
- Supabase emails might be marked as spam if SMTP not configured

### 5. Rate Limiting
Supabase has email rate limits. If you clicked multiple times, wait 60 seconds and try again.

## Alternative: Manually Reset Password via Supabase Dashboard

**For existing users:**
1. Go to: https://supabase.com/dashboard/project/xcctqbamimafkkamuwly/auth/users
2. Find user with email `youngpong@gmail.com`
3. Click the user
4. Click "Send password recovery email" OR "Reset password" 
5. You can manually set a new password from the dashboard

## Debugging Steps

1. **Check Auth Logs:**
   - https://supabase.com/dashboard/project/xcctqbamimafkkamuwly/logs/auth-logs
   - Look for password reset attempts and any errors

2. **Check Edge Function Logs:**
   - https://supabase.com/dashboard/project/xcctqbamimafkkamuwly/logs/edge-functions
   - Filter for `request-access` function
   - Check if invite was sent successfully

3. **Test with Different Email:**
   - Try a different email address to isolate if issue is specific to Gmail

## Environment Variables to Check

The edge function needs:
- `INVITE_REDIRECT_URL` - Should be set to `https://aihackathon.pro/members.html`

You can set this in:
https://supabase.com/dashboard/project/xcctqbamimafkkamuwly/settings/functions
