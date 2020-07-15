import pandas as pd
import pickle
import os
import sys
import io
import jdatetime as jd

from convert_ar_characters import convert_ar_characters
from functions import replace_comma
from functions import replace_jalalidate
from functions import find_year

# A function to read different file and prepare them
def read_blnc_data(year,path,sherkat_namad_dict):
    """
    A file to read blncesheedt data from txt and clean it for our use.
    """

    os.chdir(path)
    if str(year)[2:]+'.txt' in os.listdir():
        os.chdir(path)
        with open(str(year)[2:]+'.txt',encoding="utf8") as f:
            fileobject = io.StringIO(f.read())
        BlncData = pd.read_csv(fileobject, sep='\t',  lineterminator='\n', names=None)

    else:
        os.chdir(path)
        BlncData = pd.read_excel(str(year)[2:]+'.xlsx')    

    BlncData['شرکت']=BlncData['شرکت'].apply(lambda x: convert_ar_characters(x))
    BlncData['نماد'] = BlncData['شرکت'].map(sherkat_namad_dict)



    # Selecting Columns
    BlncData = BlncData[['نماد','شرکت', 'سال مالی', 'تاریخ مصوب','جمع دارایی‌های جاری',
           'سرمایه گذاری‌ها و سایر دارایی‌ها', 'خالص دارایی‌های ثابت',
           'جمع دارایی‌های غیر جاری', 'جمع کل دارایی‌ها', 'جمع بدهی‌های جاری',
           'جمع بدهی‌های غیر جاری', 'جمع کل بدهی‌ها', 'سرمایه',
           'سود و زیان انباشته', 'اندوخته قانونی',
           'جمع حقوق صاحبان سهام در پایان سال مالی',
           'جمع کل بدهی‌ها و حقوق صاحبان سهام',
           'جمع حقوق صاحبان سهام مصوب (در مجمع عادی)','حقوق عمومی','سایر اندوخته\u200cها']]

    # renaming columns
    col_name_dict = {'نماد':'Symbol','شرکت':'Firm','سال مالی':'Fin_year','جمع دارایی‌های جاری':'Tot_current_asset',
                      'تاریخ مصوب':'Approve_date','خالص دارایی‌های ثابت':'PPE','سرمایه گذاری‌ها و سایر دارایی‌ها':'other_longterm_asset',
                      'جمع بدهی‌های جاری':'Tot_current_lib','جمع کل دارایی‌ها':'Tot_asset','جمع دارایی‌های غیر جاری':'Tot_noncurrent_asset',
                      'سرمایه':'Capital','حقوق عمومی':'public_rights','جمع کل بدهی‌ها':'Tot_lib','جمع بدهی‌های غیر جاری':'Tot_noncurrent_lib',
                      'سایر اندوخته‌ها':'Saving_other','اندوخته قانونی':'Saving_required','سود و زیان انباشته':'Acummulated_profit',
                      'جمع حقوق صاحبان سهام در پایان سال مالی':'Equity','جمع کل بدهی‌ها و حقوق صاحبان سهام':'Debt_and_equity',
                      'جمع حقوق صاحبان سهام مصوب (در مجمع عادی)':'debt_equity_normal'}
    BlncData.rename(columns=col_name_dict,inplace=True)


    # Dates
    BlncData.Fin_year = BlncData.Fin_year.apply(lambda x: replace_jalalidate(x))
    BlncData.Approve_date = BlncData.Approve_date.apply(lambda x: replace_jalalidate(x))

    # changing to int
    for x in BlncData.columns:
        BlncData[x] = BlncData[x].apply(lambda x: replace_comma(x))
    
    # Finding Year
    BlncData = BlncData[~pd.isnull(BlncData.Fin_year)]  
    BlncData['Year'] = BlncData.Fin_year.apply(lambda x: find_year(x))
    
    BlncData['Book_value'] = BlncData.Tot_asset-BlncData.Tot_lib
    
    BlncData = BlncData[['Firm','Symbol','Fin_year','Year','Approve_date','Tot_current_asset','PPE',
                         'other_longterm_asset','Tot_noncurrent_asset','Tot_asset','Tot_current_lib', 
                         'Tot_noncurrent_lib', 'Tot_lib','Capital','Acummulated_profit', 'Saving_required',
                         'Saving_other','Equity', 'Debt_and_equity','Book_value','debt_equity_normal', 'public_rights']]
    
    out = {'data':BlncData,'columns_dict' :col_name_dict}
    return(out)