export type Link = { label?: string; url: string };
export type UseCase = { title: string; team?: string; award?: string; summary?: string; links?: Link[] };
export type Category = { category: string; useCases: UseCase[] };
export type YearEntry = { year: number; categories: Category[] };

function parseCsv(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
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

      if (row.length > 1 || (row.length === 1 && row[0].trim() !== '')) {
        rows.push(row);
      }
      row = [];
      continue;
    }

    if (ch === '\r') continue;

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

function compactLines(value: unknown): string {
  return String(value ?? '')
    .replace(/\r/g, '')
    .split('\n')
    .map((s) => s.trim())
    .filter(Boolean)
    .join(' / ');
}

function normalizeKey(value: unknown): string {
  return String(value ?? '')
    .trim()
    .toLowerCase()
    .replace(/\s+/g, ' ');
}

function toUrl(value: unknown): string {
  const v = String(value ?? '').trim();
  if (!v) return '';
  if (v.startsWith('http://') || v.startsWith('https://')) return v;
  if (v.startsWith('www.')) return `https://${v}`;
  if (v.includes('.') && !v.includes(' ')) return `https://${v}`;
  return '';
}

function prizeToAward(value: unknown): string {
  const v = String(value ?? '').trim().toLowerCase();
  if (v === '1st') return '1st Prize';
  if (v === '2nd') return '2nd Prize';
  if (v === '3rd') return '3rd Prize';
  if (!v) return '';
  return String(value ?? '');
}

export function buildFromTransposedCsv(opts: { csvText: string; year: number; defaultCategory: string }): YearEntry | null {
  const rows = parseCsv(opts.csvText);
  if (!rows.length) return null;

  const headers = rows[0] || [];
  const projectCount = Math.max(0, headers.length - 1);
  if (!projectCount) return null;

  const fields = new Map<string, string[]>();
  for (const r of rows) {
    const key = normalizeKey(r[0]);
    if (!key) continue;
    fields.set(key, r.slice(1));
  }

  const get = (name: string) => fields.get(normalizeKey(name)) || [];

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
  const categoriesRow = get('Use case category').length ? get('Use case category') : get('Category');

  const categories = new Map<string, UseCase[]>();

  for (let i = 0; i < projectCount; i++) {
    const title = compactLines(topics[i]);
    if (!title) continue;

    const rep = compactLines(reps[i]);
    const designation = compactLines(designations[i]);
    const lead = compactLines(leads[i]);
    const colead = compactLines(coleads[i]);
    const teamMembers = compactLines(members[i]);

    const teamBits: string[] = [];
    if (rep || designation) teamBits.push([rep, designation].filter(Boolean).join(' — '));
    if (lead && lead.toLowerCase() !== 'na') teamBits.push(`Lead: ${lead}`);
    if (colead && colead.toLowerCase() !== 'na') teamBits.push(`Co-lead: ${colead}`);
    if (teamMembers && teamMembers.toLowerCase() !== 'na') teamBits.push(`Team: ${teamMembers}`);
    const team = teamBits.join(' · ');

    const award = prizeToAward(prizes[i]);
    const summary = compactLines(summaries[i]) || compactLines(abouts[i]);

    const links: Link[] = [];
    const slideUrl = toUrl(slides[i]);
    if (slideUrl) links.push({ label: 'Slides', url: slideUrl });

    const otherUrl = toUrl(otherLinks[i]);
    if (otherUrl) links.push({ label: 'Other link', url: otherUrl });

    const linkedinUrl = toUrl(linkedins[i]);
    if (linkedinUrl) links.push({ label: 'LinkedIn', url: linkedinUrl });

    const category = compactLines(categoriesRow[i]) || opts.defaultCategory;
    const current = categories.get(category) || [];
    current.push({ title, team, award, summary, links });
    categories.set(category, current);
  }

  const categoriesOut: Category[] = Array.from(categories.entries())
    .sort((a, b) => String(a[0]).localeCompare(String(b[0])))
    .map(([category, useCases]) => ({ category, useCases }));

  return { year: opts.year, categories: categoriesOut };
}

export function mergeYearEntries(yearEntries: Array<YearEntry | null | undefined>): YearEntry[] {
  const byYear = new Map<number, YearEntry>();
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

  for (const [year, entry] of byYear.entries()) {
    const catMap = new Map<string, Category>();
    for (const cat of entry.categories) {
      const name = String(cat?.category || 'Uncategorized');
      const useCases = Array.isArray(cat?.useCases) ? cat.useCases : [];
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
