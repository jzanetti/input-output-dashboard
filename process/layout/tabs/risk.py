
from dash import html, dcc
from process.layout.styles import CARD_STYLE

def tab_risk_profile():
    return dcc.Tab(
        label="Herfindahl-Hirschman Index",
        value='tab-risk',
        children=[
            html.Div([
                html.H3("What is Herfindahl-Hirschman Index (HHI)", style={"marginBottom": "5px"}),
                html.P([
                    "The Herfindahl–Hirschman Index (HHI) is used to assess the diversification of suppliers (exporters) and customers (importers). ",
                    "A higher weighted HHI indicates lower diversity (for example, a value of 1 signifies complete reliance on a single foreign supplier, ",
                    "apart from domestic production), implying greater risk due to supply concentration.",
                    html.Br(),
                    html.Br(),
                    "The Weighed HHI is calculated using: ",
                    html.Br(),
                    "Weighed HHI = (Risk Weight) x (Dependency Scaler) x (HHI)",
                    html.Br(),
                    html.Br(),
                    "By default, all countries are assigned a \"risk weight\" of 1.0. However, higher weights can be applied to reflect geopolitical or ",
                    "market-specific risks associated with a particular country.",
                    html.Br(),
                    html.Br(),
                    "Additionally, a \"dependency scaler\" for foreign imports is applied. For example, if only 3 out of 10 units of a product are imported, ",
                    "the scaler is 0.3, proportionally reflecting the import dependency."
                ],
                style={"marginBottom": "20px", "color": "#555"}
                ),
                html.Div([
                    dcc.Graph(id='io-risk_profile', style={"height": "100%", "width": "100%"})
                ], style={"height": "155vh"})
            ], style=CARD_STYLE)
        ]
    )

