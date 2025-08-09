from dash import html

def get_header_layout(ABOUT_TEXT_TOP, ABOUT_TEXT_BULLETS, ABOUT_TEXT_BOTTOM, ABOUT_WEIGHTED_HHI, LABEL_STYLE):
    return html.Div([
        # Top bar with About button
        html.Div(
            style={
                "backgroundColor": "#ffffff",
                "marginBottom": "20px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "padding": "10px 20px"
            },
            children=[
                html.H1(
                    "Input-Output Flow Map Dashboard",
                    style={"textAlign": "left", "color": "#333", "margin": 0}
                ),
                html.Button(
                    "About",
                    id="about-button",
                    style={
                        "backgroundColor": "#007bff",
                        "color": "white",
                        "border": "none",
                        "padding": "8px 16px",
                        "borderRadius": "5px",
                        "cursor": "pointer",
                        "fontSize": "14px"
                    }
                )
            ]
        ),

        # Floating About modal (hidden initially)
        html.Div(
            id="about-modal",
            style={
                "display": "none",
                "position": "fixed",
                "top": "0",
                "left": "0",
                "width": "100%",
                "height": "100%",
                "backgroundColor": "rgba(0,0,0,0.4)",
                "zIndex": "1000",
                "justifyContent": "center",
                "alignItems": "center"
            },
            children=[
                html.Div(
                    style={
                        "backgroundColor": "#fff",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "width": "50%",
                        "maxHeight": "80%",
                        "overflowY": "auto",
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.3)",
                        "position": "relative"
                    },
                    children=[
                        html.Button(
                            "×",
                            id="close-about",
                            style={
                                "position": "absolute",
                                "top": "10px",
                                "right": "10px",
                                "background": "none",
                                "border": "none",
                                "fontSize": "20px",
                                "cursor": "pointer",
                                "color": "#888"
                            }
                        ),
                        html.H3("About This Dashboard"),
                        ABOUT_TEXT_TOP,
                        html.H4("How to Use:"),
                        ABOUT_TEXT_BULLETS,
                        ABOUT_TEXT_BOTTOM,
                        ABOUT_WEIGHTED_HHI
                    ]
                )
            ]
        )
    ])
