import pdblp
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt


import matplotlib.pyplot as plt
from pandas.plotting import table
from PIL import Image



con = pdblp.BCon(debug=False, port=8194, timeout=5000)
con.start()


data_combined = []


# Define the list of currency pairs
currency_pairs = [
    'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDNOK', 'USDSEK',
    'USDMXN', 'USDBRL', 'USDCNH'
]





# Loop over each currency pair to get both implied and realized volatilities
for ccy in currency_pairs:
    # Get spot price data
    spot_data = con.ref(f"{ccy} Curncy", ["PX_LAST"])
    spot_price = spot_data["value"].iloc[0] if not spot_data.empty else None

    # Define tickers for implied volatilities (1W, 2W, 1M)
    iv_tickers = [
        f"{ccy}V1W Curncy",  # 1W implied vol
        f"{ccy}V2W Curncy",  # 2W implied vol
        f"{ccy}V1M Curncy",  # 1M implied vol
    ]
    # Get implied volatility data
    iv_data = con.ref(iv_tickers, ["PX_LAST"])
    iv_1w = iv_data["value"].iloc[0] if not iv_data.empty else None
    iv_2w = iv_data["value"].iloc[1] if not iv_data.empty else None
    iv_1m = iv_data["value"].iloc[2] if not iv_data.empty else None

    # Define tickers for realized volatilities (1W, 2W, 1M)
    rv_tickers = [
        f"{ccy}H1W Curncy",  # 1W realized vol
        f"{ccy}H2W Curncy",  # 2W realized vol
        f"{ccy}H1M Curncy",  # 1M realized vol
    ]
    # Get realized volatility data
    rv_data = con.ref(rv_tickers, ["PX_LAST"])
    rv_1w = rv_data["value"].iloc[0] if not rv_data.empty else None
    rv_2w = rv_data["value"].iloc[1] if not rv_data.empty else None
    rv_1m = rv_data["value"].iloc[2] if not rv_data.empty else None

    # Append combined data for this currency pair to the list
    data_combined.append([
        ccy, spot_price, iv_1w, iv_2w, iv_1m, rv_1w, rv_2w, rv_1m
    ])




# Create a DataFrame from the combined data
df_combined = pd.DataFrame(
    data_combined,
    columns=["Currency Pair", "Spot Rate", "1W_IV", "2W_IV", "1M_IV", "1W_RV", "2W_RV", "1M_RV"]
)



df_diff = pd.DataFrame({
    "Currency Pair": df_combined["Currency Pair"],
    "1W": df_combined["1W_RV"] - df_combined["1W_IV"],
    "2W": df_combined["2W_RV"] - df_combined["2W_IV"],
    "1M": df_combined["1M_RV"] - df_combined["1M_IV"] 
})





print(df_combined)


# # Set the Currency Pair as index for the heatmap
# df_diff.set_index('Currency Pair', inplace=True)

# # Create the plot and adjust label positions explicitly
# plt.figure(figsize=(10, 6))  # Set the figure size

# # Create the heatmap
# ax = sns.heatmap(df_diff, annot=True, cmap='RdYlGn', center=0, linewidths=0.5, fmt=".2f",
#                  cbar_kws={'label': 'Volatility Difference'}, square=True)

# # Customize the title, xlabel, and ylabel
# plt.title('Gamma Monitor - 11/12/24', fontsize=16)
# plt.xlabel('Realized - Implied Vols', fontsize=12)
# plt.ylabel('Currency', fontsize=12)

# # Ensure column labels appear at the top (this should be the default behavior)
# ax.xaxis.set_ticks_position('top')
# #plt.xticks(rotation=90)

# # Display the plot
# plt.show()