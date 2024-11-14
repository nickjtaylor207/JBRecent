import pandas as pd

from BlotterCode.Functions import indentifyClientPos


# File path directory / Getting data into df
file_path = r'\Users\ntaylor\Desktop\TRADEBLOTTER.xlsx'
df_blotter = pd.read_excel(file_path, sheet_name='Blotter', usecols=range(31))


# Input: 
#       TradeDF, CLIENT NAME, CCY, Strike
df_prevTrade =  indentifyClientPos(df_blotter, 'PETER MAA', 'USDTWD', 33.5)

print(df_prevTrade)