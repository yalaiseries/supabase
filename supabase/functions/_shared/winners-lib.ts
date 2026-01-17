export type Link = { label?: string; url: string };
export type Showcase = {
  problem?: string;
  existingSolutions?: string;
  gap?: string;
  proposedSolution?: string;
  approach?: string;
  methods?: string;
  tools?: string;
  strategy?: string;
  impact?: string;
};

export type People = {
  representativeSpeaker?: string;
  designation?: string;
  linkedin?: string;
  lead?: string;
  coLeads?: string[];
  teamMembers?: string[];
};

export type UseCase = {
  title: string;
  team?: string;
  award?: string;
  summary?: string;
  links?: Link[];
  showcase?: Showcase;
  people?: People;
};
export type Category = { category: string; useCases: UseCase[] };
export type YearEntry = { year: number; categories: Category[] };

function normalizeTitle(value: unknown): string {
  return String(value ?? '')
    .trim()
    .toLowerCase()
    .replace(/\s+/g, ' ');
}

function uniqStrings(values: Array<string | undefined | null>): string[] {
  const out: string[] = [];
  const seen = new Set<string>();
  for (const v of values) {
    const s = String(v ?? '').trim();
    if (!s) continue;
    const key = s.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(s);
  }
  return out;
}

function mergeLinks(a: Link[] | undefined, b: Link[] | undefined): Link[] | undefined {
  const left = Array.isArray(a) ? a : [];
  const right = Array.isArray(b) ? b : [];
  const byUrl = new Map<string, Link>();
  for (const link of left.concat(right)) {
    if (!link || !link.url) continue;
    const url = String(link.url).trim();
    if (!url) continue;
    const existing = byUrl.get(url);
    if (!existing) {
      byUrl.set(url, { label: link.label, url });
      continue;
    }
    const existingLabel = String(existing.label ?? '').trim();
    const nextLabel = String(link.label ?? '').trim();
    if (!existingLabel && nextLabel) existing.label = nextLabel;
  }
  const out = Array.from(byUrl.values());
  return out.length ? out : undefined;
}

function mergeShowcase(a: Showcase | undefined, b: Showcase | undefined): Showcase | undefined {
  const left = a ?? {};
  const right = b ?? {};
  const merged: Showcase = {
    problem: left.problem || right.problem,
    existingSolutions: left.existingSolutions || right.existingSolutions,
    gap: left.gap || right.gap,
    proposedSolution: left.proposedSolution || right.proposedSolution,
    approach: left.approach || right.approach,
    methods: left.methods || right.methods,
    tools: left.tools || right.tools,
    strategy: left.strategy || right.strategy,
    impact: left.impact || right.impact
  };
  const hasAny = Object.values(merged).some((v) => String(v ?? '').trim().length > 0);
  return hasAny ? merged : undefined;
}

function mergePeople(a: People | undefined, b: People | undefined): People | undefined {
  const left = a ?? {};
  const right = b ?? {};

  const coLeads = uniqStrings([...(left.coLeads ?? []), ...(right.coLeads ?? [])]);
  const teamMembers = uniqStrings([...(left.teamMembers ?? []), ...(right.teamMembers ?? [])]);

  const merged: People = {
    representativeSpeaker: left.representativeSpeaker || right.representativeSpeaker,
    designation: left.designation || right.designation,
    linkedin: left.linkedin || right.linkedin,
    lead: left.lead || right.lead,
    coLeads: coLeads.length ? coLeads : undefined,
    teamMembers: teamMembers.length ? teamMembers : undefined
  };

  const hasAny =
    !!merged.representativeSpeaker ||
    !!merged.designation ||
    !!merged.linkedin ||
    !!merged.lead ||
    (Array.isArray(merged.coLeads) && merged.coLeads.length > 0) ||
    (Array.isArray(merged.teamMembers) && merged.teamMembers.length > 0);

  return hasAny ? merged : undefined;
}

function mergeUseCase(a: UseCase, b: UseCase): UseCase {
  return {
    title: a.title || b.title,
    team: a.team || b.team,
    award: a.award || b.award,
    summary: a.summary || b.summary,
    links: mergeLinks(a.links, b.links),
    showcase: mergeShowcase(a.showcase, b.showcase),
    people: mergePeople(a.people, b.people)
  };
}

export function enrichYearEntryByTitle(base: YearEntry, overlay: YearEntry): YearEntry {
  const out: YearEntry = {
    year: Number(base.year),
    categories: Array.isArray(base.categories) ? base.categories.map((c) => ({ category: c.category, useCases: c.useCases.slice() })) : []
  };

  const index = new Map<string, { cat: Category; idx: number }>();
  for (const cat of out.categories) {
    for (let i = 0; i < (cat.useCases?.length ?? 0); i++) {
      const key = normalizeTitle(cat.useCases[i]?.title);
      if (!key) continue;
      if (!index.has(key)) index.set(key, { cat, idx: i });
    }
  }

  const overlayCats = Array.isArray(overlay.categories) ? overlay.categories : [];
  for (const cat of overlayCats) {
    const useCases = Array.isArray(cat?.useCases) ? cat.useCases : [];
    for (const useCase of useCases) {
      const key = normalizeTitle(useCase?.title);
      if (!key) continue;
      const hit = index.get(key);
      if (!hit) continue;
      const existing = hit.cat.useCases[hit.idx];
      hit.cat.useCases[hit.idx] = mergeUseCase(existing, useCase);
    }
  }

  return out;
}

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

function splitPeopleList(value: unknown): string[] {
  const raw = String(value ?? '').replace(/\r/g, '').trim();
  if (!raw) return [];
  const normalized = raw
    .split(/\n|,/g)
    .map((s) => s.trim())
    .filter(Boolean)
    .filter((s) => s.toLowerCase() !== 'na');
  return Array.from(new Set(normalized));
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
  const getAny = (names: string[]) => {
    for (const n of names) {
      const v = get(n);
      if (v && v.length) return v;
    }
    return [] as string[];
  };

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

  const problems = getAny(['Problem', 'Problem statement']);
  const existingSolutions = getAny(['Existing solutions', 'Existing solution', 'Current solutions']);
  const gaps = getAny(['Gap', 'Gaps']);
  const proposedSolutions = getAny(['Proposed solution', 'Proposed Solution']);
  const approaches = getAny(['Approach', 'Approaches']);
  const methods = getAny(['Methods', 'Method']);
  const tools = getAny(['Tools', 'Tooling']);
  const strategies = getAny(['Strategy', 'Strategies']);
  const impacts = getAny(['Impact', 'Outcomes', 'Results']);

  const categories = new Map<string, UseCase[]>();

  for (let i = 0; i < projectCount; i++) {
    const title = compactLines(topics[i]);
    if (!title) continue;

    const rep = compactLines(reps[i]);
    const designation = compactLines(designations[i]);
    const lead = compactLines(leads[i]);
    const coleadRaw = String(coleads[i] ?? '');
    const teamMembersRaw = String(members[i] ?? '');

    const teamBits: string[] = [];
    if (rep || designation) teamBits.push([rep, designation].filter(Boolean).join(' — '));
    if (lead && lead.toLowerCase() !== 'na') teamBits.push(`Lead: ${lead}`);
    const coLeads = splitPeopleList(coleadRaw);
    if (coLeads.length) teamBits.push(`Co-lead: ${coLeads.join(' / ')}`);
    const teamMembersList = splitPeopleList(teamMembersRaw);
    if (teamMembersList.length) teamBits.push(`Team: ${teamMembersList.join(' / ')}`);
    const team = teamBits.join(' · ');

    const award = prizeToAward(prizes[i]);
    const summary = compactLines(summaries[i]) || compactLines(abouts[i]);

    const showcase: Showcase = {
      problem: compactLines(problems[i]),
      existingSolutions: compactLines(existingSolutions[i]),
      gap: compactLines(gaps[i]),
      proposedSolution: compactLines(proposedSolutions[i]),
      approach: compactLines(approaches[i]),
      methods: compactLines(methods[i]),
      tools: compactLines(tools[i]),
      strategy: compactLines(strategies[i]),
      impact: compactLines(impacts[i])
    };

    const hasShowcase = Object.values(showcase).some((v) => String(v || '').trim().length > 0);

    const links: Link[] = [];
    const slideUrl = toUrl(slides[i]);
    if (slideUrl) links.push({ label: 'Slides', url: slideUrl });

    const otherUrl = toUrl(otherLinks[i]);
    if (otherUrl) links.push({ label: 'Other link', url: otherUrl });

    const linkedinUrl = toUrl(linkedins[i]);
    if (linkedinUrl) links.push({ label: 'LinkedIn', url: linkedinUrl });

    const people: People = {
      representativeSpeaker: rep,
      designation,
      linkedin: linkedinUrl,
      lead: lead && lead.toLowerCase() !== 'na' ? lead : '',
      coLeads,
      teamMembers: teamMembersList
    };

    const hasPeople =
      !!people.representativeSpeaker ||
      !!people.designation ||
      !!people.linkedin ||
      !!people.lead ||
      (Array.isArray(people.coLeads) && people.coLeads.length > 0) ||
      (Array.isArray(people.teamMembers) && people.teamMembers.length > 0);

    const category = compactLines(categoriesRow[i]) || opts.defaultCategory;
    const current = categories.get(category) || [];
    current.push({
      title,
      team,
      award,
      summary,
      links,
      showcase: hasShowcase ? showcase : undefined,
      people: hasPeople ? people : undefined
    });
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

    const categories = Array.from(catMap.values()).sort((a, b) => String(a.category).localeCompare(String(b.category)));
    for (const cat of categories) {
      const merged = new Map<string, UseCase>();
      for (const useCase of cat.useCases) {
        const key = normalizeTitle(useCase?.title);
        if (!key) continue;
        const existing = merged.get(key);
        if (!existing) {
          merged.set(key, useCase);
          continue;
        }
        merged.set(key, mergeUseCase(existing, useCase));
      }
      cat.useCases = Array.from(merged.values());
    }

    entry.categories = categories;
    byYear.set(year, entry);
  }

  return Array.from(byYear.values()).sort((a, b) => Number(b.year) - Number(a.year));
}
