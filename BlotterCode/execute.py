import pandas as pd

from pos_Ident import name_positions, Client_Open_Trades, Client_Closed_Trades, classify_trade





file_path = r'\Users\ntaylor\Desktop\PrimeBlotter\FxBlotter_Date.xlsx'
df = pd.read_excel(file_path, usecols=range(46))







name = 'EXODUSPOINT DG BNP (NWM GU)'


def compilePos(name):

        
    df_client = name_positions(df, name)

    df_client_open_trades = Client_Open_Trades(df_client)

    #  df_client_Closed_trades = Client_Closed_Trades(df_client)


    df_open_trade_TYPE = df_client_open_trades.groupby('PairId').apply(classify_trade).reset_index(drop=True)

    df_open_trade_TYPE = df_open_trade_TYPE[['Trade Date', 'Client', 'B/S', 'Ccy Pair', 'Expiry Date', 'Strike', 'C/P', 'Notional',  'LP', 'PositionName', 'Upper Barrier','Lower Barrier', 'Contract', 'Product Code', 'PairId']]
    return print(df_open_trade_TYPE)




compilePos(name)












# 'EXODUSPOINT DG BNP (NWM GU)', 'SCHONFELD DMFI TG CITI (NWM GU)', 'BALYASNY PM (HSBC GU)', 'BREVAN ASMF PBESOLD BAL (HSBC GU)',  'ONE RIVER CM (DB GU)', 'PHARO MP (JPM GU)', 'WALLEYE ZA (DB GU)'

# 'BREVAN EMMSMF HM (HSBC GU)', 'BREVAN ASMF HM (JBDRX_FXHSBC)', 'WALLEYE ES (DB GU)', 'EXODUSPOINT JF (HSBC GU)', 'DRW INV JY SOCGEN (NWM GU)', 'NATIXIS VG (NWM GU)'

