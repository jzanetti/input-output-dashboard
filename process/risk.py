from process.utils import obtain_inputs
from pandas import DataFrame
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def compute_industry_risk(inputs_series, risk_weights):
    df = inputs_series.reset_index()
    df.columns = ['source', 'value']
    df['industry'] = df['source'].str.split('_', n=1).str[1]
    df['country'] = df['source'].str.split('_', n=1).str[0]

    results = []
    for industry, group in df.groupby('industry'):
        total = group['value'].sum()
        shares = group['value'] / total

        weighted_shares = shares * group['country'].map(risk_weights)
        weighted_shares = weighted_shares / weighted_shares.sum()

        weighted_HHI = (weighted_shares**2).sum()
        results.append({
            'industry': industry,
            'weighted_HHI': weighted_HHI
        })

    return DataFrame(results)


def update_risk_chart(
        df, 
        risk_weights_data, 
        selected_country, 
        selected_industry,
        metadata,
        country_info):
    # Default all weights to 1.0
    all_inputs = obtain_inputs(
        df,
        selected_industry,
        50,
        selected_country=selected_country,
        run_filter=False
    )

    selected_country_name = country_info[country_info["Code"] == selected_country]["countries"].values[0]
    selected_industry_name = metadata[metadata["Code"] == selected_industry]["Industry"].values[0]

    countries = all_inputs.index.str.split('_').str[0].unique()
    risk_weights = {c: 1.0 for c in countries}
    
    risk_weights[selected_country] = 0.0
    
    # Override with user-provided weights
    if risk_weights_data:
        risk_weights.update(risk_weights_data)

    # Prepare table data for risk weights
    table_df = DataFrame({
        "Country": list(risk_weights.keys()),
        "Weight": [round(w, 3) for w in risk_weights.values()]
    })

    # Compute metrics
    df_metrics = compute_industry_risk(all_inputs, risk_weights)

    # For exact matching rows, merge on 'industry' == 'Code':
    df_merged = df_metrics.merge(metadata, left_on='industry', right_on='Code', how='left')

    # If you want to replace the 'industry' column with the full industry name where matched:
    df_merged['industry'] = df_merged['Industry'].combine_first(df_merged['industry'])

    # Then drop extra columns:
    df_merged = df_merged.drop(columns=['Code', 'Industry'])

    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.7, 0.3],
        specs=[[{"type": "bar"}, {"type": "table"}]],
        horizontal_spacing=0.1
    )

    fig.add_trace(
        go.Bar(
            x=df_merged['industry'],
            y=df_merged['weighted_HHI'],
            text=df_merged['weighted_HHI'].round(3),
            textposition="outside",
            name="Weighted HHI"
        ),
        row=1, col=1
    )

    # Add table to col 2
    fig.add_trace(
        go.Table(
            header=dict(
                values=["Country", "Weight"],
                fill_color='lightgrey',
                align='center',
                font=dict(size=12, color='black')
            ),
            cells=dict(
                values=[table_df["Country"], table_df["Weight"]],
                align='center',
                font=dict(size=11),
                fill_color='white'
            )
        ),
        row=1, col=2
    )

    # Update layout
    fig.update_layout(
        title_text="Weighted HHI by Industry and Current Risk Weights",
        yaxis=dict(range=[0, 1.2], title="Weighted HHI"),
        xaxis=dict(title="Industry"),
        template="plotly_white",
        height=500,
        width=900,
        margin=dict(l=40, r=40, t=80, b=40)
    )

    return fig