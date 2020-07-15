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
def read_inc_data(year,path,sherkat_namad_dict):
    """
    A file to read blncesheedt data from txt and clean it for our use.
    """
    
    file_name = 'inc'+str(year)[2:]+'.csv'
    os.chdir(path)
    df = pd.read_csv(file_name)
    df.rename(columns={'نامشرکت':'نام شرکت','سالمالی':'سال مالی','تاریخمصوب':'تاریخ مصوب','ارزشروز':'ارزش روز',
                      'جمعدرآمدها':'جمع درآمدها','بهایتمامشدهکالایفروشرفته':'بهای تمام شده کالای فروش رفته','بهایتمامشدهاملاکواگذارشدهوخدماتا':'بهای تمام شده املاک فروش رفته و خدمات',
                      'هزینهتامینمنابعمالیعملیاتلیزینگه':'هزینه تامین منابع مالی عملیات لیزینگ (هزینه سود و کارمزد تامین منابع مالی)',
                      'سودناویژه':'سود ناویژه','خالصدرآمدهاوهزینههایعملیاتی':'خالص درآمدها و هزینه‌های عملیاتی',
                      'سودزیانعملیاتی':'سود (زیان) عملیاتی','هزینههایمالی':'هزینه‌های مالی','سودزیانتسعیرتسهیلاتارزیدریافتی':'سود (زیان) تسعیر تسهیلات ارزی دریافتی',
                      'خالصسایردرآمدهاهزینهها':'خالص سایر درآمدها (هزینه‌ها)','سودزیانفروشدارائیهایزیستیمولد':'سود(زیان)فروش دارائیهای زیستی مولد',
                      'تعدیلارزشسرمایهگذاریها':'تعدیل ارزش سرمایه گذاریها','سودزیانقبلازکسرمالیات':'سود (زیان) قبل از کسر مالیات',
                      'سهماقلیتازسودسالجاری':'سهم اقلیت از سود سال جاری','سودزیانپسازکسرمالیات':'سود (زیان) پس از کسر مالیات',
                      'سودانباشتهابتدایدوره':'سود انباشته ابتدای دوره','تعدیلاتسنواتی':'تعدیلات سنواتی',
                      'سودقابلتخصیص':'سود قابل تخصیص','نسبتسودبهفروش':'نسبت سود به فروش','حسابرسیشده':'حسابرسی شده',
                      'تجدیدارائهشده':'تجدید ارائه شده'},inplace=True)

    df.drop(columns=['نوع','تلفیقی','حسابرسی شده', 'تجدید ارائه شده','v35','بازار'],inplace=True)

    col_name_dict = { 'نام شرکت':'Firm','نماد':'Symbol','سال مالی':'Fin_year','تاریخ مصوب':'Approve_date',
                      'ارزش روز':'Marketcap','سرمایه':'Capital','جمع درآمدها':'Revenue',
                      'بهای تمام شده کالای فروش رفته':'Cost_of_revenue',
                      'هزینه تامین منابع مالی عملیات لیزینگ (هزینه سود و کارمزد تامین منابع مالی)':'capital_cost_',
                      'سود ناویژه':'Gross_profit','خالص درآمدها و هزینه‌های عملیاتی':'Operating_expenses',
                      'سود (زیان) عملیاتی':'Operating_income','هزینه‌های مالی':'Interest',
                      'سود (زیان) تسعیر تسهیلات ارزی دریافتی':'exchange_rate_profit','خالص سایر درآمدها (هزینه‌ها)':'Total_other_income_expenses_net',
                      'سود(زیان)فروش دارائیهای زیستی مولد':'green_profit_','تعدیل ارزش سرمایه گذاریها':'adj_investments_',
                      'سود (زیان) قبل از کسر مالیات':'EBT','مالیات':'Tax','سهم اقلیت از سود سال جاری':'minority_share_from_profit_',
                      'سود (زیان) پس از کسر مالیات':'Net_income','سود انباشته ابتدای دوره':'acumulated_profit',
                      'تعدیلات سنواتی':'adjustments','سود قابل تخصیص':'divideable_profit','epsخالص':'Net_eps','epsناخالص':'eps_',
                      'نسبت سود به فروش':'profit_to_sale','بهای تمام شده املاک فروش رفته و خدمات':'real_estate_income_'}

    df.rename(columns=col_name_dict,inplace=True)

    df['Firm'] = df['Firm'].apply(lambda x: convert_ar_characters(x))
    df['Symbol'] = df['Firm'].map(sherkat_namad_dict)

    df.Fin_year = df.Fin_year.apply(lambda x: replace_jalalidate(x))
    df.Approve_date = df.Approve_date.apply(lambda x: replace_jalalidate(x))

    # changing to int
    for x in df.columns:
        df[x] = df[x].apply(lambda x: replace_comma(x))

    df = df[~pd.isnull(df.Fin_year)]  
    df['Year'] = df.Fin_year.apply(lambda x: find_year(x))
    
    df = df[['Firm','Symbol','Fin_year','Year','Approve_date','Revenue','Cost_of_revenue','Gross_profit','Operating_expenses',
    'Operating_income','Interest','Total_other_income_expenses_net','EBT','Tax','Net_income','Net_eps','Capital',
    'Marketcap','acumulated_profit', 'adjustments', 'divideable_profit','exchange_rate_profit', 'ps',
    'profit_to_sale','eps_','minority_share_from_profit_','capital_cost_', 'real_estate_income_','green_profit_',
    'adj_investments_']]

    out = {'data':df,'columns_dict' :col_name_dict}
    return(out)