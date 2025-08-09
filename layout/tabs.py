from dash import html, dcc

def get_tabs_layout(industry_options, CARD_STYLE, LABEL_STYLE):
    return html.Div(
        style={"flex": "1"},
        children=[
            dcc.Tabs(
                id="graph-tabs",
                value='tab-1',
                colors={"border": "#ccc", "primary": "#007bff", "background": "#f8f9fa"},
                children=[
                    dcc.Tab(
                        label="Map",
                        value='tab-1',
                        children=[
                            html.Div(
                                dcc.Graph(id='io-map', style={"height": "80vh"}),
                                style=CARD_STYLE
                            )
                        ]
                    ),
                    dcc.Tab(
                        label="Share",
                        value='tab-2',
                        children=[
                            html.Div([
                                # Section Title
                                html.H3(
                                    "Industry Share Analysis",
                                    style={"marginBottom": "5px"}
                                ),
                                html.P(
                                    "Explore the distribution of input industries and their source countries. "
                                    "Use the selector below to focus on a specific industry.",
                                    style={"marginBottom": "20px", "color": "#555"}
                                ),

                                # Two-column quick explanation
                                html.Div([
                                    html.Div([
                                        html.Strong("Left Chart: "),
                                        html.Span("Volume of the selected input industry compared to others.")
                                    ], style={"flex": "1", "paddingRight": "10px"}),

                                    html.Div([
                                        html.Strong("Right Chart: "),
                                        html.Span("Share of the selected industry by source country.")
                                    ], style={"flex": "1", "paddingLeft": "10px"}),
                                ], style={
                                    "display": "flex",
                                    "marginBottom": "20px",
                                    "background": "#f9f9f9",
                                    "padding": "10px",
                                    "borderRadius": "8px",
                                    "border": "1px solid #ddd"
                                }),

                                # Dropdown
                                html.Div([
                                    html.Label("Select Input:", style=LABEL_STYLE),
                                    dcc.Dropdown(
                                        id='tab2-dropdown-selection',
                                        options=industry_options,
                                        value="A01_02",
                                        style={
                                            "width": "300px",
                                            "marginTop": "5px",
                                            "marginBottom": "20px"
                                        },
                                        clearable=False
                                    ),
                                ]),

                                # Graph
                                dcc.Graph(
                                    id='io-summary',
                                    style={"height": "75vh", "width": "100%"}
                                )
                            ], style=CARD_STYLE)
                        ]
                    ),

                    dcc.Tab(
                        label="Risk profile",
                        value='tab-3',
                        children=[
                            html.Div([
                                html.H3(
                                    "What is Herfindahl-Hirschman Index (HHI)",
                                    style={"marginBottom": "5px"}
                                ),

                                html.P(
                                    "HHI is usually used to capture customer concentration, " + \
                                    "here it is adpated to measure the diversification of supplier (exporter) and customer (importer). " + \
                                    "A higher weighted HHI indicates less diversity and potentially higher risk from relying on fewer suppliers.",
                                    style={"marginBottom": "20px", "color": "#555"}
                                ),
                                # Inputs and button aligned horizontally with spacing and consistent styling
                                html.Div([
                                    html.Div([
                                        html.Label("Country code to adjust:", style=LABEL_STYLE),
                                        dcc.Input(
                                            id="risk-country-input",
                                            type="text",
                                            placeholder="e.g., CN1",
                                            style={
                                                "width": "160px",
                                                "padding": "8px 12px",
                                                "border": "1px solid #ccc",
                                                "borderRadius": "6px",
                                                "fontSize": "14px",
                                            }
                                        ),
                                    ], style={"marginRight": "30px", "minWidth": "180px"}),

                                    html.Div([
                                        html.Label("Weight:", style=LABEL_STYLE),
                                        dcc.Input(
                                            id="risk-weight-input",
                                            type="number",
                                            value=1.0,
                                            min=0,
                                            step=0.1,
                                            style={
                                                "width": "110px",
                                                "padding": "8px 12px",
                                                "border": "1px solid #ccc",
                                                "borderRadius": "6px",
                                                "fontSize": "14px",
                                            }
                                        ),
                                    ], style={"marginRight": "30px", "minWidth": "130px"}),

                                    html.Div([
                                        html.Button(
                                            "Update Weight",
                                            id="update-risk-weight",
                                            style={
                                                "backgroundColor": "#007bff",
                                                "color": "white",
                                                "border": "none",
                                                "padding": "10px 20px",
                                                "fontSize": "14px",
                                                "fontWeight": "600",
                                                "borderRadius": "6px",
                                                "cursor": "pointer",
                                                "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
                                                "transition": "background-color 0.3s ease",
                                            }
                                        )
                                    ], style={"alignSelf": "flex-end"}),
                                ], style={
                                    "display": "flex",
                                    "alignItems": "flex-end",
                                    "flexWrap": "wrap",
                                    "gap": "20px",
                                    "marginBottom": "25px"
                                }),

                                # Graph container with modern card style
                                dcc.Graph(
                                    id='io-risk_profile',
                                    style={
                                        "height": "80vh",
                                        "borderRadius": "12px",
                                        "boxShadow": "0 8px 20px rgba(0,0,0,0.12)",
                                        "backgroundColor": "#fff",
                                        "padding": "15px"
                                    }
                                ),

                                # Store for risk weights (hidden)
                                dcc.Store(id="risk-weights-store"),
                            ], style=CARD_STYLE)
                        ]
                    )
                ]
            )
        ]
    )
