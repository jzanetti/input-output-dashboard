import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from layout.header import get_header_layout
from layout.sidebar import get_sidebar_layout
from layout.tabs import get_tabs_layout

from process.map import create_io_map
from process.summary import create_io_summary
from process.data import load_data
from process.utils import obtain_inputs
from process.risk import update_risk_chart

# -----------------------
# Load data
# -----------------------
data = load_data()
industry_options = [
    {'label': f"{row['Industry']}", 'value': row['Code']}
    for _, row in data["metadata"].iterrows()
]

# -----------------------
# About text
# -----------------------
# -----------------------
# "About" section contents
# -----------------------
ABOUT_TEXT_TOP = html.P(
    "This dashboard visualizes global Input-Output trade flows (using OECD 2020 inter-country table). "
    "It allows you to explore trade relationships between countries and industries, "
    "highlighting both major and secondary trade partners."
)

ABOUT_TEXT_BULLETS = html.Ul([
    html.Li("Select an importer country from the left panel."),
    html.Li("Choose an industry to focus on."),
    html.Li("Adjust the number of top trading partners to display."),
    html.Li("Enable or disable secondary partners and trading volume thickness."),
    html.Li("Switch between Map, Pie or Risk profile Chart views."),
])

ABOUT_TEXT_BOTTOM = html.P(
    "The map shows directional trade flows, while the pie chart breaks down "
    "contributions by partner industries. "
    "Tip: Start with fewer top partners for clearer visualization, then expand to see more details."
)

ABOUT_WEIGHTED_HHI = html.P(
    "The risk profile is illustrated by The Weighted Herfindahl-Hirschman Index (HHI), which is a measure of concentration "
    "used to assess the risk associated with the diversity of input sources in the supply chain. "
    "A higher weighted HHI indicates less diversity and potentially higher risk from relying on fewer suppliers."
)

# -----------------------
# Styling
# -----------------------
CARD_STYLE = {
    "backgroundColor": "#ffffff",
    "padding": "15px",
    "marginBottom": "15px",
    "borderRadius": "8px",
    "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
}
LABEL_STYLE = {"fontWeight": "bold", "marginBottom": "5px", "display": "block"}
DROPDOWN_STYLE = {"width": "100%", "marginBottom": "10px"}

# -----------------------
# App init
# -----------------------
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server   # <<< important: this is what WSGI will import
app.title = "Input-Output Flow Map Dashboard"

# -----------------------
# Layout
# -----------------------
app.layout = html.Div(
    style={"backgroundColor": "#f8f9fa", "fontFamily": "Arial, sans-serif"},
    children=[
        get_header_layout(ABOUT_TEXT_TOP, ABOUT_TEXT_BULLETS, ABOUT_TEXT_BOTTOM, ABOUT_WEIGHTED_HHI, LABEL_STYLE),

        html.Div(
            style={"display": "flex", "padding": "0 20px"},
            children=[
                get_sidebar_layout(data, industry_options, LABEL_STYLE, DROPDOWN_STYLE, CARD_STYLE),
                get_tabs_layout(industry_options, CARD_STYLE, LABEL_STYLE)
            ]
        )
    ]
)

# -----------------------
# Callbacks
# -----------------------
@app.callback(
    Output("about-modal", "style"),
    [Input("about-button", "n_clicks"),
     Input("close-about", "n_clicks")],
    prevent_initial_call=True
)
def toggle_modal(open_clicks, close_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return {"display": "none"}
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "about-button":
        return {
            "display": "flex",
            "position": "fixed",
            "top": "0",
            "left": "0",
            "width": "100%",
            "height": "100%",
            "backgroundColor": "rgba(0,0,0,0.4)",
            "zIndex": "1000",
            "justifyContent": "center",
            "alignItems": "center"
        }
    return {"display": "none"}

@app.callback(
    Output('tab2-dropdown-selection', 'options'),
    Output('tab2-dropdown-selection', 'value'),
    Input('graph-tabs', 'value'),
    Input('industry-dropdown', 'value'),
    Input('country-dropdown', "value")
)
def update_dropdown_options(selected_tab, selected_industry, selected_country):
    inputs = obtain_inputs(
        data["data"],
        selected_industry,
        50,
        selected_country=selected_country,
        run_filter=False
    )
    industry_opts = []
    for proc_option in list(set(inputs.index.str.split('_', n=1).str[1])):
        industry_opts.append({
            "label": data["metadata"][data["metadata"]["Code"] == proc_option]["Industry"].values[0],
            "value": proc_option
        })
    if selected_tab == "tab-2":
        options = industry_opts
        default_value = options[0]['value'] if options else None
        return options, default_value
    return [], None

@app.callback(
    Output('secondary-dependencies-container', 'style'),
    Input('graph-tabs', 'value')
)
def toggle_visibility(selected_tab):
    return {"display": "none"} if selected_tab in ['tab-2', 'tab-3'] else CARD_STYLE

@app.callback(
    Output('thickness-container', 'style'),
    Input('graph-tabs', 'value')
)
def toggle_visibility2(selected_tab):
    return {"display": "none"} if selected_tab in ['tab-2', 'tab-3'] else CARD_STYLE

@app.callback(
    Output('top-dependencies-container', 'style'),
    Input('graph-tabs', 'value')
)
def toggle_visibility3(selected_tab):
    if selected_tab in ['tab-2', 'tab-3']:
        return {"display": "none"}
    else:
        return CARD_STYLE

@app.callback(
    Output('io-summary', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('industry-dropdown', 'value'),
     Input("top-dependencies", "value"),
     Input("tab2-dropdown-selection", "value")]
)
def update_summary(selected_country, selected_output_industry, selected_deps, selected_input_industry):
    try:
        return create_io_summary(
            data["data"],
            selected_country,
            selected_output_industry,
            selected_input_industry,
            data["metadata"],
            data["all_countries"]
        )
    except Exception:
        fig = go.Figure()
        fig.add_annotation(
            text="Error: Not able to find data",
            xref="paper", yref="paper", x=0.5, y=0.5,
            showarrow=False, font=dict(size=20, color="red")
        )
        return fig

@app.callback(
    Output('io-map', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('industry-dropdown', 'value'),
     Input("top-dependencies", "value"),
     Input("secondary-dependencies", "value"),
     Input("use-thickness", "value")]
)
def update_map(selected_country, selected_industry, selected_deps, selected_sec_deps, use_thickness):
    try:
        return create_io_map(
            data["data"],
            selected_country,
            selected_industry,
            selected_deps,
            data["metadata"],
            data["all_countries"],
            selected_sec_deps=selected_sec_deps,
            use_thickness=use_thickness
        )
    except Exception:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error: Not able to find {selected_industry} for {selected_country}",
            xref="paper", yref="paper", x=0.5, y=0.5,
            showarrow=False, font=dict(size=20, color="red")
        )
        return fig


@app.callback(
    Output("risk-weights-store", "data"),
    Input("update-risk-weight", "n_clicks"),
    [dash.dependencies.State("risk-country-input", "value"),
     dash.dependencies.State("risk-weight-input", "value"),
     dash.dependencies.State("risk-weights-store", "data")],
    prevent_initial_call=True
)
def update_risk_weights(n_clicks, country, weight, current_data):
    if current_data is None:
        current_data = {}
    if country and weight is not None:
        current_data[country] = weight
    return current_data

@app.callback(
    Output("io-risk_profile", "figure"),
    [Input("risk-weights-store", "data"),
     Input('country-dropdown', 'value'),
     Input('industry-dropdown', 'value'),
     Input("top-dependencies", "value")]
)
def update_risk(risk_weights_data, selected_country, selected_industry, selected_deps):
    return update_risk_chart(
        data["data"], 
        risk_weights_data, 
        selected_country, 
        selected_industry,
        data["metadata"],
        data["all_countries"])


# -----------------------
# Run
# -----------------------
if __name__ == '__main__':
    app.run(debug=True)
