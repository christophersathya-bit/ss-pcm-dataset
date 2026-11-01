# CFD-ready files

| File | What it is |
|---|---|
| `cfd_properties.csv` | One row per material: transition T (heating/cooling), hysteresis, latent heat (J/kg), density, thermal conductivity and cp for the low- and high-temperature phases, melting point, volume change, sources |
| `apparent_cp.py` | Builds apparent-heat-capacity tables cp_app(T) for materials with complete inputs |
| `cp_tables/*.csv` | Generated tables (T, cp_app) ready for Fluent piecewise-linear cp, an OpenFOAM table or COMSOL interpolation |

## Coverage (honest)

| Property | Materials with a sourced value |
|---|---|
| Transition T + latent heat | 61 of 63 |
| cp, low-T phase (~298 K) | NPG, PE, PG/TME, TAM, AMPL (NIST WebBook) |
| Density + conductivity, both phases | NPG, PE, PG/TME (Benson & Christensen 1984, OCR; check the scan) |
| cp, high-T phase | none yet. `apparent_cp.py` uses cp_low on both sides |

Only **NPG, PE and PG/TME** currently have the full set (ρ, k, cp, T, L) for a simulation. Blank cells mean no source has been found yet. They are not zeros.

## Method: apparent heat capacity

A solid–solid PCM has no melt flow, so pure conduction with a temperature-dependent cp is the right model (no enthalpy–porosity or Boussinesq terms):

  ρ cp_app(T) ∂T/∂t = ∇·(k(T) ∇T)
  cp_app(T) = cp(T) + L · exp(−((T − Tt)/s)²) / (s √π)

The Gaussian integrates to 1, so exactly L is absorbed across the transition (`apparent_cp.py` checks this numerically). Choose the half-width `s` from the DSC peak width (default 3 K). Mesh and time step must resolve it: ΔT per step should be well below s.

Model hysteresis with separate heating and cooling curves (`T_transition_cool_C`) when the data exist. Interpolate k and ρ between the phases across the same window.
