import numpy as np
import pandas as pd
import plotly.graph_objects as go

from process import COUNTRY_COORDS
from process.utils import calculate_risk_index, quadratic_bezier, obtain_inputs


def add_links(line_index, total_lines, start_lon, end_lon, start_lat, end_lat, num_points=50):
    """
    Generate latitude and longitude points for a curved link between two coordinates
    using a quadratic Bezier curve.

    Parameters:
    - line_index: index of this line among overlapping lines
    - total_lines: total overlapping lines between same start and end points
    - start_lon, end_lon, start_lat, end_lat: coordinates
    - num_points: number of points to sample along the curve

    Returns:
    - lat, lon: lists of coordinates along the curve
    """
    # Midpoint between start and end
    mid_lon = (start_lon + end_lon) / 2
    mid_lat = (start_lat + end_lat) / 2

    # Offset magnitude to separate overlapping lines
    offset_scale = 10 * 0.5 * (line_index - (total_lines - 1) / 2)

    # Perpendicular direction
    dx, dy = end_lon - start_lon, end_lat - start_lat
    length = np.hypot(dx, dy)
    perp_dx, perp_dy = (-dy / length, dx / length) if length > 0 else (0, 0)

    # Control point for the curve
    control_lon = mid_lon + offset_scale * perp_dx
    control_lat = mid_lat + offset_scale * perp_dy

    # Bezier curve calculation (vectorized)
    t = np.linspace(0, 1, num_points)
    lon, lat = zip(*[quadratic_bezier(ti, [start_lon, start_lat],
                                      [control_lon, control_lat],
                                      [end_lon, end_lat]) for ti in t])
    return lat, lon


def create_io_map(df, selected_country, selected_industry, selected_deps,
                  metadata, country_info, selected_sec_deps=False, use_thickness=False):
    """
    Create a world map showing input flows to a specific country-industry pair.

    Parameters:
    - df: pandas DataFrame containing input-output data
    - selected_country: str, country code
    - selected_industry: str, industry code
    - selected_deps: list of dependency levels
    - metadata: DataFrame mapping industry codes to names
    - country_info: DataFrame mapping country codes to names/colors
    - selected_sec_deps: bool, include secondary dependencies
    - use_thickness: bool, scale line thickness by value

    Returns:
    - Plotly Figure object, or None if no inputs found
    """

    def get_country_name(code):
        return country_info.loc[country_info["Code"] == code, "countries"].values[0]

    def get_industry_name(code):
        return metadata.loc[metadata["Code"] == code, "Industry"].values[0]

    all_inputs = {
        f"{selected_country}_{selected_industry}":
            obtain_inputs(df, selected_industry, selected_deps, selected_country=selected_country)
    }

    if not all_inputs[f"{selected_country}_{selected_industry}"].size:
        return None

    if selected_sec_deps:
        for proc_index in all_inputs[f"{selected_country}_{selected_industry}"].index:
            proc_country, proc_industry = proc_index.split("_", 1)
            all_inputs[proc_index] = obtain_inputs(df, proc_industry, selected_deps, selected_country=proc_country)

    # Calculate risk index (currently unused in plotting, but kept for future use)
    hhi = calculate_risk_index(all_inputs[f"{selected_country}_{selected_industry}"])

    plot_data = []
    for proc_key, inputs_series in all_inputs.items():
        proc_country = proc_key.split('_', 1)[0]
        max_input = inputs_series.max() if inputs_series.max() > 0 else 1

        for idx, value in inputs_series.items():
            input_country, input_industry = idx.split('_', 1)

            # Skip self-links and countries not in coordinates
            if input_country == proc_country or input_country not in COUNTRY_COORDS:
                continue

            start_lat, start_lon = COUNTRY_COORDS[input_country]
            end_lat, end_lon = COUNTRY_COORDS[proc_country]

            thickness = max((value / max_input) * 10, 1.0) if use_thickness else 1.0

            plot_data.append({
                'input_country': input_country,
                'input_industry': input_industry,
                'output_country': proc_country,
                'value': value,
                'start_lat': start_lat,
                'start_lon': start_lon,
                'end_lat': end_lat,
                'end_lon': end_lon,
                'thickness': thickness
            })

    plot_df = pd.DataFrame(plot_data)

    fig = go.Figure()

    for (start_lon, start_lat, end_lon, end_lat), group in plot_df.groupby(
            ['start_lon', 'start_lat', 'end_lon', 'end_lat']):
        for line_idx, row in enumerate(group.itertuples()):
            lat, lon = add_links(line_idx, len(group), start_lon, end_lon, start_lat, end_lat)

            fig.add_trace(go.Scattergeo(
                lon=lon,
                lat=lat,
                mode='lines',
                line=dict(width=row.thickness,
                          color=country_info.loc[country_info["Code"] == row.input_country, "color"].values[0]),
                opacity=0.3,
                hoverinfo='text',
                text=(
                    f"{get_country_name(row.input_country)} -> {get_country_name(row.output_country)}:<br>"
                    f"{get_industry_name(row.input_industry)}: {row.value:.2f}"
                ),
                name=f"{get_country_name(row.input_country)}: {get_industry_name(row.input_industry)}"
            ))

    # Add marker for the selected country
    sel_lat, sel_lon = COUNTRY_COORDS[selected_country]
    fig.add_trace(go.Scattergeo(
        lon=[sel_lon],
        lat=[sel_lat],
        mode='markers',
        marker=dict(size=15, color='red', symbol='circle'),
        hoverinfo='text',
        text=f"{selected_country} ({selected_industry})",
        name=selected_country
    ))

    fig.update_layout(
        title=dict(
            text=f"Input Flows to {get_country_name(selected_country)} - {get_industry_name(selected_industry)}",
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            pad=dict(b=10)
        ),
        showlegend=False,
        geo=dict(
            scope='world',
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)'
        ),
        margin=dict(t=50, b=50, l=50, r=50)
    )

    return fig
