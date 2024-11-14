import pandas as pd


#------------------------------------ SEARCH POSITION Of Client----------------------------------------------------


# Input name, currency, Strike
def indentifyClientPos(df, name, CCY, Strike):

  # Identidy trade  
  df_name = df.loc[df['Name'] == name]
  df_name_curr = df_name.loc[df_name['CCY'] == CCY]
  df_spec = df_name_curr.loc[df_name_curr['Strike'] == Strike]

  # Identifying LP 
  exchID = df_spec['ExchangeID'].unique()[0]
  df_exchID = df.loc[df['ExchangeID'] == exchID]
  LPName = df_exchID.loc[df_exchID['Name'].isna(), 'Company'].unique()[0]

  # Gathering all Important Info
  df_return = df_spec[['OrderDate', 'Company',  'Name', 'Buy/Sell', 'CCY', 'ExpiryDate', 'Strike', 'OptionStrat', 'Notional (base)']]
  df_return['LPName'] = LPName
  df_AllInfo = df_return.melt(var_name='Variable', value_name='Value')


  return df_AllInfo





























