from process import INTER_COUNTRY_INPUT_OUTPUT_TABLES, INTER_COUNTRY_INPUT_OUTPUT_METADATA, INTER_COUNTRY_INPUT_OUTPUT_COUNTRYCODE
from pandas import read_csv

def read_input_output_table():

    output = {
        "table": read_csv(INTER_COUNTRY_INPUT_OUTPUT_TABLES),
        "metadata": read_csv(INTER_COUNTRY_INPUT_OUTPUT_METADATA),
        "countrycode": read_csv(INTER_COUNTRY_INPUT_OUTPUT_COUNTRYCODE)
    }

    return output

def load_data():
    data = read_input_output_table()
    input_output_table = data["table"].set_index("V1")
    all_countries = list(data["countrycode"]["Code"])

    df = input_output_table[[col for col in input_output_table.columns if any(col.startswith(prefix) for prefix in all_countries)]]
    mask = df.index.str.startswith(tuple(all_countries))
    df = df[mask]
    df.index.name = None

    metadata = data["metadata"]

    return {"data": df, "metadata": metadata, "all_countries": data["countrycode"]}
