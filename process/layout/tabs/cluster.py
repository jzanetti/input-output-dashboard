from dash import html, dcc
from process.layout.styles import CARD_STYLE

def tab_cluster():
    return dcc.Tab(
        label="Cluster",
        value='tab-cluster',
        children=[
            html.Div([
                html.H3("Export Country Clustering", style={"marginBottom": "5px"}),
                html.Div([
                    html.P(),
                    html.Ul([
                        html.Li("X-axis (clusters): groups of countries that export in similar ways to the selected country (the \"Market\" country, chosen in the left panel). Each cluster shows countries with comparable export patterns."),
                        html.Li("Y-axis (industries): represent the different industries for the \"Market Country\"."),
                        html.Li("Colors (red/blue in the heatmap): indicate the impact of exports in each cluster. Red means above-average exports, and blue means below-average exports. For example, if the heatmap's value is 5.3 for a cluster, this cluster is ~5.3 standard deviations above the mean for that industry."),
                    ], style={"color": "#555", "marginTop": "0px"}),

                    html.P(
                        "For example, if the \"Market\" is China, each cell in the heatmap shows a specific cluster's export behavior from the selected industry (e.g., A01_02) across the world, to a particular Chinese industry:",
                        style={"marginBottom": "5px", "color": "#555"}),
                    html.Ul([
                        html.Li([
                            html.Strong("High Positive Value (Bright Red, e.g., +3): "),
                            "Countries in this cluster export more of their \"A01_02\" products to that Chinese industry than the average country. For example, if Cluster 0 has +3 in 'C10_12' (food manufacturing etc.), it indicates these countries heavily supply China’s food sector, reflecting a strong trade dependency."
                        ], style={"marginBottom": "5px", "color": "#555"}),
                        html.Li([
                            html.Strong("High Negative Value (Bright Blue, e.g., -3): "),
                            "Countries in this cluster export less to that Chinese industry than the average. For example, a value of -3 in 'CN1_C26' (electronics) suggests minimal A01_02 exports to China’s electronics sector."
                        ], style={"marginBottom": "5px", "color": "#555"})
                    ]),

                    html.P("The figure illustrates export risk exposure. For example, if countries X and Y—both in the same cluster—export substantially above-average volumes of agricultural products to China’s food industry, any disruption in China’s food market would likely have an immediate effect on their agricultural exports, reflecting their strong reliance on this trade link.",
                        style={"marginBottom": "5px", "color": "#555"}
                    ),
                ]),
                dcc.Graph(id='cluster_figure', style={"height": "80vh", "width": "120vh"})
            ], style=CARD_STYLE)
        ]
    )

