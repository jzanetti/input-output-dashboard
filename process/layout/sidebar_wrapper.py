from process.layout.sidebars.map import sidebar_secondary_deps, sidebar_top_deps
from process.layout.sidebars.common import sidebar_importer, sidebar_industry 
from process.layout.sidebars.share import sidebar_tab_share
from process.layout.sidebars.risk import sidebar_risk_weights
from process.layout.sidebars.cluster import sidebar_cluster
from dash.dependencies import Input, Output
from process.layout.styles import CARD_STYLE
from pandas import DataFrame


def update_sidebars(app, data):
    @app.callback(
        [   
            Output('selected-input', 'options'),
            Output('selected-input', 'value')
        ],
        [
            Input('graph-tabs', 'value'),
            Input('io-share-data', 'data'),
            Input('industry-dropdown', 'value')
        ]
         
    )
    def update(selected_tab, io_share_data, selected_industry):
        industry_options = []
        if selected_tab == "tab-share":
            io_share_data = DataFrame(io_share_data)
            unique_code = list(io_share_data["Industry_code"].unique())
            for _, row in data["metadata"].iterrows():
                if row['Code'] in unique_code:
                    industry_options.append(
                        {'label': f"{row['Industry']}", 'value': row['Code']})
        else:
            for _, row in data["metadata"].iterrows():
                industry_options.append(
                    {'label': f"{row['Industry']}", 'value': row['Code']})

        return [industry_options, selected_industry]


def hide_sidebars(app):
    @app.callback(
        [   Output('selected-country-container', "style"),
            Output('selected-industry-container', "style"),
            Output('top-dependencies-container', "style"),
            Output('secondary-dependencies-container', 'style'),
            Output('selected-input-container', 'style'),
            Output('risk-weights-container', 'style'),
            Output('risk-cluster-container', 'style'),
        ],
        Input('graph-tabs', 'value')
    )
    def update(selected_tab):
        if selected_tab == "tab-map":
            return [
                CARD_STYLE,
                CARD_STYLE,
                CARD_STYLE,
                CARD_STYLE,
                {"display": "none"},
                {"display": "none"},
                {"display": "none"}
            ]
        elif selected_tab == "tab-share":
            return [
                CARD_STYLE,
                CARD_STYLE,
                {"display": "none"},
                {"display": "none"},
                CARD_STYLE,
                {"display": "none"},
                {"display": "none"}
            ]
        elif selected_tab == "tab-risk":
            return [
                CARD_STYLE,
                CARD_STYLE,
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
                CARD_STYLE,
                {"display": "none"}
            ]
        elif selected_tab == "tab-cluster":
            return [
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
                CARD_STYLE
            ]

def create_sidebars(app, data, industry_options, country_options):
    @app.callback(
        Output("dynamic-sidebar", "children"),
        Input("graph-tabs", "value")
    )
    def update(selected_tab):
        print("Selected tab: " + selected_tab)
        return [
                sidebar_importer(data),
                sidebar_industry(industry_options),
                sidebar_top_deps(),
                sidebar_secondary_deps(),
                sidebar_tab_share(industry_options),
                sidebar_risk_weights(data),
                sidebar_cluster(country_options, industry_options)
        ]


"""
def register_tab2_dropdown_callback(app, data):
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
"""