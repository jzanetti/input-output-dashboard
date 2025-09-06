import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from process.layout.header import get_header_layout
# from process.layout.sidebar_wrapper import get_sidebar_layout
from process.layout.tabs_wrapper import get_tabs_layout

from process.map import create_map_wrapper
from process.share import create_share_wrapper, create_share_data
from process.risk import create_risk_wrapper, create_risk_data
from process.data import load_data
from process.cluster import create_cluster_wrapper
from process.layout.others.about import about
# from process.layout.update import tab2_update, sidebar_update
from process.layout.sidebar_wrapper import create_sidebars, hide_sidebars, update_sidebars
# -----------------------
# Load data
# -----------------------
data = load_data()
industry_options = [
    {'label': f"{row['Industry']}", 'value': row['Code']}
    for _, row in data["metadata"].iterrows()
]
# country_options = list(set(data["all_countries"].Code))
country_options = []
for _, proc_row in data["all_countries"].iterrows():
    country_options.append(
        {"label": proc_row["countries"], "value": proc_row["Code"]}
    )


# -----------------------
# App init
# -----------------------
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server   # <<< important: this is what WSGI will import
app.title = "Input-Output Flow Map Dashboard"

# -----------------------
# Layout
# -----------------------
create_sidebars(app, data, industry_options, country_options)

app.layout = html.Div(
    style={"backgroundColor": "#f8f9fa", "fontFamily": "Arial, sans-serif"},
    children=[
        get_header_layout(),
        html.Div(
            style={"display": "flex", "padding": "0 20px"},
            children=[
                # get_sidebar_layout(data, industry_options, LABEL_STYLE, DROPDOWN_STYLE, CARD_STYLE),
                html.Div(
                    id="dynamic-sidebar",
                    style={"width": "20%", "minWidth": "250px", "marginRight": "20px"},
                ),
                get_tabs_layout(industry_options),
                dcc.Store(id='io-share-data'),# hidden store
                dcc.Store(id="risk-weights-store")
            ]
        )
    ]
)


# -----------------------
# Obtain dynamic data
# -----------------------
create_share_data(app, data)
create_risk_data(app)

# -----------------------
# Callbacks
# -----------------------
about(app)
hide_sidebars(app)

update_sidebars(app, data)
create_map_wrapper(app, data)
create_share_wrapper(app)
create_risk_wrapper(app, data)
create_cluster_wrapper(app, data)


# -----------------------
# Run
# -----------------------
if __name__ == '__main__':
    app.run(debug=True)
