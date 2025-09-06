from process.utils import obtain_inputs
from pandas import DataFrame
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_cluster_wrapper(app, data):
    @app.callback(
        Output("cluster_figure", "figure"),
        Output("cluster-dropdown", "options"),
        [
            Input('cluster-industry', 'value'),
            Input('cluster-country', 'value'),
            Input('cluster-input', 'value'),
            Input("cluster-dropdown", "value")
        ]
    )
    def update(cluster_industry, cluster_country, cluster_input, cluster_dropdown_value):
        df = data["data"]
        df2 = data["all_countries"]
        df3 = data["metadata"]

        import_industries = list(df3["Code"])
        export_countries = list(df2["Code"])

        # drop duplicates
        for c in [cluster_country, "ROW"]:
            if c in export_countries:
                export_countries.remove(c)

        export_rows = [f"{country}_{cluster_industry}" for country in export_countries]
        import_cols = [f"{cluster_country}_{industry}" for industry in import_industries]

        df = df.loc[export_rows, import_cols]
        df.index = df.index.str.split("_").str[0]

        thres = np.median(df.sum(axis=1))
        df = df[df.sum(axis=1) >= thres]

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df)

        # find best k
        sil_scores = []
        k_values = range(int(cluster_input), min(len(df), 12))
        for k in k_values:
            kmeans = KMeans(n_clusters=k, random_state=42)
            labels = kmeans.fit_predict(X_scaled)
            sil_scores.append(silhouette_score(X_scaled, labels))

        best_k = k_values[np.argmax(sil_scores)]
        kmeans = KMeans(n_clusters=best_k, random_state=42)
        labels = kmeans.fit_predict(X_scaled)

        cluster_centers = DataFrame(kmeans.cluster_centers_, columns=df.columns)
        cluster_centers.index = [f"Cluster {i}" for i in range(best_k)]
        cluster_centers.columns = cluster_centers.columns.str.split("_", n=1).str[1]

        x_labels = [code.split("_")[1] if "_" in code else code for code in df.columns]

        # cluster assignment mapping
        cluster_map = {f"Cluster {i}": df.index[labels == i].tolist() for i in range(best_k)}
        dropdown_options = [{"label": f"Cluster {i}", "value": i} for i in range(best_k)]

        # figure: heatmap + table for selected cluster (default 0)
        selected_cluster = 0
        table_data = [cluster_map[f"Cluster {selected_cluster}"]]

        fig = make_subplots(
            rows=1, cols=3,
            column_widths=[0.7, 0.15, 0.15],
            specs=[[{"type": "heatmap"}, {"type": "table"}, {"type": "table"}]],
            horizontal_spacing=0.01
        )

        # heatmap
        fig.add_trace(
            go.Heatmap(
                z=cluster_centers.values,
                x=x_labels,
                y=cluster_centers.index,
                colorscale="RdBu_r",
                colorbar=dict(title="Value"),
                zmin = -5.0,
                zmax = 5.0
            ),
            row=1, col=1
        )

        x_labels = list(df3["Code"].values)
        # mapping table
        mapping = dict(zip(df3["Code"], df3["Industry"]))
        table_data = [[x_labels[i] for i in range(len(x_labels))],
                    [mapping.get(x_labels[i], x_labels[i]) for i in range(len(x_labels))]]

        # table
        fig.add_trace(
            go.Table(
                header=dict(values=["Code", "Industry"], fill_color="lightgrey", align="left"),
                cells=dict(values=table_data, align="left")
            ),
            row=1, col=2
        )

        if cluster_dropdown_value is None:
            cluster_dropdown_value = 1
        # print(cluster_dropdown_value)
        output = {"label": list(labels), "country": list(df.index)}
        output = DataFrame(output)
        output = output[output["label"] == cluster_dropdown_value]
        output_list = [list(output["label"]), list(output["country"])]
        fig.add_trace(
            go.Table(
                header=dict(values=["Cluster", "Country"], fill_color="lightgrey", align="left"),
                cells=dict(values=output_list, align="left")
            ),
            row=1, col=3
        )

        return fig, dropdown_options
