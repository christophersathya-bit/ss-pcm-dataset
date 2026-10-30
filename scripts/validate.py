"""Sanity checks for data/ss_pcm_dataset.csv. Run: python scripts/validate.py"""
import csv, sys, pathlib
p = pathlib.Path(__file__).resolve().parent.parent/"data"/"ss_pcm_dataset.csv"
rows = list(csv.DictReader(open(p))); errs = []
ids = [r["id"] for r in rows]
if len(ids) != len(set(ids)): errs.append("duplicate ids")
CLASSES = {"organic","polymer","organometallic","inorganic","metallic"}
for r in rows:
    i = r["id"]
    if r["class"] not in CLASSES: errs.append(f"{i}: bad class {r['class']}")
    if r["verification_status"] not in {"verified","needs_check","to_verify"}: errs.append(f"{i}: bad status")
    if r["verification_status"]=="verified" and not (r["doi"] or r["source_url"]): errs.append(f"{i}: verified but no DOI or source_url")
    for c,lo,hi in [("T_heat_C",-273,1500),("T_cool_C",-273,1500),("dH_heat_Jg",0,500),("dH_cool_Jg",0,500)]:
        if r[c]:
            v=float(r[c])
            if not lo<=v<=hi: errs.append(f"{i}: {c}={v} out of range")
    if r["melting_point_C"] and r["T_heat_C"] and float(r["T_heat_C"])>=float(r["melting_point_C"]):
        errs.append(f"{i}: SS transition >= melting point")
    if not r["T_heat_C"] and not r["dH_heat_Jg"]: errs.append(f"{i}: no T or dH")
print(f"{len(rows)} rows checked, {len(errs)} problems")
for e in errs: print(" -", e)
sys.exit(1 if errs else 0)
