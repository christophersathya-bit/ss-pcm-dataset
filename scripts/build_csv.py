"""Builds data/ss_pcm_dataset.csv from the curated records below.
Edit RECORDS (or the CSV directly) to add entries."""
import csv, pathlib

COLS = ["id","material_name","abbreviation","formula","class","subclass","transition",
        "T_heat_C","T_cool_C","T_type","dH_heat_Jg","dH_cool_Jg","molar_mass_gmol",
        "melting_point_C","volume_change_pct","notes","reference","doi","verification_status"]

V, U = "verified", "to_verify"
def K(t): return round(t-273.15,1)
def jg(kjmol, M): return round(kjmol*1000/M,1)

R = []
def add(**kw): R.append(kw)

# ---------- Polyalcohols / plastic crystals ----------
add(material_name="Neopentyl glycol", abbreviation="NPG", formula="C5H12O2", **{"class":"organic","subclass":"polyalcohol (plastic crystal)"},
    transition="monoclinic -> cubic (plastic)", T_heat_C=K(314), T_type="onset (heating)", dH_heat_Jg=121, dH_cool_Jg=110,
    molar_mass_gmol=104.15, melting_point_C=128, volume_change_pct=4.9,
    notes="Colossal barocaloric; dT/dp ~103 K/GPa. Prior lit. 123-131 J/g.",
    reference="Lloveras et al., Nat. Commun. 10, 1803 (2019)", doi="10.1038/s41467-019-09730-9", verification_status=V)
add(material_name="Pentaglycerine (trimethylolethane)", abbreviation="PG / TME", formula="C5H12O3", **{"class":"organic","subclass":"polyalcohol (plastic crystal)"},
    transition="crystal -> plastic", T_heat_C=81, T_type="peak (heating)", dH_heat_Jg=192, T_cool_C=71,
    molar_mass_gmol=120.15, melting_point_C=198, volume_change_pct=5.4,
    notes="Same paper also quotes 175 J/g; lit. range 166-193 J/g. Cooling T 68-74 C (lit.).",
    reference="Serrano et al., J. Energy Storage 55, 105677 (2022)", doi="10.1016/j.est.2022.105677", verification_status=V)
add(material_name="Pentaerythritol", abbreviation="PE", formula="C5H12O4", **{"class":"organic","subclass":"polyalcohol (plastic crystal)"},
    transition="tetragonal -> cubic (plastic)", T_heat_C=186, T_type="peak (heating)", dH_heat_Jg=269,
    molar_mass_gmol=136.15, melting_point_C=260, notes="Lit. range ~184-188 C, 255-303 J/g. Serrano 2022 confirms T~180 C.",
    reference="Typical literature value (polyalcohol SS-PCM reviews)", doi="", verification_status=U)
add(material_name="Tris(hydroxymethyl)aminomethane", abbreviation="TAM", formula="C4H11NO3", **{"class":"organic","subclass":"polyalcohol (plastic crystal)"},
    transition="orthorhombic -> cubic (plastic)", T_heat_C=133, T_type="peak (heating)", dH_heat_Jg=285,
    molar_mass_gmol=121.14, melting_point_C=172, notes="Lit. range ~131-136 C, 270-296 J/g.",
    reference="Typical literature value (polyalcohol SS-PCM reviews)", doi="", verification_status=U)
add(material_name="2-Amino-2-methyl-1,3-propanediol", abbreviation="AMPL", formula="C4H11NO2", **{"class":"organic","subclass":"polyalcohol (plastic crystal)"},
    transition="crystal -> plastic", T_heat_C=78, T_type="peak (heating)", dH_heat_Jg=264,
    molar_mass_gmol=105.14, melting_point_C=110, notes="Lit. values vary widely (~220-270 J/g); check primary source.",
    reference="Typical literature value (polyalcohol SS-PCM reviews)", doi="", verification_status=U)

# ---------- Molecular plastic crystals (low T / barocaloric) ----------
for name, f, M, TK, kj, extra in [
    ("Adamantane","C10H16",136.24,208.6,3.38,"Ordered -> plastic fcc; reference plastic crystal"),
    ("Cyclohexane","C6H12",84.16,186.1,6.74,"Phase II -> I (plastic)"),
    ("Carbon tetrachloride","CCl4",153.82,225.5,4.58,"Monoclinic -> plastic; volatile/toxic, research only")]:
    add(material_name=name, formula=f, **{"class":"organic","subclass":"molecular plastic crystal"}, transition="ordered -> plastic",
        T_heat_C=K(TK), T_type="equilibrium", dH_heat_Jg=jg(kj,M), molar_mass_gmol=M,
        notes=f"{extra}; {kj} kJ/mol (thermochemical tables).", reference="Standard thermochemical data (e.g., NIST WebBook)", doi="", verification_status=U)

# ---------- Polymeric (PEG-based) ----------
sr = [("M.CO",110.6,52.84,109.4,29.12),("M.COM",115.7,51.65,112.4,27.85),("M.COT",117.9,51.67,114.8,27.04),
      ("H.CO",117.8,52.16,115.2,27.26),("H.COM",124.5,52.00,119.8,27.26),("H.COT",126.5,52.54,122.0,27.23)]
for s,hh,th,hc,tc in sr:
    add(material_name=f"PEG4000 bio-polyurethane, castor-oil hyperbranched polyol crosslinked ({s})", abbreviation=s,
        formula="PEG4000-PU (crosslinked)", **{"class":"polymer","subclass":"PEG-polyurethane (crosslinked)"},
        transition="PEG soft-segment crystalline -> amorphous", T_heat_C=th, T_cool_C=tc, T_type="DSC Tm/Tf (avg of 5 scans)",
        dH_heat_Jg=hh, dH_cool_Jg=hc, notes="Pristine PEG4000: 206.5 J/g @ 61.0 C (solid-liquid).",
        reference="Sci. Rep. 12, 14646 (2022)", doi="10.1038/s41598-022-17390-x", verification_status=V)
rsc = [("NPU-6000",136.5,55.8,128.0,27.7,"PEG6000"),("BPU-6000",86.0,43.4,83.1,24.5,"PEG6000"),
       ("NPU-10000",137.5,55.7,129.8,33.6,"PEG10000"),("BPU-10000",114.9,52.8,111.2,28.8,"PEG10000")]
for s,hh,th,hc,tc,peg in rsc:
    add(material_name=f"{peg} polyurethane, N-methyldiethanolamine-extended ({s})", abbreviation=s,
        formula=f"{peg}-PU (90 wt% PEG)", **{"class":"polymer","subclass":"PEG-polyurethane"},
        transition="PEG soft-segment crystalline -> amorphous", T_heat_C=th, T_cool_C=tc, T_type="peak, DSC 10 C/min",
        dH_heat_Jg=hh, dH_cool_Jg=hc, notes="90 wt% PEG.", reference="Cao et al., RSC Adv. (2017)", doi="10.1039/c7ra00405b", verification_status=V)

# ---------- Layered organic-inorganic perovskites ----------
add(material_name="Bis(docosylammonium) tetrachlorocuprate", abbreviation="(C22)2CuCl4", formula="(C22H45NH3)2CuCl4",
    **{"class":"organometallic","subclass":"layered hybrid perovskite"}, transition="alkyl-chain order-disorder (multiple steps)",
    T_heat_C=110, T_type="main transition", notes="Several steps of ~15-40 J/g each in ~30 C window; dV/V ~3%. Totals in SI Table S6.",
    volume_change_pct=3, reference="Prats et al., Mater. Chem. Front. (2025)", doi="10.1039/d5qm00712g", verification_status=V)
add(material_name="Bis(docosylammonium) tetrabromocuprate", abbreviation="(C22)2CuBr4", formula="(C22H45NH3)2CuBr4",
    **{"class":"organometallic","subclass":"layered hybrid perovskite"}, transition="alkyl-chain order-disorder",
    T_heat_C=101, T_type="main transition", dH_heat_Jg=67, volume_change_pct=6, notes="Hysteresis 0.1-1 C.",
    reference="Prats et al., Mater. Chem. Front. (2025)", doi="10.1039/d5qm00712g", verification_status=V)
add(material_name="Bis(hexadecylammonium) tetrabromocuprate", abbreviation="(C16)2CuBr4", formula="(C16H33NH3)2CuBr4",
    **{"class":"organometallic","subclass":"layered hybrid perovskite"}, transition="alkyl-chain order-disorder",
    dH_heat_Jg=57, volume_change_pct=6, notes="57 J/g solution-synthesised; 47 J/g ball-milled. T only in figure.",
    reference="Prats et al., Mater. Chem. Front. (2025)", doi="10.1039/d5qm00712g", verification_status=V)

# ---------- Inorganic salts ----------
add(material_name="Lithium sulfate", formula="Li2SO4", **{"class":"inorganic","subclass":"superionic sulfate"},
    transition="monoclinic -> cubic (superionic)", T_heat_C=578, T_type="transition", dH_heat_Jg=252, molar_mass_gmol=109.94,
    melting_point_C=859, notes="Some sources ~214-230 J/g.", reference="CIC energiGUNE (2021) summary of Doppiu et al.", doi="10.3390/ma12223658", verification_status=V)
add(material_name="Lithium sodium sulfate", abbreviation="LiNaSO4", formula="LiNaSO4", **{"class":"inorganic","subclass":"superionic sulfate"},
    transition="beta -> alpha (superionic)", T_heat_C=515, T_type="transition", dH_heat_Jg=160, molar_mass_gmol=126.0,
    notes="Theoretical 318 J/g; other lit. 158-165 J/g; 520 C quoted elsewhere.", reference="Doppiu et al., Materials 12, 3658 (2019)", doi="10.3390/ma12223658", verification_status=V)
add(material_name="Li2SO4-Na2SO4 eutectoid (79/21 mol%)", formula="Li2SO4/Na2SO4", **{"class":"inorganic","subclass":"superionic sulfate (eutectoid)"},
    transition="eutectoid", T_heat_C=470, T_type="onset (heating)", dH_heat_Jg=185, notes="Theoretical 270 J/g; 475 C quoted elsewhere.",
    reference="Doppiu et al., Materials 12, 3658 (2019)", doi="10.3390/ma12223658", verification_status=V)
add(material_name="Silver iodide", formula="AgI", **{"class":"inorganic","subclass":"superionic halide"}, transition="beta/gamma -> alpha (superionic)",
    T_heat_C=147, T_type="transition", dH_heat_Jg=jg(6.15,234.77), molar_mass_gmol=234.77, notes="~6.15 kJ/mol.",
    reference="Typical literature value", doi="", verification_status=U)
add(material_name="Potassium bifluoride", formula="KHF2", **{"class":"inorganic","subclass":"ionic salt"}, transition="tetragonal -> cubic",
    T_heat_C=196, T_type="transition", dH_heat_Jg=135, molar_mass_gmol=78.10, melting_point_C=239,
    notes="Corrosive/HF hazard. Latent heat approximate - verify.", reference="Typical literature value", doi="", verification_status=U)

# ---------- Metal oxides / metals ----------
add(material_name="Vanadium dioxide", formula="VO2", **{"class":"inorganic","subclass":"metal-insulator transition oxide"},
    transition="monoclinic -> rutile (MIT)", T_heat_C=68, T_type="transition", dH_heat_Jg=51, molar_mass_gmol=82.94,
    notes="T tunable by W doping.", reference="Typical literature value", doi="", verification_status=U)
add(material_name="Nickel-titanium (nitinol)", formula="NiTi (~50:50 at%)", **{"class":"metallic","subclass":"shape-memory alloy"},
    transition="martensite -> austenite", T_heat_C=70, T_type="Af (composition dependent)", dH_heat_Jg=24,
    notes="Transition T range ~ -50 to 110 C with composition; high thermal conductivity.", reference="Typical literature value", doi="", verification_status=U)
add(material_name="Iron", formula="Fe", **{"class":"metallic","subclass":"pure metal allotrope"}, transition="alpha (bcc) -> gamma (fcc)",
    T_heat_C=912, T_type="equilibrium", dH_heat_Jg=jg(0.9,55.85), molar_mass_gmol=55.85, notes="~0.9 kJ/mol; low latent heat, reference only.",
    reference="Standard thermochemical data", doi="", verification_status=U)

out = pathlib.Path(__file__).resolve().parent.parent/"data"/"ss_pcm_dataset.csv"
with open(out,"w",newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader()
    for i,r in enumerate(R,1):
        r["id"]=f"SSPCM-{i:04d}"; w.writerow({c:r.get(c,"") for c in COLS})
print(f"wrote {len(R)} rows -> {out}")
