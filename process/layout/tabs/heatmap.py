from dash import html, dcc

def tab_heatmap(country_options, CARD_STYLE, LABEL_STYLE):
    return dcc.Tab(
        label="Heatmap",
        value='tab-heatmap',
        children=[
            html.Div([
                html.H3("Heatmap of Input-Output Data", style={"marginBottom": "8px"}),
                html.P(
                    "Use the controls below to select a reference country and optionally apply logarithmic scaling "
                    "for improved visibility of variations in the data...",
                    style={"marginBottom": "25px", "color": "#555"}
                ),
                html.Div([
                    html.Div([
                        html.Label("Select reference country:", style=LABEL_STYLE),
                        dcc.Dropdown(
                            id='tab4-dropdown-selection',
                            options=country_options,
                            value="CN1",
                            clearable=False,
                            style={
                                "width": "250px",
                                "border": "1px solid #ccc",
                                "borderRadius": "6px",
                                "fontSize": "14px"
                            }
                        ),
                    ], style={"marginRight": "30px", "minWidth": "280px"}),

                    html.Div([
                        html.Label("Scale mode:", style=LABEL_STYLE),
                        dcc.RadioItems(
                            id='tab4-radio-log',
                            options=[
                                {'label': 'Original values', 'value': 'linear'},
                                {'label': 'Using log', 'value': 'log'}
                            ],
                            value='log',
                            inline=True,
                            inputStyle={"marginRight": "8px", "marginLeft": "12px"},
                            labelStyle={"marginRight": "25px"},
                            style={
                                "fontSize": "14px",
                                "padding": "8px 12px",
                                "border": "1px solid #ccc",
                                "borderRadius": "6px",
                            }
                        )
                    ]),
                ], style={
                    "display": "flex",
                    "alignItems": "flex-end",
                    "flexWrap": "wrap",
                    "gap": "20px",
                    "marginBottom": "25px"
                }),

                dcc.Graph(id='io-heatmap', style={"height": "80vh", "width": "80vh"})
            ], style=CARD_STYLE)
        ]
    )
