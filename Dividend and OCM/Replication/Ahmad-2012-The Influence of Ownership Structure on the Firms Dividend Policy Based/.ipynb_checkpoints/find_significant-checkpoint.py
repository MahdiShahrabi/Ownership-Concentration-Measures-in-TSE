import numpy as np
import pandas as pd

def find_significant(p,val):
    val = np.round(val,3)
    if p>0.1 or pd.isnull(p):
        return(str(val))
    elif p>0.05:
        return(str(val)+'*')
    elif p>0.01:
        return(str(val)+'**')
    else:
        return(str(val)+'***')