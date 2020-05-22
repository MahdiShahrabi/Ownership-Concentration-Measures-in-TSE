import pandas as pd
import numpy as np
import sys
import jdatetime as jd
import os
import matplotlib.pyplot as plt 
import pickle
import io
import requests
from bs4 import BeautifulSoup

from gameTheoric_concentration import gameTheoric_concentration


def fill_shapley_banzhaf(data,SDATA,fast_mode = True,time_pnt=False,major_mode='number',major_thr=10):
    
    # list initiation
    Errors = []
    
    # Columns to check
    check_data = data[['Symbol','SSCL','SSDL','BZCL','BZDL']]
    
    # Finding location of NaN to fill
    indx, col = np.where(pd.isnull(check_data))
    ITEMS = [list(x) for x in np.column_stack([check_data.index[indx], check_data.columns[col]])]
    lng_0 = len(ITEMS)
    
    # setting function based on the column name
    guide_dict = {'SS':'shapley','BZ':'banzhaf','C':'concentrated','D':'dispersed'}
    col_dict = {'SSCL':['SSCL','SSCO'],'SSDL':['SSDL','SSDO'],'BZCL':['BZCL','BZCO'],'BZDL':['BZDL']}
    
    cnt = 1
    for item in ITEMS:
        # Assigning addres
        index, mode = item
        sym = data.Symbol.iloc[index]
        col_names = col_dict[mode]
        # Progress output
        print('The symbol ',sym, ' mode: ',mode,', ',cnt,' from ', len(ITEMS))
        cnt+=1 
        
        # Finding and assigning  value
        try:
            temp = gameTheoric_concentration(sym,SDATA, index=guide_dict[mode[0:2]], how=guide_dict[mode[2]],quota = 50.01,major_mode=major_mode,major_thr=major_thr,
                                  concentration_point=0.99,time_pnt=time_pnt,fast_mode = fast_mode)
            
            data.loc[data.Symbol==sym,col_names[0]] = temp[0]
            
            # This try handles the BZDO case!
            try:
                data.loc[data.Symbol==sym,col_names[1]] = temp[1]
            except:
                pass
            
            if isinstance(temp,str):
                Errors.append([sym,mode,temp])
                data.loc[data.Symbol==sym,col_names[0]] = np.nan
                try:
                    data.loc[data.Symbol==sym,col_names[1]] = np.nan
                except:
                    pass

        except Exception as e:
                Errors.append([sym,mode,'fatal_error: '+str(e)])
                data.loc[data.Symbol==sym,col_names[0]] = np.nan
                try:
                    data.loc[data.Symbol==sym,col_names[1]] = np.nan
                except:
                    pass
                
                
                
    
     # Columns to check
    check_data = data[['Symbol','SSCL','SSDL','BZCL','BZDL']]
    
    # Finding location of NaN to fill
    indx, col = np.where(pd.isnull(check_data))
    ITEMS = [list(x) for x in np.column_stack([check_data.index[indx], check_data.columns[col]])]
    lng_1 = len(ITEMS)
    
    print('\n\n**About ',lng_0-lng_1,' out of ',lng_0,' of mising cells are filled!')
    
    
    OUT = {'CMdf':data, 'Errors':Errors}
    return(OUT)