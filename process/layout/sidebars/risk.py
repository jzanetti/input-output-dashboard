
from dash import html, dcc
from process.layout.styles import LABEL_STYLE, DROPDOWN_STYLE, CARD_STYLE, VALUE_STYLE_TYPE1, BUTTON_STYLE

def sidebar_risk_weights(data):

    country_options = []

    for _, proc_row in data["all_countries"].iterrows():
        country_options.append(
            {"label": proc_row["countries"], "value": proc_row["Code"]}
        )

    return html.Div(id="risk-weights-container", children=[
        html.Label("Input Country for Risk Adjustment:", style=LABEL_STYLE),
        dcc.Dropdown(
            id="risk-country-input",
            options=country_options,
            value='CN1',
            style=DROPDOWN_STYLE
        ),
        html.Label("Risk Weight:", style=LABEL_STYLE),
        dcc.Input(
            id="risk-weight-input",
            type="number",
            value = 1.0,
            style=VALUE_STYLE_TYPE1
        ),
        html.Button("Update", id="update-risk-weight", style = BUTTON_STYLE)

    ], style=CARD_STYLE)