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
const SUPABASE_RECONCILE_URL = 'https://xcctqbamimafkkamuwly.functions.supabase.co/register-reconcile';
const WEBHOOK_SECRET = '<REGISTRATION_WEBHOOK_SECRET>';

// Optional: set to a specific tab name. If blank, uses the active sheet.
const SHEET_NAME = '';

// Header names (most common variants).
// If your sheet uses a different label, add it here.
const EMAIL_HEADERS = ['Email address', 'Email Address', 'Email', 'E-mail', 'E-mail address'];
const NAME_HEADERS = ['Full Name', 'Name', 'Full name'];

function normalizeHeader_(value) {
  return String(value || '')
    .trim()
    .toLowerCase()
    .replace(/\s+/g, ' ');
}

function pickNamedValue_(namedValues, candidates) {
  if (!namedValues) return '';
  const keys = Object.keys(namedValues);
  for (var i = 0; i < candidates.length; i++) {
    const want = normalizeHeader_(candidates[i]);
    for (var k = 0; k < keys.length; k++) {
      const key = keys[k];
      if (normalizeHeader_(key) !== want) continue;
      const arr = namedValues[key];
      return (arr && arr[0]) ? String(arr[0]).trim() : '';
    }
  }
  return '';
}

function findHeaderIndex_(headerRow, candidates) {
  const normalized = headerRow.map(normalizeHeader_);
  for (var i = 0; i < candidates.length; i++) {
    const want = normalizeHeader_(candidates[i]);
    const idx = normalized.indexOf(want);
    if (idx >= 0) return idx;
  }
  return -1;
}

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Supabase')
    .addItem('Sync new rows', 'syncNewRows')
    .addItem('Sync ALL rows (force re-sync)', 'syncAllRows')
    .addItem('Mirror ALL rows (reconcile deletes)', 'mirrorAllRows')
    .addItem('Reset cursor (re-sync from top)', 'resetSyncCursor')
    .addToUi();
}

function getTargetSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if (SHEET_NAME) {
    const found = ss.getSheetByName(SHEET_NAME);
    if (!found) throw new Error('SHEET_NAME not found: ' + SHEET_NAME);
    return found;
  }
  return ss.getActiveSheet();
}

function normalizeEmail_(value) {
  return String(value || '').trim().toLowerCase();
}

function resetSyncCursor() {
  PropertiesService.getScriptProperties().deleteProperty('LAST_SYNC_ROW');
  SpreadsheetApp.getUi().alert('Cursor cleared. Next sync will start from the header row + 1.');
}

function postJson_(url, payload) {
  if (!url) throw new Error('Missing URL');
  if (!WEBHOOK_SECRET || WEBHOOK_SECRET.indexOf('<') !== -1) throw new Error('Set WEBHOOK_SECRET');

  const resp = UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    headers: { 'x-webhook-secret': WEBHOOK_SECRET },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });

  const code = resp.getResponseCode();
  const bodyText = resp.getContentText();
  if (code < 200 || code >= 300) {
    throw new Error('Supabase webhook failed: HTTP ' + code + ' ' + bodyText);
  }

  // Helpful for debugging: view in Apps Script → Executions → Logs.
  console.log('Supabase webhook ok: HTTP ' + code + ' ' + bodyText);
  return { code: code, bodyText: bodyText };
}

function postToSupabase_(payload) {
  if (!SUPABASE_FUNCTION_URL) throw new Error('Missing SUPABASE_FUNCTION_URL');
  return postJson_(SUPABASE_FUNCTION_URL, payload);
}

// Debug helper: run this once manually to verify the webhook call works.
// It should create/update a row in public.allowed_members.
function testWebhook() {
  const testEmail = 'test+' + new Date().getTime() + '@example.com';
  console.log('testWebhook sending email=' + testEmail + ' url=' + SUPABASE_FUNCTION_URL);
  postToSupabase_({
    email: testEmail,
    name: 'Webhook Test',
    source: 'apps_script_test',
    testedAt: new Date().toISOString()
  });
  SpreadsheetApp.getUi().alert('Webhook test sent. Check Supabase allowed_members for: ' + testEmail);
}

// Full mirror helper: sends the entire sheet to /register-reconcile.
// This is what makes "deletes" work (if you remove a row from the Sheet, it will be removed from allowed_members).
// Recommended trigger: time-based (e.g., every 1–5 minutes), plus manual runs.
function mirrorAllRows() {
  const lock = LockService.getScriptLock();
  lock.waitLock(30 * 1000);
  try {
    if (!SUPABASE_RECONCILE_URL) throw new Error('Missing SUPABASE_RECONCILE_URL');

    const sheet = getTargetSheet_();
    const values = sheet.getDataRange().getValues();
    if (!values || values.length < 2) {
      console.log('mirrorAllRows: no data rows. sheet=' + sheet.getName() + ' rows=' + (values ? values.length : 0));
      SpreadsheetApp.getUi().alert('No data rows found. Mirror will not delete anything unless you explicitly allow empty deletes.');
      return;
    }

    const header = values[0].map(String);
    const emailIdx = findHeaderIndex_(header, EMAIL_HEADERS);
    if (emailIdx < 0) throw new Error('Could not find an email header. Expected one of: ' + EMAIL_HEADERS.join(', '));

    const nameIdx = findHeaderIndex_(header, NAME_HEADERS);
    console.log('mirrorAllRows sheet=' + sheet.getName() + ' rows=' + values.length + ' emailIdx=' + emailIdx + ' nameIdx=' + nameIdx);

    const rowByEmail = {};
    for (var rowNum = 2; rowNum <= values.length; rowNum++) {
      const row = values[rowNum - 1];
      const email = normalizeEmail_(row[emailIdx]);
      if (!email) continue;
      const name = nameIdx >= 0 ? String(row[nameIdx] || '').trim() : '';
      rowByEmail[email] = {
        email: email,
        name: name,
        source: 'google_sheet',
        metadata: { sheet: sheet.getName(), row: rowNum }
      };
    }

    const rows = Object.keys(rowByEmail).map(function (k) { return rowByEmail[k]; });

    console.log('mirrorAllRows posting rows=' + rows.length + ' url=' + SUPABASE_RECONCILE_URL);
    const resp = postJson_(SUPABASE_RECONCILE_URL, {
      rows: rows,
      source: 'google_sheet',
      reconciledAt: new Date().toISOString(),
      // Safety: do NOT allow empty wipe by default.
      allowEmptyDelete: false
    });

    SpreadsheetApp.getUi().alert('Mirror complete. Response: ' + resp.bodyText);
  } finally {
    lock.releaseLock();
  }
}

// Full re-sync helper: pushes ALL rows (except header) every time.
// Use this after you recreate the table or if the cursor got out of sync.
function syncAllRows() {
  resetSyncCursor();
  const lock = LockService.getScriptLock();
  lock.waitLock(30 * 1000);
  try {
    const sheet = getTargetSheet_();
    const values = sheet.getDataRange().getValues();
    if (!values || values.length < 2) {
      console.log('syncAllRows: no data rows. sheet=' + sheet.getName() + ' rows=' + (values ? values.length : 0));
      SpreadsheetApp.getUi().alert('No data rows found.');
      return;
    }

    const header = values[0].map(String);
    const emailIdx = findHeaderIndex_(header, EMAIL_HEADERS);
    if (emailIdx < 0) throw new Error('Could not find an email header. Expected one of: ' + EMAIL_HEADERS.join(', '));

    const nameIdx = findHeaderIndex_(header, NAME_HEADERS);
    console.log('syncAllRows sheet=' + sheet.getName() + ' rows=' + values.length + ' emailIdx=' + emailIdx + ' nameIdx=' + nameIdx);

    let synced = 0;
    for (var rowNum = 2; rowNum <= values.length; rowNum++) {
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
    }

    console.log('syncAllRows complete. Added/updated: ' + synced);
    SpreadsheetApp.getUi().alert('Full sync complete. Added/updated: ' + synced);
  } finally {
    lock.releaseLock();
  }
}

// Near real-time: only works when the sheet is a Google Form responses sheet.
function onFormSubmit(e) {
  const values = (e && e.namedValues) ? e.namedValues : {};
  const email = pickNamedValue_(values, EMAIL_HEADERS);
  if (!email) return;

  const name = pickNamedValue_(values, NAME_HEADERS);

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
    if (!values || values.length < 2) {
      console.log('syncNewRows: no data rows. sheet=' + sheet.getName() + ' rows=' + (values ? values.length : 0));
      SpreadsheetApp.getUi().alert('No data rows found in sheet tab: ' + sheet.getName());
      return;
    }

    const header = values[0].map(String);
    const emailIdx = findHeaderIndex_(header, EMAIL_HEADERS);
    if (emailIdx < 0) throw new Error('Could not find an email header. Expected one of: ' + EMAIL_HEADERS.join(', '));

    const nameIdx = findHeaderIndex_(header, NAME_HEADERS);

    console.log('syncNewRows sheet=' + sheet.getName() + ' rows=' + values.length + ' emailIdx=' + emailIdx + ' nameIdx=' + nameIdx);

    const props = PropertiesService.getScriptProperties();
    const lastSyncRow = Number(props.getProperty('LAST_SYNC_ROW') || '1');
    const startRow = Math.max(2, lastSyncRow + 1); // 1-based; row 1 is header
    const endRow = values.length;

    if (startRow > endRow) {
      console.log('syncNewRows: no new rows. LAST_SYNC_ROW=' + lastSyncRow + ' endRow=' + endRow);
      SpreadsheetApp.getUi().alert('No new rows to sync. If you recreated the table, run syncAllRows() or use Reset cursor then Sync new rows.');
      return;
    }

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
