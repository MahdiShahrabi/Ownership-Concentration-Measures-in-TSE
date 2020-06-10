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

def find_shapley(percent,how='direct',quota = 50.01,major_mode='number',major_thr=20,concentration_point=0.99,time_pnt=False,fast_mode = True):
    
    """
    A function for finding Shapley-Shbik Index.
    
    This functions uses David Leech website to calculate Shapley-Shubik index.
    
    ...
    
    Parameters
    -----------
    percent: list, voting rights
    
    how: str, 'direct', 'concentrated', 'ocean', 'genf', and 'mmle'
    
    quota: float
    
    major_mode: 'percent' or 'number'
    
    major_thr: if major_mode is 'percnet'--> float
               if major_mode is 'number'--> int
            
    concentration_point: float, [less than 1]
    """
    df = percent
    
    # sorting
    percent.sort(reverse=True)
    
    # Fast mode calculates
    if percent[0]>=quota and fast_mode:
        if how is not 'ocean':
            out = pd.DataFrame(data={'Weight':percent,
                             'SSINDEX':[1]+[0]*(len(percent)-1)})
        elif how is 'ocean':
            out = pd.DataFrame(data={'Weight':percent+['Ocean'],
                             'SSINDEX':[1]+[0]*(len(percent))})

        return(out)
    
    # Checking size of input
    if len(df)<=1 and how is not 'ocean' and how is not 'concentrated':
        return('Error: Length Error!')
    
    
    ## Preparing website inputs
    if how is 'direct':
        prc = percent
        prc_str = ''
        for x in prc:
            prc_str+=str(x)
            prc_str+=' '
        payload = {'numberofplayers': len(df),
                   'quota': quota,
                   'textarea': prc_str}
        
        
    elif how is 'genf':
        prc = [int(x*100)for x in percent]
        prc_str = ''
        for x in prc:
            prc_str+=str(x)
            prc_str+=' '
        payload = {'numberofplayers': len(df),
                   'quota': int(quota*100),
                   'textarea': prc_str}    
        
        
    elif how is 'mmle':
        prc = [x for x in percent]
        prc_str = ''
        for x in prc:
            prc_str+=str(x)
            prc_str+=' '
        if major_mode=='percent':
            Majors = len([x for x in prc if x>=major_thr])
            Minors = len(df) - Majors
        elif major_mode=='number':
            Majors = len(prc[0:min(major_thr,len(prc))])
            Minors = len(prc) - Majors
        payload = {'numberofplayers': Majors,#majo3
                   'numberofplayers2': Minors,#minor
                   'quota': quota,
                   'textarea': prc_str}           
    
    
    elif how is 'ocean':
        prc = [x for x in percent]
        prc_str = ''
        for x in prc:
            prc_str+=str(x)
            prc_str+=' '
        total_weight = 100
        payload = {'numberofplayers': len(df),# number of atomic players
                   'totalweight': total_weight,
                   'quota': 50.1,
                   'textarea': prc_str}
    
    
    
    # URL Dict
    URL_shapley={'direct':"https://mywebpages.csv.warwick.ac.uk/cgi-vpi/ssdirect.cgi",
                 'genf':"https://mywebpages.csv.warwick.ac.uk/cgi-vpi/ssgenf.cgi",
                 'mmle':"https://mywebpages.csv.warwick.ac.uk/cgi-vpi/ssmmle.cgi",
                 'ocean':"https://mywebpages.csv.warwick.ac.uk/cgi-vpi/ssocean.cgi"}
    # website url
    url = URL_shapley[how]
    
    # Making request
    try:
        response = requests.request("POST", url, data = payload)
    except:
        return('Error: request error!')
    if time_pnt:
        print(' It took about ',np.round(response.elapsed.microseconds/1e6,2), 'seconds')
        
    # Parshing output html of wevsite
    parsed_html = BeautifulSoup(response.text.encode('utf8'),features="html.parser")
    
     # Finding rows or error message
    if parsed_html('tr'):
        rows = parsed_html('tr')
    else:
        return('Error: '+parsed_html.find('p').text)
    
    # Extracting rows to a list of lists
    data = []
    for row in rows:
        if row.th:
            cols = row.find_all('th')
            cols = [ele.text.strip() for ele in cols]
            if len(cols) is 1:
                data.append([cols[0],''])
            else:
                data.append([ele for ele in cols if ele]) # Get rid of empty valuespty values
        else:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele]) # Get rid of empty values
    
    # Converting list of lists to a dataframe
    try:
        if how is 'mmle':
            out = pd.DataFrame(data[1:(len(data)-1)], columns=data[0])
            out.iloc[:,0] = prc
            
        elif how is 'ocean':
            del data[0]
            del data[-2]
            data[-1][0] = 'Ocean'
            out = pd.DataFrame(data[1:len(data)], columns=data[0])
            
        else: 
            out = pd.DataFrame(data[1:], columns=data[0])
            out.iloc[:,0] = prc
        
        out.rename(columns={'Shapley-Shubik Index':'SSINDEX','SHAPLEY-SHUBIK':'SSINDEX','WEIGHT':'Weight'},inplace=True)
        return(out)
    
    except:
        return('Error: creating dataFrame error! ')