from dash import html, dcc
from process.layout.styles import LABEL_STYLE, DROPDOWN_STYLE, CARD_STYLE

def sidebar_top_deps():
    return html.Div(id="top-dependencies-container", children=[
                html.Label("Number of Top Trading Partners:", style=LABEL_STYLE),
                dcc.Dropdown(
                    id='top-dependencies',
                    options=[{"label": str(o), "value": o} for o in [10, 15, 30, 50]],
                    value=10,
                    style=DROPDOWN_STYLE
                )
            ], style=CARD_STYLE)

def sidebar_secondary_deps():
    return html.Div(id='secondary-dependencies-container', style=CARD_STYLE, children=[
                html.Label("Showing Secondary Trading Routes:", style=LABEL_STYLE),
                dcc.RadioItems(
                    id="secondary-dependencies",
                    options=[
                        {'label': 'Yes', 'value': True},
                        {'label': 'No', 'value': False}
                    ],
                    value=False,
                    labelStyle={"display": "block"}
                )
            ])
