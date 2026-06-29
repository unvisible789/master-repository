# RoofingHut Resource Library

Finished resource package for adding a searchable homeowner and tech manual/resource library to RoofingHut.

This package is designed so Grok or the server instance can use local files first, instead of searching the internet for common homeowner/tech questions.

## What Is Included

- `site/index.html` - embeddable/searchable resource library page
- `site/styles.css` - resource page styling
- `site/app.js` - browser search and filtering
- `data/roofinghut_master_library.json` - site-ready data source
- `data/roofinghut_master_library.sqlite` - local searchable database
- `data/*.csv` - editable source tables
- `data/RoofingHut_Master_Resource_File.xlsx` - Excel workbook version
- `tools/search_master_library.py` - local command-line search helper
- `tools/build_searchable_library.py` - rebuilds JSON/CSV/SQLite source files
- `GROK_HANDOFF.md` - exact instructions for adding this to RoofingHut

## Intended Site Path

Recommended public page:

`/resources/`

Recommended data location:

`/data/roofinghut_master_library.json`

## Current Coverage

The library currently covers:

- HVAC
- water heaters / hot water tanks
- thermostats
- solar and batteries
- roofing
- plumbing
- electrical
- dishwashers
- washers
- dryers
- refrigerators
- ranges
- generators
- garage doors
- pumps
- windows and doors

## Local Search Example

```powershell
python tools/search_master_library.py "Goodman GSZ14 2.5 ton"
python tools/search_master_library.py "Rheem hot water tank manual"
python tools/search_master_library.py "dishwasher not draining"
```

## Important Rule

Do not copy manufacturer PDF contents into RoofingHut unless permission allows it. Link to official documents and summarize in original RoofingHut wording.

