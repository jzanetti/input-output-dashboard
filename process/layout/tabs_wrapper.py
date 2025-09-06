from dash import html, dcc
from process.layout.tabs.map import tab_map
from process.layout.tabs.share import tab_share
from process.layout.tabs.risk import tab_risk_profile
from process.layout.tabs.heatmap import tab_heatmap
from process.layout.tabs.cluster import tab_cluster

# --- Main Layout Function ---
def get_tabs_layout(industry_options):
    return html.Div(
        style={"flex": "1"},
        children=[
            dcc.Tabs(
                id="graph-tabs",
                colors={"border": "#ccc", "primary": "#007bff", "background": "#f8f9fa"},
                children=[
                    tab_map(),
                    tab_share(industry_options),
                    tab_risk_profile(),
                    tab_cluster()
                    #tab_heatmap(country_options, CARD_STYLE, LABEL_STYLE),
                    #tab_cluster(country_options, CARD_STYLE, LABEL_STYLE)
                ]
            )
        ]
    )
