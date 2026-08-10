// Production Worker — uses KV namespace and secret webhook
// To deploy: 1) Create KV namespace via `wrangler kv:namespace create LEADS`
//             2) Bind as `LEADS` in wrangler.toml
//             3) Set webhook as secret: `wrangler secret put WEBHOOK_URL`
//             4) `wrangler deploy`
//
// For sandbox/local: see api/lead-worker.test.json (no secrets, no KV)

addEventListener("fetch", event => {
  event.respondWith(handle(event.request));
});

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400",
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
  const priorityFlag = priority === "URGENT" ? "🚨 *URGENCIA PENAL* — responder en <30 min" : "📋 Consulta";
  const areaLabel = {
    civil: "Civil",
    penal: "Penal",
    ambiental: "Ambiental",
    otro: "Otro / No estoy seguro"
  }[data.area] || data.area;

  return [
    priorityFlag,
    "",
    "*Lead desde web · Rubicón EAS*",
    "━━━━━━━━━━━━━━━━━━━━",
    `*Nombre:* ${data.name}`,
    `*Teléfono:* ${data.phone}`,
    data.email ? `*Email:* ${data.email}` : "*Email:* (no provisto)",
    `*Área:* ${areaLabel}`,
    "",
    "*Resumen:*",
    data.summary,
    "",
    "━━━━━━━━━━━━━━━━━━━━",
    `_Recibido: ${ts}_`,
    `_Source: rubiconeas.com.py_`,
    `_Priority: ${priority}_`,
  ].join("\n");
}

async function notifyN8n(lead, webhookUrl) {
  if (!webhookUrl) return { ok: false, reason: "no webhook configured" };
  try {
    const r = await fetch(webhookUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lead),
      cf: { timeout: 5000 },
    });
    return { ok: r.ok, status: r.status };
  } catch (e) {
    return { ok: false, reason: e.message };
  }
}

async function logLead(env, lead) {
  if (!env.LEADS) return null;
  try {
    const id = `lead:${Date.now()}:${Math.random().toString(36).slice(2, 8)}`;
    await env.LEADS.put(id, JSON.stringify(lead), {
      expirationTtl: 60 * 60 * 24 * 90,  // 90 days
    });
    return id;
  } catch (e) {
    return null;
  }
}

function jsonResponse(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...CORS },
  });
}

async function handle(request) {
  const url = new URL(request.url);

  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS });
  }

  if (url.pathname === "/api/lead/health") {
    return jsonResponse({
      ok: true,
      name: "rubicon-eas-lead",
      ts: new Date().toISOString(),
    });
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
    return jsonResponse({ error: "Invalid JSON", detail: e.message }, 400);
  }

  // Honeypot
  if (data.website || data.company_url) {
    return jsonResponse({ ok: true, ignored: true }, 200);
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
    consent: true,
    ts: new Date().toISOString(),
    source: "rubiconeas.com.py",
    ip: request.headers.get("CF-Connecting-IP") || null,
    userAgent: (request.headers.get("User-Agent") || "").slice(0, 200),
  };

  lead.brief = formatBrief(lead);

  // Webhook from env (set via `wrangler secret put WEBHOOK_URL`)
  const webhookUrl = WEBHOOK_URL || null;
  const webhookResult = await notifyN8n(lead, webhookUrl);

  const id = await logLead(request.env, lead);

  return jsonResponse({
    ok: true,
    id,
    brief: lead.brief,
    webhook: webhookResult,
    priority: urgentPriority(lead.area),
    instructions: urgentPriority(lead.area) === "URGENT"
      ? "Llamar ahora al abogado de turno. <30 min SLA."
      : "Revisar en <24h hábiles. Confirmar disponibilidad.",
  });
}
