"""Builds cfd/cfd_properties.csv: one row per material with the inputs a conduction/phase-change
CFD model needs. Transition data come from data/ss_pcm_dataset.csv; density and conductivity
are added only where a source gives them (others left blank)."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(ROOT/"data"/"ss_pcm_dataset.csv")))
BEN = ("Benson & Christensen, SERI/TP-255-2494 (1984), Table 4 (OCR; check scan)", "https://nrel.gov/docs/legosti/old/2494.pdf")
AKB = ("Akbulut et al., J. Phys. Chem. Solids 70, 72 (2009), doi:10.1016/j.jpcs.2008.09.001 (solid near melting, i.e. high-T phase)", "https://doi.org/10.1016/j.jpcs.2008.09.001")
SAL = ("Salgado-Pizarro et al., J. Mater. Chem. A (2024), doi:10.1039/d4ta01060d (XRD-calculated, 100 K)", "https://doi.org/10.1039/d4ta01060d")
WIKI = lambda page: ("Wikipedia infobox, room-temperature solid (secondary source; confirm in a handbook)", f"https://en.wikipedia.org/wiki/{page}")
# abbreviation or material_name -> sourced density (rho_*) and conductivity (k_*) per phase; each with its own source
THERMO = {
 "NPG": dict(rho_low=1046, rho_low_T_C=27, rho_high=984, rho_high_T_C=60, rho_src=BEN, k_low=0.253, k_high=0.209, k_src=BEN,
             note="Akbulut 2009: k = 0.22 W/m/K near melting (high-T phase). Lloveras 2019: rho 1064 kg/m3 at ~320 K, dV/V ~4.9%."),
 "PE":  dict(rho_low=1333, rho_low_T_C=170, rho_high=1218, rho_high_T_C=205, rho_src=BEN, k_low=1.0, k_high=0.508, k_src=BEN,
             note="Report gives rho 1342-1323 and k 0.963-1.07 at 170 C; midpoints used. Wikipedia room-T rho 1396 kg/m3. NIST Cp 254.4 J/mol/K at 373 K (Nitta, Seki et al.)."),
 "PG / TME": dict(rho_low=1193, rho_low_T_C=65, rho_high=1118, rho_high_T_C=95, rho_src=BEN, k_low=0.361, k_high=0.335, k_src=BEN,
             note="Serrano et al. 2022: true density 1188-1230 kg/m3 (room T). Wikipedia: 1220 kg/m3."),
 "AMPL": dict(k_high=0.45, k_src=AKB, note="AMPL-NPG alloy (42.2 mol% NPG): k = 0.32 W/m/K (Akbulut 2009)."),
 "TAM": dict(rho_low=1328, rho_low_T_C=25, rho_src=WIKI("Tris")),
 "Adamantane": dict(rho_high=1070, rho_high_T_C=25, rho_src=WIKI("Adamantane"), note="At 25 C adamantane is already in its high-T (plastic) phase."),
 "Carbon tetrabromide": dict(rho_low=3420, rho_low_T_C=25, rho_src=WIKI("Carbon_tetrabromide")),
 "Hexachloroethane": dict(rho_low=2091, rho_low_T_C=25, rho_src=WIKI("Hexachloroethane")),
 "Silver iodide": dict(rho_low=5680, rho_low_T_C=25, rho_src=WIKI("Silver_iodide")),
 "Potassium bifluoride": dict(rho_low=2370, rho_low_T_C=25, rho_src=WIKI("Potassium_bifluoride")),
 "Vanadium dioxide": dict(rho_low=4571, rho_low_T_C=25, rho_high=4653, rho_src=WIKI("Vanadium(IV)_oxide"), note="rho_high is the tetragonal (rutile) phase."),
 "Nickel-titanium (nitinol)": dict(rho_low=6450, rho_high=6450, rho_src=WIKI("Nickel_titanium"), k_low=8.6, k_high=18.0, k_src=WIKI("Nickel_titanium"),
             note="k: martensite 0.086, austenite 0.18 W/cm/K (Wikipedia infobox)."),
 "Lithium sulfate": dict(rho_low=2221, rho_low_T_C=25, rho_src=WIKI("Lithium_sulfate")),
 "(C12)2MnCl4": dict(rho_low=1229, rho_low_T_C=-173, rho_src=SAL, note="Composites with graphite in PDMS/resin: k ~0.2-0.3 W/m/K (Delgado-Ferreiro et al. 2025, doi:10.1039/d5ta04364f)."),
}
PEG_NOTE = "Pristine linear PEG 1000-20000: k = 0.29-0.34 W/m/K at 298 K (Kou et al., J. Chem. Thermodyn. 128, 259 (2019), doi:10.1016/j.jct.2018.08.031); PU value not measured."
NIST2 = lambda cid: f"https://webbook.nist.gov/cgi/cbook.cgi?ID={cid}&Mask=2"
# abbreviation -> (Cp,solid J/mol/K, T K, reference, NIST id, molar mass)  low-T phase, from NIST WebBook
CP = {"NPG":(183.18,298.15,"Zhang, Zou et al.","C126307",104.15), "PE":(190.41,298.15,"Westrum","C115775",136.15),
      "PG / TME":(182.6,299.15,"Suenaga, Matsuo et al.","C77850",120.15), "TAM":(171.27,298.15,"Ying and Lin","C77861",121.14),
      "AMPL":(161.37,301.4,"Zhang and Yang (1990)","C115695",105.14)}
COLS = ["id","material_name","abbreviation","class","T_transition_heat_C","T_transition_cool_C","T_type","hysteresis_K",
        "latent_heat_heat_Jkg","latent_heat_cool_Jkg","rho_low_kgm3","rho_low_T_C","rho_high_kgm3","rho_high_T_C",
        "k_low_WmK","k_high_WmK","cp_low_JkgK","cp_low_T_C","cp_high_JkgK","cp_source","cp_source_url","T_melt_C","volume_change_pct",
        "transition_source","rho_source","rho_source_url","k_source","k_source_url","notes","verification_status"]
out=[]
for r in rows:
    if r["class"]=="polymer" and False: pass
    th = THERMO.get(r["abbreviation"]) or THERMO.get(r["material_name"], {})
    Th, Tc = r["T_heat_C"], r["T_cool_C"]
    hyst = round(float(Th)-float(Tc),2) if Th and Tc else ""
    out.append(dict(id=r["id"], material_name=r["material_name"], abbreviation=r["abbreviation"], **{"class":r["class"]},
        T_transition_heat_C=Th, T_transition_cool_C=Tc, T_type=r["T_type"], hysteresis_K=hyst,
        latent_heat_heat_Jkg=round(float(r["dH_heat_Jg"])*1000) if r["dH_heat_Jg"] else "",
        latent_heat_cool_Jkg=round(float(r["dH_cool_Jg"])*1000) if r["dH_cool_Jg"] else "",
        rho_low_kgm3=th.get("rho_low",""), rho_low_T_C=th.get("rho_low_T_C",""), rho_high_kgm3=th.get("rho_high",""), rho_high_T_C=th.get("rho_high_T_C",""),
        k_low_WmK=th.get("k_low",""), k_high_WmK=th.get("k_high",""), cp_low_JkgK=round(CP[r["abbreviation"]][0]/CP[r["abbreviation"]][4]*1000) if r["abbreviation"] in CP else "",
        cp_low_T_C=round(CP[r["abbreviation"]][1]-273.15,1) if r["abbreviation"] in CP else "", cp_high_JkgK="",
        cp_source=(CP[r["abbreviation"]][2]+", via NIST WebBook") if r["abbreviation"] in CP else "",
        cp_source_url=NIST2(CP[r["abbreviation"]][3]) if r["abbreviation"] in CP else "",
        T_melt_C=r["melting_point_C"], volume_change_pct=r["volume_change_pct"],
        transition_source=r["doi"] or r["source_url"],
        rho_source=th.get("rho_src",("",""))[0], rho_source_url=th.get("rho_src",("",""))[1],
        k_source=th.get("k_src",("",""))[0], k_source_url=th.get("k_src",("",""))[1],
        notes=(th.get("note","") + (" " + PEG_NOTE if r["class"]=="polymer" else "")).strip(), verification_status=r["verification_status"]))
with open(ROOT/"cfd"/"cfd_properties.csv","w",newline="") as fh:
    w=csv.DictWriter(fh, fieldnames=COLS); w.writeheader(); w.writerows(out)
print(len(out),"rows;", sum(1 for o in out if o["rho_low_kgm3"] or o["rho_high_kgm3"]), "with density;", sum(1 for o in out if o["k_low_WmK"] or o["k_high_WmK"]), "with conductivity")
