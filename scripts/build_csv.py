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

# =====================  v0.3 additions  =====================
N = "needs_check"   # source identified, but value derived or read from OCR / unpublished draft; confirm in the original

# ---------- Layered perovskites (n-CnH2n+1NH3)2MCl4 -- values as compiled in review Table 3 ----------
ZHOU = dict(reference="Zhou, Zhang & Fang, Chem. Ind. Eng. Prog. 40(3), 1371-1383 (2021), Table 3 (review; primary refs [6],[57])",
            doi="10.16085/j.issn.1000-6613.2020-0875", verification_status=V)
for n, M_, Ts, Hs, Tm, Hm in [
    (12,"Zn",[88.23],[105.01],None,None),
    (12,"Co",[63.85,67.85],[33.72,59.30],None,None),
    (12,"Mn",[53.85,55.85],[74.31,6.59],None,None),
    (10,"Cu",[33.77],[55.13],36.91,7.53),
    (10,"Zn",[80.14],[82.90],162.79,18.14),
    (10,"Cd",[27.0,61.0],[34.5,8.25],121.0,13.13),
    (10,"Hg",[36.73],[28.02],203.0,50.42),
    (10,"Mn",[32.80],[77.44],None,None),
    (10,"Co",[77.71],[74.38],165.0,13.70)]:
    main = Ts[Hs.index(max(Hs))]
    note = "; ".join(f"{t} C: {h} J/g" for t,h in zip(Ts,Hs))
    if len(Ts)>1: note = "Multiple SS transitions (" + note + "); dH = sum, T = largest peak."
    else: note = "Single SS transition."
    if Tm and main >= Tm: note += f" Listed melting {Tm} C ({Hm} J/g) is close to the SS transition."
    add(material_name=f"Bis(n-alkylammonium) tetrachloro-{M_} (C{n})", abbreviation=f"(C{n})2{M_}Cl4",
        formula=f"(C{n}H{2*n+1}NH3)2{M_}Cl4", **{"class":"organometallic","subclass":"layered hybrid perovskite"},
        transition="alkyl-chain order-disorder", T_heat_C=main, T_type="as listed in review", dH_heat_Jg=round(sum(Hs),2),
        melting_point_C=Tm or "", notes=note + (f" Melting enthalpy {Hm} J/g." if Hm else ""), **ZHOU)
add(material_name="Bis(n-decylammonium) tetrachloronickelate (C10)", abbreviation="(C10)2NiCl4", formula="(C10H21NH3)2NiCl4",
    **{"class":"organometallic","subclass":"layered hybrid perovskite"}, transition="alkyl-chain order-disorder (two steps)",
    T_heat_C=32.0, T_type="as listed in review (second step 58.0 C)", dH_heat_Jg=15.2, melting_point_C=135.0,
    notes="Review prints one enthalpy (15.2 J/g) for two transitions (32, 58 C); assignment unclear. Melting 65.76 J/g.", **ZHOU)

# ---------- Plastic crystals: T and transition entropy from Li et al. (Table S2); dH = T*dS (derived) ----------
LI = dict(reference="Li et al., Colossal barocaloric effects in plastic crystals (Nature 2019), Suppl. Table S2; dH derived as T*dS",
          doi="", source_url="https://arxiv.org/abs/1808.07834", verification_status=N)
for name, f, M_, TK, dS in [
    ("Carbon tetrabromide","CBr4",331.63,320,20.82),
    ("Hexachloroethane","C2Cl6",236.74,344.6,23.84),
    ("Cyclohexanol","C6H12O",100.16,263,35.16),
    ("Pivalic acid (2,2-dimethylpropanoic acid)","C5H10O2",102.13,280,36.15),
    ("2-Methyl-2-nitro-1-propanol","C4H9NO3",119.12,308,55.62),
    ("2-Methyl-2-nitro-1,3-propanediol","C4H9NO4",135.12,352,73.19),
    ("Tris(hydroxymethyl)acetic acid","C5H10O5",150.13,397,77.37),
    ("Fullerene C60","C60",720.66,260,30.0)]:
    add(material_name=name, formula=f, **{"class":"organic","subclass":"molecular plastic crystal"}, transition="ordered -> plastic",
        T_heat_C=K(TK), T_type="transition T (table)", dH_heat_Jg=round(TK*dS/M_,1), molar_mass_gmol=M_,
        notes=f"dS = {dS} J/mol/K (table); dH = T*dS = {TK*dS/1000:.2f} kJ/mol.", **LI)

# ---------- Barocaloric 1-X-adamantanes (author manuscript values) ----------
AZ = dict(reference="Aznar et al., Appl. Mater. Today 23, 101023 (2021) - values from author manuscript table",
          doi="10.1016/j.apmt.2021.101023", verification_status=N)
add(material_name="1-Chloroadamantane", abbreviation="1-Cl-ada", formula="C10H15Cl", **{"class":"organic","subclass":"molecular plastic crystal (barocaloric)"},
    transition="ordered -> plastic", T_heat_C=K(254), T_cool_C=K(245), T_type="I<->II at 1 atm (heating/cooling assignment inferred)",
    dH_heat_Jg=32.0, dH_cool_Jg=31.5, molar_mass_gmol=170.68, notes="dT/dp ~27 K/kbar; dS ~132-136 J/K/kg. Confirm in published version.", **AZ)
add(material_name="1-Bromoadamantane", abbreviation="1-Br-ada", formula="C10H15Br", **{"class":"organic","subclass":"molecular plastic crystal (barocaloric)"},
    transition="ordered -> plastic", T_heat_C=K(316), T_cool_C=K(308), T_type="I<->II at 1 atm (heating/cooling assignment inferred)",
    dH_heat_Jg=32.0, dH_cool_Jg=31.0, molar_mass_gmol=215.13, notes="dT/dp ~33-36 K/kbar; dS ~102-104 J/K/kg. Confirm in published version.", **AZ)

# ---------- Polyalcohol mixtures ----------
BEN = dict(reference="Benson & Christensen, SERI/TP-255-2494 (1984), Table 2 (OCR of scanned report)",
           doi="", source_url="https://nrel.gov/docs/legosti/old/2494.pdf", verification_status=N)
for pe, tme, npg, T, H in [(10,80,10,79,15.6),(10,45,45,79,10.7),(15,70,15,74,15.5),(15,15,70,17,6.32),(25,50,25,73,15.8),
                           (25,25,50,64,8.08),(30,60,10,94,18.2),(30,10,60,127,4.69),(33.3,33.3,33.3,79,14.2),
                           (45,45,10,109,21.8),(45,10,45,140,12.2),(50,25,25,134,18.1),(70,15,15,158,25.9)]:
    Mmix = (pe*136.15 + tme*120.15 + npg*104.15)/(pe+tme+npg)
    add(material_name=f"PE/TME/NPG ternary ({pe}/{tme}/{npg} mol%)", abbreviation=f"PE-TME-NPG {pe}/{tme}/{npg}",
        formula="C5H12O4 / C5H12O3 / C5H12O2", **{"class":"organic","subclass":"polyalcohol mixture"},
        transition="solid-solid (mixture)", T_heat_C=T, T_type="as reported", dH_heat_Jg=round(H*1000/Mmix,1), molar_mass_gmol=round(Mmix,2),
        notes=f"{H} kJ/mol of mixture. Column order PE/TME/NPG inferred from table header; check the scanned table.", **BEN)
MSF = dict(reference="Binary Mixture of Solid-Solid PCM: Synthesis, Characterization and Experimental Study, Mater. Sci. Forum 978, 407-420 (2020)",
           doi="", source_url="https://www.scientific.net/MSF.978.407", verification_status=V)
for wt, th, hh, tc, hc in [(2,41.2,121,28.5,106),(6,43.1,133,28.2,119)]:
    add(material_name=f"NPG + {wt} wt% PE", abbreviation=f"NPG-PE{wt}", formula="C5H12O2 + C5H12O4",
        **{"class":"organic","subclass":"polyalcohol mixture"}, transition="solid-solid (mixture)",
        T_heat_C=th, T_cool_C=tc, T_type="as reported (abstract)", dH_heat_Jg=hh, dH_cool_Jg=hc, notes="Composition wording in abstract is ambiguous about the base component.", **MSF)

# =====================  v0.5 additions: new classes  =====================
# ---------- Ionic plastic crystals / organic salts ----------
LM = dict(reference="Lopez-Morales et al., J. Energy Storage 72, 108379 (2023)", doi="10.1016/j.est.2023.108379", verification_status=V)
for an, T, H, Tm, Td, extra in [("NO3",41.4,156.6,167.0,201.9,"latent heat loss ~1% after 50 cycles; 162.5 J/cm3"),
                                ("Cl",20.0,101.2,234.1,229.5,"3.6% loss after 50 cycles; 91.9 J/cm3"),
                                ("FOR",29.7,58.4,58.6,139.4,"formate; 6.2% loss after 50 cycles; SS transition very close to melting")]:
    add(material_name=f"Protic dialkylammonium salt [DOA][{an}]", abbreviation=f"[DOA][{an}]", formula=f"[DOA][{an}]",
        **{"class":"ionic","subclass":"protic ionic plastic crystal (OIPC)"}, transition="solid-solid (two steps)",
        T_heat_C=T, T_type="onset (heating), DSC 5 C/min", dH_heat_Jg=H, melting_point_C=Tm,
        notes=f"dH = sum of two SS peaks. Decomposition onset {Td} C; {extra}. DOA cation as named in source; k 0.18-0.37 W/m/K across the series.", **LM)
add(material_name="Methylammonium tetrafluoroborate", abbreviation="[MA][BF4]", formula="CH6BF4N",
    **{"class":"ionic","subclass":"ionic plastic crystal"}, transition="ordered -> plastic", T_heat_C=K(254), T_cool_C=K(243),
    T_type="DSC peak (heating/cooling)", dH_heat_Jg=42, molar_mass_gmol=118.87, volume_change_pct=7.5,
    notes="Stable to ~400 K (TGA). Literature (Yamamuro): 252 K, 43.49 J/g. dT/dp ~25 K/kbar.",
    reference="Dafonte-Rodriguez et al., Inorg. Chem. Front. (2026)", doi="10.1039/D6QI00156D", verification_status=V)
SAV = dict(reference="Salvatori et al., J. Mater. Chem. A 11, 12140 (2023), Table 1; dH derived as T*dS", doi="10.1039/D2TA10033A", verification_status=N)
add(material_name="Quinuclidinium perrhenate", abbreviation="HQuin-ReO4", formula="C7H14NO4Re", **{"class":"ionic","subclass":"ferroelectric molecular-ionic plastic crystal"},
    transition="III -> II (main); II -> I at 367 K", T_heat_C=K(344), T_cool_C=K(341), T_type="transition (table)", dH_heat_Jg=round(344*59.1/1000,1),
    molar_mass_gmol=362.4, notes="dS 59.1 J/kg/K (III/II) + 15.6 J/kg/K (II/I at 367 K, ~5.7 J/g). dV 0.011 cm3/g.", **SAV)
add(material_name="Tetramethylammonium tetrachloroferrate", abbreviation="TMA-FeCl4", formula="C4H12Cl4FeN", **{"class":"ionic","subclass":"ferroelectric molecular-ionic plastic crystal"},
    transition="II -> I (main); III -> II at 343 K", T_heat_C=K(384), T_cool_C=K(381), T_type="transition (table)", dH_heat_Jg=round(384*58.7/1000,1),
    molar_mass_gmol=271.8, notes="dS 58.7 J/kg/K (II/I) + 8.3 J/kg/K (III/II, ~2.8 J/g). dV 0.021 cm3/g.", **SAV)
add(material_name="Lithium carba-closo-dodecaborate", abbreviation="LiCB11H12", formula="LiCB11H12", **{"class":"ionic","subclass":"carborane salt (plastic crystal)"},
    transition="II -> I order-disorder", T_heat_C=K(390), T_type="DSC, 0 GPa (390 +/- 10 K)", dH_heat_Jg=round(390*208/1000,1), volume_change_pct=13,
    notes="dS ~208 J/kg/K at 1 atm; dH derived as T*dS. Colossal barocaloric; Li-ion diffusion in high-T phase.",
    reference="Zeng et al., Colossal reversible barocaloric effects in a plastic crystal ... (2023)", doi="", source_url="https://arxiv.org/abs/2302.06993", verification_status=N)

# ---------- Spin-crossover ----------
add(material_name="Trinuclear spin-crossover complex Fe3(bntrz)6(tcnset)6", abbreviation="FBT", formula="Fe3(bntrz)6(tcnset)6",
    **{"class":"organometallic","subclass":"spin-crossover complex"}, transition="low spin -> high spin", T_heat_C=K(318), T_cool_C=K(316),
    T_type="DSC peak", dH_heat_Jg=25, notes="25 +/- 2 kJ/kg; dS 80 J/kg/K; hysteresis 2 K; dT/dp 25 K/kbar; dV 2.05e-5 m3/kg.",
    reference="Romanini et al., Adv. Mater. 33, 2008076 (2021)", doi="10.1002/adma.202008076", verification_status=V)

# ---------- More inorganic salts ----------
add(material_name="Ammonium thiocyanate", abbreviation="NH4SCN", formula="CH4N2S", **{"class":"inorganic","subclass":"ammonium salt (order-disorder)"},
    transition="monoclinic -> orthorhombic", T_heat_C=K(364), T_cool_C=K(335), T_type="transition, ambient pressure", dH_heat_Jg=43,
    molar_mass_gmol=76.12, volume_change_pct=5, notes="Barocaloric thermal battery concept; dT/dp ~0.3 K/MPa; dS_max ~129 J/kg/K.",
    reference="Zhang et al., Barocaloric thermal batteries (2021)", doi="", source_url="https://arxiv.org/abs/2103.04348", verification_status=V)

# ---------- NiTi-based shape-memory alloys ----------
add(material_name="NiTi, solution heat-treated (Ni50.28Ti49.36)", abbreviation="Ni50.28Ti49.36-SHT", formula="Ni50.28Ti49.36",
    **{"class":"metallic","subclass":"NiTi-based shape-memory alloy"}, transition="martensite -> austenite", T_heat_C=78, T_cool_C=38,
    T_type="DSC, 10 C/min", dH_heat_Jg=28, notes="Solution annealing raised latent heat from 12 (as-received) to 28 J/g.",
    reference="Sharar et al., High-capacity high-power TES using solid-solid martensitic transformations", doi="", source_url="https://arxiv.org/abs/2011.12339", verification_status=V)
SH = dict(reference="Sharar et al., Suppl. Table S1 (compiled from original literature)", doi="", source_url="https://arxiv.org/abs/1901.06990", verification_status=V)
SMA = [("Ni48.62Ti",90,27),("Ni49.5Ti",91,30.1),("Ni49.6Ti",-3.8,18.3),("Ni49.63Ti",46.7,21.6),("Ni49.68Ti",81.9,31.7),("Ni49.74Ti",86.3,22.9),
 ("Ni50.01Ti",52.7,27),("Ni50.13Ti",-21.9,14.9),("Ni50.17Ti",-39.1,9.1),("Ni50.18Ti",47.2,26.7),("Ni50.21Ti",4.1,16.5),("Ni50.42Ti",17,23.3),
 ("Ni50.49Ti",17.8,23.9),("Ni50.58Ti",-10.8,18.8),
 ("Ni50Ti49.9Cr0.1",89.25,30),("Ni50Ti49.75Cr0.25",63.25,23.7),("Ni50Ti49.5Cr0.5",42.35,23.3),("Ni50Ti49.2Cr0.8",13.05,20.8),("Ni50Ti49Cr1",-12.8,15.2),("Ni50Ti48.75Cr1.25",-46.2,10.1),
 ("Ni50Ti49.9V0.1",101.15,30.1),("Ni50Ti49.75V0.25",82.9,24.9),("Ni50Ti49V1",64.5,23.2),("Ni50Ti48V2",54.7,22.2),("Ni50Ti47V3",35.9,16.9),("Ni50Ti45V5",18.3,12),("Ni50Ti44V6",15.15,10.6),
 ("Ni43Ti52Cu5",73.2,24.2),("Ni43.5Ti51.5Cu5",77.6,24.7),("Ni44Ti51Cu5",77.75,24.1),("Ni44.25Ti50.75Cu5",73.95,25.9),("Ni44.5Ti50.5Cu5",74.75,25.7),("Ni44.6Ti50.4Cu5",77.9,29.1),
 ("Ni44.75Ti50.25Cu5",81.55,23.6),("Ni45Ti50Cu5",80.65,29.3),("Ni45.2Ti49.8Cu5",57.15,25.2),("Ni45.3Ti49.7Cu5",48.4,24.3),("Ni45.7Ti49.3Cu5",30.05,21.7),("Ni45.9Ti49.1Cu5",10.45,14.3),
 ("Ni46.2Ti48.8Cu5",-21.4,14),("Ni47.5Ti50Cu2.5",94.2,31),("Ni42.5Ti50Cu7.5",76.8,27.9),
 ("Ni49.8Ti48.2Hf2",103.5,29.3),("Ni49.8Ti46.2Hf4",114.65,29.1),("Ni49.8Ti44.2Hf6",128.35,29.1),("Ni49.8Ti42.2Hf8",160.2,30.3),
 ("Ni45Ti50Pd5",72.2,25.8),("Ni43Ti50Pd7",66.2,23.8),("Ni41Ti50Pd9",63.25,18.4),("Ni37Ti50Pd13",86.05,16.4),("Ni35Ti50Pd15",99.35,17.7),("Ni33Ti50Pd17",118.45,18.7),
 ("Ni29Ti50Pd21",160.45,21.6),("Ni20Ti50Pd30",267.85,29.7),
 ("Ni49.5Ti49.5Zr1",100.6,30.6),("Ni49.5Ti47.5Zr3",102.7,23.3),("Ni49.5Ti45.5Zr5",104,27),("Ni49.5Ti40.5Zr10",142,27.3),("Ni49.5Ti35.5Zr15",221.65,28.8),("Ni49.5Ti30.5Zr20",322.55,35),
 ("Ni28.5Ti50.5Pt21",330.85,22.4),("Ni43.5Ti50Cu5Co1.5",53.85,25.9),("Ni42Ti50Cu5Co3",30.2,23.8),("Ni40Ti50Cu5Co5",-5.35,21.6),
 ("Ni42.9Ti50Cu5Pd2.1",66.35,14.9),("Ni41.9Ti50Cu5Pd3.1",73.1,16),("Ni39.2Ti50Cu5Pd5.8",67.45,14.2),("Ni38.3Ti50Cu5Pd6.7",65.65,13.6),("Ni32.2Ti50Cu5Pd12.8",59.85,12.3)]
import re as _re
for comp, T, H in SMA:
    els = [e for e in _re.findall(r"[A-Z][a-z]?", comp) if e not in ("Ni","Ti")]
    sub = "NiTi binary" if not els else "NiTi-" + "-".join(els)
    add(material_name=f"{comp} shape-memory alloy", abbreviation=comp, formula=comp, **{"class":"metallic","subclass":f"NiTi-based shape-memory alloy ({sub})"},
        transition="martensite -> austenite", T_heat_C=T, T_type="M->A transition (compiled table)", dH_heat_Jg=H, notes="Composition in at.%.", **SH)

out = pathlib.Path(__file__).resolve().parent.parent/"data"/"ss_pcm_dataset.csv"
with open(out,"w",newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader()
    for i,r in enumerate(R,1):
        r["id"]=f"SSPCM-{i:04d}"; w.writerow({c:r.get(c,"") for c in COLS})
print(f"wrote {len(R)} rows -> {out}")
