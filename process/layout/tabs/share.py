from dash import html, dcc
from process.layout.styles import CARD_STYLE, LABEL_STYLE

#html.Div(id="io-summary-container")
def tab_share(industry_options):
    return dcc.Tab(
        label="Share",
        value='tab-share',
        children=[
            html.Div([
                html.H3("Input Output Analysis - Country Share", style={"marginBottom": "5px"}),
                html.P(
                    "Explore the distribution of input industries and their source countries. ",
                    style={"marginBottom": "0px", "color": "#555"}
                ),
                dcc.Graph(id='io-summary', style={"height": "75vh", "width": "100%"})
            ], style=CARD_STYLE)
        ]
    )
