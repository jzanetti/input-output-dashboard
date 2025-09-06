from dash import html, dcc
from process.layout.styles import LABEL_STYLE, DROPDOWN_STYLE, CARD_STYLE

def sidebar_tab_share(industry_options):
    return html.Div(id="selected-input-container", children=[
        html.Label("Input industry:", style=LABEL_STYLE),
        dcc.Dropdown(
            id='selected-input',
            options=industry_options,
            value='A01_02',
            style=DROPDOWN_STYLE
        )
        ], style=CARD_STYLE)