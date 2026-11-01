"""Builds cfd/cfd_properties.csv: one row per material with the inputs a conduction/phase-change
CFD model needs. Transition data come from data/ss_pcm_dataset.csv; density and conductivity
are added only where a source gives them (others left blank)."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(ROOT/"data"/"ss_pcm_dataset.csv")))
BEN = ("Benson & Christensen, SERI/TP-255-2494 (1984), Table 4 (OCR; check scan)", "https://nrel.gov/docs/legosti/old/2494.pdf")
# abbreviation -> sourced thermophysical values (low-T phase / high-T phase)
THERMO = {
 "NPG": dict(rho_low=1046, rho_low_T_C=27, rho_high=984, rho_high_T_C=60, k_low=0.253, k_high=0.209, ref=BEN[0], url=BEN[1],
             note="Lloveras et al. 2019 give 1064 kg/m3 at ~320 K and dV/V ~4.9%."),
 "PE":  dict(rho_low=1333, rho_low_T_C=170, rho_high=1218, rho_high_T_C=205, k_low=1.0, k_high=0.508, ref=BEN[0], url=BEN[1],
             note="Report gives rho 1342-1323 and k 0.963-1.07 at 170 C; midpoints used. NIST also lists Cp 254.4 J/mol/K at 373 K (Nitta, Seki et al.)."),
 "PG / TME": dict(rho_low=1193, rho_low_T_C=65, rho_high=1118, rho_high_T_C=95, k_low=0.361, k_high=0.335, ref=BEN[0], url=BEN[1],
             note="Serrano et al. 2022 measured true density 1188-1230 kg/m3 (room T) for pressed/cast PG."),
}
NIST2 = lambda cid: f"https://webbook.nist.gov/cgi/cbook.cgi?ID={cid}&Mask=2"
# abbreviation -> (Cp,solid J/mol/K, T K, reference, NIST id, molar mass)  low-T phase, from NIST WebBook
CP = {"NPG":(183.18,298.15,"Zhang, Zou et al.","C126307",104.15), "PE":(190.41,298.15,"Westrum","C115775",136.15),
      "PG / TME":(182.6,299.15,"Suenaga, Matsuo et al.","C77850",120.15), "TAM":(171.27,298.15,"Ying and Lin","C77861",121.14),
      "AMPL":(161.37,301.4,"Zhang and Yang (1990)","C115695",105.14)}
COLS = ["id","material_name","abbreviation","class","T_transition_heat_C","T_transition_cool_C","T_type","hysteresis_K",
        "latent_heat_heat_Jkg","latent_heat_cool_Jkg","rho_low_kgm3","rho_low_T_C","rho_high_kgm3","rho_high_T_C",
        "k_low_WmK","k_high_WmK","cp_low_JkgK","cp_low_T_C","cp_high_JkgK","cp_source","cp_source_url","T_melt_C","volume_change_pct",
        "transition_source","thermo_source","thermo_source_url","notes","verification_status"]
out=[]
for r in rows:
    if r["class"]=="polymer" and False: pass
    th = THERMO.get(r["abbreviation"], {})
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
        transition_source=r["doi"] or r["source_url"], thermo_source=th.get("ref",""), thermo_source_url=th.get("url",""),
        notes=th.get("note",""), verification_status=r["verification_status"]))
with open(ROOT/"cfd"/"cfd_properties.csv","w",newline="") as fh:
    w=csv.DictWriter(fh, fieldnames=COLS); w.writeheader(); w.writerows(out)
print(len(out),"rows;", sum(1 for o in out if o["rho_low_kgm3"]), "with density/conductivity")
