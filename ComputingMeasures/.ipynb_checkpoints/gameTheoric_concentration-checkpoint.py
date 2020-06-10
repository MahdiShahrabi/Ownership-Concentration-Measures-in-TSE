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

from find_shapley import find_shapley
from find_banzhaf import find_banzhaf

def gameTheoric_concentration(symbol,SDATA, index='shapley', how='concentrated',quota = 50.01,major_mode='number',major_thr=20,
                              concentration_point=0.99,time_pnt=False,fast_mode = True):
    
    """
    Returns index for largest and ocean shareholder!
    """
    
    # Chcking inputs
    if how not in ['dispersed','concentrated']:
        raise ValueError('how must be in [\'dispersed\',\'concentrated\']!')
        
    if index not in ['shapley','banzhaf']:
        raise ValueError('indes must be in [\'shapley\',\'banzhaf\']!')
    
    # List of percents
    percent_list = list(SDATA.percent[SDATA.Symbol==symbol])
    
    # Finding functions
    func = {'shapley':find_shapley,'banzhaf':find_banzhaf}[index]
    
    # Finding results
    if how is 'concentrated':
        prc = [x for x in percent_list]
        unassigned = 100 - sum(prc)
        cons_point = concentration_point
        number = int(np.floor(unassigned/cons_point))
        residual = np.round(unassigned - number*cons_point,2)
        percent_list = prc+[cons_point]*number+[residual]    
        
        if len(percent_list)<15:
            results = func(percent=percent_list,how='direct',quota = quota,major_mode=major_mode,
                            major_thr=major_thr,concentration_point=concentration_point,time_pnt=time_pnt,fast_mode = fast_mode)
        
        if len(percent_list)>=15 or isinstance(results,str):
            results = func(percent=percent_list,how='mmle',quota = quota,major_mode=major_mode,
                            major_thr=major_thr,concentration_point=concentration_point,time_pnt=time_pnt,fast_mode = fast_mode)
    
    
    elif how is 'dispersed' and index is 'shapley':
        results = func(percent=percent_list,how='ocean',quota = quota,major_mode=major_mode,
                            major_thr=major_thr,concentration_point=concentration_point,time_pnt=time_pnt,fast_mode = fast_mode)
    
    elif how is 'dispersed' and index is 'banzhaf':
        updated_quota = quota - (100-sum(percent_list))/2
        if len(percent_list)<15:
            results = func(percent=percent_list,how='direct',quota = updated_quota,major_mode=major_mode,
                            major_thr=major_thr,concentration_point=concentration_point,time_pnt=time_pnt,fast_mode = fast_mode)
        if len(percent_list)>=15 or isinstance(results,str):
            results = func(percent=percent_list,how='mmle',quota = updated_quota,major_mode=major_mode,
                            major_thr=major_thr,concentration_point=concentration_point,time_pnt=time_pnt,fast_mode = fast_mode)
    

    
    ## Returning output
    if index is 'shapley' and np.logical_not(isinstance(results,str)):
        if how is 'concentrated':
            return([float(results.iloc[0,1]),
                   sum(results[results.Weight<=concentration_point]['SSINDEX'].apply(lambda x: float(x)))])
        elif how is 'dispersed':
            return([float(results.iloc[0,1]),
                   float(results[results.Weight=='Ocean']['SSINDEX'])])
            
    elif index is 'banzhaf' and np.logical_not(isinstance(results,str)):
        if how is 'concentrated':
            return([float(results.iloc[0,2]),
                   sum(results[results.Weight<=concentration_point]['Norm_Banzhaf'].apply(lambda x: float(x)))])
        elif how is 'dispersed':
            return([float(results.iloc[0,2]),
                   np.nan])
    else:
        return(results)