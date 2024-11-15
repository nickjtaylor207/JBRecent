import pdblp

import xbbg 

from xbbg import blp
import pandas as pd

import numpy as np

from datetime import datetime, timedelta

import matplotlib.pyplot as plt





# Define date range for data retrieval
start_date = "2023-11-15"  # Adjust as needed
end_date = "2024-11-14"    # Adjust as needed













































































# -------------------------------- General Commodity Prices ------------------------------------------

def Daily_GetGenCommodity(startdate, enddate):
    # List of General commodity tickers from Bloomberg
    commodities = [
        "CO1 Comdty",    # Brent Crude Oil
        "CL1 Comdty",    # WTI Crude Oil
        "NG1 Comdty",    # Henry Hub Natural Gas
        "XAU BGN Curncy",   # Gold
        "XAG Curncy",   # Silver
        "HG1 Comdty",    # Copper
        "W 1 COMB Comdty", # Wheat
        "C 1 COMB Comdty",  # Corn
        "S 1 COMB Comdty",  # Soybeans
        "RR1 COMB Comdty",  # Rice
        "XW1 Comdty"  # Coal
    ]


    # Fetch historical data
    df_commodities = {}

    for ticker in commodities:
 
        # Retrieve historical data for each commodity
        data = blp.bdh(
            tickers=ticker,
            flds=["PX_LAST"],  # Adjust fields as needed
            start_date=start_date,
            end_date=end_date,
            Per="D"  # Daily data
        )
        # Rename columns for clarity
        data.columns = [ticker]
        df_commodities[ticker] = data


    # Combine all data into a single DataFrame
    df_commodities_all = pd.concat(df_commodities, axis=1).dropna()


    # Ensure column names remain consistent
    df_commodities_all.columns = df_commodities_all.columns.droplevel(0) if isinstance(df_commodities_all.columns, pd.MultiIndex) else df_commodities_all.columns
    df_commodities_all = df_commodities_all.sort_index(ascending=True)

    return df_commodities_all












# -------------------------------- Big Equity Indexs ------------------------------------------

def Daily_GetEQIndex(startdate, enddate):

    Indices = [
        "SPX Index",       # S&P 500 Index
        "INDU Index",      # Dow Jones Industrial Average
        "CCMP Index",      # NASDAQ Composite Index
        "RTY Index",       # Russell 2000 Index
        "SX5E Index",      # Euro Stoxx 50
        "CAC Index",       # CAC 40 (France)
        "DAX Index",       # DAX Index (Germany)
        "FTSEMIB Index",   # FTSE MIB (Italy)
        "UKX Index",       # FTSE 100 (UK)
        "NKY Index",       # Nikkei 225 (Japan)
        "TPX Index",       # TOPIX (Japan)
        "SHCOMP Index",    # Shanghai Composite Index (China)
        "SHSZ300 Index",   # CSI 300 Index (China)
        "HSI Index",       # Hang Seng Index (Hong Kong)
        "SENSEX Index",    # BSE Sensex Index (India)
        "NIFTY Index",     # NIFTY 50 Index (India)
        "AS51 Index",      # ASX 200 Index (Australia)
        "SPTSX Index",     # S&P/TSX Composite Index (Canada)
        "IBOV Index",      # IBOVESPA Index (Brazil)
        "IMOEX Index",     # MOEX Russia Index (Russia)
        "KOSPI Index",     # KOSPI (South Korea)
        "MXWO Index",      # MSCI World Index
        "MXEF Index"       # MSCI Emerging Markets Index
    ]

    # Fetch historical data
    df_indices = {}

    for ticker in Indices:
        
        data_indices = blp.bdh(
            tickers=ticker,
            flds=["PX_LAST"],  # Adjust fields as needed
            start_date=startdate,
            end_date=enddate,
            Per="D"  # Daily data
        )
        # Rename the column to the ticker name
        data_indices.columns = [ticker]
        # Add data to dictionary
        df_indices[ticker] = data_indices

    # Combine all data into a single DataFrame
    df_IndicesAll = pd.concat(df_indices, axis=1)

    # Ensure column names remain consistent
    df_IndicesAll.columns = df_IndicesAll.columns.droplevel(0) if isinstance(df_IndicesAll.columns, pd.MultiIndex) else df_IndicesAll.columns

    df_IndicesAll = df_IndicesAll.sort_index(ascending=True)

    return df_IndicesAll























# -------------------------------- Gov Bond Yields ------------------------------------------

def Daily_getGovBondYield(startdate, enddate):

    Gov_Bonds = [
        "GT10 Govt",  # US 10-Year Treasury Note
        "GT2 Govt",   # US 2-Year Treasury Note
        "GT5 Govt",   # US 5-Year Treasury Note
        "GT30 Govt",  # US 30-Year Treasury Bond
        "GTDEM10Y Govt",  # German 10-Year Bund
        "GTJPY10Y Govt",  # Japanese 10-Year JGB
        "GTGBP10Y Govt",  # UK 10-Year Gilt
        "GTITL10Y Govt",  # Italian 10-Year BTP
        "GTAUD10Y Govt"  # Australian 10-Year Bond
        # "GTCHY10Y Govt",  # Chinese 10-Year CGB 
    ]


    # Fetch historical data
    df_govBonds = {}

    for ticker in Gov_Bonds:
    
        data_govBonds = blp.bdh(
            tickers=ticker,
            flds=["PX_LAST"],  # Adjust fields as needed
            start_date=startdate,
            end_date=enddate,
            Per="D"  # Daily data
        )

        data_govBonds.columns = [ticker]
        df_govBonds[ticker] = data_govBonds


    df_GovBondsAll = pd.concat(df_govBonds, axis=1).dropna()

    # Ensure column names remain consistent
    df_GovBondsAll.columns = df_GovBondsAll.columns.droplevel(0) if isinstance(df_GovBondsAll.columns, pd.MultiIndex) else df_GovBondsAll.columns

    df_GovBondsAll = df_GovBondsAll.sort_index(ascending=True)

    return df_GovBondsAll













































































# con = pdblp.BCon(debug=False, port=8194, timeout=5000)
# con.start()



# # ccy = Currency Pair |  tenor = days to expire of interest  |  day = Days of window  
# def Spot_dayData(ccy, day):

#     ticker = f"{ccy} Curncy" 

#     end_time = datetime.now()
#     start_time = end_time - timedelta(days=day*2)

#     # Fetch the data
#     data = blp.bdh(
#         tickers=ticker,
#         start_date=start_time,
#         end_date=datetime.today().strftime('%Y-%m-%d')
#     )

#     data = data.rename(columns={"Last_Price": "Spot_Price"})

#     df_return = data.tail(day)

#     return df_return




# ccy = 'EURUSD'
# tenors = ['1W', '2W', '3W', '1M', '2M']
# day = 20

# df_spot = Spot_dayData(ccy, day)




























































