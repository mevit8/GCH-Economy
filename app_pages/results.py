"""Explore results page — four choropleth world maps."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.data import SECTORS, SECTOR_META, load_gtap_data, get_summary_stats

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

COLOR_SCALES = {
    "Agriculture": "YlGn",
    "Industry":    "Blues",
    "Transport":   "Oranges",
    "Services":    "Purples",
}


def _make_map(df: pd.DataFrame, sector: str, selected_country: str | None) -> go.Figure:
    """Build a Plotly choropleth for one sector."""
    meta = SECTOR_META[sector]
    col = df[sector]
    v_min, v_max = col.min(), col.max()

    fig = px.choropleth(
        df,
        locations="iso3",
        color=sector,
        hover_name="country_raw",
        hover_data={
            "iso3": False,
            sector: ":.1f",
        },
        color_continuous_scale=COLOR_SCALES[sector],
        range_color=(v_min, v_max),
        labels={sector: "% change"},
        projection="natural earth",
    )

    fig.update_traces(
        marker_line_width=0.4,
        marker_line_color="white",
    )

    # Highlight selected country
    if selected_country and selected_country != "None":
        sel_df = df[df["country_raw"] == selected_country]
        if not sel_df.empty:
            fig.add_trace(
                go.Choropleth(
                    locations=sel_df["iso3"],
                    z=[1],
                    colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
                    showscale=False,
                    marker_line_color="#FF4B4B",
                    marker_line_width=2.5,
                    hoverinfo="skip",
                )
            )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="rgba(128,128,128,0.3)",
            showland=True,
            landcolor="rgba(240,240,240,0.5)",
            showocean=True,
            oceancolor="rgba(210,230,250,0.4)",
            showlakes=False,
            projection_type="natural earth",
            bgcolor="rgba(0,0,0,0)",
        ),
        coloraxis_colorbar=dict(
            title=dict(text="% change", side="right"),
            thickness=12,
            len=0.7,
            tickformat=".0f",
            ticksuffix="%",
        ),
        height=320,
    )
    return fig


def _sector_card(df: pd.DataFrame, sector: str, selected_country: str | None):
    """Render one sector block: header + map + metrics."""
    meta = SECTOR_META[sector]
    stats = get_summary_stats(df, sector)

    # Header
    st.markdown(f"### {meta['icon']} {sector}")
    st.caption(meta["description"])

    # Country callout
    if selected_country and selected_country != "None":
        row = df[df["country_raw"] == selected_country]
        if not row.empty:
            val = row[sector].values[0]
            delta_str = f"{val:+.1f}%"
            st.metric(
                label=f"{selected_country} — % change in output",
                value=delta_str,
                delta=delta_str,
                delta_color="normal",
            )

    # Map
    fig = _make_map(df, sector, selected_country)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Summary metrics row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Global mean", f"{stats['mean']:+.1f}%")
    m2.metric("Median", f"{stats['median']:+.1f}%")
    m3.metric("Countries ↑", str(stats["n_positive"]))
    m4.metric("Countries ↓", str(stats["n_negative"]))


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render():
    # ── Sidebar controls ────────────────────────────────────────────────────
    with st.sidebar:
        st.subheader(":material/tune: Controls")

        scenario = st.selectbox(
            "Scenario",
            options=[
                "Business-as-usual (BAU)",
                "Reference",
                "National Commitments (NC)",
            ],
            index=0,
        )

        st.info(
            "Only BAU results are available in this release. "
            "Reference and NC scenarios coming soon.",
            icon=":material/info:",
        )

        st.caption(
            "Note: the current dataset contains BAU results. "
            "Reference and NC scenarios will be added in future releases."
        )

        st.divider()

        df = load_gtap_data("data/Results_GTAP.csv")

        country_options = ["None"] + sorted(df["country_raw"].tolist())
        selected_country = st.selectbox(
            "Highlight country",
            options=country_options,
            index=0,
            help="Select a country to highlight on all maps and show its values.",
        )

        st.divider()

        sectors_to_show = st.multiselect(
            "Sectors to display",
            options=SECTORS,
            default=SECTORS,
            help="Show or hide individual sector maps.",
        )

    # ── Page intro ──────────────────────────────────────────────────────────
    st.markdown(
        f"Showing **% change in sectoral output** relative to the baseline "
        f"under the **{scenario}** scenario. Each map covers ~{len(df)} countries "
        f"from the GTAP dataset."
    )

    if not sectors_to_show:
        st.warning("Select at least one sector from the sidebar to display results.")
        return

    # ── Two-column grid of maps ─────────────────────────────────────────────
    pairs = [sectors_to_show[i : i + 2] for i in range(0, len(sectors_to_show), 2)]

    for pair in pairs:
        cols = st.columns(len(pair))
        for col, sector in zip(cols, pair):
            with col:
                _sector_card(df, sector, selected_country if selected_country != "None" else None)
        st.space("small")

    # ── Cross-sector bar chart for highlighted country ──────────────────────
    if selected_country and selected_country != "None":
        st.divider()
        st.subheader(f":material/bar_chart: {selected_country} — all sectors")

        row = df[df["country_raw"] == selected_country]
        if not row.empty:
            plot_df = pd.DataFrame(
                {
                    "Sector": sectors_to_show,
                    "Change (%)": [row[s].values[0] for s in sectors_to_show],
                }
            )
            fig_bar = px.bar(
                plot_df,
                x="Sector",
                y="Change (%)",
                color="Sector",
                color_discrete_map={
                    "Agriculture": "#4caf50",
                    "Industry": "#2196f3",
                    "Transport": "#ff9800",
                    "Services": "#9c27b0",
                },
                text_auto=".1f",
            )
            fig_bar.update_layout(
                showlegend=False,
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis_title="% change in output",
                xaxis_title="",
                height=300,
            )
            fig_bar.update_traces(textposition="outside")
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    # ── Methodology note ────────────────────────────────────────────────────
    st.divider()
    with st.expander(":material/info: Methodology note", expanded=False):
        st.markdown(
            """
            **How these values were estimated:**
            The GTAP-E model starts from a global benchmark equilibrium calibrated
            to the GTAP Data Base v11. A scenario is introduced as a shock (changes
            in GDP, capital, population, labour, land use and/or climate-policy
            targets). Prices and quantities adjust across all sectors and regions
            until a new equilibrium is found. The result shown here is the
            **percentage deviation in sectoral output** between the scenario
            equilibrium and the baseline — one value per country per broad sector
            group.

            *Source: Burniaux & Truong (2002), GTAP-E Technical Paper No. 16;
            Aguiar et al. (2022), GTAP Data Base v11.*
            """
        )
render()