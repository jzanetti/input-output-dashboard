from process.utils import obtain_inputs
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def create_io_summary(
    df,
    selected_country,
    selected_output_industry,
    selected_input_industry,
    metadata,
    country_info
):
    """
    Create an input-output summary figure with a bar chart and pie chart.

    Parameters
    ----------
    df : pd.DataFrame
        IO data.
    selected_country : str
        ISO country code.
    selected_output_industry : str
        Industry code for the output.
    selected_input_industry : str
        Industry code for the input.
    selected_deps : list
        List of dependencies.
    metadata : pd.DataFrame
        Industry metadata (Code, Industry).
    country_info : pd.DataFrame
        Country metadata (Code, countries).

    Returns
    -------
    fig : plotly.graph_objects.Figure or None
        The generated Plotly figure, or None if no input industry is selected.
    """
    if not selected_input_industry:
        return None

    # --- Data Preparation ---
    inputs = obtain_inputs(
        df,
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
        country_info[["Code", "countries"]],
        left_on="Country_Code",
        right_on="Code",
        how="left"
    ).merge(
        metadata[["Code", "Industry"]],
        left_on="Industry_code",
        right_on="Code",
        how="left",
        suffixes=("", "_industry")
    )

    inputs = inputs[["countries", "Industry_code", "Industry", "value"]]

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
        rows=1, cols=2,
        specs=[[{"type": "xy"}, {"type": "domain"}]],
        subplot_titles=(
            f"Inputs for {selected_output_industry_name}",
            f"Country Share for {selected_input_industry_name}"
        )
    )

    # Bar Chart
    code_values = inputs.groupby("Industry")["value"].sum().reset_index()
    colors = [
        "red" if code == selected_input_industry_name else "skyblue"
        for code in code_values["Industry"]
    ]
    fig.add_trace(
        go.Bar(
            x=code_values["Industry"],
            y=code_values["value"],
            marker_color=colors
        ),
        row=1, col=1
    )

    # Pie Chart
    fig.add_trace(
        go.Pie(
            values=proc_inputs["percentage"],
            labels=proc_inputs["countries"],
            hovertemplate="Label: %{label}<br>Percentage: %{value}%<br>Value: %{customdata}",
            customdata=proc_inputs["value"],
            name=f"{selected_input_industry} (Total: {total_value})"
        ),
        row=1, col=2
    )

    # --- Layout ---
    fig.update_annotations(font_size=10)
    fig.update_layout(
        title_text=(
            f"For the production of <b>{selected_output_industry_name} ({selected_output_industry})</b> "
            f"in {selected_country}:<br>"
            f"The contribution from <b>{selected_input_industry_name} ({selected_input_industry})</b> "
            f"is {total_value} million USD"
        ),
        showlegend=False,
        height=800,
        width=1200,
        margin=dict(l=40, r=40, t=100, b=0)
    )

    return fig
