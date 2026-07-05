# INFEWS-MSA-Data

Co-simulation framework, model outputs, and interactive dashboard for the
**Iowa Urban Food-Energy-Water Systems (FEWS)** project, covering the
Des Moines Metropolitan Statistical Area (DM-MSA). This repository supports
the manuscript *"A Co-simulation Framework to Integrate Social and
Biophysical Models for Urban FEW Systems,"* submitted to *Environmental
Modelling & Software*.

**Live dashboard:** https://iowaurbanfews.streamlit.app

## What this repository contains

Three independently-run simulation models are coupled through a
non-intrusive co-simulation framework: model outputs are exchanged as files
at defined synchronization points rather than through in-memory coupling,
so each model remains internally independent and separately verifiable.

| Model | Tool | Role |
|---|---|---|
| Agent-Based Model (ABM) | NetLogo | Simulates farmer land-allocation decisions (row crops vs. specialty crops) |
| Watershed model (SWAT) | Soil and Water Assessment Tool | Simulates streamflow, sediment, and nutrient loading from ABM-derived land use |
| Life Cycle Assessment (LCA) | USEEIO | Quantifies energy use and global warming potential from the resulting food-system scenario |

A Streamlit multipage app (`Home.py` + `pages/`) visualizes baseline results
for each model individually, plus 5 combined co-simulation scenarios.

## Repository structure

```
Home.py                     # dashboard entry point (streamlit run Home.py)
pages/                      # one file per dashboard page (Streamlit auto-discovers this folder)
  10_Integrated_Modeling.py
  20_Agent_Based_Model.py
  30_Life_Cycle_Assessment.py
  45_Soil_and_Water_Assessment_Tool.py
  60_CoSim_Scenarios.py
  90_Contact_Us!.py
ABM_exp/                    # aggregated ABM experiment output (read by the dashboard)
SWAT_base_2025/             # baseline SWAT run, current model vintage
SWAT_Cosim_results/         # per-scenario SWAT outputs (5 co-simulation scenarios)
Outputs_Co_sim_*/           # per-scenario LCA outputs (5 co-simulation scenarios)
lca_*.{csv,pickle}          # baseline/local LCA data used by the standalone LCA page
metadata/                   # machine-readable data/model documentation (see below)
codemeta.json               # software metadata (CodeMeta vocabulary)
CITATION.cff                # citation metadata (GitHub "Cite this repository" / Zenodo)
LICENSE                     # MIT (code); see "License" section below for data license
LICENSE-DATA                # CC-BY-4.0 (data)
requirements.txt            # Python dependencies
.devcontainer/               # GitHub Codespaces configuration
```

Only the files listed above are read by the live dashboard. Raw
intermediate model runs and superseded data vintages that underlie the
published figures but are not rendered on the dashboard are retained
separately for reproducibility/provenance (see "Archived data" below)
rather than in the deployed app repository, to keep the deployed
application lightweight.

## Machine-readable metadata (for agentic/automated pipelines)

To make the data and model interfaces directly consumable by automated
tools (LLM agents, data catalogs, reproducibility checkers) rather than
requiring a human to read the dashboard source code, this repository
provides structured metadata:

- **`codemeta.json`** -- software identity, license, authors, related
  publication (CodeMeta / Schema.org vocabulary; parsed by Software
  Heritage, Zenodo, and other research-software registries).
- **`CITATION.cff`** -- citation metadata in the Citation File Format,
  natively read by GitHub and Zenodo.
- **`metadata/scenarios.json`** -- machine-readable description of the 5
  co-simulation scenarios: what ABM policy lever each one varies, and the
  exact output file each scenario writes.
- **`metadata/model_interfaces.json`** -- a model-card-style description
  of each model's (ABM/SWAT/LCA) inputs, output file formats, column
  names, and units, and which dashboard page consumes each file.

An automated pipeline (or a person unfamiliar with the code) can read
`metadata/model_interfaces.json` to know, for example, that
`SWAT_base_2025/SWAT_base_2025_rch_output.csv` has a `FLOW_OUTcms` column
in cubic meters/second, indexed by reach (`RCH`) and month (`MON`),
without needing to open `pages/45_Soil_and_Water_Assessment_Tool.py`.

## Running the dashboard locally

```bash
pip install -r requirements.txt
streamlit run Home.py
```

Or open this repository in GitHub Codespaces, which uses
`.devcontainer/devcontainer.json` to install dependencies and launch the
app automatically.

## Data dictionary (summary)

See `metadata/model_interfaces.json` for full column-level documentation.
At a glance:

| File | Model | Contents |
|---|---|---|
| `ABM_exp/df_exp_avg_ABM.pkl` | ABM | Specialty-crop acreage by year, per experiment strategy |
| `ABM_exp/df_exp_avg.pkl` | ABM | Specialty-crop acreage by year, per co-simulation scenario |
| `SWAT_base_2025/SWAT_base_2025_rch_output.csv` | SWAT | Baseline streamflow/sediment/nutrient loads, 2020-2050 |
| `SWAT_Cosim_results/output_<scenario>.csv` | SWAT | Streamflow/sediment/nutrient loads per co-simulation scenario |
| `lca_dataset.csv` | LCA | Energy use and GWP under BASE vs. LOCAL food-system scenarios |
| `Outputs_<scenario>/lca_<scenario>.csv` | LCA | Energy use and GWP per co-simulation scenario |

## Archived data

Raw per-run ABM outputs (`ABM_Co_sim_*` folders), superseded model
vintages, and intermediate SWAT/LCA post-processing files
(`Final_yields_*`, `swat_lca_*_diet/_ylds`, `Co_sim_analysis.*`) are not
required to reproduce the dashboard and have been moved out of the active
repository to keep it lightweight. They remain available as a project
archive; contact the corresponding author for access, or see the archive
link in a future repository release.

## License

- **Code** (Python scripts, `.devcontainer/`, this documentation): MIT
  License. See `LICENSE`.
- **Data** (SWAT, ABM, and LCA model outputs distributed in this
  repository): Creative Commons Attribution 4.0 International (CC-BY-4.0).
  See `LICENSE-DATA`. You may share and adapt the data for any purpose,
  provided appropriate credit is given.

This dual-license split (permissive license for code, attribution license
for data) follows common practice for research software repositories that
bundle both code and generated datasets.

## Citation

If you use this repository, please cite both the software
(`CITATION.cff` / `codemeta.json`) and the associated manuscript:

> [Author list]. "A Co-simulation Framework to Integrate Social and
> Biophysical Models for Urban FEW Systems." *Environmental Modelling &
> Software* (in review, 2026).

## Contact

Questions about the models, data, or dashboard: see the "Contact Us" page
of the live dashboard, or open a GitHub issue on this repository.
