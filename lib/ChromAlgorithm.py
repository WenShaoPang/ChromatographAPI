import numpy as np
if __name__ == '__main__':
    import sys
    from os import path
    sys.path.append( path.dirname(path.dirname( path.abspath(__file__) ) ))

from lib.Smoother import (
    Moving_average, 
    data_Bunching, 
    Savitzky_Golay_Smooth, 
    pseudo_gaussian_smooth
)
from lib import AirPLS
from lib.peakDetectionAlgorithm import adjustPeaksBoundary, peakSearchAlgorithm
from lib.thresholdCalc import threshold


def SmoothData( 
    method="Savitzky_Golay_Smooth", 
    time=[], 
    signal=[] , 
    window_size=13, 
    *args,
    **kwargs
    ):
    # -----------基本參數初始化------------
    # 把 window size 處理為奇數
    window_size = window_size+1 if window_size%2 == 0 else window_size

    order = kwargs.get('order') if 'order' in kwargs else 3
    mode = kwargs.get('mode') if 'mode' in kwargs else 'nearest'
    sigma = kwargs.get('sigma') if 'sigma' in kwargs else 7
    #---------------------------------------

    if method == "Savitzky_Golay_Smooth":
        '''
        def Savitzky_Golay_Smooth(signal=[], windowsize=5, order=3, mode="nearest"):
            return smoothdata
        '''
        signal = Savitzky_Golay_Smooth( signal, window_size, order, mode )
        return time, signal

    elif method == "Pseudo_Gaussian_Smooth":
        '''
        pseudo_gaussian_smooth(signal=[],sigma=7,mode="nearest")
        return smoothdata
        '''
        signal = pseudo_gaussian_smooth( signal,sigma,mode )
        return time, signal


    elif method == "Moving_average":
        '''
        def Moving_average(Signal=[],windowsize=3):
            return smoothdata
        '''
        signal = Moving_average( signal,window_size )
        return time, signal
    else:
        return time, signal

def Detrand(method="AirPLS",signal=[],*args, **kwargs):
    
    lambda_ = kwargs.get('lambda_') if 'lambda_' in kwargs else 10000
    if method == "AirPLS":
        detrand_data = AirPLS.airPLS( np.array( signal ), lambda_)
    else:
        detrand_data = signal
    return detrand_data

def SmoothDeriv( time=[], signal=[], SmoothMethod='', count=3 ):
    pass