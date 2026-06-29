const DATA_PATH = "../data/roofinghut_master_library.json";

const state = {
  records: [],
  query: "",
  trade: "",
  type: "",
};

const els = {
  search: document.getElementById("resourceSearch"),
  trade: document.getElementById("tradeFilter"),
  type: document.getElementById("typeFilter"),
  results: document.getElementById("results"),
  resultCount: document.getElementById("resultCount"),
  totalCount: document.getElementById("totalCount"),
  manualCount: document.getElementById("manualCount"),
  hubCount: document.getElementById("hubCount"),
  tradeCount: document.getElementById("tradeCount"),
};

function normalize(value) {
  return String(value || "").toLowerCase();
}

function compact(values) {
  return values.filter(Boolean).join(" ");
}

function flattenLibrary(data) {
  const records = [];

  for (const item of data.exact_manual_index || []) {
    records.push({
      kind: "manual",
      trade: item.trade,
      brand: item.brand,
      title: item.document_title,
      subtitle: compact([item.series, item.model, item.equipment]),
      body: compact([item.product_family, item.document_type, item.key_specs, item.audience, item.notes]),
      url: item.url,
      warning: normalize(item.audience).includes("tech"),
    });
  }

  for (const item of data.brand_document_hubs || []) {
    records.push({
      kind: "brand_hub",
      trade: item.trade,
      brand: item.brand,
      title: item.resource_name,
      subtitle: item.equipment_scope,
      body: compact([item.resource_types, item.source_type, item.notes]),
      url: item.url,
      warning: false,
    });
  }

  for (const item of data.troubleshooting_topics || []) {
    records.push({
      kind: "troubleshooting",
      trade: item.trade,
      brand: "",
      title: item.problem,
      subtitle: "Troubleshooting starting point",
      body: compact([item.first_checks, item.needed_documents]),
      url: "",
      warning: /electrical|gas|refrigerant|pro-level|licensed/i.test(item.first_checks || ""),
    });
  }

  for (const item of data.lookup_rules || []) {
    records.push({
      kind: "lookup_rule",
      trade: "Lookup Rules",
      brand: "",
      title: item.topic,
      subtitle: "Reference rule",
      body: compact([item.rule, item.caution]),
      url: "",
      warning: false,
    });
  }

  for (const item of data.trade_coverage || []) {
    records.push({
      kind: "coverage",
      trade: item.trade,
      brand: "",
      title: `${item.trade} coverage`,
      subtitle: item.product_families,
      body: item.document_types_needed,
      url: "",
      warning: false,
    });
  }

  return records;
}

function score(record, terms) {
  const text = normalize(compact([record.kind, record.trade, record.brand, record.title, record.subtitle, record.body]));
  if (!terms.length) return 1;
  let total = 0;
  for (const term of terms) {
    if (text.includes(term)) total += 3;
    if (normalize(record.title).includes(term)) total += 2;
    if (normalize(record.brand).includes(term)) total += 2;
  }
  return total;
}

function kindLabel(kind) {
  return {
    manual: "Exact manual",
    brand_hub: "Brand hub",
    troubleshooting: "Troubleshooting",
    lookup_rule: "Lookup rule",
    coverage: "Coverage",
  }[kind] || kind;
}

function render() {
  const terms = normalize(state.query).split(/\s+/).filter(Boolean);
  const filtered = state.records
    .map((record) => ({ record, score: score(record, terms) }))
    .filter(({ record, score: itemScore }) => {
      if (state.trade && record.trade !== state.trade) return false;
      if (state.type && record.kind !== state.type) return false;
      return itemScore > 0;
    })
    .sort((a, b) => b.score - a.score || a.record.title.localeCompare(b.record.title))
    .slice(0, 80)
    .map(({ record }) => record);

  els.resultCount.textContent = `${filtered.length} shown`;

  if (!filtered.length) {
    els.results.innerHTML = `<div class="empty">No matching local resource found yet. Add an exact model row to the library or search by brand/product type.</div>`;
    return;
  }

  els.results.innerHTML = filtered.map((record) => `
    <article class="result-card">
      <div class="badge-row">
        <span class="badge ${record.kind === "manual" ? "manual" : ""}">${kindLabel(record.kind)}</span>
        ${record.trade ? `<span class="badge">${record.trade}</span>` : ""}
        ${record.brand ? `<span class="badge">${record.brand}</span>` : ""}
        ${record.warning ? `<span class="badge warning">Tech caution</span>` : ""}
      </div>
      <h3>${escapeHtml(record.title)}</h3>
      ${record.subtitle ? `<p><strong>${escapeHtml(record.subtitle)}</strong></p>` : ""}
      ${record.body ? `<p>${escapeHtml(record.body)}</p>` : ""}
      ${record.url ? `<p><a href="${escapeAttribute(record.url)}" target="_blank" rel="noopener">Open official resource</a></p>` : ""}
    </article>
  `).join("");
}

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("'", "&#39;");
}

function populateFilters() {
  const trades = [...new Set(state.records.map((item) => item.trade).filter(Boolean))].sort();
  for (const trade of trades) {
    const option = document.createElement("option");
    option.value = trade;
    option.textContent = trade;
    els.trade.appendChild(option);
  }
}

function updateStats() {
  const trades = new Set(state.records.map((item) => item.trade).filter(Boolean));
  els.totalCount.textContent = state.records.length;
  els.manualCount.textContent = state.records.filter((item) => item.kind === "manual").length;
  els.hubCount.textContent = state.records.filter((item) => item.kind === "brand_hub").length;
  els.tradeCount.textContent = trades.size;
}

async function init() {
  try {
    const response = await fetch(DATA_PATH);
    const data = await response.json();
    state.records = flattenLibrary(data);
    populateFilters();
    updateStats();
    render();
  } catch (error) {
    els.resultCount.textContent = "Library failed to load";
    els.results.innerHTML = `<div class="empty">Could not load local library data. Check that <code>${DATA_PATH}</code> exists on the site.</div>`;
  }
}

els.search.addEventListener("input", (event) => {
  state.query = event.target.value;
  render();
});

els.trade.addEventListener("change", (event) => {
  state.trade = event.target.value;
  render();
});

els.type.addEventListener("change", (event) => {
  state.type = event.target.value;
  render();
});

init();

