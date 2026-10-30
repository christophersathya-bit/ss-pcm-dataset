"""Builds data/ss_pcm_dataset.csv from the curated records below.
Edit RECORDS (or the CSV directly) to add entries."""
import csv, pathlib

COLS = ["id","material_name","abbreviation","formula","class","subclass","transition",
        "T_heat_C","T_cool_C","T_type","dH_heat_Jg","dH_cool_Jg","molar_mass_gmol",
        "melting_point_C","volume_change_pct","notes","reference","doi","source_url","verification_status"]

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
    transition="tetragonal -> cubic (plastic)", T_heat_C=K(458.3), T_type="calorimetric transition T", dH_heat_Jg=jg(40.5,136.15),
    molar_mass_gmol=136.15, melting_point_C=260, notes="40.5 kJ/mol. Other NIST-listed values 35.1-43.9 kJ/mol at 455-461 K.",
    reference="Barone & Della Gatta, J. Chem. Soc. Faraday Trans. 86, 75-79 (1990), via NIST WebBook", doi="", source_url="https://webbook.nist.gov/cgi/cbook.cgi?ID=C115775&Mask=4", verification_status=V)
add(material_name="Tris(hydroxymethyl)aminomethane", abbreviation="TAM", formula="C4H11NO3", **{"class":"organic","subclass":"polyalcohol (plastic crystal)"},
    transition="orthorhombic -> cubic (plastic)", T_heat_C=K(407.44), T_type="calorimetric transition T", dH_heat_Jg=jg(33.416,121.14),
    molar_mass_gmol=121.14, melting_point_C=K(443.4), notes="33.416 kJ/mol (bifurcated transition). Murrill & Breed 1970: 34.26 kJ/mol at 405 K.",
    reference="Ying & Lin (1990), via NIST WebBook", doi="", source_url="https://webbook.nist.gov/cgi/cbook.cgi?ID=C77861&Mask=4", verification_status=V)
add(material_name="2-Amino-2-methyl-1,3-propanediol", abbreviation="AMPL", formula="C4H11NO2", **{"class":"organic","subclass":"polyalcohol (plastic crystal)"},
    transition="crystal -> plastic", T_heat_C=K(351.25), T_type="calorimetric transition T", dH_heat_Jg=jg(24.68,105.14),
    molar_mass_gmol=105.14, melting_point_C=110, notes="24.68 kJ/mol. Murrill & Breed 1970: 25.2 kJ/mol at 352 K; Zhang & Yang 1990 split it into two steps (5.0 + 18.5 kJ/mol).",
    reference="Barrio, Font et al., Calorim. Anal. Therm. 22, 291-297 (1991), via NIST WebBook", doi="", source_url="https://webbook.nist.gov/cgi/cbook.cgi?ID=C115695&Mask=4", verification_status=V)

# ---------- Molecular plastic crystals (low T / barocaloric) ----------
for name, f, M, TK, kj, extra, ref, cid in [
    ("Adamantane","C10H16",136.24,208.62,3.376,"Ordered -> plastic fcc","Chang & Westrum (1960)","C281232"),
    ("Cyclohexane","C6H12",84.16,186.1,6.7396,"Phase II -> I (plastic)","Ruehrwein & Huffman (1943)","C110827"),
    ("Carbon tetrachloride","CCl4",153.82,225.35,4.581,"Monoclinic -> plastic; volatile/toxic, research only","Chang & Westrum (1970)","C56235")]:
    add(material_name=name, formula=f, **{"class":"organic","subclass":"molecular plastic crystal"}, transition="ordered -> plastic",
        T_heat_C=K(TK), T_type="equilibrium", dH_heat_Jg=jg(kj,M), molar_mass_gmol=M,
        notes=f"{extra}; {kj} kJ/mol.", reference=f"{ref}, via NIST WebBook", doi="",
        source_url=f"https://webbook.nist.gov/cgi/cbook.cgi?ID={cid}&Mask=4", verification_status=V)

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
    T_heat_C=147, T_type="~420 K (transition region 405-425 K)", dH_heat_Jg=jg(758.4*8.314/1000,234.77), molar_mass_gmol=234.77,
    notes="758.4 R*K = 6.31 kJ/mol (beta/gamma -> alpha). Total incl. pre-transition ~1150 R*K = 9.6 kJ/mol.",
    reference="Shaviv, Westrum et al., J. Chem. Thermodyn. 21, 631-651 (1989)", doi="10.1016/0021-9614(89)90177-8", verification_status=V)
add(material_name="Potassium bifluoride", formula="KHF2", **{"class":"inorganic","subclass":"ionic salt"}, transition="tetragonal -> cubic",
    T_heat_C=196, T_type="transition", dH_heat_Jg=135, molar_mass_gmol=78.10, melting_point_C=239,
    notes="Corrosive/HF hazard. No primary source found yet; candidate: Westrum & Pitzer, JACS 71, 1940 (1949), doi:10.1021/ja01174a012 (not checked).",
    reference="Unsourced typical value", doi="", verification_status=U)

# ---------- Metal oxides / metals ----------
add(material_name="Vanadium dioxide", formula="VO2", **{"class":"inorganic","subclass":"metal-insulator transition oxide"},
    transition="monoclinic -> rutile (MIT)", T_heat_C=68, T_type="Tc", dH_heat_Jg=45, molar_mass_gmol=82.94,
    notes="~45 J/g is quoted by Muramoto 2020 from their 2018 work. Takai et al. RSC Adv. 2018 (doi:10.1039/c8ra02159g) measured 17.8 J/g for commercial VO2 and 21.6 J/g for milled VO2. T tunable by W doping.",
    reference="Muramoto et al., Front. Mater. 7 (2020)", doi="10.3389/fmats.2020.00005", verification_status=V)
add(material_name="Nickel-titanium (nitinol)", formula="NiTi (~50:50 at%)", **{"class":"metallic","subclass":"shape-memory alloy"},
    transition="martensite -> austenite", T_heat_C=57, T_cool_C=35, T_type="DSC peak, 10 C/min (cooling = A -> R-phase)", dH_heat_Jg=13.46, dH_cool_Jg=4.6,
    notes="Commercial NiTi. Survey of >75 NiTi alloys: -50 to 330 C, 9.1-35.1 J/g.",
    reference="Sharar et al., Solid-State Thermal Energy Storage Using Reversible Martensitic Transformations (Appl. Phys. Lett.)", doi="",
    source_url="https://arxiv.org/abs/1901.06990", verification_status=V)

out = pathlib.Path(__file__).resolve().parent.parent/"data"/"ss_pcm_dataset.csv"
with open(out,"w",newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader()
    for i,r in enumerate(R,1):
        r["id"]=f"SSPCM-{i:04d}"; w.writerow({c:r.get(c,"") for c in COLS})
print(f"wrote {len(R)} rows -> {out}")
