"""Builds ml/ files from data/ss_pcm_dataset.csv.
Each SMILES is checked with RDKit: its formula and molar mass must match the dataset row."""
import csv, pathlib, math
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, Crippen
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = {r["id"]: r for r in csv.DictReader(open(ROOT/"data"/"ss_pcm_dataset.csv"))}
by_name = {r["material_name"]: r for r in rows.values()}

SMILES = {  # material_name -> SMILES (pure molecular compounds only)
 "Neopentyl glycol": "CC(C)(CO)CO",
 "Pentaglycerine (trimethylolethane)": "CC(CO)(CO)CO",
 "Pentaerythritol": "OCC(CO)(CO)CO",
 "Tris(hydroxymethyl)aminomethane": "NC(CO)(CO)CO",
 "2-Amino-2-methyl-1,3-propanediol": "CC(N)(CO)CO",
 "Adamantane": "C1C2CC3CC1CC(C2)C3",
 "Cyclohexane": "C1CCCCC1",
 "Carbon tetrachloride": "ClC(Cl)(Cl)Cl",
 "Carbon tetrabromide": "BrC(Br)(Br)Br",
 "Hexachloroethane": "ClC(Cl)(Cl)C(Cl)(Cl)Cl",
 "Cyclohexanol": "OC1CCCCC1",
 "Pivalic acid (2,2-dimethylpropanoic acid)": "CC(C)(C)C(=O)O",
 "2-Methyl-2-nitro-1-propanol": "CC(C)(CO)[N+](=O)[O-]",
 "2-Methyl-2-nitro-1,3-propanediol": "CC(CO)(CO)[N+](=O)[O-]",
 "Tris(hydroxymethyl)acetic acid": "OCC(CO)(CO)C(=O)O",
 "1-Chloroadamantane": "ClC12CC3CC(CC(C3)C1)C2",
 "1-Bromoadamantane": "BrC12CC3CC(CC(C3)C1)C2",
}
COMP = {"PE": SMILES["Pentaerythritol"], "TME": SMILES["Pentaglycerine (trimethylolethane)"], "NPG": SMILES["Neopentyl glycol"]}

def f(x): return float(x) if x not in ("", None) else None
def desc(m):
    return dict(mw=round(Descriptors.MolWt(m),3), heavy_atoms=m.GetNumHeavyAtoms(),
        n_OH=len(m.GetSubstructMatches(Chem.MolFromSmarts("[OX2H]"))),
        n_NH2=len(m.GetSubstructMatches(Chem.MolFromSmarts("[NX3;H2]"))),
        hbd=rdMolDescriptors.CalcNumHBD(m), hba=rdMolDescriptors.CalcNumHBA(m),
        tpsa=round(rdMolDescriptors.CalcTPSA(m),2), rot_bonds=rdMolDescriptors.CalcNumRotatableBonds(m),
        rings=rdMolDescriptors.CalcNumRings(m), frac_sp3=round(rdMolDescriptors.CalcFractionCSP3(m),3),
        logp=round(Crippen.MolLogP(m),3), has_quaternary_C=int(m.HasSubstructMatch(Chem.MolFromSmarts("[CX4;H0]([#6,#7,#8,#17,#35])([#6,#7,#8,#17,#35])([#6,#7,#8,#17,#35])[#6,#7,#8,#17,#35]"))))
def targets(r, M):
    T = f(r["T_heat_C"]); H = f(r["dH_heat_Jg"])
    TK = round(T+273.15,2) if T is not None else None
    Hm = round(H*M/1000,3) if (H is not None and M) else None
    S = round(Hm*1000/TK,2) if (Hm and TK) else None
    return dict(T_trans_K=TK, dH_Jg=H, dH_kJmol=Hm, dS_JmolK=S,
                T_melt_K=round(f(r["melting_point_C"])+273.15,2) if r["melting_point_C"] else "")

# ---- 1) pure molecules ----
mol_rows = []
for name, smi in SMILES.items():
    r = by_name[name]; m = Chem.MolFromSmiles(smi)
    assert m is not None, name
    fm = CalcMolFormula(m).replace("+","").replace("-","")
    assert fm == r["formula"], (name, fm, r["formula"])
    d = desc(m)
    if r["molar_mass_gmol"]: assert abs(d["mw"]-float(r["molar_mass_gmol"]))<0.1, (name, d["mw"])
    mol_rows.append(dict(id=r["id"], name=name, smiles=Chem.MolToSmiles(m), inchikey=Chem.MolToInchiKey(m),
        subclass=r["subclass"], **d, **targets(r, d["mw"]), verification_status=r["verification_status"], doi=r["doi"], source_url=r["source_url"]))
with open(ROOT/"ml"/"molecules.csv","w",newline="") as fh:
    w=csv.DictWriter(fh, fieldnames=list(mol_rows[0])); w.writeheader(); w.writerows(mol_rows)

# ---- 2) layered perovskites: cation SMILES + metal descriptors ----
METAL = {"Cu":(63.546,"Cu2+",0.73),"Zn":(65.38,"Zn2+",0.74),"Mn":(54.938,"Mn2+",0.83),"Co":(58.933,"Co2+",0.745),
         "Cd":(112.41,"Cd2+",0.95),"Hg":(200.59,"Hg2+",1.02),"Ni":(58.693,"Ni2+",0.69)}  # Shannon radii (6-coord, high spin), Angstrom
per_rows=[]
for r in rows.values():
    if r["subclass"]!="layered hybrid perovskite": continue
    import re
    mt = re.match(r"\(C(\d+)H\d+NH3\)2(Cu|Zn|Mn|Co|Cd|Hg|Ni)(Cl|Br)4", r["formula"])
    n, M_, X = int(mt.group(1)), mt.group(2), mt.group(3)
    cat = Chem.MolFromSmiles("C"*n+"[NH3+]")
    Mtot = 2*Descriptors.MolWt(cat) + METAL[M_][0] + 4*(35.453 if X=="Cl" else 79.904)
    per_rows.append(dict(id=r["id"], formula=r["formula"], cation_smiles=Chem.MolToSmiles(cat), n_alkyl=n, metal=M_,
        metal_ionic_radius_A=METAL[M_][2], halide=X, molar_mass_gmol=round(Mtot,2), **targets(r, Mtot),
        verification_status=r["verification_status"], doi=r["doi"]))
with open(ROOT/"ml"/"perovskites.csv","w",newline="") as fh:
    w=csv.DictWriter(fh, fieldnames=list(per_rows[0])); w.writeheader(); w.writerows(per_rows)

# ---- 3) mixtures: component SMILES + mole fractions ----
mix_rows=[]
for r in rows.values():
    if r["subclass"]!="polyalcohol mixture": continue
    if r["abbreviation"].startswith("PE-TME-NPG"):
        x = [float(v)/100 for v in r["abbreviation"].split()[1].split("/")]; s=sum(x); x=[v/s for v in x]
        comps=[("PE",x[0]),("TME",x[1]),("NPG",x[2])]; basis="mol"
    else:
        wt=float(r["abbreviation"].replace("NPG-PE",""))/100; comps=[("NPG",1-wt),("PE",wt)]; basis="wt"
    M_ = f(r["molar_mass_gmol"])
    t = targets(r, M_) if M_ else dict(T_trans_K=round(f(r["T_heat_C"])+273.15,2), dH_Jg=f(r["dH_heat_Jg"]), dH_kJmol="", dS_JmolK="", T_melt_K="")
    d = dict(id=r["id"], name=r["material_name"], fraction_basis=basis)
    for i,(c,v) in enumerate(comps,1): d[f"comp{i}"]=c; d[f"comp{i}_smiles"]=COMP[c]; d[f"comp{i}_frac"]=round(v,4)
    for i in range(len(comps)+1,4): d[f"comp{i}"]=d[f"comp{i}_smiles"]=d[f"comp{i}_frac"]=""
    d.update(t); d.update(verification_status=r["verification_status"], doi=r["doi"], source_url=r["source_url"]); mix_rows.append(d)
with open(ROOT/"ml"/"mixtures.csv","w",newline="") as fh:
    w=csv.DictWriter(fh, fieldnames=list(mix_rows[0])); w.writeheader(); w.writerows(mix_rows)
print(len(mol_rows),"molecules,",len(per_rows),"perovskites,",len(mix_rows),"mixtures")
