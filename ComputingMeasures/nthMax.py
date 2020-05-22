import numpy as np

def nth_max(data,nth=1,interval=False):
    data = data.sort_values(ascending=False)
    if interval:
        return(np.round(data.iloc[min(nth[0]-1,len(data)-1):min(nth[1],len(data))],2))
    else:
        return(np.round(data.iloc[min(nth-1,len(data)-1)],2))