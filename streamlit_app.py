import streamlit as st

st.set_page_config(
    page_title="EconomicGCH",
    page_icon=":material/account_balance:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar — shown on all pages
with st.sidebar:
    _, col, _ = st.columns([0.5, 3, 0.5])
    with col:
        st.image("assets/final_logo.svg")   # AE4RIA — adjust path per app
    st.space("small")
    _, col, _ = st.columns([0.5, 3, 0.5])
    with col:
        st.image("assets/logo.png")         # SDSN — adjust path per app
    st.divider()
    st.caption("**Economic System**")
    st.caption(
        "Computable General Equilibrium modelling with GTAP-E · "
        "Global Climate Hub"
    )
    st.divider()
    st.caption("**Scenarios**")
    st.markdown(
        """
        - **BAU** — Business-as-usual (SSP2–RCP4.5)
        - **Reference** — With climate impacts
        - **NC** — National Commitments
        """
    )

# Navigation
page = st.navigation(
    [
        st.Page("app_pages/introduction.py", title="Introduction", icon=":material/home:", default=True),
        st.Page("app_pages/methodology.py",  title="Methodology",  icon=":material/schema:"),
        st.Page("app_pages/results.py",      title="Explore results", icon=":material/map:"),
    ],
    position="top",
)

st.title(f"Economic System {page.icon}")
st.caption("Computable General Equilibrium modelling with GTAP-E · Global Climate Hub")

page.run()