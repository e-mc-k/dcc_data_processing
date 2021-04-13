# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 14:34:44 2021

@author: E. Kias
"""
import numpy as np
import pandas as pd
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot

# Input for cleaned data and other needed parameters
target_folder = r'P:\Internal Data\Testing\Quidnet_Deformable_Cell\Test_Data\210408_Test31_SkinFormingSoln_Overnight'
pumping_rate = 20 #mL/min
test_id = 'DCC Test 31 - Skin Forming Solution 1'
#
dataqpath = target_folder + r"\Dataq_Data.xlsx"
balancelinkpath = target_folder + r"\Balancelink_Data.xlsx"
df_dataq = pd.read_excel(dataqpath, skiprows=(4))
df_blink = pd.read_excel(balancelinkpath)
df_blink.columns = ['mass (g)', 'Time', 'sec']



def calculate_Pressure_In():
    if (df_dataq.columns[1]) == 'psi':
        foo = 1
        df_dataq['Volt_PIn'] = (df_dataq['psi']+25)/25
        df_dataq['Pressure_In'] = df_dataq['Volt_PIn']*25.44-25.503
    elif (df_dataq.columns[1]) == 'Volt':
        foo = 2
        df_dataq['Pressure_In'] = df_dataq[df_dataq.columns[1]]*25.44-25.503

calculate_Pressure_In()

# Calculate other dataq data values
df_dataq['Pressure_OB'] = df_dataq[df_dataq.columns[4]]*25.12563-13.0653
df_dataq['Pressure_OB_filter'] = df_dataq['Pressure_OB']
df_dataq['Pressure_BP'] = 2.6
df_dataq['Pressure_dP'] = df_dataq['Pressure_In'] - df_dataq['Pressure_BP']
df_dataq['Displaced_Vol'] = 0.0
df_dataq['min'] = df_dataq['sec']/60
# df_dataq['Time2'] = pd.to_datetime(df_dataq['Time'], format= "%H:%M:%S")
# df_blink['Time2'] = pd.to_datetime(df_blink['Time'], format= " %H:%M:%S")

np_dataq = df_dataq.to_numpy()
# np_blink = df_blink.to_numpy()

def calculate_displaced_Vol():
    for i in range(1,np.size(np_dataq,0)):
        if np_dataq[i,2] < 4.0:
            np_dataq[i,15] = np_dataq[i-1,15]
        elif np_dataq[i,2] > 5.0085:
            time_inc = np_dataq[i,0]-np_dataq[i-1,0]
            np_dataq[i,15] = np_dataq[i-1,15]+time_inc*pumping_rate/60
        else:
            time_inc = np_dataq[i,0]-np_dataq[i-1,0]
            np_dataq[i,15] = np_dataq[i-1,15]-time_inc*pumping_rate/60
    
calculate_displaced_Vol()
df_dataq['Displaced_Vol']=pd.Series(np_dataq[:,15])

# Calculate balance link values
df_blink['min'] = df_blink['sec']/60

# Reduce data to plot to 0.25 Hz
rslt_df_dataq = df_dataq[df_dataq['sec'] % 4 == 0]
rslt_df_blink = df_blink[df_blink['sec'] % 4 == 0]

# Create traces
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=rslt_df_dataq["min"], y=rslt_df_dataq["Displaced_Vol"],
                    mode='lines',
                    name='Displaced Volume',
                    line=dict(color='brown')
                    ),
                    secondary_y=True
              )
fig.add_trace(go.Scatter(x=rslt_df_dataq["min"], y=rslt_df_dataq["Pressure_dP"],
                    # mode='lines+markers',
                    mode='lines',
                    name='Differential Pressure',
                    line=dict(color='red')
                    )
              )
fig.add_trace(go.Scatter(x=rslt_df_blink["min"], y=rslt_df_blink["mass (g)"],
                    mode='lines',
                    name='Leak-Off Mass',
                    line=dict(color='darkblue')
                    ),
                    secondary_y=True
              )
fig.add_trace(go.Scatter(x=rslt_df_dataq["min"], y=rslt_df_dataq["Pressure_OB"],
                    mode='lines',
                    name='OB Pressure',
                    line=dict(color='gray')
                    )
              )


# Add figure title
fig.update_layout(
        title_text=test_id
    )

# Set x-axis title
fig.update_xaxes(title_text="<b>Elapsed Time (min)</b>"
                 )

# Set y-axes titles
fig.update_yaxes(
    title_text="<b>Pressure (psi)</b>", 
    secondary_y=False
    )
fig.update_yaxes(
    title_text="<b>Mass (g)</b>", 
    secondary_y=True
    )


plot(fig)
fig.write_html(target_folder + "\\" + test_id + ".html")
