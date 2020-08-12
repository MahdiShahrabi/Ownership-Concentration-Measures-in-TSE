## Loading Libraries
import pandas as pd
import numpy as np
import sys
import jdatetime as jd
import os
import pickle

## Loading functions
from convert_ar_characters import convert_ar_characters
from nthMax import nth_max
from gini import gini
from find_shapley import find_shapley
from find_banzhaf import find_banzhaf
from gameTheoric_concentration import gameTheoric_concentration
from fill_shapley_banzhaf import fill_shapley_banzhaf

def find_measures(year,month=0,pnt=False):
    if month is 0:
        # Yearly
        file_name_holderdata = "Shareholder"+str(year)+".csv"
        file_name_measures = "Measures"+str(year)+".csv"
        path = r"C:\Users\Mahdi\OneDrive\Master Thesis\Data"
    else:
        file_name_holderdata = "Shareholder"+str(year)+'_'+str(month)+".csv"
        file_name_measures = "Measures"+str(year)+'_'+str(month)+".csv"
        path = r"C:\Users\Mahdi\OneDrive\Master Thesis\Data\MonthlyShareholder"
        
    os.chdir(path)
    SDATA = pd.read_csv(file_name_holderdata,index_col=0).drop_duplicates()
    
    
    # Creating Dataframe for saving concentration mearsurs
    CMdf = SDATA.groupby('Symbol',as_index=False).agg({'Id_tse':'first','Industry':'first','percent':'sum',
                                                       'ShareHolder':'count','MarketCap':'first'}).rename(columns=
                                                                {'ShareHolder':'Num_holders','percent':'sum_over1'})
    CMdf.reset_index(drop=True,inplace=True)
    Orginal_Size = len(CMdf)
    print('Number of observed firms in year ',str(year),' is : ',Orginal_Size)
    
    # Largest Owner
    temp = SDATA.groupby('Symbol',as_index=False).agg({'percent':'max'}).rename(columns={'percent':'Largest_Owner'})
    CMdf = pd.merge(CMdf,temp,left_on='Symbol',right_on='Symbol',how='left')
    
    # First/Second
    temp = SDATA.groupby('Symbol',as_index=False).agg({'percent':{lambda x: max(x)/nth_max(x,nth=2,interval=False)}}).rename(columns={'percent':'First_Second'})
    CMdf = pd.merge(CMdf,temp,left_on='Symbol',right_on='Symbol',how='left').rename(columns={('First_Second', '<lambda>'):'First_Second'})
    
    # First/SumToFour
    temp = SDATA.groupby('Symbol',as_index=False).agg({'percent':{lambda x: max(x)/sum(nth_max(x,nth=[2,4],interval=True))}}).rename(
    columns={'percent':'First_Sumtwofour'})
    CMdf = pd.merge(CMdf,temp,left_on='Symbol',right_on='Symbol',how='left').rename(columns={('First_Sumtwofour', '<lambda>'):'First_Sumtwofour'})
    
    # Sumfive
    temp = SDATA.groupby('Symbol',as_index=False).agg({'percent':{lambda x: sum(nth_max(x,nth=[1,5],interval=True))}}).rename(columns={'percent':'Sumfive'})
    CMdf = pd.merge(CMdf,temp,left_on='Symbol',right_on='Symbol',how='left').rename(columns={('Sumfive', '<lambda>'):'Sumfive'})
    
    temp = SDATA.groupby('Symbol',as_index=False).agg({'percent':{lambda x: sum(nth_max(x,nth=[1,4],interval=True))}}).rename(columns={'percent':'Sumfour'})
    CMdf = pd.merge(CMdf,temp,left_on='Symbol',right_on='Symbol',how='left').rename(columns={('Sumfour', '<lambda>'):'Sumfour'})


    temp = SDATA.groupby('Symbol',as_index=False).agg({'percent':{lambda x: sum(nth_max(x,nth=[1,3],interval=True))}}).rename(columns={'percent':'Sumthree'})
    CMdf = pd.merge(CMdf,temp,left_on='Symbol',right_on='Symbol',how='left').rename(columns={('Sumthree', '<lambda>'):'Sumthree'})


    temp = SDATA.groupby('Symbol',as_index=False).agg({'percent':{lambda x: sum(nth_max(x,nth=[1,2],interval=True))}}).rename(columns={'percent':'Sumtwo'})
    CMdf = pd.merge(CMdf,temp,left_on='Symbol',right_on='Symbol',how='left').rename(columns={('Sumtwo', '<lambda>'):'Sumtwo'})
    
    # Gini
    temp = SDATA.groupby('Symbol',as_index=False).agg({'percent':{lambda x: gini(list(x))}}).rename(columns={'percent':'Gini'})
    CMdf = pd.merge(CMdf,temp,left_on='Symbol',right_on='Symbol',how='left').rename(columns={('Gini', '<lambda>'):'Gini'})
    
    # Herfindahl
    temp = SDATA.groupby('Symbol',as_index=False).agg({'percent':{lambda x: sum([(t/100)**2 for t in list(x)])}}).rename(columns={'percent':'Herfindhal'})
    CMdf = pd.merge(CMdf,temp,left_on='Symbol',right_on='Symbol',how='left').rename(columns={('Herfindhal', '<lambda>'):'Herfindhal'})
    
    # Shapley-Shubik
    # For refilling
    try:
        os.chdir(path)
        CMdf_load = pd.read_csv(file_name_measures)
        CMdf = pd.merge(CMdf,CMdf_load[['Symbol','SSCL', 'SSCO', 'SSDL', 'SSDO', 'BZCL', 'BZCO', 'BZDL']],left_on='Symbol',right_on='Symbol',how='left')
        print('RE-FILL!')
    except:
        print('NEW!')
        # For the first time
        # Initiating columns
        CMdf['SSCL'] = np.nan
        CMdf['SSCO'] = np.nan
        CMdf['SSDL'] = np.nan
        CMdf['SSDO'] = np.nan
        CMdf['BZCL'] = np.nan
        CMdf['BZCO'] = np.nan
        CMdf['BZDL'] = np.nan
        
    data = fill_shapley_banzhaf(data = CMdf,SDATA=SDATA,fast_mode = True,time_pnt=pnt,major_thr = 10)
    CMdf = data['CMdf']

    print('len(Errors): ',len(data['Errors']))
    data['Errors']
    [x for x in data['Errors'] if x[2]!= 'Error: request error!']   
    
    
    Output_Size = len(CMdf)
    print('Orginal Size is ',Orginal_Size,' and output size is: ', Output_Size)
    os.chdir(path)
    CMdf.to_csv(file_name_measures)
    return(file_name_measures+' is done!\n')
    