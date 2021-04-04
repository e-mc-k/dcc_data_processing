# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 14:34:44 2021

@author: E. Kias
"""
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.offline import plot

dataqpath = r"/Users/Bubba/Documents/Python_Projects/DCC_Processing/data/210316_PPGSlurry1230pMud_Test16_2p5OBBP.2inP"
balancelinkpath = r"/Users/Bubba/Documents/Python_Projects/DCC_Processing/data/210316_PPGSlurry1230pMud_Test16_2p5OBBP_MASS.TXT"
df_dataq = pd.read_csv(dataqpath, skiprows=(4))
df_blink = pd.read_csv(balancelinkpath)
df_blink.columns = ['mass (g)', 'Time']
pumping_rate = 20 #mL/min

def calculate_Pressure_In():
    if (df_dataq.columns[1]) == 'psi':
        foo = 1
        df_dataq['Volt_PIn'] = (df_dataq['Volt']+25)/25
        df_dataq['Pressure_In'] = df_dataq['Volt_PIn']*25.44-25.503
    elif (df_dataq.columns[1]) == 'Volt':
        foo = 2
        df_dataq['Pressure_In'] = df_dataq[df_dataq.columns[1]]*25.44-25.503

calculate_Pressure_In()

df_dataq['Pressure_OB'] = df_dataq[df_dataq.columns[4]]
df_dataq['Pressure_BP'] = 2.6
df_dataq['Pressure_dP'] = df_dataq['Pressure_In'] - df_dataq['Pressure_BP']
df_dataq['Displaced_Vol'] = 0.0

np_dataq = df_dataq.to_numpy()

def calculate_displaced_Vol():
    for i in range(1,np.size(np_dataq,0)):
        if np_dataq[i,2] < 4.0:
            np_dataq[i,15] = np_dataq[i-1,15]
        elif np_dataq[i,2] > 5.0085:
            time_inc = np_dataq[i,0]-np_dataq[i-1,0]
            np_dataq[i,15] = np_dataq[i-1,15]+time_inc*pumping_rate/60
        else:
            np_dataq[i,15] = np_dataq[i-1,15]-time_inc*pumping_rate/60
    
calculate_displaced_Vol()
df_dataq['Displaced_Vol']=pd.Series(np_dataq[:,15])



# ---Figures
fig = px.line(df_dataq, x="sec", y="Displaced_Vol")
plot(fig)

# def calculate_displaced_Vol():
#     length = df_dataq.shape[0]
    
#     for i in (1,length):
#         if df_dataq[2][i+1] < 4.0:
#             df_dataq.['Displaced_Vol'][i] = 
 
# Functions Defined Below ----------------------------------------------------
# must define first, this is just scrap text
            
            
# =IF(D7<4,V6,IF(D7>5.0085,V6+20/60*(A7-A6),V6-20/60*(A7-A6)))        
# for i in df.index:
#     print("Total income in "+ df["Date"][i]+ " is:"+str(df["Income_1"][i]+df["Income_2"][i]))