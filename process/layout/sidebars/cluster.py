
from dash import html, dcc
from process.layout.styles import LABEL_STYLE, CARD_STYLE, VALUE_STYLE_TYPE1, DROPDOWN_STYLE

def sidebar_cluster(country_options, industry_options):

    return html.Div(id="risk-cluster-container", children=[

        html.Label("Export Industry:", style=LABEL_STYLE),
        dcc.Dropdown(
            id="cluster-industry",
            options=industry_options,
            value='A01_02',
            style=DROPDOWN_STYLE,
        ),

        html.Label("Market:", style=LABEL_STYLE),
        dcc.Dropdown(
            id="cluster-country",
            options=country_options,
            value='CN1',
            style=DROPDOWN_STYLE,
        ),

        html.P("How different countries export \"Export Industry\" to affect different industries in the \"Market\" country"),

        html.Label("Number of country clusters:", style=LABEL_STYLE),
        dcc.Input(
            id="cluster-input",
            type="number",
            value = 3,
            max = 5,
            min = 2,
            style=VALUE_STYLE_TYPE1
        ),

        html.Label("Select a cluster", style=LABEL_STYLE),
        dcc.Dropdown(
            id="cluster-dropdown",
            options=[],  # we will update options dynamically in callback
            value=0,     # default cluster
            clearable=False
        ),

    ], style=CARD_STYLE)