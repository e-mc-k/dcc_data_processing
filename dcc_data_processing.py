# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 14:34:44 2021

@author: E. Kias
"""
import numpy as np
import pandas as pd


dataqpath = r"P:\Internal Data\Testing\Quidnet_Deformable_Cell\Test_Data\210316_PPGSlurry1230pMud_Test16_2p5OBBP\210316_PPGSlurry1230pMud_Test16_2p5OBBP.2inP"
balancelinkpath = r"P:\Internal Data\Testing\Quidnet_Deformable_Cell\Test_Data\210316_PPGSlurry1230pMud_Test16_2p5OBBP\210316_PPGSlurry1230pMud_Test16_2p5OBBP_MASS.TXT"
df_dataq = pd.read_csv(dataqpath, skiprows=(4))
df_blink = pd.read_csv(balancelinkpath)
df_blink.columns = ['mass (g)', 'Time']