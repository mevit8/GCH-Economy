import streamlit as st

st.markdown(
    """
    The CGE model starts from an **initial equilibrium** of the world economy,
    where each firm buys inputs, employs labour and capital, sells output, trades
    with other regions, pays taxes and responds to prices.
    """
)

st.subheader("How a scenario works")

st.info("**:material/bolt: Shock introduction**\n\nA scenario is introduced as a shock — for example faster GDP growth, lower agricultural productivity, a land constraint, higher energy prices or a climate-policy target.", icon=":material/bolt:")
st.info("**:material/sync: Agent responses**\n\nThe model traces how firms, households and governments respond: producers change input use and production levels, consumers adjust demand, trade flows shift, and prices move to restore balance.", icon=":material/sync:")
st.info("**:material/check_circle: New equilibrium**\n\nA new economic equilibrium is reached and compared with the initial or reference pathway to quantify the effect of the shock.", icon=":material/check_circle:")

st.subheader("Sector groups")

with st.expander("🌾 Agriculture", expanded=False):
    st.markdown("Primary production of crops, livestock, fisheries and forestry. Strongly linked to land, water availability, food security and rural income.")
    st.caption("**Sub-sectors:** Paddy rice · wheat · cereal grains · vegetables, fruits and nuts · oil seeds · sugar crops · livestock · raw milk · fishing · forestry")

with st.expander("🏭 Industry", expanded=False):
    st.markdown("Manufacturing, mining, materials and energy-related production. Central for employment, value added, energy demand and industrial emissions.")
    st.caption("**Sub-sectors:** Food products · textiles · wood and paper · metals · chemicals · pharmaceuticals · rubber and plastics · machinery · vehicles · coal mining · crude oil · gas · petroleum products · electricity")

with st.expander("🚢 Transport", expanded=False):
    st.markdown("Mobility and freight activities connecting households, firms, tourism and trade. A major driver of fuel use and transport-related emissions.")
    st.caption("**Sub-sectors:** Land transport · air transport · water transport")

with st.expander("🏦 Services", expanded=False):
    st.markdown("Market and public services supporting households, businesses, tourism and public welfare. Less energy-intensive per unit of output but large and fast-growing.")
    st.caption("**Sub-sectors:** Construction · trade · accommodation and food services · warehousing · communication · financial and insurance services · real estate · business services · public administration · education · health · dwellings · water services")

st.subheader("Key output: sectoral output (% change)")
st.markdown(
    """
    The primary result displayed in the **Explore results** tab is the
    **percentage change in sectoral output** relative to the baseline — one
    value per sector per country, presented as four choropleth world maps.
    """
)