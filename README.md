# Solid–Solid Phase Change Materials (SS-PCM) Dataset

An open, curated dataset of **solid–solid phase change materials** for thermal energy storage:
transition temperatures, latent heats, and related properties, with sources.

> **Status: v0.1 seed (29 materials).** The literature holds roughly a few hundred distinct SS-PCMs
> (~1,000–2,000 entries counting mixtures and polymer formulations). See `data/class_overview.csv`.

## Contents
| File | Description |
|---|---|
| `data/ss_pcm_dataset.csv` | Main dataset (one row per material/sample) |
| `data/data_dictionary.md` | Column definitions and units |
| `data/class_overview.csv` | SS-PCM classes, examples, approximate counts and property ranges |
| `scripts/build_csv.py` | Source of the curated records; regenerates the CSV |
| `scripts/validate.py` | Sanity checks (ranges, DOIs, T < melting point, duplicates) |

## Coverage (v0.1)
| Class | Rows |
|---|---|
| Organic – polyalcohols (NPG, PG, PE, TAM, AMPL) | 5 |
| Organic – molecular plastic crystals | 3 |
| Polymer – PEG-polyurethanes | 10 |
| Organometallic – layered hybrid perovskites | 3 |
| Inorganic – sulfates, AgI, KHF2, VO2 | 6 |
| Metallic – NiTi, Fe | 2 |

## Scope
**Included:** materials whose storage transition is a true solid-to-solid transition
(order–disorder, plastic-crystal, polymorphic, martensitic, superionic, metal–insulator).

**Excluded:** "form-stable" / "shape-stabilized" composites (e.g. paraffin in HDPE, PEG in porous carbon),
which are macroscopically solid but melt at the microscale. These could be added later as a separate class.

## Data quality
Each row has a `verification_status`:
- **`verified`** (18 rows): value checked against the cited paper (DOI given).
- **`to_verify`** (11 rows): typical literature/handbook value; needs a primary-source DOI before research use.

Reported values depend on DSC heating rate, sample purity, and onset vs. peak definition. See `T_type` and `notes`.

## Usage
```python
import pandas as pd
df = pd.read_csv("data/ss_pcm_dataset.csv")
df[df.verification_status == "verified"].sort_values("dH_heat_Jg", ascending=False)
```

## Contributing
1. Add a record in `scripts/build_csv.py` (or edit the CSV) with a DOI.
2. Run `python scripts/build_csv.py && python scripts/validate.py`.
3. Open a pull request.

Priority next steps: verify the `to_verify` rows; add polyalcohol binary mixtures (NPG–PE, NPG–TAM, PG–TAM),
the (CnH2n+1NH3)2MCl4 series (n = 8–18; M = Cu, Zn, Mn, Co), and barocaloric plastic crystals (adamantanes, carboranes).

## Key sources
- Lloveras et al., *Nat. Commun.* 10, 1803 (2019) — doi:10.1038/s41467-019-09730-9
- Serrano et al., *J. Energy Storage* 55, 105677 (2022) — doi:10.1016/j.est.2022.105677
- Doppiu et al., *Materials* 12, 3658 (2019) — doi:10.3390/ma12223658
- Prats et al., *Mater. Chem. Front.* (2025) — doi:10.1039/d5qm00712g
- *Sci. Rep.* 12, 14646 (2022) — doi:10.1038/s41598-022-17390-x
- Cao et al., *RSC Adv.* (2017) — doi:10.1039/c7ra00405b

## License
Data: CC BY 4.0 · Code: MIT
