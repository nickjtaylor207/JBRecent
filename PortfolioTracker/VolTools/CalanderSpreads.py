
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from pandas.plotting import table
from PIL import Image

from xbbg import blp
from datetime import datetime, timedelta

from scipy.stats import percentileofscore


end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")



ccy = 'EURUSD'




tenors = ['1W', '2W', '1M', '2M', '3M', '6M', '1Y', '2Y']

# Initialize an empty dictionary to store data
df_vols = {}

# Fetch data for each tenor
for tenor in tenors:
    ticker_IV = f"EURUSDV{tenor} BGN Curncy"


    # Retrieve historical data
    data_IV = blp.bdh(
        tickers=ticker_IV,
        flds="PX_LAST",  # Adjust field if needed
        start_date=start_date,
        end_date=end_date
    )
    # Rename the column to the tenor for clarity
    data_IV.columns = [tenor]
    # Store the data in the dictionary
    df_vols[tenor] = data_IV


# Combine all tenor data into a single DataFrame
df_vols_all = pd.concat(df_vols.values(), axis=1)






spreads = {
    "1M-1Y": ("1M", "1Y"),
    "1W-2W": ("1W", "2W"),
    "1W-1M": ("1W", "1M"),
    "1M-3M": ("1M", "3M"),
    "1M-6M": ("1M", "6M"),
    "3M-1Y": ("3M", "1Y"),
    "6M-1Y": ("6M", "1Y"),
    "1Y-2Y": ("1Y", "2Y"),
}




spread_data = []

# Calculate the current spread for each combination
for spread_name, (tenor1, tenor2) in spreads.items():

    if tenor1 in df_vols_all.columns and tenor2 in df_vols_all.columns:

        current_value = df_vols_all.iloc[-1][tenor1] - df_vols_all.iloc[-1][tenor2]
        spread_data.append({"Spread": spread_name, "Current Spread": current_value})



# Convert the list of dictionaries into a DataFrame
current_spreads = pd.DataFrame(spread_data)

# Set "Spread" as the index for better readability
current_spreads.set_index("Spread", inplace=True)


print(current_spreads)

print(df_vols_all)