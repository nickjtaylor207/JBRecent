import pdblp

from xbbg import blp
import pandas as pd

import numpy as np

from datetime import datetime, timedelta



# Establish a connection
con = pdblp.BCon(debug=False, port=8194, timeout=5000)
con.start()




# ------------------Intraday------------------------------------------


currency_pairs = [
    'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDNOK', 'USDSEK',
    'USDMXN', 'USDBRL', 'USDCNH'
]




# Getting spot data of each currency of interest 
def fetch_ccySpot_intraday_all(currency_pairs, hist_time, increment):
    # Get current time and time based on `hist_time`
    end_time = datetime.now()
    start_time = end_time - timedelta(days=hist_time)
    
    # Initialize a dictionary to store close prices
    close_prices = {}
    
    # Loop through each currency pair
    for ccy in currency_pairs:
        # Fetch intraday data
        df = con.bdib(
            ticker=f"{ccy} Curncy",       # Bloomberg ticker format
            start_datetime=start_time,    # Start time
            end_datetime=end_time,        # End time
            event_type="TRADE",           # Event type (TRADE data for FX)
            interval=increment            # Interval (in minutes)
        )
        
        # Store only the 'close' column in the dictionary
        close_prices[ccy] = df['close']
    
    # Combine all close prices into a single DataFrame
    combined_df = pd.DataFrame(close_prices)
    
    # Return the resulting DataFrame
    return combined_df



# realized vol for given window (in minutes)
def realized_vol(returns, window):
    return returns.rolling(window=window).std() * np.sqrt(252) # Anualized rolling standard deviation



# Acual calculations of volitilities for specific periods 
def calculate_volatilities(df, period_dict):
    
    returns = df.pct_change().dropna() # Calculate daily returns
    
    # Calculate volatilities for each specified period
    volatilities = {}
    for period_name, window in period_dict.items():
        vol_df = realized_vol(returns, window)
        volatilities[period_name] = vol_df
    
    # Concatenate volatilities across the specified periods
    combined_vol_df = pd.concat(volatilities, keys=volatilities.keys())
    
    return combined_vol_df



hist_time=31 # Days previous data
increment=5 # individual time increments


# Get the spot data 
df_all = fetch_ccySpot_intraday_all(currency_pairs, hist_time, increment)



periods = {'1w': int((5 * 1440) / increment)}      # '1w': int((5 * 1440) / increment), '2w': int((10 * 1440) / increment), '1m': int((21 * 1440) / increment)








# Calculate the volatilities for each currency pair and period
vol_df = calculate_volatilities(df_all, periods)



print(df_all)












#----------------NON-Intraday----------------------------------------------------------------------


# # Define the list of currency pairs
# currency_pairs = [
#     'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDNOK', 'USDSEK',
#     'USDMXN', 'USDBRL', 'USDCNH'
# ]

# # Bloomberg format for tickers
# tickers = [f"{pair} Curncy" for pair in currency_pairs]
# field = 'PX_LAST'

# # Fetch data for all currency pairs in a single call
# data_histSpot = blp.bdh(
#     tickers=tickers,
#     flds=field,
#     start_date=(pd.Timestamp.now() - pd.DateOffset(years=1)).strftime('%Y-%m-%d'),
#     end_date=pd.Timestamp.now().strftime('%Y-%m-%d')
# )

# # Calculate daily returns
# returns = data_histSpot.pct_change().dropna()

# # Define a function to calculate realized volatility for a given window (e.g., 1m, 3m, 1y)
# def realized_vol(returns, window):
#     # Calculate rolling standard deviation and annualize it
#     return returns.rolling(window=window).std() * np.sqrt(252)

# # calculate volatility based on specified periods
# def calculate_volatility(returns, period_dict):
#     # Calculate volatilities for each period in the dictionary
#     volatilities = {period: realized_vol(returns, window) for period, window in period_dict.items()}
    
#     vol_df = pd.concat(volatilities)
#     return vol_df






# default_periods = {'1m': 21}

# # Example usage: calculate volatility for 1m, 3m, and 1y by default
# vol_df = calculate_volatility(returns, default_periods)

# # Display the resulting DataFrame
# print(vol_df)




















#------------------------------------------------------------------------------------------------

































# # Calculate realized volatility
# def calculate_realized_vol(prices):
#     returns = np.log(prices / prices.shift(1)).dropna()
#     realized_vol = returns.std() * np.sqrt(252)  # Annualized volatility
#     return realized_vol


# lookback_periods = {'1M': 21, '3M': 63, '1Y': 252}  # Approximate trading days





# # ---------------------- getting historical Vol --------------------------------

# con = pdblp.BCon(debug=False, port=8194, timeout=5000)
# con.start()


# data_HV = []




# # Loop over each currency pair
# for ccy in currency_pairs:
#     # Fetch the spot rate
#     spot_data = con.ref(f"{ccy} Curncy", ["PX_LAST"])
#     spot_price = spot_data["value"].iloc[0] if not spot_data.empty else None
    
#     # Fetch historical daily prices for the currency pair
#     historical_data = con.bdh(f"{ccy} Curncy", "PX_LAST", start_date="2023-01-01", end_date="2024-01-01")
    
#     # Calculate realized volatilities
#     rv_1m = calculate_realized_vol(historical_data['PX_LAST'][-lookback_periods['1M']:])
#     rv_3m = calculate_realized_vol(historical_data['PX_LAST'][-lookback_periods['3M']:])
#     rv_1y = calculate_realized_vol(historical_data['PX_LAST'][-lookback_periods['1Y']:])
    
#     # Append data for this currency pair
#     data_HV.append([ccy, spot_price, rv_1m, rv_3m, rv_1y])

# # Create a DataFrame from the collected data
# df = pd.DataFrame(data_HV, columns=["Currency Pair", "Spot Rate", "1M Realized Vol", "3M Realized Vol", "1Y Realized Vol"])

# # Display the DataFrame
# print(df)