import pdblp
from xbbg import blp


from datetime import datetime, timedelta
import pandas as pd





# Establish a connection
con = pdblp.BCon(debug=False, port=8194, timeout=5000)
con.start()





# ccy = Currency Pair |  tenor = days to expire of interest  |  day = Days of window  
def Spot_dayData(ccy, day):

    ticker = f"{ccy} Curncy" 

    end_time = datetime.now()
    start_time = end_time - timedelta(days=day*2)

    # Fetch the data
    data = blp.bdh(
        tickers=ticker,
        start_date=start_time,
        end_date=datetime.today().strftime('%Y-%m-%d')
    )

    data = data.rename(columns={"Last_Price": "Spot_Price"})

    df_return = data.tail(day)

    return df_return














# ccy = Currency Pair |  tenor = days to expire of interest  |  day = Days of window  
def IV_dayData(ccy, tenors, day):
    start_date = (datetime.today() - timedelta(days=(day * 2))).strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')
    
    data_frames = []

    # Loop through each tenor and fetch data
    for tenor in tenors:
        ticker = f"{ccy}V{tenor} BGN Curncy"
        field = "PX_LAST"

        # Fetch the data for each tenor
        data = blp.bdh(
            tickers=ticker,
            flds=field,
            start_date=start_date,
            end_date=end_date
        )

        # Rename the column to indicate the tenor
        data = data.rename(columns={"PX_LAST": f"{tenor}_ImpliedVol"})
        
        # Keep only the last 'day' rows for each tenor
        data = data.tail(day)

        data_frames.append(data)

    # Concatenate all the tenor data along columns
    df_return = pd.concat(data_frames, axis=1)

    return df_return



ccy = 'EURUSD'
tenors = ['1W', '2W', '3W', '1M', '2M']
day = 20

df_spot = Spot_dayData(ccy, day)


df_IVs = IV_dayData(ccy, tenors, day)
print(df_IVs)





combined_df = pd.concat([df_spot, df_IVs], axis=1)

print(combined_df.columns)