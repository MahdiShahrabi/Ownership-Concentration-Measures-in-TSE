import jdatetime as jd

######################################

def replace_comma(x):
    try:
        out = int(x.replace(',',''))
    except:
        out = x
    return(out)

######################################

def replace_jalalidate(x):
    try:
        out = jd.date(day=int(x[8:10]), month=int(x[5:7]),year=int(x[0:4]))
    except:
        out = x
        
    return(out)

######################################

def find_year(x):
    
    year = x.year
    month = x.month
    
    if month<=6:
        out = year-1
    elif month>6 and month<=12:
        out = year
        
    return(out)