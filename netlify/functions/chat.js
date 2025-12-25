// Netlify Function: /.netlify/functions/chat
// Minimal “answer from website info” chat endpoint.
//
// Setup on Netlify (Site configuration → Environment variables):
// - OPENAI_API_KEY (required)
// - OPENAI_MODEL (optional, default: gpt-4o-mini)
// - TAVILY_API_KEY (optional, enables web search)
//
// Optional datasets:
// - Add small text/JSON files under /data and reference them in /netlify/functions/kb.md,
//   or enable keyword search below.

const fs = require("fs");
const path = require("path");

function json(statusCode, body) {
  return {
    statusCode,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
    body: JSON.stringify(body),
  };
}

function readKb() {
  const kbPath = path.join(__dirname, "kb.md");
  return fs.readFileSync(kbPath, "utf8");
}

function listDatasetFiles() {
  const root = process.cwd();
  const dataDir = path.join(root, "data");
  if (!fs.existsSync(dataDir)) return [];
  return fs
    .readdirSync(dataDir)
    .filter((f) => !f.startsWith("."))
    .slice(0, 20)
    .map((f) => path.join(dataDir, f));
}

function keywordSearchInFiles(query, filePaths) {
  const q = query.toLowerCase();
  const hits = [];
  for (const filePath of filePaths) {
    try {
      const text = fs.readFileSync(filePath, "utf8");
      const idx = text.toLowerCase().indexOf(q);
      if (idx >= 0) {
        const start = Math.max(0, idx - 180);
        const end = Math.min(text.length, idx + q.length + 260);
        hits.push({
          file: path.basename(filePath),
          snippet: text.slice(start, end).replace(/\s+/g, " ").trim(),
        });
      }
    } catch {
      // ignore
    }
    if (hits.length >= 5) break;
  }
  return hits;
}

async function maybeWebSearch(question) {
  const tavilyKey = process.env.TAVILY_API_KEY;
  if (!tavilyKey) return null;

  const resp = await fetch("https://api.tavily.com/search", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      api_key: tavilyKey,
      query: question,
      search_depth: "basic",
      max_results: 5,
    }),
  });

  if (!resp.ok) return null;
  const data = await resp.json();
  const results = Array.isArray(data?.results) ? data.results : [];

  const lines = results
    .slice(0, 5)
    .map((r, i) => `- [${i + 1}] ${r.title || ""}\n  ${r.url || ""}\n  ${r.content || ""}`)
    .join("\n");

  return lines ? `Web search results (may be incomplete):\n${lines}` : null;
}

exports.handler = async function handler(event) {
  if (event.httpMethod !== "POST") {
    return json(405, { error: "Method not allowed" });
  }

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    return json(500, {
      error: "Missing OPENAI_API_KEY. Add it in Netlify → Site configuration → Environment variables.",
    });
  }

  let payload;
  try {
    payload = JSON.parse(event.body || "{}");
  } catch {
    return json(400, { error: "Invalid JSON" });
  }

  const question = String(payload.question || "").trim();
  if (!question) return json(400, { error: "Missing question" });

  const model = process.env.OPENAI_MODEL || "gpt-4o-mini";

  let kb;
  try {
    kb = readKb();
  } catch {
    kb = "";
  }

  const datasetFiles = listDatasetFiles();
  const datasetHits = datasetFiles.length ? keywordSearchInFiles(question, datasetFiles) : [];
  const datasetContext = datasetHits.length
    ? `Dataset matches (keyword):\n${datasetHits
        .map((h) => `- ${h.file}: ${h.snippet}`)
        .join("\n")}`
    : "";

  const webContext = await maybeWebSearch(question);

  // Simple retrieval: send local KB (small enough). If it grows, switch to chunking + embeddings.
  const messages = [
    {
      role: "system",
      content:
        "You are the website assistant for AI (Hackathon) Series — Agentic AI Learning Hub (2026). Answer primarily using the provided website knowledge. If dataset matches are provided, you may use them. If web search results are provided, you may use them but clearly label anything that comes from web search. If the answer is not available, say you don't have that info and suggest the contact email. Keep answers concise and factual.",
    },
    {
      role: "user",
      content: `Website knowledge:\n${kb}\n\n${datasetContext ? datasetContext + "\n\n" : ""}${webContext ? webContext + "\n\n" : ""}Question: ${question}`,
    },
  ];

  const resp = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model,
      messages,
      temperature: 0.2,
    }),
  });

  if (!resp.ok) {
    const text = await resp.text();
    return json(502, { error: `Upstream error (${resp.status}): ${text}` });
  }

  const data = await resp.json();
  const answer = data?.choices?.[0]?.message?.content?.trim() || "";
  return json(200, { answer });
};
