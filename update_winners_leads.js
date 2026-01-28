// Update all team leads with position, company, and LinkedIn profiles

const SUPABASE_URL = 'https://xcctqbamimafkkamuwly.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjY3RxYmFtaW1hZmtrYW11d2x5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzcxOTI5MzUsImV4cCI6MjA1Mjc2ODkzNX0.0BHjwATp6-MvVP4xQPp_mnKV8ZJO6ssPtVeOI5KDjg8';

// Team leads data with position, company, and LinkedIn - mapped by lead name
const teamLeadsData = {
  'Samuel OOI': { position: 'BIM Associate', company: 'Kyoob', linkedin: 'linkedin.com/in/samuelooi96' },
  'Jason LI': { position: 'Senior Associate', company: 'M.Moser', linkedin: 'linkedin.com/in/jasonli-bim' },
  'CHONG Wen Jin': { position: 'Deputy Director (Built Environment Digital Twin)', company: 'BCA', linkedin: 'linkedin.com/in/chong-wen-jin' },
  'HUANG Ranzi': { position: 'Digital Design Leader', company: 'Arup', linkedin: 'linkedin.com/in/ranzihuang' },
  'YANG Fan': { position: 'Co-Founder', company: 'Flexo Sense', linkedin: 'linkedin.com/in/yang-fan-29a979131' },
  'Frederico Ramos': { position: 'Associate - Design Technology', company: 'Aedas', linkedin: 'linkedin.com/in/fredericoramos' },
  'SEAH Kwee Yong': { position: 'Managing Director', company: 'SISV', linkedin: 'linkedin.com/in/kwee-yong-seah-3b135829' },
  'CHAK Lee Meng': { position: 'BIM Director', company: 'CENS', linkedin: 'linkedin.com/in/leemeng' },
  'CHONG Shyh Hao': { position: 'Manager (Digitalisation)', company: 'HDB', linkedin: 'linkedin.com/in/shyhhao-chong' },
  'Atenn NEOH': { position: 'BIM Consultant', company: 'RDC', linkedin: 'linkedin.com/in/atenn-neoh-0a802b83' },
  'Quentin SIM': { position: 'Co-Founder / CTO', company: 'PODIUM.io', linkedin: 'linkedin.com/in/quentin-sim' },
  'TAN Wei Sheng': { position: 'BIM Manager', company: 'ONG&ONG', linkedin: 'linkedin.com/in/tanweisheng' },
  'PONG Woon Wei': { position: 'Manager (Built Environment Digital Twin)', company: 'BCA', linkedin: 'linkedin.com/in/pong-woon-wei-37b33058' },
  'Vignesh KAUSHIK': { position: 'BIM Leader', company: 'Gensler', linkedin: 'linkedin.com/in/vignesh-kaushik' },
  'Gerard TEO': { position: 'Co-Founder', company: 'IDA Tech', linkedin: 'linkedin.com/in/gerardte0' }
};

async function updateWinnersLeads() {
  console.log('Fetching current winners data...\n');
  
  const response = await fetch(`${SUPABASE_URL}/rest/v1/winners_payload?year=in.(2024,2025)&select=year,team,payload&order=year.desc,team`, {
    headers: {
      'apikey': SUPABASE_ANON_KEY,
      'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
    }
  });
  
  const data = await response.json();
  console.log(`Found ${data.length} records\n`);
  
  let updated = 0;
  let skipped = 0;
  
  for (const record of data) {
    const { year, team, payload } = record;
    
    if (!payload.categories) {
      console.log(`⚠️  Skipping ${year} ${team} - no categories found`);
      skipped++;
      continue;
    }
    
    let hasChanges = false;
    const updatedPayload = JSON.parse(JSON.stringify(payload)); // Deep clone
    
    // Iterate through categories and useCases
    for (const category of updatedPayload.categories) {
      if (!category.useCases) continue;
      
      for (const useCase of category.useCases) {
        const currentLead = useCase.people?.lead;
        
        if (!currentLead || typeof currentLead !== 'string') continue;
        
        const leadInfo = teamLeadsData[currentLead];
        if (!leadInfo) {
          console.log(`  ⚠️  No data for lead: ${currentLead}`);
          continue;
        }
        
        // Check if already updated
        if (typeof currentLead === 'object' && currentLead.position) {
          console.log(`  ✓ Already updated: ${currentLead}`);
          continue;
        }
        
        // Update lead to object format
        useCase.people.lead = {
          name: currentLead,
          ...leadInfo
        };
        
        console.log(`  → Updating ${currentLead}: ${leadInfo.position}, ${leadInfo.company}`);
        hasChanges = true;
      }
    }
    
    if (!hasChanges) {
      console.log(`✓ ${year} ${team} - no changes needed\n`);
      skipped++;
      continue;
    }
    
    console.log(`Updating ${year} ${team}...`);
    
    const updateResponse = await fetch(`${SUPABASE_URL}/rest/v1/winners_payload?year=eq.${year}&team=eq.${encodeURIComponent(team)}`, {
      method: 'PATCH',
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
      },
      body: JSON.stringify({ payload: updatedPayload })
    });
    
    if (updateResponse.ok) {
      console.log(`✅ Successfully updated ${year} ${team}\n`);
      updated++;
    } else {
      const error = await updateResponse.text();
      console.error(`❌ Failed to update ${year} ${team}: ${error}\n`);
    }
  }
  
  console.log(`\n=== Summary ===`);
  console.log(`Updated: ${updated}`);
  console.log(`Skipped: ${skipped}`);
  console.log(`Total: ${data.length}`);
}

updateWinnersLeads().catch(console.error);
