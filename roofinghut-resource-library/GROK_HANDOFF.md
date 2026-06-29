# Grok Handoff: Add RoofingHut Resource Library

Goal: add a professional searchable resource library to RoofingHut that helps homeowners and techs find manuals, wiring diagrams, troubleshooting resources, product documentation, rebate links, and official brand support pages.

## Files To Use

Use this package:

`roofinghut-resource-library/`

Use the static page:

`roofinghut-resource-library/site/index.html`

Use the data:

`roofinghut-resource-library/data/roofinghut_master_library.json`

## Recommended Implementation

1. Add a new RoofingHut page at `/resources/`.
2. Use the design and behavior from `site/index.html`, `site/styles.css`, and `site/app.js`.
3. Copy `data/roofinghut_master_library.json` into the site public data folder.
4. Make the resource page load the JSON locally.
5. Add navigation links from:
   - Home page
   - Products page
   - Roofing guides
   - HVAC guide pages
   - Water heater / rebates pages
   - Solar pages
6. Add internal sections or filters for:
   - Manuals
   - Brand support hubs
   - Troubleshooting
   - Lookup rules
   - Trade coverage

## SEO Requirements

Page title:

`Homeowner & Tech Manual Library | RoofingHut`

Meta description:

`Search RoofingHut's homeowner and tech resource library for HVAC manuals, water heater support, roofing documents, appliance help, electrical resources, solar guides, troubleshooting links, and official brand documentation.`

Suggested H1:

`Homeowner & Tech Resource Library`

Suggested intro copy:

`Find official manuals, product document hubs, troubleshooting starting points, wiring-diagram sources, and homeowner-safe guidance across roofing, HVAC, water heaters, appliances, electrical, plumbing, solar, generators, garage doors, pumps, windows, and more.`

## Safety Copy

Add a clear safety notice:

`Some manuals and wiring diagrams are intended for licensed professionals. RoofingHut helps users find official resources, but electrical, gas, refrigerant, roofing fall-risk, generator, and panel work should be handled by qualified pros.`

## Expansion Instructions

Use `data/exact_manual_index.csv` for exact model-level records.

Use `data/brand_document_hubs.csv` when exact model-level records do not exist yet.

When adding new records:

- Prefer official manufacturer sources.
- Include model/series, document type, document title, official URL, audience, and key specs.
- Mark tech-only resources clearly.
- Do not scrape or republish copyrighted PDFs.
- Link to official sources and write original summaries.

## First High-Value Expansion Targets

1. Add exact manuals for top Goodman, Trane, Carrier, Lennox, Rheem, Bosch, Mitsubishi and Daikin heat pump models.
2. Add exact manuals for common Rheem, A.O. Smith, Bradford White, Navien and Rinnai water heaters.
3. Add appliance manual hubs and troubleshooting pages for Whirlpool, GE, LG, Samsung, Bosch and Frigidaire.
4. Add electrical support for Square D, Eaton, Siemens, Leviton, Lutron, Generac and Reliance.
5. Add roof brand install/warranty summaries for GAF, Owens Corning, CertainTeed, IKO, Atlas, TAMKO and Malarkey.

