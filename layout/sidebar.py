from dash import html, dcc

def get_sidebar_layout(data, industry_options, LABEL_STYLE, DROPDOWN_STYLE, CARD_STYLE):
    return html.Div(
        style={"width": "20%", "minWidth": "250px", "marginRight": "20px"},
        children=[
            html.Div([
                html.Label("Importer:", style=LABEL_STYLE),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[{"label": c, "value": c} for c in list(data["all_countries"]["Code"])],
                    value='NZL',
                    style=DROPDOWN_STYLE
                )
            ], style=CARD_STYLE),

            html.Div([
                html.Label("Industry:", style=LABEL_STYLE),
                dcc.Dropdown(
                    id='industry-dropdown',
                    options=industry_options,
                    value='A01_02',
                    style=DROPDOWN_STYLE
                )
            ], style=CARD_STYLE),

            html.Div(id="top-dependencies-container", children=[
                html.Label("Top Trading Partners:", style=LABEL_STYLE),
                dcc.Dropdown(
                    id='top-dependencies',
                    options=[{"label": str(o), "value": o} for o in [10, 15, 30, 50]],
                    value=10,
                    style=DROPDOWN_STYLE
                )
            ], style=CARD_STYLE),

            html.Div(id='secondary-dependencies-container', style=CARD_STYLE, children=[
                html.Label("Enable secondary trading routes:", style=LABEL_STYLE),
                dcc.RadioItems(
                    id="secondary-dependencies",
                    options=[
                        {'label': 'Yes', 'value': True},
                        {'label': 'No', 'value': False}
                    ],
                    value=False,
                    labelStyle={"display": "block"}
                )
            ]),

            html.Div(id='thickness-container', style=CARD_STYLE, children=[
                html.Label("Enable trade volume in plot:", style=LABEL_STYLE),
                dcc.RadioItems(
                    id="use-thickness",
                    options=[
                        {'label': 'Yes', 'value': True},
                        {'label': 'No', 'value': False}
                    ],
                    value=True,
                    labelStyle={"display": "block"}
                )
            ]),
        ]
    )
