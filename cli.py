

from process.data import read_input_output_table

data = read_input_output_table()
input_output_table = data["table"].set_index("V1")

all_countries = list(data["countrycode"]["Code"])
df = input_output_table[[col for col in input_output_table.columns if any(col.startswith(prefix) for prefix in all_countries)]]
mask = df.index.str.startswith(tuple(all_countries))
df = df[mask]
df.index.name = None

df["NZL_A01_02"]

top_3 = df['NZL_A01_02'].nlargest(3)

# Filter rows where index does not start with 'NZL'
mask = ~df.index.str.startswith('NZL')
filtered_df = df[mask]

# Get the top 3 rows with the largest values in 'NZL_A01_02'
top_3 = filtered_df['NZL_A01_02'].nlargest(3)