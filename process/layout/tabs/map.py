from dash import html, dcc
from process.layout.styles import CARD_STYLE

def tab_map():
    return dcc.Tab(
        label="Map",
        value='tab-map',
        children=[
            html.Div(
                dcc.Graph(id='io-map', style={"height": "80vh"}),
                style=CARD_STYLE
            )
        ]
    )