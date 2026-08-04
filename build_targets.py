#!/usr/bin/env python3
"""Build targets_2026.json from the RRP submissions extract and the target
methodology table.

  python3 build_targets.py 2026_full_view_extr.xlsx Indicator_calculation_pbi_26.xlsx

Submissions carry one 2026 target per partner and indicator; the methodology
table says how those partner targets roll up to the response-level target:
  Sum  -> add every partner's target
  Max  -> the single highest partner target (shared caseload, no double count)

The dashboard joins the result to its achievement rows on norm(indicator),
so indicator wording must stay identical to the reporting form.
"""
import json
import re
import sys
import unicodedata
from datetime import date

import openpyxl


def norm(s):
    """Same normalization the dashboard uses (see norm() in index.html)."""
    s = unicodedata.normalize("NFKD", str(s if s is not None else ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^\x00-\x7F]", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def num(v):
    if v is None or str(v).strip() == "":
        return 0.0
    try:
        return float(str(v).replace(",", "").replace(" ", ""))
    except ValueError:
        return 0.0


def rows_of(path):
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True).active
    return [r for r in ws.iter_rows(values_only=True)]


def load_methods(path):
    """sector / indicator / methodology, with a header row that may be padded."""
    out = {}
    for r in rows_of(path):
        cells = [c for c in r if c is not None and str(c).strip() != ""]
        if len(cells) < 3:
            continue
        sector, indicator, method = str(cells[0]), str(cells[1]), str(cells[2])
        if norm(method) not in ("sum", "max"):
            continue  # header row
        out[norm(indicator)] = {"sector": sector.strip(),
                                "method": method.strip().title()}
    return out


def build(subs_path, method_path):
    methods = load_methods(method_path)
    rows = rows_of(subs_path)
    hdr = [norm(h) for h in rows[0]]
    col = {name: hdr.index(name) for name in hdr}

    def cell(r, *names):
        for n in names:
            if n in col and col[n] < len(r):
                return r[col[n]]
        return None

    inds = {}
    for r in rows[1:]:
        indicator = cell(r, "indicators 25-26 indicator")
        if not indicator or not str(indicator).strip():
            continue
        k = norm(indicator)
        e = inds.setdefault(k, {
            "indicator": str(indicator).strip(),
            "sector": str(cell(r, "sector") or "").strip(),
            "outcome": str(cell(r, "sectors 25-26 outcome area") or "").strip(),
            "activity": str(cell(r, "activities 25-26 activity") or "").strip(),
            "method": methods.get(k, {}).get("method", "Sum"),
            "byPartner": {},
        })
        partner = str(cell(r, "parent partner") or "").strip() or "(not stated)"
        p = e["byPartner"].setdefault(partner, {"partner": partner, "target": 0.0,
                                                "budget": 0.0, "submissions": 0})
        # one partner may submit several lines for the same indicator; those are
        # always additive within the partner — the methodology governs the
        # roll-up across partners only.
        p["target"] += num(cell(r, "target 2026"))
        p["budget"] += num(cell(r, "budget 2026"))
        p["submissions"] += 1

    out = []
    for e in inds.values():
        partners = sorted(e.pop("byPartner").values(), key=lambda p: -p["target"])
        vals = [p["target"] for p in partners]
        e["target"] = max(vals) if e["method"].lower() == "max" else sum(vals)
        e["budget"] = sum(p["budget"] for p in partners)
        e["partners"] = len(partners)
        e["submissions"] = sum(p["submissions"] for p in partners)
        e["byPartner"] = [{"partner": p["partner"],
                           "target": int(p["target"]) if p["target"] == int(p["target"]) else p["target"],
                           "budget": int(p["budget"]) if p["budget"] == int(p["budget"]) else p["budget"],
                           "submissions": p["submissions"]} for p in partners]
        e["target"] = int(e["target"]) if e["target"] == int(e["target"]) else e["target"]
        e["budget"] = int(e["budget"]) if e["budget"] == int(e["budget"]) else e["budget"]
        out.append(e)
    out.sort(key=lambda e: (e["sector"], e["indicator"]))

    return {
        "meta": {
            "generated": date.today().isoformat(),
            "sources": [subs_path.split("/")[-1], method_path.split("/")[-1]],
            "indicators": len(out),
            "submissions": sum(e["submissions"] for e in out),
            "note": "target = partner targets aggregated per the indicator's "
                    "methodology (Sum adds partners, Max takes the highest)",
        },
        "indicators": out,
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    data = build(sys.argv[1], sys.argv[2])
    with open("targets_2026.json", "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    print(f"targets_2026.json — {data['meta']['indicators']} indicators, "
          f"{data['meta']['submissions']} submissions")
