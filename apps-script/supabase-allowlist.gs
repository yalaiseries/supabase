// Google Sheets → Supabase allowlist sync
//
// Purpose:
// - Read the sheet column "Email address"
// - Call Supabase Edge Function /register-sync
// - Supabase writes/updates public.allowed_members
//
// Data minimization:
// - For membership gating, you only need Email address (and optionally Full Name).
// - This script intentionally does NOT send the entire row / survey answers by default.
//
// Setup:
// 1) In your Supabase project, deploy the Edge Function: register-sync
// 2) In Supabase Dashboard → Project Settings → Functions → Secrets:
//    - REGISTRATION_WEBHOOK_SECRET = <long random secret>
// 3) Set the constants below.
// 4) In Apps Script → Triggers:
//    - If this is a Google Form responses sheet: use onFormSubmit (near real-time)
//    - Otherwise: use syncNewRows (time-driven)

const SUPABASE_FUNCTION_URL = 'https://xcctqbamimafkkamuwly.functions.supabase.co/register-sync';
const WEBHOOK_SECRET = '<REGISTRATION_WEBHOOK_SECRET>';

// Optional: set to a specific tab name. If blank, uses the active sheet.
const SHEET_NAME = '';

// Header names (must match your sheet header row exactly)
const EMAIL_HEADER = 'Email address';
const NAME_HEADER = 'Full Name'; // optional; adjust if your sheet uses a different header

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Supabase')
    .addItem('Sync new rows', 'syncNewRows')
    .addItem('Reset cursor (re-sync from top)', 'resetSyncCursor')
    .addToUi();
}

function getTargetSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if (SHEET_NAME && ss.getSheetByName(SHEET_NAME)) return ss.getSheetByName(SHEET_NAME);
  return ss.getActiveSheet();
}

function normalizeEmail_(value) {
  return String(value || '').trim().toLowerCase();
}

function resetSyncCursor() {
  PropertiesService.getScriptProperties().deleteProperty('LAST_SYNC_ROW');
  SpreadsheetApp.getUi().alert('Cursor cleared. Next sync will start from the header row + 1.');
}

function postToSupabase_(payload) {
  if (!SUPABASE_FUNCTION_URL) throw new Error('Missing SUPABASE_FUNCTION_URL');
  if (!WEBHOOK_SECRET || WEBHOOK_SECRET.indexOf('<') !== -1) throw new Error('Set WEBHOOK_SECRET');

  const resp = UrlFetchApp.fetch(SUPABASE_FUNCTION_URL, {
    method: 'post',
    contentType: 'application/json',
    headers: { 'x-webhook-secret': WEBHOOK_SECRET },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });

  const code = resp.getResponseCode();
  if (code < 200 || code >= 300) {
    throw new Error('register-sync failed: HTTP ' + code + ' ' + resp.getContentText());
  }

  // Helpful for debugging: view in Apps Script → Executions → Logs.
  console.log('register-sync ok: HTTP ' + code);
}

// Debug helper: run this once manually to verify the webhook call works.
// It should create/update a row in public.allowed_members.
function testWebhook() {
  const testEmail = 'test+' + new Date().getTime() + '@example.com';
  postToSupabase_({
    email: testEmail,
    name: 'Webhook Test',
    source: 'apps_script_test',
    testedAt: new Date().toISOString()
  });
  SpreadsheetApp.getUi().alert('Webhook test sent. Check Supabase allowed_members for: ' + testEmail);
}

// Near real-time: only works when the sheet is a Google Form responses sheet.
function onFormSubmit(e) {
  const values = (e && e.namedValues) ? e.namedValues : {};
  const email = (values[EMAIL_HEADER] && values[EMAIL_HEADER][0]) ? values[EMAIL_HEADER][0].trim() : '';
  if (!email) return;

  const name = (values[NAME_HEADER] && values[NAME_HEADER][0]) ? values[NAME_HEADER][0].trim() : '';

  postToSupabase_({
    email: normalizeEmail_(email),
    name: name,
    source: 'google_form',
    submittedAt: new Date().toISOString()
  });

  console.log('onFormSubmit synced email: ' + normalizeEmail_(email));
}

// Polling: works for any sheet.
function syncNewRows() {
  const lock = LockService.getScriptLock();
  lock.waitLock(30 * 1000);
  try {
    const sheet = getTargetSheet_();
    const values = sheet.getDataRange().getValues();
    if (!values || values.length < 2) return;

    const header = values[0].map(String);
    const emailIdx = header.indexOf(EMAIL_HEADER);
    if (emailIdx < 0) throw new Error('Could not find header: ' + EMAIL_HEADER);

    const nameIdx = header.indexOf(NAME_HEADER);

    const props = PropertiesService.getScriptProperties();
    const lastSyncRow = Number(props.getProperty('LAST_SYNC_ROW') || '1');
    const startRow = Math.max(2, lastSyncRow + 1); // 1-based; row 1 is header
    const endRow = values.length;

    let synced = 0;
    for (let rowNum = startRow; rowNum <= endRow; rowNum++) {
      const row = values[rowNum - 1];
      const email = normalizeEmail_(row[emailIdx]);
      if (!email) continue;

      const name = nameIdx >= 0 ? String(row[nameIdx] || '').trim() : '';

      postToSupabase_({
        email,
        name,
        source: 'google_sheet',
        syncedAt: new Date().toISOString()
      });

      synced++;
      props.setProperty('LAST_SYNC_ROW', String(rowNum));
    }

    console.log('syncNewRows complete. Added/updated: ' + synced);
    SpreadsheetApp.getUi().alert('Sync complete. Added/updated: ' + synced);
  } finally {
    lock.releaseLock();
  }
}
