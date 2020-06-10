import pandas as pd
import pickle
import os
import sys
import io
import jdatetime as jd

from convert_ar_characters import convert_ar_characters

# A function to read different file and prepare them
def read_blnc_data(file='98.txt',path=r"C:\Users\Mahdi\OneDrive\Master Thesis\Data"):
    """
    A file to read blncesheedt data from txt and clean it for our use.
    """

    os.chdir(path)
    with open(file,encoding="utf8") as f:
        fileobject = io.StringIO(f.read())

    BlncData = pd.read_csv(fileobject, sep='\t',  lineterminator='\n', names=None)
    
    # Selecting Columns
    BlncData = BlncData[['نماد', 'سال مالی', 'تاریخ مصوب','جمع دارایی‌های جاری',
           'سرمایه گذاری‌ها و سایر دارایی‌ها', 'خالص دارایی‌های ثابت',
           'جمع دارایی‌های غیر جاری', 'جمع کل دارایی‌ها', 'جمع بدهی‌های جاری',
           'جمع بدهی‌های غیر جاری', 'جمع کل بدهی‌ها', 'سرمایه',
           'سود و زیان انباشته', 'اندوخته قانونی',
           'جمع حقوق صاحبان سهام در پایان سال مالی',
           'جمع کل بدهی‌ها و حقوق صاحبان سهام',
           'جمع حقوق صاحبان سهام مصوب (در مجمع عادی)']]
    
    # renaming columns
    BlncData.rename(columns={'نماد':'Symbol','سال مالی':'Fin_year','جمع دارایی‌های جاری':'Tot_current_asset','تاریخ مصوب':'approve_date',
                             'خالص دارایی‌های ثابت':'Net_fixed_assed','سرمایه گذاری‌ها و سایر دارایی‌ها':'other_asset',
                             'جمع بدهی‌های جاری':'Tot_current_lib','جمع کل دارایی‌ها':'Tot_asset','جمع دارایی‌های غیر جاری':'Tot_uncurrent_asset',
                             'سرمایه':'Capital','حقوق عمومی':'Public_rights','جمع کل بدهی‌ها':'Tot_lib','جمع بدهی‌های غیر جاری':'Tot_uncurrent_lib',
                             'سایر اندوخته‌ها':'Other_saving','اندوخته قانونی':'Reserved_saving','سود و زیان انباشته':'Comulated_profit_loss',
                             'جمع حقوق صاحبان سهام در پایان سال مالی':'Equity_at_year_end','جمع کل بدهی‌ها و حقوق صاحبان سهام':'Debt_Equity',
                              'جمع حقوق صاحبان سهام مصوب (در مجمع عادی)':'Debt_Equity_normal'},inplace=True)

    # DataOrg.Symbol: convert_ar_characters(x)
    Names = BlncData.Symbol.drop_duplicates()
    Conv_Names = Names.apply(lambda x : convert_ar_characters(x))
    BlncData_Symbol_ArtoFa_dict = dict(zip(Names,Conv_Names))
    BlncData['Symbol'] = BlncData.Symbol.map(BlncData_Symbol_ArtoFa_dict)

    # Dates
    BlncData = BlncData[~pd.isnull(BlncData.Fin_year)]
    BlncData.Fin_year = BlncData.Fin_year.apply(lambda x: jd.date(day=int(x[8:10]), month=int(x[5:7]),year=int(x[0:4])))

    BlncData = BlncData[~pd.isnull(BlncData.approve_date)]
    BlncData.approve_date = BlncData.approve_date.apply(lambda x: jd.date(day=int(x[8:10]), month=int(x[5:7]),year=int(x[0:4])))
    
    # changing to int
    for x in BlncData.columns[3:]:
        BlncData = BlncData[~pd.isnull(BlncData[x])]
        BlncData[x] = BlncData[x].apply(lambda x: int(x.replace(',','')))
        
    return(BlncData)