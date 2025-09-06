from dash import html, dcc
from process.layout.styles import LABEL_STYLE, DROPDOWN_STYLE, CARD_STYLE

def sidebar_importer(data):

    country_options = []

    for _, proc_row in data["all_countries"].iterrows():
        country_options.append(
            {"label": proc_row["countries"], "value": proc_row["Code"]}
        )


    return html.Div(id="selected-country-container", children=[
                html.Label("Country:", style=LABEL_STYLE),
                dcc.Dropdown(
                    id='country-dropdown',
                    # options=[{"label": c, "value": c} for c in list(data["all_countries"]["Code"])],
                    options = country_options,
                    value='NZL',
                    style=DROPDOWN_STYLE
                )
                ], style=CARD_STYLE)

def sidebar_industry(industry_options):
    return html.Div(id="selected-industry-container", children=[
                html.Label("Industry:", style=LABEL_STYLE),
                dcc.Dropdown(
                    id='industry-dropdown',
                    options=industry_options,
                    value='A01_02',
                    style=DROPDOWN_STYLE
                )
            ], style=CARD_STYLE)