exports.handler = async (event, context) => {
  async function requireSupabaseUser() {
    const headers = (event && event.headers) || {};
    const auth = headers.authorization || headers.Authorization || '';
    if (!auth || !String(auth).toLowerCase().startsWith('bearer ')) {
      return { ok: false, error: 'Unauthorized. Please sign in.' };
    }

    const supabaseUrl = process.env.SUPABASE_URL;
    const supabaseAnonKey = process.env.SUPABASE_ANON_KEY;
    if (!supabaseUrl || !supabaseAnonKey) {
      return { ok: false, error: 'Server auth is not configured (missing SUPABASE_URL/SUPABASE_ANON_KEY).' };
    }

    try {
      const res = await fetch(`${supabaseUrl.replace(/\/$/, '')}/auth/v1/user`, {
        headers: {
          apikey: supabaseAnonKey,
          authorization: auth
        }
      });
      if (!res.ok) {
        return { ok: false, error: 'Unauthorized. Please sign in.' };
      }
      const user = await res.json().catch(() => null);
      return { ok: true, user };
    } catch (e) {
      return { ok: false, error: 'Auth check failed.' };
    }
  }

  const auth = await requireSupabaseUser();
  if (!auth.ok) {
    return {
      statusCode: 401,
      headers: {
        'content-type': 'application/json; charset=utf-8',
        'cache-control': 'no-store'
      },
      body: JSON.stringify({
        error: auth.error
      })
    };
  }

  const fs = require('fs');
  const path = require('path');

  function parseCsv(text) {
    const rows = [];
    let row = [];
    let field = '';
    let inQuotes = false;

    for (let i = 0; i < text.length; i++) {
      const ch = text[i];

      if (inQuotes) {
        if (ch === '"') {
          const next = text[i + 1];
          if (next === '"') {
            field += '"';
            i++;
          } else {
            inQuotes = false;
          }
        } else {
          field += ch;
        }
        continue;
      }

      if (ch === '"') {
        inQuotes = true;
        continue;
      }

      if (ch === ',') {
        row.push(field);
        field = '';
        continue;
      }

      if (ch === '\n') {
        row.push(field);
        field = '';

        // Ignore completely empty trailing row
        if (row.length > 1 || (row.length === 1 && row[0].trim() !== '')) {
          rows.push(row);
        }
        row = [];
        continue;
      }

      if (ch === '\r') {
        continue;
      }

      field += ch;
    }

    if (field.length || row.length) {
      row.push(field);
      if (row.length > 1 || (row.length === 1 && row[0].trim() !== '')) {
        rows.push(row);
      }
    }

    return rows;
  }

  function compactLines(value) {
    return String(value || '')
      .replace(/\r/g, '')
      .split('\n')
      .map((s) => s.trim())
      .filter(Boolean)
      .join(' / ');
  }

  function normalizeKey(value) {
    return String(value || '')
      .trim()
      .toLowerCase()
      .replace(/\s+/g, ' ');
  }

  function isLikelyUrl(value) {
    const v = String(value || '').trim();
    return v.startsWith('http://') || v.startsWith('https://');
  }

  function toUrl(value) {
    const v = String(value || '').trim();
    if (!v) return '';
    if (v.startsWith('http://') || v.startsWith('https://')) return v;
    if (v.startsWith('www.')) return `https://${v}`;
    if (v.includes('.') && !v.includes(' ')) return `https://${v}`;
    return '';
  }

  function prizeToAward(value) {
    const v = String(value || '').trim().toLowerCase();
    if (v === '1st') return '1st Prize';
    if (v === '2nd') return '2nd Prize';
    if (v === '3rd') return '3rd Prize';
    if (!v) return '';
    return value;
  }

  function buildFromTransposedCsv({ csvText, year, defaultCategory }) {
    const rows = parseCsv(csvText);
    if (!rows.length) return null;

    // First column: field name. Remaining columns: use cases.
    const headers = rows[0] || [];
    const projectCount = Math.max(0, headers.length - 1);
    if (!projectCount) return null;

    const fields = new Map();
    for (const r of rows) {
      const key = normalizeKey(r[0]);
      if (!key) continue;
      fields.set(key, r.slice(1));
    }

    const get = (name) => fields.get(normalizeKey(name)) || [];

    const topics = get('Topic');
    const reps = get('Representative Speaker');
    const designations = get('Designation').length ? get('Designation') : get('Rep Designation');
    const linkedins = get('Linkedin');
    const leads = get('Lead');
    const coleads = get('Co-lead');
    const members = get('Team Members').length ? get('Team Members') : get('Team Member');
    const slides = get('Slide');
    const otherLinks = get('Other Links');
    const abouts = get('About');
    const prizes = get('Prize');
    const summaries =
      get('One sentence summary of What, Why, Benefits & How') ||
      get('One sentence summary of what, why, benefits & how') ||
      get('One sentence summary');
    const categoriesRow = get('Use case category').length
      ? get('Use case category')
      : get('Category');

    const categories = new Map();

    for (let i = 0; i < projectCount; i++) {
      const title = compactLines(topics[i]);
      if (!title) continue;

      const rep = compactLines(reps[i]);
      const designation = compactLines(designations[i]);
      const lead = compactLines(leads[i]);
      const colead = compactLines(coleads[i]);
      const teamMembers = compactLines(members[i]);

      const teamBits = [];
      if (rep || designation) teamBits.push([rep, designation].filter(Boolean).join(' — '));
      if (lead && lead.toLowerCase() !== 'na') teamBits.push(`Lead: ${lead}`);
      if (colead && colead.toLowerCase() !== 'na') teamBits.push(`Co-lead: ${colead}`);
      if (teamMembers && teamMembers.toLowerCase() !== 'na') teamBits.push(`Team: ${teamMembers}`);
      const team = teamBits.join(' · ');

      const award = prizeToAward(prizes[i]);
      const summary = compactLines(summaries[i]) || compactLines(abouts[i]);

      const links = [];
      const slideUrl = toUrl(slides[i]);
      if (slideUrl) links.push({ label: 'Slides', url: slideUrl });

      const otherUrl = toUrl(otherLinks[i]);
      if (otherUrl) links.push({ label: 'Other link', url: otherUrl });

      const linkedinUrl = toUrl(linkedins[i]);
      if (linkedinUrl) links.push({ label: 'LinkedIn', url: linkedinUrl });

      const category = compactLines(categoriesRow[i]) || defaultCategory;
      const current = categories.get(category) || [];
      current.push({ title, team, award, summary, links });
      categories.set(category, current);
    }

    const categoriesOut = Array.from(categories.entries())
      .sort((a, b) => String(a[0]).localeCompare(String(b[0])))
      .map(([category, useCases]) => ({ category, useCases }));

    return {
      year,
      categories: categoriesOut
    };
  }

  function mergeYearEntries(yearEntries) {
    const byYear = new Map();
    for (const entry of yearEntries) {
      if (!entry || !Number.isFinite(Number(entry.year))) continue;
      const year = Number(entry.year);
      const existing = byYear.get(year);
      if (!existing) {
        byYear.set(year, { year, categories: Array.isArray(entry.categories) ? entry.categories : [] });
        continue;
      }
      const cats = Array.isArray(entry.categories) ? entry.categories : [];
      existing.categories = existing.categories.concat(cats);
    }

    // De-duplicate categories by name (merge useCases)
    for (const [year, entry] of byYear.entries()) {
      const catMap = new Map();
      for (const cat of entry.categories) {
        const name = String(cat && cat.category ? cat.category : 'Uncategorized');
        const useCases = Array.isArray(cat && cat.useCases) ? cat.useCases : [];
        const existing = catMap.get(name);
        if (!existing) {
          catMap.set(name, { category: name, useCases: useCases.slice() });
        } else {
          existing.useCases = existing.useCases.concat(useCases);
        }
      }
      entry.categories = Array.from(catMap.values()).sort((a, b) => String(a.category).localeCompare(String(b.category)));
      byYear.set(year, entry);
    }

    return Array.from(byYear.values()).sort((a, b) => Number(b.year) - Number(a.year));
  }

  function safeParseJson(text) {
    try {
      const value = JSON.parse(text);
      return value;
    } catch (e) {
      return null;
    }
  }

  function loadYearEntriesFromJsonFile(filename) {
    try {
      const p = path.join(__dirname, filename);
      if (!fs.existsSync(p)) return [];
      const text = fs.readFileSync(p, 'utf8');
      const parsed = safeParseJson(text);
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
      return [];
    }
  }

  // 2025: Transposed CSV export from the "Top Winners" and "Innovation Awards" sheets.
  let winners = [];
  try {
    const csvPath2025 = path.join(__dirname, 'winners-data-2025.csv');
    const csvText2025 = fs.readFileSync(csvPath2025, 'utf8');
    const top2025 = buildFromTransposedCsv({
      csvText: csvText2025,
      year: 2025,
      defaultCategory: 'Top Winners'
    });
    if (top2025 && top2025.categories && top2025.categories.length) winners.push(top2025);
  } catch (e) {
    // If the data file is missing, keep winners empty.
  }

  try {
    const csvPath2025Innovation = path.join(__dirname, 'winners-data-2025-innovation.csv');
    if (fs.existsSync(csvPath2025Innovation)) {
      const csvText = fs.readFileSync(csvPath2025Innovation, 'utf8');
      const innovation2025 = buildFromTransposedCsv({
        csvText,
        year: 2025,
        defaultCategory: 'Innovation Awards'
      });
      if (innovation2025 && innovation2025.categories && innovation2025.categories.length) winners.push(innovation2025);
    }
  } catch (e) {
    // ignore
  }

  // Optional: add a 2024 dataset file later (winners-data-2024.csv) using the same layout.
  try {
    const csvPath2024 = path.join(__dirname, 'winners-data-2024.csv');
    if (fs.existsSync(csvPath2024)) {
      const csvText2024 = fs.readFileSync(csvPath2024, 'utf8');
      const year2024 = buildFromTransposedCsv({
        csvText: csvText2024,
        year: 2024,
        defaultCategory: 'Winners'
      });
      if (year2024 && year2024.categories && year2024.categories.length) {
        winners.push(year2024);
      }
    }
  } catch (e) {
    // ignore
  }

  // Optional: enrich with structured JSON entries (e.g., longer write-ups) without forcing CSV.
  winners = winners.concat(loadYearEntriesFromJsonFile('winners-extra.json'));

  winners = mergeYearEntries(winners);

  return {
    statusCode: 200,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'no-store'
    },
    body: JSON.stringify({
      winners
    })
  };
};
