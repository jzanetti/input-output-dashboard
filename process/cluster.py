import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import re

# -------------------------
# Step 1: Load OECD ICIO data
# -------------------------
df = pd.read_csv("etc/2020.csv", index_col=0)
df2 = pd.read_csv("etc/country_code.csv", index_col=0)
# Helper: extract country code from <country>_<industry>
def get_country(label):
    return re.split(r'[_]', label)[0]


# -------------------------
# Step 2: Filter by selected countries (both rows and columns)
# -------------------------
keep_countries = [
    'ARG', 'AUS', 'AUT', 'BEL', 'BGD', 'BGR', 'BLR', 
    'BRA', 'BRN', 'CAN', 'CHE', 'CHL', 'CHN', 'CIV', 
    'CMR', 'COL', 'CRI', 'CYP', 'CZE', 'DEU', 'DNK', 
    'EGY', 'ESP', 'EST', 'FIN', 'FRA', 'GBR', 'GRC']
# keep_countries = list(df2.index)
def is_selected_country(label):
    return get_country(label) in keep_countries

df = df[df.index.map(is_selected_country)]
df = df.loc[:, df.columns.map(is_selected_country)]


# -------------------------
# Step 2: Create country vectors of trade *shares*
# -------------------------
def trade_pattern_matrix(io_df):
    row_countries = [get_country(r) for r in io_df.index]
    col_countries = [get_country(c) for c in io_df.columns]
    
    countries = sorted(set(row_countries))
    industries = sorted(set([c.split('_', 1)[1] for c in io_df.columns]))

    # We will create: country x (partner_country, industry) matrix
    partner_industry_cols = []
    for partner in countries:
        for industry in industries:
            partner_industry_cols.append(f"{partner}_{industry}")

    country_vectors = pd.DataFrame(0.0, index=countries, columns=partner_industry_cols)

    # Fill matrix: For each exporting country, sum flows to each (partner, industry)
    for i, exporter in enumerate(row_countries):
        print(f"processing {i}/{len(row_countries)}")
        for j, col_name in enumerate(io_df.columns):
            partner_country = col_countries[j]
            partner_industry = col_name.split('_', 1)[1]
            key = f"{partner_country}_{partner_industry}"
            country_vectors.loc[exporter, key] += io_df.iat[i, j]

    # Convert absolute flows into shares (row sum = 1 for each country)
    country_vectors = country_vectors.div(country_vectors.sum(axis=1), axis=0).fillna(0)

    return country_vectors

X_share = trade_pattern_matrix(df)

# -------------------------
# Step 3: Standardize features
# -------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_share)

# -------------------------
# Step 4: Dimensionality reduction
# -------------------------
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# -------------------------
# Step 5: Clustering
# -------------------------
"""
best_k, best_score = None, -1
for k in range(2, len(X_share)):
    print(k)
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_scaled)  # Use scaled *shares*, not PCA
    score = silhouette_score(X_scaled, labels)
    if score > best_score:
        best_k, best_score = k, score
"""


best_k, best_score = None, -1
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X_scaled)

# -------------------------
# Step 6: Plot PCA for visualization
# -------------------------
plt.figure(figsize=(8,6))
for cluster_id in range(best_k):
    plt.scatter(X_pca[labels == cluster_id, 0],
                X_pca[labels == cluster_id, 1],
                label=f"Cluster {cluster_id+1}")
for i, country in enumerate(X_share.index):
    plt.text(X_pca[i, 0], X_pca[i, 1], country, fontsize=8)
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.title("Country Clusters based on Trade Composition")
plt.legend()
plt.tight_layout()
plt.savefig("test.png")

# -------------------------
# Step 7: Output cluster assignments
# -------------------------
clusters_df = pd.DataFrame({
    "Country": X_share.index,
    "Cluster": labels
}).sort_values("Cluster")

print(clusters_df)
