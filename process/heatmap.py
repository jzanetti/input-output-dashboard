import pandas as pd
import numpy as np
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def strip_country(label):
    return label.split("_", 1)[1] if "_" in label else label

def create_heatmap(
    df: pd.DataFrame,
    df_metadata: pd.DataFrame,
    selected_country: str,
    reference_country: str,
    use_log: str = "linear"
) -> go.Figure:

    # Generate index and column labels for the heatmap
    industries = df_metadata['Code'].tolist()
    row_labels = [f"{selected_country}_{industry}" for industry in industries]
    col_labels = [f"{reference_country}_{industry}" for industry in industries]

    # Extract submatrix for heatmap (vectorized)
    heatmap_data = df.loc[row_labels, col_labels].astype(float)

    col_labels_reversed = col_labels[::-1]
    heatmap_data = heatmap_data[col_labels_reversed]

    # Handle missing values by filling with zeros (or np.nan if preferred)
    # heatmap_data = heatmap_data.fillna(0)

    # Apply log scaling if requested
    if use_log == "log":
        heatmap_data = np.log1p(heatmap_data)

    # Prepare hovertemplate for better readability
    hovertemplate = (
        "<b>From %{y}</b><br>" +
        "<b>To %{x}</b><br>" +
        "Value: %{z:.4f}<extra></extra>"
    )

    x_labels = [strip_country(lbl) for lbl in col_labels_reversed]
    y_labels = [strip_country(lbl) for lbl in row_labels]

    # Create heatmap trace
    heatmap_trace = go.Heatmap(
        z=heatmap_data.values,
        x=x_labels,
        y=y_labels,
        colorscale='jet',
        colorbar=dict(
            title=dict(text="Input Value", side="right"),
            ticks="outside",
            thickness=20
        ),
        zmin=np.nanmin(heatmap_data.values),
        zmax=np.nanmax(heatmap_data.values),
        hovertemplate=hovertemplate
    )

    # Diagonal line from top-left to bottom-right (industry vs same industry)
    diag_trace = go.Scatter(
        x=x_labels[::-1],
        y=y_labels,
        mode='lines',
        line=dict(color='red', dash='dash', width=2),
        hoverinfo='skip',
        showlegend=False
    )

    # Compose figure
    fig = go.Figure(data=[heatmap_trace, diag_trace])

    # Layout styling for clarity and professionalism
    fig.update_layout(
        title=dict(
            text=f"Input-Output Heatmap: from {selected_country} (y-axis) to {reference_country} (x-axis)",
            x=0.5,
            xanchor='center',
            font=dict(size=18, family="Arial, sans-serif")
        ),
        xaxis=dict(
            title=f"Industries of {reference_country}",
            tickangle=45,
            tickfont=dict(size=11),
            automargin=True,
            showgrid=False,
            zeroline=False,
            side='bottom',
        ),
        yaxis=dict(
            title=f"Industries of {selected_country}",
            autorange='reversed',
            tickfont=dict(size=11),
            automargin=True,
            showgrid=False,
            zeroline=False,
            scaleanchor="x",  # ensures same scale as x-axis
            scaleratio=1,
        ),
        margin=dict(l=100, r=40, t=80, b=120),
        plot_bgcolor='white',
        hovermode='closest'
    )

    return fig
