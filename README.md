# EconomicGCH

**Economic System Explorer** — part of the Global Climate Hub platform.

Built on GTAP-E (Burniaux & Truong, 2002), a multi-region, multi-sector
Computable General Equilibrium model that explicitly represents energy
commodities and fossil-fuel CO₂ emissions.

## Pages

| Page | Description |
|------|-------------|
| **Introduction** | Overview of the CGE approach, model and scenarios |
| **Methodology** | How GTAP-E works: shocks, agent responses, new equilibrium |
| **Explore results** | Four interactive world maps — % change in sectoral output per country |

## Sectors

- 🌾 **Agriculture** — crops, livestock, fisheries, forestry
- 🏭 **Industry** — manufacturing, mining, energy production
- 🚢 **Transport** — land, air and water freight/mobility
- 🏦 **Services** — financial, public, business and social services

## Scenarios

- **BAU** — Business-as-usual (SSP2–RCP4.5, no additional climate policy)
- **Reference** — No additional climate policy but with explicit climate impacts
- **NC** — National Commitments (NDCs + climate-neutrality targets)

## Setup

```bash
# 1. Clone
git clone <repo-url>
cd economicgch

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
streamlit run streamlit_app.py
```

## Project structure

```
economicgch/
├── streamlit_app.py        # Entry point & navigation
├── app_pages/
│   ├── introduction.py     # Introduction tab
│   ├── methodology.py      # Methodology tab
│   └── results.py          # Explore results tab (maps)
├── utils/
│   └── data.py             # Data loading, ISO-3 mapping, stats
├── data/
│   └── Results_GTAP.csv    # GTAP-E output (% change by country & sector)
├── .streamlit/
│   └── config.toml         # Theme & layout configuration
├── requirements.txt
├── .gitignore
└── README.md
```

## Data

`data/Results_GTAP.csv` contains the percentage change in sectoral output
for ~128 countries across four sector groups (Agriculture, Industry,
Transport, Services) under the BAU scenario.

## References

- Hertel, T. W. (Ed.) (1997). *Global Trade Analysis*. Cambridge University Press.
- Burniaux, J.-M., & Truong, T. P. (2002). GTAP-E. GTAP Technical Paper No. 16.
- Aguiar, A., et al. (2022). The GTAP Data Base: Version 11. *JGEA*, 7(2).
- Dixon, P. B., & Jorgenson, D. W. (Eds.) (2013). *Handbook of CGE Modeling*. Elsevier.
