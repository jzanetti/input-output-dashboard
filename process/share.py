from process.utils import obtain_inputs
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from pandas import DataFrame


def create_share_data(app, data):

    @app.callback(
        Output('io-share-data', 'data'),
        [Input('country-dropdown', 'value'),
        Input('industry-dropdown', 'value')]
    )
    def update(selected_country, selected_output_industry):
        inputs = obtain_inputs(
            data["data"],
            selected_output_industry,
            50,
            selected_country=selected_country,
            run_filter=False
        ).reset_index()

        value_col = f"{selected_country}_{selected_output_industry}"
        inputs = inputs.rename(columns={value_col: "value"})

        # Split index into country and industry codes
        split_codes = inputs["index"].str.split("_", n=1, expand=True)
        inputs["Country_Code"], inputs["Industry_code"] = split_codes[0], split_codes[1]

        # Merge country & industry names
        inputs = inputs.merge(
            data["all_countries"][["Code", "countries"]],
            left_on="Country_Code",
            right_on="Code",
            how="left"
        ).merge(
            data["metadata"][["Code", "Industry"]],
            left_on="Industry_code",
            right_on="Code",
            how="left",
            suffixes=("", "_industry")
        )

        return inputs[["countries", "Industry_code", "Industry", "value"]].to_dict('records')

    


def create_share_wrapper(app):

    @app.callback(
        Output('io-summary', 'figure'),
        [
            Input('io-share-data', 'data'),
            Input('country-dropdown', 'value'),
            Input('industry-dropdown', 'value'),
            Input("selected-input", "value")
        ]
    )
    def update(io_share_data, selected_country, selected_output_industry, selected_input_industry):
        return create_io_summary(
            io_share_data,
            selected_country,
            selected_output_industry,
            selected_input_industry
        )




def create_io_summary(
    io_share_data,
    selected_country,
    selected_output_industry,
    selected_input_industry,
):
    if not selected_input_industry:
        return None

    inputs = DataFrame(io_share_data)
    
    # Filter for the selected input industry
    proc_inputs = inputs[inputs["Industry_code"] == selected_input_industry].copy()

    proc_inputs["percentage"] = (proc_inputs["value"] / proc_inputs["value"].sum() * 100).round(2)
    total_value = round(proc_inputs["value"].sum(), 1)

    # Get readable names
    selected_output_industry_name = inputs.loc[
        inputs["Industry_code"] == selected_output_industry, "Industry"
    ].iloc[0]
    selected_input_industry_name = inputs.loc[
        inputs["Industry_code"] == selected_input_industry, "Industry"
    ].iloc[0]

    # --- Create Figure ---
    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{"type": "xy"}, {"type": "domain"}, {"type": "table"}]],
        subplot_titles=(
            f"{selected_output_industry_name}",
            f"Country Share"
        )
    )

    # Bar Chart
    code_values = inputs.groupby("Industry_code")["value"].sum().reset_index()
    colors = [
        "red" if code == selected_input_industry else "skyblue"
        for code in code_values["Industry_code"]
    ]
    fig.add_trace(
        go.Bar(
            x=code_values["Industry_code"],
            y=code_values["value"],
            marker_color=colors
        ),
        row=1, col=1
    )

    pie_text = [f"{p}%" if p > 10 else "" for p in proc_inputs["percentage"]]
    # Pie Chart
    fig.add_trace(
        go.Pie(
            values=proc_inputs["percentage"],
            labels=proc_inputs["countries"],
            hovertemplate="Label: %{label}<br>Percentage: %{value}%<br>Value: %{customdata}",
            customdata=proc_inputs["value"],
            name=f"{selected_input_industry} (Total: {total_value})",
            text=pie_text,              # selective labels
            textinfo="text",            # only use text (not value or percent)
        ),
        row=1, col=2
    )

    x_labels = list(code_values.Industry_code.values)
    # mapping table
    mapping = dict(zip(inputs["Industry_code"], inputs["Industry"]))
    table_data = [[x_labels[i] for i in range(len(x_labels))],
                [mapping.get(x_labels[i], x_labels[i]) for i in range(len(x_labels))]]
    fig.add_trace(
        go.Table(
            header=dict(values=["Industry_code", "Industry"], fill_color="lightgrey", align="left"),
            cells=dict(values=table_data, align="left")
        ),
        row=1, col=3
    )

    # --- Layout ---
    fig.update_annotations(font_size=15)
    fig.update_layout(
        title=dict(
            text=(
                f"For the output of <b>{selected_output_industry_name} ({selected_output_industry})</b> "
                f"in {selected_country}:<br>"
                f"The input from <b>{selected_input_industry_name} ({selected_input_industry})</b> "
                f"is {total_value} million USD<br>"
            ),
            font=dict(size=16),
            y=0.98,  # position (fraction of plot height, 1=top)
            pad=dict(l=-50, t=10, b=50)  # extra padding above and below title
        ),
        showlegend=False,
        height=500,
        width=1200,
        margin=dict(l=40, r=40, t=100, b=50)
    )

    return fig
