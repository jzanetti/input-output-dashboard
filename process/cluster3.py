import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import linkage, dendrogram
import plotly.express as px

# -------------------------
# Step 0: Load Data
# -------------------------
df = pd.read_csv("etc/2020.csv", index_col=0)
df2 = pd.read_csv("etc/country_code.csv", index_col=0)
df3 = pd.read_csv("etc/metadata.csv", index_col=0)

import_countries = "CN1"
import_industries = list(df3.index)

export_countries = list(df2.index) # ['ARG', 'AUS', 'AUT', 'BEL', 'BGD', 'BGR', 'BLR', 'NZL']
# export_countries = ['ARG', 'AUS', 'AUT', 'BEL', 'BGD', 'BGR', 'BLR', 'NZL']
export_industry = "A01_02"

try: 
    export_countries.remove(import_countries)
except ValueError:
    pass

try: 
    export_countries.remove("ROW")
except ValueError:
    pass
min_cluster = 2

export_rows = [f"{country}_{export_industry}" for country in export_countries]
import_cols = [f"{import_countries}_{industry}" for industry in import_industries]
df = df.loc[export_rows, import_cols]
df.index = df.index.str.split("_").str[0]
df = df[df.sum(axis=1) >= 500]
#df = df.div(df.sum(axis=1), axis=0) * 100
#df = df.dropna(axis=0, how='any')
# -------------------------
# Step 3: Scale
# -------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# -------------------------
# Step 4: Find Best k
# -------------------------
sil_scores = []
inertias = []
k_values = range(min_cluster, min(len(df), 12))  # avoid too large k
for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_scaled)
    sil = silhouette_score(X_scaled, labels)
    sil_scores.append(sil)
    inertias.append(kmeans.inertia_)

fig, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(k_values, inertias, 'o-', color='blue', label='Inertia (Elbow)')
ax1.set_xlabel("Number of clusters (k)")
ax1.set_ylabel("Inertia", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

ax2 = ax1.twinx()
ax2.plot(k_values, sil_scores, 's-', color='red', label='Silhouette Score')
ax2.set_ylabel("Silhouette Score", color='red')
ax2.tick_params(axis='y', labelcolor='red')

plt.title("Elbow & Silhouette Analysis")
fig.tight_layout()
plt.savefig("Elbow_Silhouette_Analysis.png")

# -------------------------
# Step 5: Final Clustering
# -------------------------
best_k = k_values[np.argmax(sil_scores)]
kmeans = KMeans(n_clusters=best_k, random_state=42)
labels = kmeans.fit_predict(X_scaled)

# -------------------------
# Step 6: PCA Scatter Plot
# -------------------------
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

pca_df = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
pca_df['Cluster'] = labels
pca_df['Entity'] = df.index  # Keep country_industry names

plt.figure(figsize=(8, 6))
sns.scatterplot(
    data=pca_df,
    x='PC1', y='PC2',
    hue='Cluster',
    palette='tab10',
    s=100
)

for _, row in pca_df.iterrows():
    plt.text(row['PC1'] + 0.02, row['PC2'] + 0.02, row['Entity'], fontsize=8)

plt.title("KMeans Clusters (PCA Projection)")
plt.legend(title='Cluster')
fig.tight_layout()
plt.savefig("cluster.png")

# -------------------------
# Step 7: Heatmap of Cluster Centers
# This heatmap shows the ‘average’ trade behavior of each group from the scatter plot. 
# Each row represents one cluster, and each column is a specific trade flow to China in a particular industry. 
# Red colors mean higher-than-average trade, blue means lower-than-average. 
# So, by looking at this, we see which industries and countries tend to trade more or less compared to others within their group.

# Example to make it clearer:
# Say the heatmap column is "CN1_A01_02" (trade from some country-industry to China’s agriculture sector), 
# and for Cluster 2, the heatmap cell is bright red with a value of +3.
# This means:
#   * The countries-industries in Cluster 2 export significantly more to China’s agriculture sector compared 
#     to the overall average export level in that industry across all clusters.
#  * Conversely, a blue value like -2 would mean: That cluster exports less than average to China’s agriculture sector.
# -------------------------
cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=df.columns)
cluster_centers.index = [f"Cluster {i}" for i in range(best_k)]

plt.figure(figsize=(12, 6))
sns.heatmap(cluster_centers, cmap='seismic', center=0, vmin=-5, vmax=5)

plt.title("Cluster Centers: Trade Pattern Profiles")
fig.tight_layout()
plt.savefig("cluster_centers.png", bbox_inches='tight')


# -------------------------
# Step 8: Dendrogram
# -------------------------
linked = linkage(X_scaled, method='ward')
plt.figure(figsize=(8, 6))
dendrogram(linked, labels=df.index.tolist(), orientation='right')
plt.title("Hierarchical Clustering Dendrogram")
fig.tight_layout()
plt.savefig("Hierarchical_Clustering_Dendrogram.png")

output = {"label": list(labels), "country": list(df.index)}

output = pd.DataFrame(output)

output.to_csv("output.csv")