// Update challenge topics for 2025 based on participant survey feedback priority
const SUPABASE_URL = 'https://xcctqbamimafkkamuwly.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjY3RxYmFtaW1hZmtrYW11d2x5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzcxOTI5MzUsImV4cCI6MjA1Mjc2ODkzNX0.0BHjwATp6-MvVP4xQPp_mnKV8ZJO6ssPtVeOI5KDjg8';

const challengeTopics2025 = [
  {
    code: "Design",
    title: "Generative AI for Design Competency and Sustainability",
    description: "Helps create better designs by optimising layouts, improving resource use, and reducing costs through data-driven simulations and analysis, achieving more efficient and sustainable outcomes."
  },
  {
    code: "Checks",
    title: "AI Integrated Design and Regulatory Compliance approach",
    description: "Ensures designs meet project requirements and authority regulations by automating compliance checks, improving teamwork using tools such as algorithmic programming, AI, BIM, cloud computing, and common data environments, resulting in better coordination and increased productivity."
  },
  {
    code: "Fabrication, Construction and O&M",
    title: "AI for Digital Fabrication, Digital Construction and Digital Assets Deliveries",
    description: "Enhances fabrication, construction, and digital assets delivery by using digital tools such as AR/VR, digital twins, modular DfMA/PPVC, and intelligent systems, resulting in optimised fabrication and construction processes and improved project deliveries."
  },
  {
    code: "Manage",
    title: "AI-Enhanced Project and Change Management",
    description: "Simplifies project management by predicting delays, tracking changes, and updating schedules automatically and systematically, leading to improved project outcomes, greater efficiency, and better adaptability."
  },
  {
    code: "Contract",
    title: "Smart Contracts and AI for Contract Administration",
    description: "Streamlines contract management by automating tracking, reducing risks, and ensuring payments and deadlines are met according to contract requirements, resulting in AI-driven, on-time, on-budget, and high-quality project delivery."
  },
  {
    code: "Others",
    title: "Self-defined problem statement with AI-driven solutions and agentic workflows",
    description: "Exploring Proof of Concept development to use AI agentic workflows in solving practical issues"
  }
];

async function updateChallengeTopics() {
  console.log('Updating 2025 challenge topics in Supabase...\n');
  
  const url = `${SUPABASE_URL}/rest/v1/winners_payload?year=eq.2025&select=team,challenge_topics`;
  
  // First, fetch current records to see what exists
  const fetchResponse = await fetch(url, {
    headers: {
      'apikey': SUPABASE_ANON_KEY,
      'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
    }
  });
  
  if (!fetchResponse.ok) {
    console.error(`Failed to fetch: ${fetchResponse.status} ${fetchResponse.statusText}`);
    return;
  }
  
  const records = await fetchResponse.json();
  console.log(`Found ${records.length} records for year 2025\n`);
  
  // Update all 2025 records with the new challenge topics
  for (const record of records) {
    console.log(`Updating team: ${record.team}`);
    
    const updateUrl = `${SUPABASE_URL}/rest/v1/winners_payload?year=eq.2025&team=eq.${encodeURIComponent(record.team)}`;
    
    const updateResponse = await fetch(updateUrl, {
      method: 'PATCH',
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
      },
      body: JSON.stringify({
        challenge_topics: challengeTopics2025
      })
    });
    
    if (updateResponse.ok) {
      console.log(`✅ Successfully updated ${record.team}`);
    } else {
      const error = await updateResponse.text();
      console.error(`❌ Failed to update ${record.team}: ${error}`);
    }
  }
  
  console.log('\n✅ Challenge topics update complete!');
  console.log('\nNew topics order (priority from survey):');
  challengeTopics2025.forEach((topic, idx) => {
    console.log(`${idx + 1}. [${topic.code}] ${topic.title}`);
  });
}

updateChallengeTopics().catch(console.error);
