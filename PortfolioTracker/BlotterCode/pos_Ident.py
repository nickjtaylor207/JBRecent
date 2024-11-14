import pandas as pd
import numpy as np







# ---------------------------------------------------------------------------------------------------------
# Gets all trades done with named individual  
# Input: Full Trade Blotter, Name of Client
# Output: df of all trades done (Excluded FXFWDs)
def name_positions(df, name):


  df_name = df.loc[df['Client'] == name]
  df_name = df_name[~df_name['Contract'].str.contains("FXNDF", na=False)]
  df_name = df_name[~df_name['Contract'].str.contains("FXFWD", na=False)] 

  #If done live, -- No corrosponding FWD

  # Selecting Relavent Info
  df_present = df_name[['PairId', 'Contract', 'Client', 'Product Code', 'Ccy Pair', 'Strike', 'C/P', 'B/S', 'Notional', 'Trade Date', 'Expiry Date', 'Opt.Prem.Amt', 'Prem Ccy', 'Option Type',
        'Barrier Type', 'Lower Barrier', 'Upper Barrier', 'Knock In/Out',
        'Touch Up/Dn', 'Multileg', 'Trade Status']] 

  # Identifying LPs
  pair_ids = df_name['PairId'].unique()  

  df_LP = df[df['PairId'].isin(pair_ids)]
  df_LP = df_LP[~df_LP['Contract'].str.contains("FXNDF", na=False)] #Filters out LP FWD Exchanges 
  df_LP = df_LP[df_LP['Client'].str.contains("LP", na=False, case=False)] # df with just LP 



  df_LP_important = df_LP[['PairId', 'Client']]
  df_LP_important_NoDup = df_LP_important.drop_duplicates()
  df_LP_important_NoDup


  # MErging and renaming LP data into main df
  df_present = pd.merge(df_present, df_LP_important_NoDup, on='PairId', how='left', )
  df_present.rename(columns={'Client_x': 'Client'}, inplace=True)
  df_present.rename(columns={'Client_y': 'LP'}, inplace=True) 

  return df_present




# ---------------------------------------------------------------------------------------------------------
# Presents clients OPEN TRADES
# Input: Trades made by clients (From name_positions)
# Output: List of trades active 
def Client_Open_Trades(df): 

  df_openTrades = df[df['Trade Status'].str.contains("Active", na=False)]

  return df_openTrades




# Presents clients CLOSED TRADES
# Input: Trades made by clients (From name_positions)
# Output: List of trades closed by us 
def Client_Closed_Trades(df): 

  columns_to_check = [
    'Contract', 'Client', 'Ccy Pair', 'Strike', 'C/P', 
    'Expiry Date', 'Option Type', 'Barrier Type', 'Lower Barrier', 
    'Upper Barrier', 'Knock In/Out', 'Touch Up/Dn']

  df_closedTrades = df[df.duplicated(subset=columns_to_check, keep=False)]

  return df_closedTrades


# ---------------------------------------------------------------------------------------------------------






# ---------------------------------------------------------------------------------------------------------
# Classifies the trade type of the option (Grouping Function)
def classify_trade(group):
    # Initialize PositionName as NaN
    group['PositionName'] = np.nan

    # Case 1: Single row in the group
    if len(group) == 1:
        row = group.iloc[0]
        
        # FX Options
        if row['Contract'] == 'FXOPT':

            if row['C/P'] == 'C' and row['B/S'] == 'B':
                group['PositionName'] = 'LONG CALL'

            elif row['C/P'] == 'C' and row['B/S'] == 'S':
                group['PositionName'] = 'SHORT CALL'

            elif row['C/P'] == 'P' and row['B/S'] == 'B':
                group['PositionName'] = 'LONG PUT'

            elif row['C/P'] == 'P' and row['B/S'] == 'S':
                group['PositionName'] = 'SHORT PUT'



        # Exotic Options
        if row['Contract'] == 'DOPT':

            # Digital Knock Outs
            if row['Option Type'] == 'DigiKO':
              
                # Up and Out
                if row['Barrier Type'] == 'UO':
                    group['PositionName'] = 'DigiKO Call'
                    group['Upper Barrier'] = row['Upper Barrier']
                
                # Down and Out
                if row['Barrier Type'] == 'DO':
                    group['PositionName'] = 'DigiKO Put'
                    group['Lower Barrier'] = row['Lower Barrier']



            # Window Digital Knockouts
            if row['Contract'] == 'DDKO':
            
                group['PositionName'] = 'WindowDigiKO'
                group['Upper Barrier'] = row['Upper Barrier']
                group['Lower Barrier'] = row['Lower Barrier']



            # Euro Digi Put W/ Double Knock Out
            if row['Product Code'] == 'BQKP':
                group['PositionName'] = 'EURO DIGI PUT DKO'
            # Euro Digi Call W/ Double Knock Out
            if row['Product Code'] == 'BQKC':
                group['PositionName'] = 'EURO DIGI CALL DKO'



            # One Touch Down Instant Payout
            if row['Product Code'] == 'BAP':
                group['PositionName'] = '1T DOWN INST-PAY'
            

            # One Touch UP Instant Payout
            if row['Product Code'] == 'BAC':
                group['PositionName'] = '1T UP INST-PAY'



        # Exotic Options
        #if row['Contract'] == 'EOPT':







    

    
    # Case 2: Multiple rows in the group
    elif len(group) == 2:
        # Sort rows by 'Strike' for consistent comparison
        group = group.sort_values(by='Strike').reset_index(drop=True)
        
        # Extract rows data for clarity
        row1 = group.iloc[0]
        row2 = group.iloc[1] 


        # ---------------- Call Spreads-------------------------------
        if row1['C/P'] == 'C' and row2['C/P'] == 'C':

            # LONG Call SPREAD - Buy Low Strike, Sell High Strike
            if row1['Strike'] < row2['Strike'] and row1['B/S'] == 'B' and row2['B/S'] == 'S':
                group['PositionName'] = 'LONG CALL SPREAD'

            # SHORT PUT SPREAD - Buy Low Strike, Sell High Strike
            if row1['Strike'] < row2['Strike'] and row1['B/S'] == 'S' and row2['B/S'] == 'B':
                group['PositionName'] = 'SHORT CALL SPREAD'

        


        # ------------- Put Spreads ---------------------------------------
        if row1['C/P'] == 'P' and row2['C/P'] == 'P':

            # LONG PUT SPREAD - Sell Low Strike, Buy High Strike
            if row1['Strike'] < row2['Strike'] and row1['B/S'] == 'S' and row2['B/S'] == 'B':
                group['PositionName'] = 'LONG PUT SPREAD'

            # SHORT PUT SPREAD - Buy Low Strike, Sell High Strike
            if row1['Strike'] < row2['Strike'] and row1['B/S'] == 'B' and row2['B/S'] == 'S':
                group['PositionName'] = 'SHORT PUT SPREAD'
        




        # ------------- STRADLES || STRANGLES --------------------------------------------
        if  row1['C/P'] == 'P' and row2['C/P'] == 'C':

            
            # LONG STRANGLE - Buy low strike Put, Buy high strike Call 
            if row1['B/S'] == 'B' and row2['B/S'] == 'B' and row1['Strike'] < row2['Strike']:
                group['PositionName'] = 'LONG STRANGLE'

            # SHORT STRANGLE - Buy low strike Put, Buy high strike Call 
            if row1['B/S'] == 'S' and row2['B/S'] == 'S' and row1['Strike'] < row2['Strike']:
                group['PositionName'] = 'SHORT STRANGLE'
        


            # LONG STRADDLE - Buy same strike Put, Buy same strike Call 
            if row1['B/S'] == 'B' and row2['B/S'] == 'B' and row1['Strike'] == row2['Strike']:
                group['PositionName'] = 'LONG STRADDLE'

            # SHORT STRADDLE - Sell same strike Put, Sell same strike Call 
            if row1['B/S'] == 'S' and row2['B/S'] == 'S' and row1['Strike'] == row2['Strike']:
                group['PositionName'] = 'SHORT STRADDLE'


        # ------- STRADDLE (if Call entered first)
        if  row1['C/P'] == 'C' and row2['C/P'] == 'P':

            # LONG STRADDLE - Buy same strike Put, Buy same strike Call 
            if row1['B/S'] == 'B' and row2['B/S'] == 'B' and row1['Strike'] == row2['Strike']:
                group['PositionName'] = 'LONG STRADDLE'

            # SHORT STRADDLE - Sell same strike Put, Sell same strike Call 
            if row1['B/S'] == 'S' and row2['B/S'] == 'S' and row1['Strike'] == row2['Strike']:
                group['PositionName'] = 'SHORT STRADDLE'





        
    
        # ------------- RISK REVERSAL ----------------------------------
        if row1['C/P'] == 'P' and row2['C/P'] == 'C':
            


            # LONG RISK REVERASL - Sell low strike Put, Buy high strike Call 
            if row1['Strike'] < row2['Strike'] and row1['B/S'] == 'S' and row2['B/S'] == 'B':
             
                if row1['Expiry Date'] == row2['Expiry Date']: 
                    group['PositionName'] = 'LONG RISK REVERSAL'
                if row1['Expiry Date'] != row2['Expiry Date']:
                    group['PositionName'] = 'LONG CALENDAR RISK REVERSAL' 

            # SHORT RISK REVERASL - Buy low strike Put, Sell high strike Call 
            if row1['Strike'] < row2['Strike'] and row1['B/S'] == 'B' and row2['B/S'] == 'S':
             
                if row1['Expiry Date'] == row2['Expiry Date']: 
                    group['PositionName'] = 'SHORT RISK REVERSAL'
                if row1['Expiry Date'] != row2['Expiry Date']:
                    group['PositionName'] = 'SHORT CALENDAR RISK REVERSAL' 





    return group

# ---------------------------------------------------------------------------------------------------------


