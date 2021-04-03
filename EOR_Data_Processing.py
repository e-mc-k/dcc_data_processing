# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 08:47:34 2020

@author: evan.kias
"""

#Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

###################USER INPUT##################################################
## EOR5 Info
# EOR5 Sample ID
EOR5_ID = 'Colton 2CA'
# EOR5 Sample dimensions
Length1 = 1.854
Diameter1 = 2.525
# EOR5 Fluid in cP
Visc1 = 2.0805

## EOR6 Info
# EOR6 Sample ID
EOR6_ID = 'Colton 13_2A'
# EOR6 sample dimensions
Length2 = 1.905
Diameter2 = 2.513
# EOR6 Fluid in cP
Visc2 = 2.0805

# Moving Average Increment (min) # not yet implemented!!!!!!!
# inc = 60

# Define filepaths for the DXD (filepath1_) and EOR (filepath2_) data files
filepath1_ = r"P:\Data\Evan\Laboratory\17_SSK_Data_Processing\EOR_Equipment\01_EOR_Equip\dataset2\DXD_Log_9_8_827am_edited.csv"
filepath2_ = r"P:\Data\Evan\Laboratory\17_SSK_Data_Processing\EOR_Equipment\01_EOR_Equip\dataset2\Colton samples 2CA and 13_2A_brine inj 9_8_2020"

####################CODE BELOW#################################################

## Load EOR data file
df_eor = pd.read_csv(filepath2_, skiprows=45, error_bad_lines=False)
# Delete unneccessary columns
cols2 = np.arange(start=1, stop=10)
cols2 = np.append(cols2, [12,13,16,17,19])
cols3 = np.arange(start=21, stop=46)
cols3 = np.append(cols2, cols3)
df_eor.drop(df_eor.columns[cols3], axis=1, inplace=True)
# Rename columns (Pump1 is EOR5 and Pump2 is EOR6)
df_eor.columns = ['DateTime_EOR', 'EOR_Pump1Vol', 'EOR_Pump1Rate', 'EOR_Pump2Vol', 'EOR_Pump2Rate', 'EOR5_Up', 'EOR5_Down']
# Change datetime format
df_eor['DateTime_EOR'] = pd.to_datetime(df_eor['DateTime_EOR'])
# Get length for later use in trimming data block
len_df_eor = len(df_eor)

## Load DXD data file
df_dxd = pd.read_csv(filepath1_, skiprows=7, error_bad_lines=False)
# Delete unneccessary columns
# cols1 = np.arange(start=2, stop=44)
# cols1 = np.append(cols1, [45,46,48,49,51,52,54,55])
cols1 = [3,4,6,7,9,10,12]
df_dxd.drop(df_dxd.columns[cols1], axis=1, inplace=True)
# Rename columns
df_dxd.columns = ['Date', 'Time', 'EOR5_Confining', 'EOR6_Confining', 'EOR6_Up', 'EOR6_Down']
# Change datetime format and delete old datetime columns
df_dxd['DateTime_DXD'] = pd.to_datetime(df_dxd['Date'] + " " + df_dxd['Time'])
cols = ['DateTime_DXD','EOR5_Confining', 'EOR6_Confining', 'EOR6_Up', 'EOR6_Down']
df_dxd = df_dxd[cols]
# Get length for later use in trimming data block
len_df_dxd = len(df_dxd)

## Concatenate the EOR and DXD dataframes
df_eor = df_eor.join(df_dxd)
       
## Sync Time
# Find out which data set starts first and find difference between elapsed time
# of the dataset which starts first and the start time of the data set that
# started second
if df_eor.DateTime_EOR[0] < df_eor.DateTime_DXD[0]:
    df_eor['dT'] = (df_eor.DateTime_EOR - df_eor.DateTime_DXD[0]).astype('timedelta64[s]')
    sync_key = 1
else:
    df_eor['dT'] = (df_eor.DateTime_DXD - df_eor.DateTime_EOR[0]).astype('timedelta64[s]')
    sync_key = 2
# Find index of minimum value in df_eor['dT'], thats the sync index    
arr_dT = df_eor.dT.values
arr_dT = np.absolute(arr_dT)
sync_idx = np.where(arr_dT == arr_dT.min())  
# Build synced array of all important data and trim data to shortest file length
arr_eor = df_eor.values
arr_eor = np.delete(arr_eor,[7,8,9,10,11,12],1)
arr_dxd = df_dxd.values
if sync_key == 1:
    arr_eor = np.delete(arr_eor,np.s_[0:sync_idx[0][0]],axis=0)
if sync_key == 2:
    arr_dxd = np.delete(arr_dxd,np.s_[0:sync_idx[0][0]],axis=0)
if len_df_dxd<len_df_eor:
    arr_eor = np.delete(arr_eor,np.s_[len_df_dxd:len_df_eor],axis=0)
if len_df_dxd>len_df_eor:
    arr_dxd = np.delete(arr_dxd,np.s_[len_df_eor:len_df_dxd],axis=0)
# Concatenate all data back into one array and build elapsed time array        
arr = np.concatenate((arr_eor,arr_dxd), axis=1)
elapsed_time = np.arange(0,(len(arr))/120,1/120) # Assume 30 second increments
# Array column key:
    #0: EOR timedate
    #1: EOR_Pump1Vol (EOR5 Pump)
    #2: EOR_Pump1Rate (EOR5 Pump)
    #3: EOR_Pump2Vol (EOR6 Pump)
    #4: EOR_Pump2Rate (EOR6 Pump)
    #5: EOR5_Up Pressure
    #6: EOR5_Down Pressure
    #7: DXD timedate
    #8: EOR5 Confining Pressure
    #9: EOR6 Confining Pressure
    #10: EOR6 Up Pressure
    #11: EOR6 Down Pressure

## Calculate Permeability
# Calculate sample x-sectional area
Area1 = np.pi/4*Diameter1**2
Area2 = np.pi/4*Diameter2**2
# Calculate differential pressure
dP1 = arr[:,5]-arr[:,6] #EOR5 dP
dP2 = arr[:,10]-arr[:,11] #EOR6 dP
# Calculate instantaneous rate for each pump
time_diff = 0.5 #assume 30 second time difference between points
Pump1_diff = np.diff(arr[:,1]) 
Pump1_rate = Pump1_diff/time_diff
Pump1_rate = np.append(np.zeros(1),Pump1_rate)
Pump2_diff = np.diff(arr[:,3]) 
Pump2_rate = Pump2_diff/time_diff
Pump2_rate = np.append(np.zeros(1),Pump2_rate)
# Calculate Perm
Perm1 = (Visc1*Length1*14.7/(60*Area1))*(Pump1_rate/dP1)*10**6
Perm2 = (Visc2*Length2*14.7/(60*Area2))*(Pump2_rate/dP2)*10**6

## Plot EOR5 and EOR6 Separately
# Some plot magic for multiple axes
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

# First, EOR5
fig, host = plt.subplots()
fig.subplots_adjust(right=0.75)

par1 = host.twinx()
par2 = host.twinx()

# Offset the right spine of par2.  The ticks and label have already been
# placed on the right by twinx above.
par2.spines["right"].set_position(("axes", 1.2))
# Having been created by twinx, par2 has its frame off, so the line of its
# detached spine is invisible.  First, activate the frame but make the patch
# and spines invisible.
make_patch_spines_invisible(par2)
# Second, show the right spine.
par2.spines["right"].set_visible(True)

p1, = host.plot(elapsed_time, arr[:,5], "b-", label="Up Pressure")
p2, = par1.plot(elapsed_time, arr[:,2], "r-", label="Flow Rate")
p3, = par2.plot(elapsed_time, Perm1, "g-", label="Permeability")
p4, = host.plot(elapsed_time, arr[:,6], "b--", label="Down Pressure")

# host.set_xlim(0, 1000)
# host.set_ylim(0, 2)
# par1.set_ylim(0, 4)
# par2.set_ylim(1, 65)

host.set_xlabel("Test Time (Hr)")
host.set_ylabel("Pressure (psi)")
par1.set_ylabel("Flow Rate (mL/min)")
par2.set_ylabel("Permeability (uD)")

host.yaxis.label.set_color(p1.get_color())
par1.yaxis.label.set_color(p2.get_color())
par2.yaxis.label.set_color(p3.get_color())

tkw = dict(size=4, width=1.5)
host.tick_params(axis='y', colors=p1.get_color(), **tkw)
par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
host.tick_params(axis='x', **tkw)

lines = [p1, p4, p2, p3]

par2.legend(lines, [l.get_label() for l in lines], loc='upper left')
plt.title('EOR5 - '+ EOR5_ID)
plt.show()

# Now, EOR6
fig, host = plt.subplots()
fig.subplots_adjust(right=0.75)

par1 = host.twinx()
par2 = host.twinx()

# Offset the right spine of par2.  The ticks and label have already been
# placed on the right by twinx above.
par2.spines["right"].set_position(("axes", 1.2))
# Having been created by twinx, par2 has its frame off, so the line of its
# detached spine is invisible.  First, activate the frame but make the patch
# and spines invisible.
make_patch_spines_invisible(par2)
# Second, show the right spine.
par2.spines["right"].set_visible(True)

p1, = host.plot(elapsed_time, arr[:,10], "b-", label="Up Pressure")
p2, = par1.plot(elapsed_time, arr[:,4], "r-", label="Flow Rate")
p3, = par2.plot(elapsed_time, Perm2, "g-", label="Permeability")
p4, = host.plot(elapsed_time, arr[:,11], "b--", label="Down Pressure")

# host.set_xlim(0, 1000)
# host.set_ylim(0, 2)
# par1.set_ylim(0, 4)
# par2.set_ylim(1, 65)

host.set_xlabel("Test Time (Hr)")
host.set_ylabel("Pressure (psi)")
par1.set_ylabel("Flow Rate (mL/min)")
par2.set_ylabel("Permeability (uD)")

host.yaxis.label.set_color(p1.get_color())
par1.yaxis.label.set_color(p2.get_color())
par2.yaxis.label.set_color(p3.get_color())

tkw = dict(size=4, width=1.5)
host.tick_params(axis='y', colors=p1.get_color(), **tkw)
par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
host.tick_params(axis='x', **tkw)

lines = [p1, p4, p2, p3]

par2.legend(lines, [l.get_label() for l in lines], loc='upper left')
plt.title('EOR6 - '+ EOR6_ID)
plt.show()