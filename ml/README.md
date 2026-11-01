# ML-ready files

Derived from `data/ss_pcm_dataset.csv` by `scripts/build_ml.py`. Rerun that script after editing the dataset.

| File | Rows | What it is |
|---|---|---|
| `molecules.csv` | 21 | Pure molecular and ionic SS-PCMs (polyalcohols, plastic crystals, adamantanes, ionic salts) with SMILES, InChIKey, RDKit descriptors and targets |
| `perovskites.csv` | 13 | Layered perovskites (CnH2n+1NH3)2MX4: cation SMILES, chain length, metal, metal ionic radius, halide, targets |
| `alloys.csv` | 70 | NiTi-based shape-memory alloys: at.% of Ni, Ti, Cu, Hf, Pd, Zr, Cr, V, Co, Pt, Ni/Ti ratio, targets (T, ΔH) |
| `mixtures.csv` | 15 | Polyalcohol mixtures: up to 3 components (SMILES + mole or weight fraction) and targets |

**Targets:** `T_trans_K`, `dH_Jg`, `dH_kJmol`, `dS_JmolK` (= ΔH/T), `T_melt_K` (where known).
**Descriptors (molecules):** MW, heavy atoms, OH and NH2 counts, H-bond donors and acceptors, TPSA, rotatable bonds, rings, fraction sp3, logP, quaternary-carbon flag.

## Quality

- Every SMILES is checked with RDKit: its formula and molar mass must match the dataset row, or the script stops.
- Keep `verification_status` as a sample weight or filter. `needs_check` rows include values derived as T·ΔS.
- Metal ionic radii are Shannon (1976) 6-coordinate values (doi:10.1107/S0567739476001551). Zn and Co tetrachlorometallates contain isolated tetrahedra, so treat the radius as an approximate descriptor.
- Fullerene C60, polymers, carborane salts, spin-crossover complex and inorganic oxides are not in the molecule file. `alloys.csv` suits composition-based regression (e.g. predicting transformation temperature from Ni content and ternary additions).

## Using this for generating new molecules

About 50 molecular rows are far too few to train a generative model from scratch. Recommended route:

1. **Pretrain** a generator (SMILES/SELFIES VAE, graph model, or a chemical language model) on a large unlabelled set such as ZINC, PubChem or QM9.
2. **Train a property predictor** on `molecules.csv` (+ mixtures) for `T_trans_K` and `dS_JmolK`, using descriptors or fingerprints with Gaussian-process or tree models, and leave-one-family-out validation.
3. **Optimise in latent space** (or with reinforcement learning or a genetic algorithm) towards the target window, e.g. 300–330 K for PV cooling and high ΔS.
4. **Filter** candidates for globular shape (quaternary carbon, high symmetry) and H-bonding groups, the motifs behind high-entropy plastic-crystal transitions. Then rank them for DFT, MD or experimental follow-up.

Expanding the labelled set (e.g. the full Li et al. Table S2, more polyalcohol derivatives and NIST phase-change data) will matter more than model choice.
