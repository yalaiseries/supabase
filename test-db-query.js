// Quick test to see what's in the winners_payload table
const SUPABASE_URL = 'https://xcctqbamimafkkamuwly.supabase.co';
const SERVICE_ROLE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjY3RxYmFtaW1hZmtrYW11d2x5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNzEwOTc5NywiZXhwIjoyMDUyNjg1Nzk3fQ.X7WCEMlqEPD-o6ZCH3c4lP7wdUn2Sf4fGz1hK9ixgWE';

const url = new URL(`${SUPABASE_URL}/rest/v1/winners_payload`);
url.searchParams.set('select', 'year,payload');
url.searchParams.set('order', 'year.desc');

fetch(url.toString(), {
  headers: {
    apikey: SERVICE_ROLE_KEY,
    authorization: `Bearer ${SERVICE_ROLE_KEY}`
  }
})
  .then(resp => {
    console.log('Status:', resp.status);
    return resp.json();
  })
  .then(data => {
    console.log('Rows:', data.length);
    data.forEach(row => {
      console.log('\n--- Year:', row.year);
      console.log('Payload type:', typeof row.payload);
      console.log('Payload is array:', Array.isArray(row.payload));
      console.log('Payload preview:', JSON.stringify(row.payload).substring(0, 200));
      if (row.payload && typeof row.payload === 'object') {
        console.log('Has year field:', 'year' in row.payload);
        console.log('Has categories field:', 'categories' in row.payload);
        if ('categories' in row.payload) {
          console.log('Categories count:', Array.isArray(row.payload.categories) ? row.payload.categories.length : 'not an array');
        }
      }
    });
  })
  .catch(err => console.error('Error:', err));
