# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 14:34:44 2021

@author: E. Kias
"""
import numpy as np
import pandas as pd


dataqpath = r"P:\Internal Data\Testing\Quidnet_Deformable_Cell\Data_Reduction_Tools\dcc_data_processing\data\210316_PPGSlurry1230pMud_Test16_2p5OBBP.2inP"
balancelinkpath = r"P:\Internal Data\Testing\Quidnet_Deformable_Cell\Data_Reduction_Tools\dcc_data_processing\data\210316_PPGSlurry1230pMud_Test16_2p5OBBP_MASS.TXT"
df_dataq = pd.read_csv(dataqpath, skiprows=(4))
df_blink = pd.read_csv(balancelinkpath)
df_blink.columns = ['mass (g)', 'Time']

df_dataq['bob'] = np.where(df_dataq['Volt']<1.12,0,1)
df_dataq['bob2'] = df_dataq['bob']*3 + 1
