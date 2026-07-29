# Moldova RRP Partners' Achievements — dashboard

Self-contained HTML dashboard (charts, Moldova raion map, sector chiclet slicer,
cross-filtering). It loads data from `data.json` in the same folder, and falls
back to a copy embedded in the HTML if `data.json` is missing.

## Files
- `moldova_rrp_dashboard.html` — the dashboard (open in any browser).
- `data.json` — the data it displays. Replace this to refresh.
- `xlsx_to_json.py` — convert an ActivityInfo Excel export into `data.json`.
- `fetch_activityinfo.py` — pull directly from the ActivityInfo API into `data.json`.
- `.github/workflows/refresh.yml` — optional scheduled auto-refresh (see below).

## Which export to use
For the full "Partners' Achievements" view (outcome areas, indicators, and
achievement per indicator), export the **Report Activities** tab — the granular
rows that include `Sector - outcome area Outcome area`,
`Indicators 2026 Indicator 2026`, `Total achievement`, and
`Location Admin 1 Name`. The project-form export works too but has no
outcome/indicator/achievement columns, so those visuals stay hidden.

The dashboard maps columns itself in `CONFIG.columnMap` (top of the HTML). If a
column doesn't map, add its exact header there.

## Refresh the data (manual)
1. In ActivityInfo, export the report to Excel.
2. `pip install openpyxl`
3. `python xlsx_to_json.py "your_export.xlsx"`  → writes `data.json`
4. Commit and push `data.json`. The live page updates on next load
   (use the "Refresh data" button to reload without a hard refresh).

## Host on GitHub Pages
1. Create a repo and add these files at its root.
2. Push to the `main` branch.
3. Repo → Settings → Pages → Source: "Deploy from a branch" → `main` / `root` → Save.
4. After a minute the dashboard is live at:
   `https://<your-username>.github.io/<repo-name>/moldova_rrp_dashboard.html`

`data.json` is served from the same origin, so there's no CORS issue.

## Embed on your website
Paste the Pages URL into your website builder's "embed / external content" field,
or use an iframe:

```html
<iframe
  src="https://<your-username>.github.io/<repo-name>/moldova_rrp_dashboard.html"
  style="width:100%;height:1200px;border:0"
  loading="lazy"
  title="Moldova RRP Partners' Achievements"></iframe>
```

Adjust `height` to fit; the layout is responsive and reflows on narrow screens.

## Optional: automatic refresh (GitHub Actions)
`.github/workflows/refresh.yml` runs `fetch_activityinfo.py` on a schedule,
commits `data.json` when it changes, and Pages redeploys automatically.

Set-up:
1. Repo → Settings → Secrets and variables → Actions → New repository secret:
   name `ACTIVITYINFO_TOKEN`, value = your API token. (Do **not** hard-code the
   token in the repo.)
2. Confirm `fetch_activityinfo.py` runs locally first (it prints the columns it
   found). The API path can differ per form; adjust the endpoint/parsing there
   if needed.
3. The workflow is scheduled daily by default — edit the `cron` line to taste,
   or trigger it manually from the Actions tab.

## Security note
Don't commit your ActivityInfo token to the repo. Keep it in a GitHub secret
(for Actions) or on your own machine (for local runs). The dashboard itself
needs no token — it only reads `data.json`.
