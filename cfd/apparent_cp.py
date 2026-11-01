"""Generate apparent-heat-capacity tables cp_app(T) for CFD (Fluent piecewise-linear cp,
OpenFOAM table, COMSOL interpolation). Uses the apparent heat capacity method:

    cp_app(T) = cp_s(T) + L * D(T),   D(T) = exp(-((T - Tt)/s)^2) / (s * sqrt(pi))

where D integrates to 1, so the latent heat L is released exactly once across the transition.
Only materials with transition T, latent heat and cp in cfd_properties.csv are written.
cp_high is unknown for all entries, so cp_low is used on both sides (state this in your paper).

Usage:  python cfd/apparent_cp.py [--width 3.0]   (s = transition half-width in K)
"""
import csv, math, pathlib, argparse
ap = argparse.ArgumentParser(); ap.add_argument("--width", type=float, default=3.0, help="Gaussian half-width s [K]")
a = ap.parse_args()
here = pathlib.Path(__file__).resolve().parent
out_dir = here/"cp_tables"; out_dir.mkdir(exist_ok=True)
for r in csv.DictReader(open(here/"cfd_properties.csv")):
    if not (r["T_transition_heat_C"] and r["latent_heat_heat_Jkg"] and r["cp_low_JkgK"]): continue
    Tt, L, cp = float(r["T_transition_heat_C"]), float(r["latent_heat_heat_Jkg"]), float(r["cp_low_JkgK"])
    cp_hi = float(r["cp_high_JkgK"]) if r["cp_high_JkgK"] else cp
    s = a.width
    name = (r["abbreviation"] or r["material_name"]).replace(" / ","_").replace(" ","_")
    with open(out_dir/f"{name}_cp_app.csv","w",newline="") as fh:
        w = csv.writer(fh); w.writerow(["T_C","T_K","cp_app_JkgK"])
        T = Tt - 6*s
        while T <= Tt + 6*s + 1e-9:
            base = cp if T < Tt else cp_hi
            w.writerow([round(T,2), round(T+273.15,2), round(base + L*math.exp(-((T-Tt)/s)**2)/(s*math.sqrt(math.pi)),1)])
            T += s/4
    print("wrote", out_dir/f"{name}_cp_app.csv")
