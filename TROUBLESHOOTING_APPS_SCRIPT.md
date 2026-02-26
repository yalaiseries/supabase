# Troubleshooting: Google Apps Script → Supabase allowed_members

## Common Issues and Solutions

### Issue 1: RLS (Row Level Security) blocking writes

**Symptom:** Edge Function returns 401/403 or "Could not verify registration" error

**Root Cause:** RLS policies are missing or too restrictive. The Edge Function should use `SERVICE_ROLE_KEY`, which bypasses RLS, but missing secrets or incorrect policies can still cause failures.

**Solution:**
```sql
-- Keep RLS enabled and allow signed-in users to read only their own email row
ALTER TABLE public.allowed_members ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS allowed_members_select_own_email ON public.allowed_members;
CREATE POLICY allowed_members_select_own_email
  ON public.allowed_members
  FOR SELECT
  TO authenticated
  USING (lower(email) = lower(coalesce(auth.jwt() ->> 'email', '')));
```

Then verify your Edge Function secrets include `SERVICE_ROLE_KEY` (or `SUPABASE_SERVICE_ROLE_KEY`).

Or deploy the migration:
```powershell
# Deploy the migration with RLS-safe policies
supabase db push
```

### Issue 2: Missing REGISTRATION_WEBHOOK_SECRET

**Symptom:** Apps Script error: "Missing webhook secret"

**Solution:**
1. In Supabase Dashboard → Project Settings → Edge Functions → Secrets
2. Add secret: `REGISTRATION_WEBHOOK_SECRET` = (generate a long random string)
3. In Google Apps Script → Project Settings → Script properties
4. Add property: `REGISTRATION_WEBHOOK_SECRET` = (same value as above)

Or use the menu: **Supabase → Set webhook secret** in your Google Sheet

### Issue 3: Edge Function not deployed

**Symptom:** 404 error when calling the webhook URL

**Solution:**
```powershell
# Deploy the Edge Functions
supabase functions deploy register-sync
supabase functions deploy register-reconcile
```

Or push to GitHub if you have CI/CD set up (the workflow will auto-deploy).

### Issue 4: SERVICE_ROLE_KEY not configured

**Symptom:** "Server not configured" error in Edge Function

**Solution:**
The Edge Function needs the service role key to write to `allowed_members`:

1. Go to Supabase Dashboard → Project Settings → API
2. Copy the `service_role` key (⚠️ Keep this secret!)
3. Go to Project Settings → Edge Functions → Secrets
4. Add secret: `SERVICE_ROLE_KEY` = (paste the service role key)

Alternatively, set `SUPABASE_SERVICE_ROLE_KEY` in Edge Function secrets.

### Issue 5: Table doesn't exist

**Symptom:** "Database table 'public.allowed_members' was not found"

**Solution:**
Run the schema creation script:
```powershell
# From the workspace root
supabase db reset  # WARNING: This will reset your database!

# Or run the schema manually:
# Copy contents of supabase/sql/schema.sql
# Paste into Supabase Dashboard → SQL Editor → Run
```

## Testing the Setup

### Test 1: Manual webhook test

In Google Apps Script, run the `testWebhook()` function:
1. Open Apps Script editor
2. Select `testWebhook` from the dropdown
3. Click **Run**
4. Check execution log for success message
5. Verify in Supabase: Go to Table Editor → `allowed_members` → Look for test email

### Test 2: Form submission test

1. Submit a test entry in your Google Form
2. Check Apps Script → Executions for successful run
3. Verify the email appears in `allowed_members` table

### Test 3: Edge Function direct test

```powershell
# Test the register-sync endpoint directly
$secret = "YOUR_REGISTRATION_WEBHOOK_SECRET"
$url = "https://xcctqbamimafkkamuwly.functions.supabase.co/register-sync"

$headers = @{
    "x-webhook-secret" = $secret
    "Content-Type" = "application/json"
}

$body = @{
    email = "test@example.com"
    name = "Test User"
    source = "manual_test"
} | ConvertTo-Json

Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body
```

Expected response: `{"ok":true}`

## Viewing Logs

### Apps Script Logs
1. Google Apps Script editor → **Executions**
2. Click on a recent execution to see detailed logs
3. Look for `console.log` messages showing webhook responses

### Supabase Edge Function Logs
1. Supabase Dashboard → Edge Functions
2. Click on `register-sync`
3. View **Invocations** tab for recent calls and errors

### Database Logs
1. Supabase Dashboard → Logs
2. Filter by:
   - Type: Postgres
   - Level: Error
3. Look for permission denied or RLS errors

## Migration Deployment

If you created the migration file, deploy it:

```powershell
# Login to Supabase (if not already)
supabase login

# Link to your project (if not already)
supabase link --project-ref xcctqbamimafkkamuwly

# Push migrations to production
supabase db push
```

## Quick Checklist

- [ ] Table `public.allowed_members` exists
- [ ] RLS is **enabled** on `allowed_members` table
- [ ] Edge Function `register-sync` is deployed
- [ ] Secret `REGISTRATION_WEBHOOK_SECRET` is set in both:
  - [ ] Supabase Edge Function Secrets
  - [ ] Google Apps Script Script Properties
- [ ] Secret `SERVICE_ROLE_KEY` (or `SUPABASE_SERVICE_ROLE_KEY`) is set in Edge Function Secrets
- [ ] Apps Script has trigger configured (`onFormSubmit` or `syncNewRows`)
- [ ] Test webhook function works (run `testWebhook()`)
- [ ] Can manually verify entry appears in `allowed_members` table
