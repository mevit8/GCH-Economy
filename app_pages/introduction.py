import streamlit as st

st.markdown(
    """
    The **economic system** describes how households, firms, governments and
    international markets interact through production, consumption, trade,
    investment, income and prices.

    A **Computable General Equilibrium (CGE)** model represents these
    interactions in a consistent economy-wide framework (Dixon & Jorgenson, 2013).
    """
)

col1, col2, col3 = st.columns(3)
with col1:
    st.info(
        "**Policy shocks → price & quantity adjustments**\n\n"
        "When a policy, climate or resource shock is introduced, prices and "
        "quantities adjust across all connected markets until a new equilibrium.",
        icon=":material/sync_alt:",
    )
with col2:
    st.info(
        "**Economy-wide macro layer**\n\n"
        "Translates changes in land, water, energy, climate and policy into "
        "GDP, sectoral output, prices, trade, welfare and emissions.",
        icon=":material/account_balance:",
    )
with col3:
    st.info(
        "**Cross-sector spillovers**\n\n"
        "Interventions in one system (e.g. land-use change, carbon pricing, "
        "water scarcity) generate spillovers that isolated sectoral models miss.",
        icon=":material/hub:",
    )

st.subheader("Model: GTAP-E")
st.markdown(
    """
    The economics system is modelled with **GTAP-E** (Burniaux & Truong, 2002),
    the energy-environmental extension of the Global Trade Analysis Project (GTAP)
    CGE model (Hertel, 1997). GTAP-E is a multi-region, multi-sector model that
    explicitly represents energy commodities and fossil-fuel CO₂ emissions. The
    GTAP Data Base provides the global benchmark data used to calibrate the model
    (Aguiar et al., 2022).
    """
)

left, right = st.columns(2)
with left:
    st.markdown("#### Typical inputs")
    st.markdown(
        "Shocks to factors of production, energy prices, productivity, "
        "climate-policy variables, and taxes."
    )
with right:
    st.markdown("#### Typical outputs")
    st.markdown(
        "Sectoral activity outputs, prices, trade, GDP, welfare, factor "
        "returns and emissions. The key output for linking with the energy "
        "system is **sectoral output** — it provides the activity level used "
        "to estimate future energy requirements."
    )

st.subheader("Scenarios")

tab_bau, tab_ref, tab_nc = st.tabs(
    ["Business-as-usual (BAU)", "Reference", "National Commitments (NC)"]
)

with tab_bau:
    st.markdown(
        """
        The **BAU** scenario represents a future pathway **without additional
        climate policy intervention** and without explicit climate-change impacts.
        Economic activity evolves according to current socioeconomic trends under
        a "middle-of-the-road" state (**SSP2 – RCP4.5**), with changes in GDP,
        capital, population, labour and land use derived from the LandGCH model
        introduced as shocks.
        """
    )

with tab_ref:
    st.markdown(
        """
        The **Reference** scenario represents a future pathway **without
        additional climate policy intervention but with explicit climate-change
        impacts**. Economic activity evolves under current socioeconomic trends,
        with changes in GDP, capital, population, labour and land use from
        LandGCH introduced as shocks.
        """
    )

with tab_nc:
    st.markdown(
        """
        The **National Commitments (NC)** scenario represents a **policy-driven
        pathway** in which countries implement their Nationally Determined
        Contributions (NDCs) and broader commitments toward climate neutrality.
        The economic system responds to climate-policy shocks such as changes in
        energy use, emissions constraints and carbon taxes.
        """
    )

st.subheader("References")
st.markdown(
    """
    - Dixon, P. B., & Jorgenson, D. W. (Eds.) (2013). *Handbook of Computable General Equilibrium Modeling.* Elsevier.
    - Hertel, T. W. (Ed.) (1997). *Global Trade Analysis: Modeling and Applications.* Cambridge University Press.
    - Burniaux, J.-M., & Truong, T. P. (2002). GTAP-E: An Energy-Environmental Version of the GTAP Model. GTAP Technical Paper No. 16.
    - Aguiar, A., et al. (2022). The GTAP Data Base: Version 11. *Journal of Global Economic Analysis*, 7(2), 1–37.
    """
)