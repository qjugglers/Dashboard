import streamlit as st
from new_functions2 import *
import os
import time
from datetime import datetime


st.set_page_config(layout="wide")
try:
    import glob
    import os
    final_out_new=pd.DataFrame()
    final_out_new.to_csv("last_dataframe.csv",index=False)
    csv_files = glob.glob("C://Users//Administrator//Desktop//Algo_files//temp//"+"*.csv")
    for file in csv_files:
        os.remove(file)
except Exception as e:
    pass

def highlight_rows(row):
    if row['Status'] == "FINISHED":
        return ['background-color: khaki'] * len(row)
    if row["Status"]=="rejection":
        return ['background-color: gainsboro'] * len(row)
    else:
        return [''] * len(row)
    

def format_value(value):
    if isinstance(value, str) and value.strip() == '':
        return value  # Return the space as is
    else:
        return '{:.2f}'.format(value)


col1, col2, col3,col4,col5,col6,col7,col8,col9= st.columns(9)
with col1:
    username = st.selectbox('',['79434689',"XFD06",'FDE645',"XFD03","XFD04","DLL564"])


dataframe_df=st.empty()
symbol="BANKNIFTY"
while True:
# for i in range(3):
    try:
        try:
            output_df("TEST",f"{username}")
            os.system('cls' if os.name == 'nt' else 'clear')
            # #print("&&&&&&&&&&&&&&&&&&&&")
        except Exception as e:
            #print(e)
            pass
        try:        
            df=pd.read_csv("last_dataframe.csv")    
            
            try:
                df=df[["Strategy_name","CE_Strike","PE_Strike","CE_Price","PE_Price","combined_sl","Quantity","triggered",
                    "CE_live_price","PE_live_price","trigger_time",f"{username}","UT_Strike","UT_Price",                
                "UT_PRICE_Live","straddle_PL","UT_PL"]]
                df["straddle_PL"]=df["straddle_PL"]*df["Quantity"]
                df["UT_PL"]=df["UT_PL"]*df["Quantity"]
                try:
                    df["Combine_live"]=df["CE_live_price"]+df["PE_live_price"]
                except Exception as e:
                    pass
                try:
                    df['trigger_time'] = pd.to_datetime(df['trigger_time'], format='%H%M%S', errors='coerce').dt.strftime('%H:%M:%S')
                    # df['trigger_time'] = df['trigger_time'].replace('_', pd.NaT)
                    # df['trigger_time'] = pd.to_datetime(df['trigger_time'], format='%H%M%S.%f').dt.strftime('%H:%M:%S')
                except Exception as e:
                    #print(e)
                    pass
                try:
                    df["Total_PL"] = np.where(df['UT_PL'].notna(), df['UT_PL']+df['straddle_PL'], df['straddle_PL'])
                except Exception as e:
                    pass
                df=df[["Strategy_name","PE_Strike","CE_Price","PE_Price","combined_sl","Combine_live","Quantity","triggered",
                    "trigger_time",f"{username}","UT_Strike","UT_Price",                
                "UT_PRICE_Live","straddle_PL","UT_PL","Total_PL"]]
                df.rename(columns = {'CE_Price':'CE_Entry','PE_Price':'PE_Entry',f"{username}":"Status","PE_Strike":"Strike"}, inplace = True) 
                #print(df)
                straddle_PL_sum = df['straddle_PL'].sum()
                UT_PL_sum = df['UT_PL'].sum()
                total_pl=df['Total_PL'].sum()
                new_row = {}
                for column in df.columns:
                    new_row[column] = '' if column not in ['straddle_PL', 'UT_PL',"Total_PL"] else\
                          (straddle_PL_sum if column == 'straddle_PL' else UT_PL_sum if column == 'UT_PL' else total_pl)
                new_row_df = pd.DataFrame([new_row])
                df = pd.concat([df, new_row_df], ignore_index=True)
                styled_df = df.style.apply(highlight_rows, axis=1).format({
                                    'straddle_PL': format_value,
                                    'CE_Entry': format_value,
                                    'PE_Entry': format_value,
                                    'UT_PL': format_value, 
                                    'combined_sl': format_value,
                                    'Combine_live': format_value,
                                    'UT_Price': format_value,
                                    'UT_PRICE_Live': format_value,
                                    "Total_PL":format_value
                                })
                # styled_df = df.style.apply(highlight_rows, axis=1).format({'straddle_PL': '{:.2f}','CE_Entry': '{:.2f}','PE_Entry': '{:.2f}',
                #                                                             'UT_PL': '{:.2f}','combined_sl': '{:.2f}','Combine_live': '{:.2f}',
                #                                                             'UT_Strike': '{:.0f}','Total_PL': '{:.2f}','UT_Price': '{:.2f}','UT_PRICE_Live': '{:.2f}'})
                
                dataframe_df.table(styled_df)
            except Exception as e:
                print("******************")
                df=pd.read_csv("last_dataframe.csv")  
                print(e)
                df["straddle_PL"]=df["straddle_PL"]*df["Quantity"]
                df["UT_PL"]=df["UT_PL"]*df["Quantity"]
                try:
                    df=df.rename(columns = {'CE_Price':'CE_Entry','PE_Price':'PE_Entry',f"{username}":"Status"}) 
                except Exception as e:
                    df=df.rename(columns = {'CE_Price':'CE_Entry','PE_Price':'PE_Entry',int(username):"Status"})
                try:
                    df["Combine_live"]=df["CE_live_price"]+df["PE_live_price"]
                except Exception as e:
                    pass
                tf2=df[["Strategy_name","CE_Entry","PE_Entry","combined_sl","Combine_live","PE_Strike","Quantity","triggered",
                    "Status",
                "CE_Sqoff_Price","PE_Sqoff_Price","UT_Price","UT_SL_Price","straddle_PL","UT_PL"]]
                # tf2.rename(columns = {"PE_Strike":"Strike"}, inplace = True) 

                if not tf2.empty:
                    
                    straddle_PL_sum = tf2['straddle_PL'].sum()
                    UT_PL_sum = tf2['UT_PL'].sum()

                    new_row = {}
                    for column in tf2.columns:
                        new_row[column] = '' if column not in ['straddle_PL', 'UT_PL'] else (straddle_PL_sum if column == 'straddle_PL' else UT_PL_sum)
                    new_row_df = pd.DataFrame([new_row])
                    tf2 = pd.concat([tf2, new_row_df], ignore_index=True)
                    styled_df = tf2.style.apply(highlight_rows, axis=1).format({
                                        'straddle_PL': format_value,
                                        'CE_Entry': format_value,
                                        'PE_Entry': format_value,
                                        'UT_PL': format_value, 
                                        'combined_sl': format_value,
                                        'Combine_live': format_value,
                                        'UT_Price': format_value,
                                        'UT_PRICE_Live': format_value,
                                        "Total_PL":format_value
                                    })
                    dataframe_df.table(styled_df)
        except Exception as e:
            print(e)
            print("###########################")
            df=pd.read_csv("last_dataframe.csv")
            if not df.empty:            
                styled_df = df.style.apply(highlight_rows, axis=1)
                dataframe_df.table(df)
        
    except Exception as e:
        df=pd.DataFrame()
        dataframe_df.table(df)
        pass
    
        

