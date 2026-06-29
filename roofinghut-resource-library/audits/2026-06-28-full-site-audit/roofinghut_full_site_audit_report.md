# RoofingHut Full Site Audit - 2026-06-28

## Executive Summary
RoofingHut is much stronger than earlier: pages load, H1s are clean, content is not thin, resources/products are expanded, and image alt text appears fixed. The biggest opportunities now are SEO title/meta cleanup, ad placement consistency, trust/claim accuracy, resource-library usability, affiliate/product link cleanup, and stronger internal linking around high-value pages.

## Crawl Snapshot
- Pages crawled from sitemap: 86
- Average word count: ~1,439 words
- H1 issues: 0
- Thin page issues: 0 by basic word-count check
- Pages with missing alt text: 0 in this crawl
- Affiliate/product pages found: 58
- Weak/overlong titles: 54
- Weak/overlong/short meta descriptions: 24
- Bad/blocked links detected: 13

## Highest Priority Fixes

### 1. Fix SEO titles that are too long
Most state roof-cost pages use long titles like:
`Texas Roof Replacement Cost (2026) ? Ballpark Ranges & Calculator ? Roofinghut`
Many are 80-90+ characters. Shorten them to around 50-65 characters.

Better pattern:
`Texas Roof Replacement Cost 2026 | RoofingHut`
`Florida Roof Cost 2026: Hurricane-Zone Guide`
`NC Roof Replacement Cost 2026 | Calculator`

### 2. Rewrite weak meta descriptions
Some descriptions are too long, especially main pages/products/resources. Some resource category descriptions are too short.

Resources page currently claims a comprehensive 90,000+ record library, but the live metadata reports about 72,551 manual records plus hubs/rules/topics. Adjust claims unless 90k is actually supported elsewhere.

Better resources description:
`Search RoofingHut's homeowner and tech resource finder for HVAC, water heater, appliance, roofing, solar, electrical, plumbing, generator, pump and garage-door manuals, official brand hubs and troubleshooting links.`

### 3. Improve ad placement consistency
Ads are often too low to be seen:
- Homepage first ad around 5,350px
- Products first ad around 7,800px
- Resources first ad around 18,900px
- HEAR rebates first ad around 15,470px
- Blog posts often first ad around 7,600-10,000px
- Solar page is better, first ad around 562px

Recommended pattern:
- First ad after intro/first useful section, around 700-1,400px
- Second ad mid-content
- Footer ad as extra only
- Products: ad after first 8-12 product cards
- Resources: ad after search/filter area and another after results
- HEAR page: ad after state selector/intro and mid-state list

### 4. Fix/verify bad links
Likely bot-blocking but manually verify:
- Payhip links returning 403 to crawler
- Several state energy pages returning 403

Real product issues still found:
- Amazon `B0000DD5UE`
- Amazon `B08K2Q62RB`

### 5. Make resource library more honest and useful
The live resource library has sharded data and a large record count. Many records are official lookup pages, not direct PDFs. That is fine, but wording should say:
- ?manual finder?
- ?official document hub index?
- ?model lookup links?

Avoid implying RoofingHut hosts every manual directly.

### 6. Add stronger trust signals
Add or improve:
- Last updated date on major guides
- How data is estimated
- Sources/methodology section
- Affiliate disclosure near product grids
- Safety warnings on electrical/HVAC/gas/roof work
- ?Official source? labels in resource library

### 7. Strengthen internal linking
Add contextual links between:
- Roof cost pages -> roof calculator -> products -> contractor vetting
- HEAR rebates -> HVAC/water heater/solar resources -> products
- Products -> resource/manual library by trade
- Solar -> solar tax credit -> HEAR -> GetSunHut tools
- Blog posts -> products/resources/rebates where relevant

### 8. Improve products page revenue path
Products page has good intent but should be optimized:
- Keep best products at top by trade
- Fix remaining Amazon 404s
- Add ?why this product matters? short notes
- Add direct links from blog buying guides to product category filters
- Avoid ad placement before buy buttons, but add ad after first row/section

### 9. Expand state pages beyond template feel
State roof cost pages are useful but may look templated. Add state-specific details:
- climate risks
- insurance issues
- permit/building code notes
- storm/wind/hail concerns
- regional labor cost logic
- links to nearby state guides
- state-specific roof material recommendations

### 10. Performance / technical notes
- Main pages have reasonable HTML size, but products has 50 images and ~134KB HTML.
- Resources uses large sharded JSON. Good approach, but test mobile performance.
- HTTP header is `text/html` without charset, though meta charset is UTF-8. Browsers render fine, but adding `charset=utf-8` at server/header level is cleaner.

## Grok Fix Prompt
Use this prompt with Grok Desktop:

```text
Run a full RoofingHut improvement pass focused on traffic, usefulness, trust, SEO, ad revenue, and affiliate revenue.

Do not break live pages. Back up first. Make changes in small batches and test after each batch.

Audit findings to fix:
1. Shorten overlong SEO titles, especially state roof-cost pages. Target 50-65 characters.
2. Rewrite weak meta descriptions. Target 120-160 characters. Make them specific and honest.
3. Fix resource library wording: it should say manual finder/resource index/official lookup hub unless exact direct manuals are available. Do not claim 90,000+ unless the live data truly supports it.
4. Move ads higher on long pages without making the site spammy:
   - first ad after intro/first useful section around 700-1400px
   - second ad mid-content
   - footer ad as extra only
   - products ad after first 8-12 product cards
   - resources ad after search/filter area and after enough results
   - HEAR rebates ad after state selector/intro and mid-list
5. Fix remaining Amazon 404s found in audit: B0000DD5UE and B08K2Q62RB. Replace with live matching products and update card copy if needed.
6. Manually verify crawler-403 Payhip/state links. If real users see errors, replace them with working official/store links.
7. Add trust signals: last updated dates, methodology/source notes, affiliate disclosure near product grids, safety warnings for pro-only work.
8. Strengthen internal linking between calculators, products, resources, HEAR rebates, solar, contractor vetting, and state roof-cost pages.
9. Make state roof-cost pages feel less templated with climate/code/insurance/material notes by state.
10. Test mobile layout, resource search, product CTAs, ad boxes, and outbound links.

After changes, provide:
- pages changed
- before/after title/meta examples
- first ad position per major page
- fixed links list
- remaining risks
```
