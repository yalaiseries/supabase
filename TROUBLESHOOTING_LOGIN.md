# Login Troubleshooting Guide

## Issue: Cannot sign in with youngpong@gmail.com on Edge/Chrome

### Common Causes & Solutions

#### 1. **Email not in allowlist**
**Check**: Verify the email exists in Supabase `allowed_members` table
```sql
SELECT * FROM public.allowed_members WHERE email = 'youngpong@gmail.com';
```

**Fix**: If not found, add to allowlist:
```sql
INSERT INTO public.allowed_members (email, name, source)
VALUES ('youngpong@gmail.com', 'User Name', 'manual')
ON CONFLICT (email) DO NOTHING;
```

#### 2. **Account not created in Supabase Auth**
**Check**: Go to Supabase Dashboard → Authentication → Users
- Search for `youngpong@gmail.com`

**Fix**: If account doesn't exist:
- User should click **"Email me a link to set/reset my password"** on members.html
- This will:
  - Create the account automatically if email is in allowlist
  - Send password setup email
  - User clicks email link → sets password → can log in

#### 3. **Browser cookies/cache issues**
**Symptoms**: 
- Login works in Incognito/Private mode
- Login fails in normal browser

**Fix**:
1. Clear browser cache and cookies for aihackathon.pro
2. Or use Incognito/Private mode temporarily
3. Try signing out completely, clearing cache, then signing in again

#### 4. **Redirect URL not configured**
**Check**: Supabase Dashboard → Authentication → URL Configuration
- Ensure these are listed in **Redirect URLs**:
  ```
  https://www.aihackathon.pro/members.html
  https://aihackathon.pro/members.html
  https://yalaiseries.github.io/supabase/members.html
  ```

**Fix**: Add missing URLs if needed

#### 5. **Email confirmation pending**
**Symptoms**: Account created but can't log in

**Check**: Supabase Dashboard → Authentication → Users → find user
- Look at "Email Confirmed" status

**Fix**: 
- If not confirmed, either:
  - User checks spam folder for confirmation email
  - Or admin can manually confirm the email in dashboard
  - Or disable email confirmation: Auth → Providers → Email → Uncheck "Confirm email"

#### 6. **Wrong password**
**Symptoms**: "Invalid login credentials" error

**Fix**:
1. Click **"Email me a link to set/reset my password"**
2. Check email (including spam)
3. Click reset link
4. Set new password on members.html
5. Try logging in again

#### 7. **JavaScript/Supabase client not loading**
**Symptoms**: No error message, buttons don't respond

**Check**: Open browser DevTools (F12) → Console tab
- Look for errors like "Supabase is not defined" or network errors

**Fix**:
- Refresh page (Ctrl+Shift+R)
- Check internet connection
- Check if browser extensions (ad blockers) are blocking scripts

#### 8. **Browser-specific issues (Edge/Chrome)**
**Symptoms**: Works in Firefox but not Edge/Chrome

**Potential causes**:
- Third-party cookies blocked
- Enhanced tracking prevention

**Fix**:
1. **Edge**: Settings → Privacy → Tracking prevention → Set to "Balanced"
2. **Chrome**: Settings → Privacy and security → Cookies → "Allow all cookies" (temporarily)
3. Add aihackathon.pro and supabase.co to allowed sites

### Quick Diagnostic Steps

Run this checklist:

1. ✅ Is `youngpong@gmail.com` in `allowed_members` table?
2. ✅ Does the user account exist in Supabase Auth Users?
3. ✅ Is the email confirmed?
4. ✅ Can the user log in using Incognito mode?
5. ✅ Are there any errors in browser console (F12)?
6. ✅ Are redirect URLs configured correctly in Supabase?

### Recommended Solution Path

**For the user (youngpong@gmail.com):**

1. Go to https://www.aihackathon.pro/members.html
2. Enter email: `youngpong@gmail.com`
3. Click **"Email me a link to set/reset my password"**
4. Check email inbox (and spam folder)
5. Click the password reset link in the email
6. On the members page, enter a new password
7. Click "Set password"
8. Now try logging in with email + the new password

**For the admin:**

1. Verify email is in allowlist:
   ```sql
   SELECT * FROM public.allowed_members WHERE email = 'youngpong@gmail.com';
   ```
2. If not found, add it:
   ```sql
   INSERT INTO public.allowed_members (email, name, source)
   VALUES ('youngpong@gmail.com', 'Name Here', 'manual');
   ```
3. Ask user to follow password reset flow above

### Still not working?

Check Supabase logs:
- Dashboard → Logs → Auth logs
- Look for failed login attempts with this email
- Error messages will indicate the specific issue

Common error codes:
- `400`: Invalid request (check email format)
- `401`: Invalid credentials (wrong password)
- `403`: Email not confirmed or not in allowlist
- `422`: Email not found in system
