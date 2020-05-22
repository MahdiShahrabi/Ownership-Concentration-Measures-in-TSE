import numpy as np

def gini(data):
    data.sort(reverse = True)
    N = len(data)
    mu = np.mean(data)
    ser = [(i+1)*data[i] for i in range(len(data))]
    try:
        gamma = (N+1)/(N-1)-(2*sum(ser))/(mu*N*(N-1))
    except:
        gamma = 0
    return(gamma)