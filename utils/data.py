"""
Data loading and processing utilities for EconomicGCH.
"""

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Country name → ISO-3166 alpha-3 code mapping
# Covers the abbreviated / non-standard names used in the GTAP dataset.
# ---------------------------------------------------------------------------
COUNTRY_ISO3 = {
    # Africa – North
    "Algeria": "DZA", "Egypt": "EGY", "Morocco": "MAR", "Tunisia": "TUN",
    # Africa – West
    "Benin": "BEN", "BurkinaFaso": "BFA", "Camroon": "CMR", "CotedIvore": "CIV",
    "Ghana": "GHA", "Niger": "NER", "Nigeria": "NGA", "Senegal": "SEN", "Togo": "TGO",
    # Africa – Central
    "Chad": "TCD", "Congo": "COD", "RepofCongo": "COG", "EqGuinea": "GNQ", "Gabon": "GAB",
    # Africa – East
    "Ethiopia": "ETH", "Kenya": "KEN", "Madagascar": "MDG", "Mauritius": "MUS",
    "Mozambique": "MOZ", "Rwanda": "RWA", "Sudan": "SDN", "Tanzania": "TZA",
    "Uganda": "UGA", "Zambia": "ZMB", "Zimbabwe": "ZWE",
    # Africa – South
    "Botswana": "BWA", "Namibia": "NAM", "SouthAfrica": "ZAF",
    "Eswatini": "SWZ", "Namimbia": "NAM", "SouthAfr": "ZAF",
    # Middle East
    "Iran": "IRN", "Iraq": "IRQ", "Israel": "ISR", "Jordan": "JOR", "Kuwait": "KWT",
    "Oman": "OMN", "Qatar": "QAT", "SaudiArabia": "SAU", "SaudiArab": "SAU",
    "Turkey": "TUR", "UAE": "ARE", "Yemen": "YEM",
    "Bahrain": "BHR", "Lebanon": "LBN", "Syria": "SYR",
    # Asia – South
    "Bangladesh": "BGD", "India": "IND", "Nepal": "NPL", "Pakistan": "PAK",
    "SriLanka": "LKA",
    # Asia – East & SE
    "China": "CHN", "HongKong": "HKG", "HingKong": "HKG", "Japan": "JPN",
    "Korea": "KOR", "Mongolia": "MNG", "Taiwan": "TWN",
    "Cambodia": "KHM", "Indonesia": "IDN", "Laos": "LAO", "Malaysia": "MYS",
    "Myanmar": "MMR", "Philippines": "PHL", "Singapore": "SGP", "Thailand": "THA",
    "Vietnam": "VNM", "Brunei": "BRN",
    # Oceania
    "Australia": "AUS", "NewZealand": "NZL",
    # Americas – North
    "Canada": "CAN", "Mexico": "MEX", "USA": "USA", "US": "USA",
    # Americas – Central & Caribbean
    "CostaRica": "CRI", "Honduras": "HND", "Nicaragua": "NIC", "Panama": "PAN",
    "Guatemala": "GTM", "ElSalvador": "SLV", "DominicanRe": "DOM",
    "Haiti": "HTI", "Jamaica": "JAM", "Trinidad": "TTO",
    # Americas – South
    "Argentina": "ARG", "Bolivia": "BOL", "Brazil": "BRA", "Chile": "CHL",
    "Colombia": "COL", "Ecuador": "ECU", "Paraguay": "PRY", "Peru": "PER",
    "Uruguay": "URY", "Venezuela": "VEN",
    # Europe – West
    "Austria": "AUT", "Belgium": "BEL", "Denmark": "DNK", "Finland": "FIN",
    "France": "FRA", "Germany": "DEU", "Greece": "GRC", "IRE": "IRL",
    "ITALY": "ITA", "LUXE": "LUX", "NTH": "NLD", "POR": "PRT",
    "SPA": "ESP", "SWED": "SWE", "SWIZ": "CHE", "UK": "GBR",
    "AUST": "AUT", "BELG": "BEL", "DEN": "DNK", "FINL": "FIN",
    "FRAN": "FRA", "GER": "DEU", "GRE": "GRC",
    # Europe – Central & Eastern
    "BULG": "BGR", "BUL": "BGR", "CROA": "HRV", "CRO": "HRV",
    "CZE": "CZE", "CZH": "CZE", "ESTO": "EST", "HUNG": "HUN",
    "LAT": "LVA", "LTH": "LTU", "MAL": "MLT", "POLA": "POL", "ROM": "ROU",
    "SLK": "SVK", "SLO": "SVN", "CYPR": "CYP",
    # Europe – Other
    "ALBA": "ALB", "SER": "SRB", "NORW": "NOR",
    # Former Soviet / Central Asia
    "Armenia": "ARM", "Azerbaijan": "AZE", "Belarus": "BLR", "Georgia": "GEO",
    "Kazakhstan": "KAZ", "Kyrgyzstan": "KGZ", "Kyrgystan": "KGZ",
    "Tajikistan": "TJK", "Russia": "RUS", "Ukraine": "UKR", "Uzbekistan": "UZB",
}

SECTORS = ["Agriculture", "Industry", "Transport", "Services"]

SECTOR_META = {
    "Agriculture": {
        "description": (
            "Primary production of crops, livestock, fisheries and forestry. "
            "Strongly linked to land, water availability, food security and rural income."
        ),
        "subsectors": (
            "Paddy rice, wheat, cereal grains, vegetables, fruits and nuts, oil seeds, "
            "sugar crops, livestock, raw milk, fishing and forestry."
        ),
        "color_scale": "YlGn",
        "icon": "🌾",
    },
    "Industry": {
        "description": (
            "Manufacturing, mining, materials and energy-related production. "
            "Central for employment, value added, energy demand and industrial emissions."
        ),
        "subsectors": (
            "Food products, textiles, wood and paper, metals, chemicals, pharmaceuticals, "
            "rubber and plastics, machinery, vehicles, coal mining, crude oil, gas, "
            "petroleum products and electricity."
        ),
        "color_scale": "Blues",
        "icon": "🏭",
    },
    "Transport": {
        "description": (
            "Mobility and freight activities connecting households, firms, tourism and trade. "
            "A major driver of fuel use and transport-related emissions."
        ),
        "subsectors": "Land transport, air transport and water transport.",
        "color_scale": "Oranges",
        "icon": "🚢",
    },
    "Services": {
        "description": (
            "Market and public services supporting households, businesses, tourism and public welfare. "
            "Less energy-intensive per unit of output but large and fast-growing in many economies."
        ),
        "subsectors": (
            "Construction, trade, accommodation and food services, warehousing, communication, "
            "financial and insurance services, real estate, business services, public administration, "
            "education, health, dwellings and water services."
        ),
        "color_scale": "Purples",
        "icon": "🏦",
    },
}

SCENARIOS = {
    "Business-as-usual (BAU)": {
        "code": "bau",
        "description": (
            "Future pathway without additional climate policy intervention. "
            "Economic activity evolves under SSP2–RCP4.5 ('middle-of-the-road'), "
            "with changes in GDP, capital, population and land use from LandGCH."
        ),
    },
    "Reference": {
        "code": "ref",
        "description": (
            "Future pathway without additional climate policy intervention but with "
            "explicit climate-change impacts. Economic activity evolves under current "
            "socioeconomic trends with climate impacts factored in."
        ),
    },
    "National Commitments (NC)": {
        "code": "nc",
        "description": (
            "Policy-driven pathway in which countries implement their Nationally Determined "
            "Contributions (NDCs). The economic system responds to climate-policy shocks "
            "such as changes in energy use, emissions constraints and carbon taxes."
        ),
    },
}


def load_gtap_data(filepath: str = "data/Results_GTAP.csv") -> pd.DataFrame:
    """Load and clean the GTAP results CSV."""
    df = pd.read_csv(filepath, index_col=0)
    df.index.name = "country_raw"
    df = df.reset_index()

    # Map to ISO-3 codes for choropleth
    df["iso3"] = df["country_raw"].map(COUNTRY_ISO3)

    # Human-readable country name fallback
    df["country_label"] = df["country_raw"].apply(
        lambda x: x.replace("_", " ")
    )

    # Drop rows without a mapping (unknown codes)
    n_before = len(df)
    df = df.dropna(subset=["iso3"])
    n_dropped = n_before - len(df)
    if n_dropped:
        import warnings
        warnings.warn(f"{n_dropped} rows dropped – no ISO-3 code found.")

    return df


def get_summary_stats(df: pd.DataFrame, sector: str) -> dict:
    """Return summary statistics for a sector column."""
    col = df[sector].dropna()
    return {
        "mean": col.mean(),
        "median": col.median(),
        "min": col.min(),
        "max": col.max(),
        "n_positive": int((col > 0).sum()),
        "n_negative": int((col < 0).sum()),
    }
