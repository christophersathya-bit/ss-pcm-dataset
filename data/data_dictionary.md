# Data dictionary — `ss_pcm_dataset.csv`

| Column | Unit | Description |
|---|---|---|
| id | – | Unique ID `SSPCM-####` |
| material_name | – | Common or descriptive name |
| abbreviation | – | Common short name, or sample code from the source |
| formula | – | Chemical formula or composition description |
| class | – | `organic`, `polymer`, `organometallic`, `inorganic`, `metallic`, `ionic` |
| subclass | – | Finer family (e.g. polyalcohol, PEG-polyurethane, layered perovskite) |
| transition | – | Nature of the solid–solid transition |
| T_heat_C | °C | Transition temperature on heating |
| T_cool_C | °C | Transition temperature on cooling (if reported) |
| T_type | – | How T was defined (onset / peak / equilibrium) and method notes |
| dH_heat_Jg | J/g | Transition enthalpy on heating |
| dH_cool_Jg | J/g | Transition enthalpy on cooling |
| molar_mass_gmol | g/mol | Molar mass (pure compounds only) |
| melting_point_C | °C | Melting point (upper operating limit) |
| volume_change_pct | % | Volume change across the transition |
| notes | – | Ranges, caveats, conversions |
| reference | – | Short citation |
| doi | – | DOI of the source used |
| source_url | – | Link to the source when no DOI is available (e.g. NIST WebBook, arXiv) |
| verification_status | – | `verified` = value checked against the cited source; `needs_check` = source known but value derived/OCR/manuscript; `to_verify` = no primary source found yet |

Conversions: kJ/mol → J/g = kJ/mol × 1000 / M. K → °C = K − 273.15.
