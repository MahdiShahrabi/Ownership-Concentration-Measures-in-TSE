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
def read_cf_data(year,path,sherkat_namad_dict):
    """
    A file to read blncesheedt data from txt and clean it for our use.
    """
    
    file_name = 'CF'+str(year)[2:]+'.csv'
    os.chdir(path)
    df = pd.read_csv(file_name)
    df.drop(columns=['v75','v28','بازار','نوع','تلفیقی','حسابرسیشده','تجدیدارائهشده'],inplace=True)
    
    df.rename(columns={'نامشرکت':'نام شرکت','سالمالی':'سال مالی','تاریخمصوب':'تاریخ مصوب','ارزشروز':'ارزش روز','تجدیدارائهشده':'تجدید ارائه شده',
    'جریانخالصورودخروجوجوهنقد':'جریان خالص وجوه نقد','حسابرسیشده':'حسابرسی شده','سودسهامپرداختیبهسهامداراناقلیت':'سود سهام پرداختی سهامداران اقلیت',
    'سودسهامدریافتیازشرکتها':'سود سهام دریافتی از شرکت ها','سودسهامپرداختی':'سود سهام پرداختی','سهمگروهازسودشرکتهایوابسته':'سهم گرو از سود شرکت های وابسته',
    'سوددریافتیبابتسرمایهگذاریها':'سود دریافتی بابت سرمایه گذاری ها','سودپرداختیبابتتسهیلاتمالی':'سود پرداختی بابت تسهیلات مالی','سودسهامدولت':'سود سهام دولت',
    'سوددریافتیبابتسپردههایکوتاهوبلند':'سود دریافتی بابت سپرده های کوتاه و بلند','سوداوراقمشارکت':'سود اوراق مشارکت','سودحاصلازسرمایهگذاریهاازمحلذخایر':'سود حاصل از سرمایه گذاری ها از محل ذخایر',
    'سایردریافتوپرداختها':'سایر دریافت و پرداخت ها','مالیاتبردرآمدپرداختی':'مالیات بر درآمد پرداختی','جمعجریانخالصبازدهسرمایهگذاریها':'جمع جریان خالص بازده سرمایه گذاری ها',
    'خریدداراییثابت':'خرید دارایی ثابت','فروشداراییثابت':'فروش دارایی ثابت','خریدداراییهاینامشهود':'خرید دارایی های نامشهود','فروشداراییهاینامشهود':'فروش دارایی های نامشهود',
    'خریدسایرداراییها':'خرید سایر دارایی ها','فروشسایرداراییها':'فروش سایر دارایی ها','خریدسرمایهگذاریکوتاهمدت':'خرید سرمایه گذاری کوتاه مدت',
    'فروشسرمایهگذاریکوتاهمدت':'فروش سرمایه گذاری کوتاه مدت','خریدسرمایهگذاریبلندمدت':'خرید سرمایه گذاری بلند مدت','فروشسرمایهگذاریبلندمدت':'فروش سرمایه گذاری بلند مدت',
    'وجوهپرداختیبابتخریداوراقمشارکت':'وجوه پرداختی حاصل از خرید اوراق مشارکت','وجوهحاصلازبازخریداوراقمشارکتوسپر':'وجوه حاصل از بازخرید اوراق مشارکت و سپرده های بانکی',
    'وجوهحاصلازخریدسهام':'وجوه حاصل از خرید سهام','وجوه حاصل از فروش سهام':'وجوه حاصل از فروش سهام','وجوهحاصلازسرمایهگذاریدرپروژهها':'وجوه حاصل از سرمایه گذاری در پروژه ها',
    'وجوهپرداختیبابتتحصیلپروژهها':'وجوه پرداختی بابت تحصیل پروژه ها','سایروجوهپرداختییادریافتی':'سایر وجوه پرداختی دریافتی','زمیننگهداریشدهبرایساختاملاک':'زیمن نگهداری شده برای ساخت املاک',
    'وجوهپرداختیبابتخریددارائیهایغیرج':'وجوه پرداختی بابت خرید دارائیهای غیر جاری نگهداری شده برای فروش','وجوهدریافتیبابتفروشدارائیهاینگهد':'وجوه دریافتی بابت فروش دارائیهای نگهداری شده برای فروش',
    'وجوهپرداختیبابتخریدبخشیازسهامشرک':'وجوه پرداختی بابت خرید بخشی از سهام شرکت فرعی','وجوهدریافتیبابتفروشبخشیازسهامشرک':'وجوه دریافتی بابت فروش بخشی از سهام شرکت فرعی',
    'تسهیلاتاعطاییبهاشخاص':'تسهیلات اعطایی به اشخاص','استردادتسهیلاتاعطاییبهاشخاص':'استرداد تسهیلات اعطایی به اشخاص','وصولاصلسپردههایسرمایهگذاریهایبان':'وصول اصل سپرده‌های سرمایه‌گذاریهای بانکی',
    'وجوهپرداختیبابتتحصیلسرمایهگذارید':'وجوه پرداختی بابت تحصیل سرمایه گذاری در پیمان بیع متقابل','جمعجریانخالصفعالیتهایسرمایهگذاری':'جمع جریان خالص فعالیتهای سرمایه گذاری',
    'جمعجریانخالصقبلازتامینمالی':'جمع جریان خالص قبل از تامین مالی','وجوهحاصلازافزایشسرمایه':'وجوه حاصل از افزایش سرمایه','وجوهپرداختیبابتاوراقمشارکت':'وجوه پرداختی بابت اوراق مشارکت',
    'بازپرداختودایعمشترکین':'باز پرداخت ودایع مشترکین','وجوهدریافتیازسهامدارانبابتتامینن':'وجوه دریافتی از سهامداران بابت تامین نقدینگی','وجوهحاصلازافزایشسرمایهشرکتهایفرع':'وجوه حاصل از افزایش سرمایه شرکتهای فرعی-سهم اقلیت',
    'افزایشکاهشدرحسابهایشرکاء':'افزایش(کاهش)در حسابهای شرکاء','دریافتتسهیلاتمالی':'دریافت تسهیلات مالی','قرضالحسنهدریافتی':'قرض الحسنه دریافتی',
    'بازپرداختقرضالحسنه':'باز پرداخت قرض الحسنه','وجوهحاصلازانتشاراوراقگواهیسپردهخ':'وجوه حاصل از انتشار اوراق گواهی سپرده خاص',
    'پرداختمخارجتامینمالی':'پرداخت مخارج تامین مالی','افزایشحقوقسهامداراناقلیت':'افزایش حقوق سهامداران اقلیت','وجوهپرداختیبابتتحصیلسهامشرکتاصلی':'وجوه پرداختی بابت تحصیل سهام شرکت اصلی توسط شرکتهای فرعی',
    'بازپرداختتسهیلاتمالی':'باز پرداخت تسهیلات مالی','جمعجریانخالصفعالیتهایتامینمالی':'جمع جریان خالص فعالیتهای تامین مالی',
    'خالصافزایشکاهشوجهنقد':'خالص افزایش کاهش وجه نقد','ماندهوجهنقددرابتدایسال':'مانده وجه نقد در ابتدای سال','تغییراتنرخارز':'تغییرات نرخ ارز',
    'ماندهوجهنقددرانتهایسال':'مانده وجه نقد در انتهای سال','مبادلاتغیرنقدی':'مبادلات غیر نقدی','پاداشهیئتمدیره':'پاداش هیئت مدیره'},inplace=True)

    col_name_dict = { 'شرکت':'Firm','نماد':'Symbol','سال مالی':'Fin_year','تاریخ مصوب':'Approve_date',
                    'خالص افزایش کاهش وجه نقد':'Change_in_cash','مانده وجه نقد در انتهای سال':'End_cash_position',
                    'مانده وجه نقد در ابتدای سال':'Begining_cash_position','جریان خالص وجوه نقد':'Operating_cash_flow',
                    'جمع جریان خالص فعالیتهای تامین مالی':'Financing_cash_flow','جمع جریان خالص فعالیتهای سرمایه گذاری':'Investing_cash_flow'}

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

    df_all = df[['Year','Firm', 'Symbol', 'Fin_year', 'Approve_date',
           'Operating_cash_flow','Investing_cash_flow',
           'Financing_cash_flow','Begining_cash_position','Change_in_cash','End_cash_position',
           'سود سهام دریافتی از شرکت ها','سود سهام پرداختی سهامداران اقلیت', 'سهم گرو از سود شرکت های وابسته',
           'سود سهام پرداختی', 'سود پرداختی بابت تسهیلات مالی',
           'سود دریافتی بابت سرمایه گذاری ها', 'سود اوراق مشارکت',
           'سود دریافتی بابت سپرده های کوتاه و بلند', 'سود سهام دولت',
           'پاداش هیئت مدیره', 'سود حاصل از سرمایه گذاری ها از محل ذخایر',
           'سایر دریافت و پرداخت ها', 'جمع جریان خالص بازده سرمایه گذاری ها',
           'مالیات بر درآمد پرداختی', 'خرید دارایی ثابت', 'فروش دارایی ثابت',
           'خرید دارایی های نامشهود', 'فروش دارایی های نامشهود',
           'خرید سایر دارایی ها', 'فروش سایر دارایی ها',
           'خرید سرمایه گذاری کوتاه مدت', 'فروش سرمایه گذاری کوتاه مدت',
           'خرید سرمایه گذاری بلند مدت', 'فروش سرمایه گذاری بلند مدت',
           'وجوه پرداختی حاصل از خرید اوراق مشارکت', 'وجوه حاصل از خرید سهام',
           'وجوهحاصلازفروشسهام',
           'وجوه حاصل از بازخرید اوراق مشارکت و سپرده های بانکی',
           'وجوه حاصل از سرمایه گذاری در پروژه ها',
           'وجوه پرداختی بابت تحصیل پروژه ها', 'سایر وجوه پرداختی دریافتی',
           'زیمن نگهداری شده برای ساخت املاک',
           'وجوه پرداختی بابت خرید دارائیهای غیر جاری نگهداری شده برای فروش',
           'وجوه دریافتی بابت فروش دارائیهای نگهداری شده برای فروش',
           'وجوه پرداختی بابت خرید بخشی از سهام شرکت فرعی',
       'وجوه دریافتی بابت فروش بخشی از سهام شرکت فرعی',
       'تسهیلات اعطایی به اشخاص', 'استرداد تسهیلات اعطایی به اشخاص',
       'وصول اصل سپرده‌های سرمایه‌گذاریهای بانکی',
       'وجوه پرداختی بابت تحصیل سرمایه گذاری در پیمان بیع متقابل',
        'جمع جریان خالص قبل از تامین مالی',
       'وجوه حاصل از افزایش سرمایه', 'وجوه پرداختی بابت اوراق مشارکت',
       'باز پرداخت ودایع مشترکین',
       'وجوه دریافتی از سهامداران بابت تامین نقدینگی',
       'وجوه حاصل از افزایش سرمایه شرکتهای فرعی-سهم اقلیت',
       'افزایش(کاهش)در حسابهای شرکاء', 'دریافت تسهیلات مالی',
       'قرض الحسنه دریافتی', 'باز پرداخت قرض الحسنه',
       'وجوه حاصل از انتشار اوراق گواهی سپرده خاص', 'پرداخت مخارج تامین مالی',
       'افزایش حقوق سهامداران اقلیت',
       'وجوه پرداختی بابت تحصیل سهام شرکت اصلی توسط شرکتهای فرعی',
       'باز پرداخت تسهیلات مالی', 'سایر',
       'تغییرات نرخ ارز','مبادلات غیر نقدی']]
    
    df_short = df[['Year','Firm', 'Symbol', 'Fin_year','Operating_cash_flow','Investing_cash_flow',
           'Financing_cash_flow','Begining_cash_position','Change_in_cash','End_cash_position']]


    out = {'data_short':df_short,'data_all':df_all,'columns_dict' :col_name_dict}
    return(out)