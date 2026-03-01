# URGENT: Password Reset Not Working - Fix Required

## Problem
Public users cannot reset passwords or receive login emails on https://www.aihackathon.pro/members.html

## Root Cause
Supabase Auth email delivery requires proper configuration. Without it, NO emails are sent.

## IMMEDIATE FIX REQUIRED (Choose One)

### Option 1: Configure SMTP in Supabase (RECOMMENDED - 5 minutes)

**This enables reliable email delivery**

1. Go to: https://supabase.com/dashboard/project/xcctqbamimafkkamuwly/settings/auth

2. Scroll to **SMTP Settings** section

3. Enable "Enable Custom SMTP" toggle

4. Configure with one of these providers:

   **Gmail (Quickest for testing):**
   ```
   Host: smtp.gmail.com
   Port: 587
   Username: your-gmail@gmail.com
   Password: [App Password - NOT your Gmail password]
   Sender email: your-gmail@gmail.com
   Sender name: AI Hackathon Series
   ```
   
   **SendGrid (Recommended for production):**
   ```
   Host: smtp.sendgrid.net
   Port: 587
   Username: apikey
   Password: [Your SendGrid API Key]
   Sender email: noreply@aihackathon.pro
   Sender name: AI Hackathon Series
   ```

5. Click "Save"

6. Test by clicking "Send test email"

### Option 2: Whitelist Redirect URLs (REQUIRED REGARDLESS)

1. Go to: https://supabase.com/dashboard/project/xcctqbamimafkkamuwly/auth/url-configuration

2. Under **Redirect URLs**, add:
   ```
   https://aihackathon.pro/members.html
   https://www.aihackathon.pro/members.html
   http://localhost:3000/members.html
   ```

3. Click "Save"

### Option 3: Check Email Templates are Enabled

1. Go to: https://supabase.com/dashboard/project/xcctqbamimafkkamuwly/auth/templates

2. Verify these are enabled:
   - ✅ Confirm signup
   - ✅ Magic Link
   - ✅ Change Email Address
   - ✅ Reset Password

### Option 4: Set Edge Function Environment Variable

1. Go to: https://supabase.com/dashboard/project/xcctqbamimafkkamuwly/settings/functions

2. Add secret:
   ```
   Key: INVITE_REDIRECT_URL
   Value: https://aihackathon.pro/members.html
   ```

3. Redeploy the `request-access` function

## Verification Steps

After configuration:

1. Go to https://www.aihackathon.pro/members.html
2. Enter email: youngpong@gmail.com
3. Click "Email me a link to set/reset my password"
4. Check email inbox (and spam folder)
5. Should receive email within 1-2 minutes

## Debug Logs

**Check if emails are being attempted:**
- Auth Logs: https://supabase.com/dashboard/project/xcctqbamimafkkamuwly/logs/auth-logs
- Look for "password_recovery" events

**Check edge function:**
- Function Logs: https://supabase.com/dashboard/project/xcctqbamimafkkamuwly/logs/edge-functions
- Filter: request-access

## Temporary Workaround (While Fixing Email)

**Manually create user accounts:**
1. Go to: https://supabase.com/dashboard/project/xcctqbamimafkkamuwly/auth/users
2. Click "Invite user"
3. Enter email address
4. User will receive invite email (if SMTP configured) OR you can manually set password

## Status Check

- [ ] SMTP configured and tested
- [ ] Redirect URLs whitelisted  
- [ ] Email templates enabled
- [ ] INVITE_REDIRECT_URL environment variable set
- [ ] Test email sent and received successfully

## Contact

If still not working after following all steps, check:
1. Spam/junk folder
2. Supabase Auth logs for error messages
3. Try with a different email provider (not Gmail)
