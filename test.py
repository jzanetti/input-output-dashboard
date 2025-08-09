import pandas as pd
import plotly.graph_objects as go
import numpy as np
from process import COUNTRY_COORDS
from random import uniform
from process.utils import calculate_risk_index


def quadratic_bezier(t, p0, p1, p2):
    """Calculate points on a quadratic Bezier curve.
    t: Parameter from 0 to 1
    p0: Start point [x, y]
    p1: Control point [x, y]
    p2: End point [x, y]
    """
    x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
    y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
    return x, y

def create_io_map(df, selected_country, selected_industry, metadata):
    """
    Create a map showing input flows to a country-industry pair with risk index.
    
    Parameters:
    - df: pandas DataFrame with country-industry pairs as row indices and columns
    - selected_country: str, country name (e.g., 'USA')
    - selected_industry: str, industry name (e.g., 'Agriculture')
    
    Returns:
    - fig: Plotly Figure object
    """
    # Extract relevant column
    target_col = f"{selected_country}_{selected_industry}"
    if target_col not in df.columns:
        raise ValueError(f"Column {target_col} not found in DataFrame")
    
    # Get input data (exclude zero or negative inputs)
    inputs = df[target_col]
    inputs = inputs[inputs > 0]
    filtered_df = inputs[~inputs.index.str.startswith('NZL')]
    inputs = filtered_df.nlargest(30)

    # Calculate risk index
    risk_index = calculate_risk_index(inputs)
    
    # Extract country names and prepare data for plotting
    plot_data = []
    for idx, value in inputs.items():
        input_country, input_industry = idx.split('_', 1)
        if input_country == selected_country or input_country not in COUNTRY_COORDS:
            continue
        start_lat, start_lon = COUNTRY_COORDS[input_country]
        end_lat, end_lon = COUNTRY_COORDS[selected_country]
        plot_data.append({
            'input_country': input_country,
            'input_industry': input_industry,
            'value': value,
            'start_lat': start_lat,
            'start_lon': start_lon,
            'end_lat': end_lat,
            'end_lon': end_lon
        })
    
    # Convert to DataFrame for grouping
    plot_df = pd.DataFrame(plot_data)
    
    # Group by start/end coordinates to identify overlapping lines
    grouped = plot_df.groupby(['start_lon', 'start_lat', 'end_lon', 'end_lat'])
    
    # Define a color palette
    input_countries = list(set(plot_df['input_country']))
    color_palette = [
        '#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD',
        '#8C564B', '#E377C2', '#7F7F7F', '#BCBD22', '#17BECF'
    ]
    country_colors = {country: color_palette[i % len(color_palette)] 
                     for i, country in enumerate(input_countries)}
    
    # Normalize input values for arrow thickness (scale between 1 and 10)
    max_input = inputs.max() if inputs.max() > 0 else 1
    thicknesses = (inputs / max_input) * 10
    
    # Create figure
    fig = go.Figure()
    
    # Number of points for smooth Bezier curves
    num_points = 50
    
    # Add smooth curves for each input
    for (start_lon, start_lat, end_lon, end_lat), group in grouped:
        num_lines = len(group)
        for i, row in enumerate(group.itertuples()):
            # Calculate midpoint for control point
            row_input_industry_str = metadata[metadata["Code"] == row.input_industry]["Industry"].values[0]
            mid_lon = (start_lon + end_lon) / 2
            mid_lat = (start_lat + end_lat) / 2
            
            # Calculate perpendicular offset
            offset_magnitude = 10 * 0.5 * (i - (num_lines - 1) / 2)  # Adjust scale as needed
            # offset_magnitude = 0.001
            dx = end_lon - start_lon
            dy = end_lat - start_lat
            length = np.sqrt(dx**2 + dy**2)
            
            if length > 0:
                perp_dx = -dy / length
                perp_dy = dx / length
            else:
                perp_dx, perp_dy = 0, 0
            
            # Apply offset to midpoint
            control_lon = mid_lon + offset_magnitude * perp_dx
            control_lat = mid_lat + offset_magnitude * perp_dy
            
            # Generate Bezier curve points
            t = np.linspace(0, 1, num_points)
            lon, lat = [], []
            for ti in t:
                x, y = quadratic_bezier(ti, [start_lon, start_lat], [control_lon, control_lat], [end_lon, end_lat])
                lon.append(x)
                lat.append(y)
            
            # Add trace
            thickness = 1 # thicknesses[f"{row.input_country}_{row.input_industry}"]
            color = country_colors.get(row.input_country, '#7F7F7F')
            fig.add_trace(go.Scattergeo(
                lon=lon,
                lat=lat,
                mode='lines',
                line=dict(width=thickness, color=color),
                opacity=0.3,
                hoverinfo='text',
                text=f"{row.input_country}_{row_input_industry_str} to {selected_country}: {row.value:.2f}",
                name=f"{row.input_country}: {row_input_industry_str}"
            ))
    
    # Add marker for selected country
    fig.add_trace(go.Scattergeo(
        lon=[COUNTRY_COORDS[selected_country][1]],
        lat=[COUNTRY_COORDS[selected_country][0]],
        mode='markers',
        marker=dict(size=15, color='red', symbol='circle'),
        hoverinfo='text',
        text=f"{selected_country} ({selected_industry})",
        name=selected_country
    ))
    
    # Add risk index annotation
    fig.add_annotation(
        x=0.05,
        y=0.95,
        xref="paper",
        yref="paper",
        text=f"Risk Index: {risk_index:.3f}",
        showarrow=False,
        font=dict(size=12, color="black"),
        bgcolor="white",
        bordercolor="black",
        borderwidth=1
    )
    
    # Update layout for map
    fig.update_layout(
        title=f"Input Flows to {selected_country} - {selected_industry}",
        showlegend=True,
        geo=dict(
            scope='world',
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)'
        )
    )
    
    return fig

# Example usage
if __name__ == "__main__":
    from process.data import read_input_output_table

    data = read_input_output_table()
    input_output_table = data["table"].set_index("V1")

    all_countries = list(data["countrycode"]["Code"])
    df = input_output_table[[col for col in input_output_table.columns if any(col.startswith(prefix) for prefix in all_countries)]]
    mask = df.index.str.startswith(tuple(all_countries))
    df = df[mask]
    df.index.name = None

    # Create map
    fig = create_io_map(df, "NZL", "Q", data["metadata"])
    fig.show()