"""Regenerates figures/*.svg (vector, paper-ready) from data/ss_pcm_dataset.csv.
For PNG, change the extension in the savefig calls."""
import csv, pathlib, collections
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(ROOT/"data"/"ss_pcm_dataset.csv")))
FIG = ROOT/"figures"; FIG.mkdir(exist_ok=True)
INK, INK2, GRID, BLUE, ORANGE, AQUA = "#1f1f1e", "#5f5e5a", "#e6e5e0", "#2a78d6", "#eb6834", "#1baf7a"
plt.rcParams.update({"font.size":10, "axes.edgecolor":INK2, "axes.labelcolor":INK, "xtick.color":INK2, "ytick.color":INK2,
                     "axes.spines.top":False, "axes.spines.right":False, "axes.grid":True, "grid.color":GRID, "grid.linewidth":0.6,
                     "axes.axisbelow":True, "savefig.dpi":160, "svg.fonttype":"none", "svg.hashsalt":"ss-pcm", "savefig.bbox":"tight", "figure.facecolor":"white"})
GROUP = {"polyalcohol (plastic crystal)":"Polyalcohols", "polyalcohol mixture":"Polyalcohol mixtures",
         "molecular plastic crystal":"Plastic crystals", "molecular plastic crystal (barocaloric)":"Plastic crystals",
         "PEG-polyurethane":"PEG-polyurethanes", "PEG-polyurethane (crosslinked)":"PEG-polyurethanes",
         "layered hybrid perovskite":"Layered perovskites"}
def grp(r): return GROUP.get(r["subclass"], "Inorganic & metallic")
ORDER = ["Polyalcohols","Polyalcohol mixtures","Plastic crystals","PEG-polyurethanes","Layered perovskites","Inorganic & metallic"]
pts = [(float(r["T_heat_C"]), float(r["dH_heat_Jg"]), grp(r), r) for r in rows if r["T_heat_C"] and r["dH_heat_Jg"]]

# Fig 1: T vs dH, small multiples (one highlighted group per panel, others as gray context)
fig, axs = plt.subplots(2, 3, figsize=(11, 6.4), sharex=True, sharey=True)
for ax, g in zip(axs.flat, ORDER):
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=14, color="#cfcdc6", lw=0)
    sel = [p for p in pts if p[2]==g]
    ax.scatter([p[0] for p in sel], [p[1] for p in sel], s=34, color=BLUE, edgecolor="white", lw=1.2, zorder=3)
    ax.set_title(f"{g}  (n={len(sel)} plotted)", fontsize=10, color=INK, loc="left")
    ax.set_xlim(-100, 600); ax.set_ylim(0, 320); ax.set_xticks([-100,0,100,200,300,400,500,600])
from matplotlib.lines import Line2D
fig.legend(handles=[Line2D([],[],marker="o",ls="",color=BLUE,markersize=7,label="Materials in this class (panel title)"),
                    Line2D([],[],marker="o",ls="",color="#cfcdc6",markersize=6,label="All other materials (for context)")],
           loc="upper right", ncol=2, frameon=False, bbox_to_anchor=(0.99, 1.0))
for ax in axs[1]: ax.set_xlabel("Transition temperature on heating (°C)")
for ax in axs[:,0]: ax.set_ylabel("Latent heat (J/g)")
fig.suptitle("Solid–solid PCMs: transition temperature vs latent heat", x=0.01, ha="left", fontsize=12, color=INK)
fig.savefig(FIG/"fig1_T_vs_latent_heat.svg"); plt.close(fig)

# Fig 2: entries per class, stacked by verification status
cnt = collections.Counter((grp(r), r["verification_status"]) for r in rows)
fig, ax = plt.subplots(figsize=(8, 3.6)); left = [0]*len(ORDER)
for st, col, lab in [("verified",BLUE,"Verified"),("needs_check",ORANGE,"Needs check"),("to_verify",AQUA,"To verify")]:
    v = [cnt[(g,st)] for g in ORDER]
    ax.barh(ORDER, v, left=left, color=col, edgecolor="white", lw=2, label=lab, height=0.6)
    left = [a+b for a,b in zip(left, v)]
for y, tot in enumerate(left): ax.text(tot+0.3, y, str(tot), va="center", color=INK2, fontsize=9)
ax.invert_yaxis(); ax.set_xlabel("Number of entries"); ax.grid(axis="y", visible=False)
ax.set_xlim(0, 17); ax.legend(frameon=False, loc="lower center", ncol=3, bbox_to_anchor=(0.5, 1.0)); ax.set_title(f"Dataset coverage (n={len(rows)})", loc="left", color=INK, pad=28)
fig.savefig(FIG/"fig2_coverage_by_class.svg"); plt.close(fig)

# Fig 3: PVT window, candidates 20-90 C
cand = sorted([p for p in pts if 20 <= p[0] <= 90], key=lambda p: p[0])
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.axvspan(25, 45, color=BLUE, alpha=0.08, lw=0); ax.axvspan(50, 80, color=ORANGE, alpha=0.08, lw=0)
ax.text(35, 305, "PV cooling\n25–45 °C", ha="center", va="top", color=INK2, fontsize=9)
ax.text(65, 305, "Thermal storage\n50–80 °C", ha="center", va="top", color=INK2, fontsize=9)
safe = lambda r: not any(x in r["formula"] for x in ("Cd","Hg","CBr4","C2Cl6"))
for p in cand:
    ok = safe(p[3])
    ax.scatter(p[0], p[1], s=42, color=BLUE if ok else "#b4b2a9", marker="o" if ok else "x", lw=1.2 if not ok else 1, edgecolor="white" if ok else None, zorder=3)
label = {"NPG":(-6,6),"AMPL":(-8,8),"NPU-10000":(4,6),"NPG-PE6":(4,6),"(C10)2MnCl4":(-6,4),"PE-TME-NPG 10/80/10":(-10,8)}
for p in cand:
    ab = p[3]["abbreviation"]
    if ab in label: ax.annotate(ab, (p[0],p[1]), xytext=label[ab], textcoords="offset points", fontsize=8.5, color=INK, ha="right" if label[ab][0]<0 else "left")
ax.scatter([],[],s=42,color=BLUE,label="Candidate"); ax.scatter([],[],s=42,color="#b4b2a9",marker="x",label="Toxic / hazardous (Cd, Hg, CBr4, C2Cl6)")
ax.legend(frameon=False, loc="upper left", fontsize=8.5, bbox_to_anchor=(0,0.88))
ax.set_xlim(18, 92); ax.set_ylim(0, 320); ax.set_xlabel("Transition temperature on heating (°C)"); ax.set_ylabel("Latent heat (J/g)")
ax.set_title(f"Candidates for photovoltaic-thermal (PVT) systems (n={len(cand)})", loc="left", color=INK)
fig.savefig(FIG/"fig3_pvt_candidates.svg"); plt.close(fig)

# Fig 4: distribution of transition temperatures
T = [float(r["T_heat_C"]) for r in rows if r["T_heat_C"]]
fig, ax = plt.subplots(figsize=(8, 3.4))
ax.hist(T, bins=range(-100, 625, 25), color=BLUE, edgecolor="white", lw=2)
ax.set_xlabel("Transition temperature on heating (°C)"); ax.set_ylabel("Entries"); ax.grid(axis="x", visible=False)
ax.set_title(f"Distribution of transition temperatures (n={len(T)})", loc="left", color=INK)
fig.savefig(FIG/"fig4_T_distribution.svg"); plt.close(fig)
print("figures written")
