# Refugee Response 2026: Partners' Achievements — Republic of Moldova

Interactive dashboard tracking the implementation of the Refugee Response Plan
(RRP) in the Republic of Moldova. It presents partners' reported achievements
for 2026 — who is doing what, where, and for whom — to support coordination of
the refugee response.

Live dashboard: https://mdachim.github.io/rrp_2026/

## What it shows

- **Overview** — headline summary of the current reporting quarter and a
  sector navigation panel with cluster icons.
- **Who** — number of reporting partners, activities per organization,
  activities by mandating agency, and projects by status.
- **What** — RRP outcome areas and sectors, with activity counts per outcome
  area and the number of partners active in each sector.
- **Where** — choropleth map of Moldova's 37 first-level administrative units
  (raions, municipalities, UTA Gagauzia, Transnistrian region and Bender),
  based on official Government of Moldova boundaries, plus a count of
  country-wide activities.
- **When and for whom** — the underlying activity table with outcome area,
  indicator, reported achievement (total, or disaggregated into refugee and
  host-community beneficiaries), dates and location.

## Interactivity

All visuals are cross-filtered. Selections combine across:
- sector icons in the navigation panel,
- bars in any chart,
- raions on the map,
- dropdown filters (raion, implementation modality, mandating agency, sector,
  RRP status).

The table is sortable by any column.

## Data

The dashboard is powered by partner reporting in **ActivityInfo** (2026 Project
Reporting Form and its Report Activities subform). Each record is one reported
indicator achievement, carrying its project's attributes (partner, mandating
agency, status, dates, RRP flag, geographical scope) alongside the activity's
sector, outcome area, indicator, location and beneficiary figures.

Reported achievements are shown either as an undisaggregated total or split by
population group (refugees / host community), reflecting how each indicator is
disaggregated at the source. An activity is counted as country-wide when its
project has country-wide geographical scope and the activity is not attributed
to a specific raion.

Data is stored in `data.json` and refreshed periodically from ActivityInfo
exports; the data preparation is done offline.

## Repository contents

| File | Purpose |
|---|---|
| `index.html` | The dashboard itself — layout, visuals and logic |
| `data.json` | Activity-level dataset |
| `indicator_config.json` | Indicator reference table: outcome area, sector, activity, unit and the aggregation methodology applied to each indicator |
| `partner_types.json` | Partner reference table: organization type (UN agency, international NGO, national NGO, etc.) |
| `pbi blue.png` | Logo shown in the dashboard header |
| `icons/` | Sector icons used by the sector navigation panel |

The dashboard loads the dataset and both reference tables at run time, so data
refreshes and reference updates are made by replacing the relevant JSON file —
`index.html` itself does not change.

## Technology

Single-page HTML/JavaScript application with no build step or backend:
Chart.js for charts, Leaflet for the map, official GoM admin-1 boundaries
embedded as GeoJSON. Hosted on GitHub Pages and embeddable via iframe.
