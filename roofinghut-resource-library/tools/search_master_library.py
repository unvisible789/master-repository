import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "roofinghut_master_library.sqlite"

ALIASES = {
    "hot": "water",
    "tank": "water heater",
    "ac": "air conditioner",
    "a/c": "air conditioner",
    "hp": "heat pump",
    "dish washer": "dishwasher",
    "fridge": "refrigerator",
    "stove": "range",
}

def expand(query: str) -> str:
    q = query.lower()
    extra = []
    for k, v in ALIASES.items():
        if k in q:
            extra.append(v)
    return (query + " " + " ".join(extra)).strip()

def search(query: str, limit: int = 15):
    query = expand(query)
    terms = [t.strip().lower() for t in query.replace("/", " ").replace("-", " ").split() if t.strip()]
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    results = []

    # First use broad LIKE scoring so normal human wording works.
    tables = [
        ("exact_manual_index", "manual", "trade, brand, document_title, url, product_family, series, model, equipment, document_type, key_specs, audience, notes"),
        ("brand_document_hubs", "brand_hub", "trade, brand, resource_name, url, equipment_scope, resource_types, source_type, notes"),
        ("troubleshooting_topics", "troubleshooting", "trade, problem, first_checks, needed_documents"),
        ("lookup_rules", "lookup_rule", "topic, rule, caution"),
        ("trade_coverage", "coverage", "trade, product_families, document_types_needed"),
    ]
    for table, kind, cols_csv in tables:
        cols = [c.strip() for c in cols_csv.split(",")]
        rows = cur.execute(f"SELECT rowid, {cols_csv} FROM {table}").fetchall()
        for row in rows:
            haystack = " ".join(str(row[c] or "") for c in cols).lower()
            score = sum(3 if t in haystack else 0 for t in terms)
            # Boost exact model/brand-ish hits.
            if query.lower() in haystack:
                score += 10
            if score:
                results.append((score, kind, dict(row)))

    results.sort(key=lambda item: item[0], reverse=True)
    conn.close()
    return results[:limit]

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]).strip()
    if not q:
        print("Usage: python search_master_library.py <query>")
        sys.exit(1)
    for score, kind, row in search(q):
        print(f"[{score}] {kind}")
        if kind == "manual":
            print(f"{row.get('brand')} {row.get('series')} {row.get('model')} - {row.get('document_title')}")
            print(row.get("url"))
        elif kind == "brand_hub":
            print(f"{row.get('trade')} / {row.get('brand')} - {row.get('resource_name')}")
            print(row.get("url"))
        elif kind == "troubleshooting":
            print(f"{row.get('trade')} - {row.get('problem')}")
            print(row.get("first_checks"))
        elif kind == "lookup_rule":
            print(f"{row.get('topic')}: {row.get('rule')}")
        else:
            print(f"{row.get('trade')}: {row.get('product_families')}")
        print()
