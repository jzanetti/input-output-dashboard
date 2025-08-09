from pandas import concat
from numpy import sum as np_sum
from numpy import log as np_log
from numpy import sort as np_sort
from numpy import cumsum as np_cumsum
from pandas import DataFrame

def calculate_risk_index(inputs):
    """
    Calculate risk index based on input diversity using normalized HHI.
    
    Parameters:
    - inputs: pandas Series, non-zero input values for a country-industry pair
    
    Returns:
    - risk_index: float, normalized HHI (0 to 1, higher means higher risk)
    """
    if inputs.empty:
        return 0.0

    # --- Helper: Gini function ---
    def gini(x):
        x = np_sort(x)
        n = len(x)
        cumx = np_cumsum(x)
        return (n + 1 - 2 * np_sum(cumx) / cumx[-1]) / n

    # --- Step 1: Extract industries ---
    df = inputs.reset_index()
    df.columns = ['source', 'value']
    df['industry'] = df['source'].str.split('_').str[-1]  # last part after underscore
    df['country'] = df['source'].str.split('_').str[0]   # first part before underscore

    # --- Step 2: Calculate metrics per industry ---
    results = []

    for industry, group in df.groupby('industry'):
        total = group['value'].sum()
        shares = group['value'] / total
        
        HHI = np_sum(shares**2)
        inverse_HHI = 1 / HHI
        entropy = -np_sum(shares * np_log(shares))
        entropy_norm = entropy / np_log(len(shares))
        gini_coeff = gini(shares.values)
        
        results.append({
            'industry': industry,
            'total_inputs': total,
            'num_sources': len(group),
            'HHI': HHI,
            'inverse_HHI': inverse_HHI,
            'entropy': entropy,
            'entropy_norm': entropy_norm,
            'gini': gini_coeff
        })

    industry_metrics = DataFrame(results)

    return industry_metrics


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


def obtain_inputs(df, selected_industry, selected_deps, selected_country: str = "NZL", run_filter: bool = True):
    target_col = f"{selected_country}_{selected_industry}"
    if target_col not in df.columns:
        raise ValueError(f"Column {target_col} not found in DataFrame")
    inputs = df[target_col]
    inputs = inputs[inputs > 0]

    filtered_df = inputs[~inputs.index.str.startswith(selected_country)]

    filtered_df = filtered_df.nlargest(int(selected_deps))

    if not run_filter:
        for proc_industrial in list(set(filtered_df.index.str.split("_", n=1).str[1])):
            filtered_df = concat(
                [filtered_df, inputs[inputs.index == f"{selected_country}_{proc_industrial}"]], 
                axis=0, 
                ignore_index=False)
            
    return filtered_df

