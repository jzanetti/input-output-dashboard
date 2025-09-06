from dash.dependencies import Input, Output
from process.utils import obtain_inputs
from process.layout.sidebars.map import sidebar_importer, sidebar_industry, sidebar_secondary_deps, sidebar_line_thickness, sidebar_top_deps

def sidebar_update(app, data, industry_options):
    @app.callback(
        Output("dynamic-sidebar", "children"),
        Input("graph-tabs", "value")
    )
    def update_sidebar(selected_tab):
        if selected_tab == "tab-1":  # e.g., your map tab id
            return [
                sidebar_importer(data),
                sidebar_secondary_deps()
            ]
        elif selected_tab == "tab-heatmap":
            return [
                sidebar_industry(industry_options),
                sidebar_top_deps()
            ]
        elif selected_tab == "tab-cluster":
            return [
                sidebar_line_thickness()
            ]
        else:
            # default sidebar
            return [
                sidebar_importer(data),
                sidebar_industry(industry_options),
                sidebar_top_deps(),
                sidebar_secondary_deps(),
                sidebar_line_thickness()
            ]



def tab2_update(app, data):
    @app.callback(
        Output('tab2-dropdown-selection', 'options'),
        Output('tab2-dropdown-selection', 'value'),
        Input('graph-tabs', 'value'),
        Input('industry-dropdown', 'value'),
        Input('country-dropdown', "value")
    )
    def update(selected_tab, selected_industry, selected_country):
        if selected_tab != "tab-2":
            return [], None




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

        options = industry_opts
        default_value = options[0]['value'] if options else None
        return options, default_value
