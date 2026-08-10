// Test variant — no KV, no secret webhook. Returns brief but doesn't forward.
// Use this for local development and CI smoke tests.

addEventListener("fetch", event => {
  event.respondWith(handle(event.request));
});

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

const AREAS = ["civil", "penal", "ambiental", "otro"];

function isValidEmail(s) {
  return typeof s === "string" && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);
}

function isValidPhone(s) {
  if (typeof s !== "string") return false;
  const cleaned = s.replace(/[\s\-().]/g, "");
  return /^\+?\d{8,15}$/.test(cleaned);
}

function isValidName(s) {
  return typeof s === "string" && s.trim().length >= 2 && s.length <= 100;
}

function isValidArea(s) {
  return AREAS.includes(s);
}

function isValidSummary(s) {
  return typeof s === "string" && s.trim().length >= 10 && s.length <= 5000;
}

function urgentPriority(area) {
  if (area === "penal") return "URGENT";
  return "NORMAL";
}

function formatBrief(data) {
  const ts = new Date().toISOString();
  const priority = urgentPriority(data.area);
  const priorityFlag = priority === "URGENT" ? "🚨 *URGENCIA PENAL*" : "📋 Consulta";
  const areaLabel = {
    civil: "Civil",
    penal: "Penal",
    ambiental: "Ambiental",
    otro: "Otro"
  }[data.area] || data.area;

  return [
    priorityFlag,
    "",
    "*Lead desde web · Rubicón EAS*",
    `*Nombre:* ${data.name}`,
    `*Teléfono:* ${data.phone}`,
    data.email ? `*Email:* ${data.email}` : "*Email:* (no provisto)",
    `*Área:* ${areaLabel}`,
    "",
    "*Resumen:*",
    data.summary,
    "",
    `_Recibido: ${ts}_`,
  ].join("\n");
}

function jsonResponse(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...CORS },
  });
}

async function handle(request) {
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS });
  }

  const url = new URL(request.url);

  if (url.pathname === "/api/lead/health") {
    return jsonResponse({ ok: true, mode: "test", ts: new Date().toISOString() });
  }

  if (url.pathname !== "/api/lead") {
    return jsonResponse({ error: "Not found" }, 404);
  }
  if (request.method !== "POST") {
    return jsonResponse({ error: "Method not allowed" }, 405);
  }

  let data;
  try {
    const ct = request.headers.get("Content-Type") || "";
    if (ct.includes("application/json")) {
      data = await request.json();
    } else {
      return jsonResponse({ error: "Send JSON" }, 415);
    }
  } catch (e) {
    return jsonResponse({ error: "Invalid JSON" }, 400);
  }

  const errors = [];
  if (!isValidName(data.name)) errors.push("name");
  if (!isValidPhone(data.phone)) errors.push("phone");
  if (data.email && !isValidEmail(data.email)) errors.push("email");
  if (!isValidArea(data.area)) errors.push("area");
  if (!isValidSummary(data.summary)) errors.push("summary");

  if (errors.length > 0) {
    return jsonResponse({ error: "Validation failed", fields: errors }, 400);
  }

  const lead = {
    name: data.name.trim(),
    phone: data.phone.trim(),
    email: (data.email || "").trim(),
    area: data.area,
    summary: data.summary.trim(),
    ts: new Date().toISOString(),
    source: "rubiconeas.com.py",
  };

  const brief = formatBrief(lead);
  lead.brief = brief;

  return jsonResponse({
    ok: true,
    brief,
    priority: urgentPriority(lead.area),
    mode: "test",
  });
}
