import numpy as np
from scipy.signal import savgol_filter
if __name__ == '__main__':
    import sys
    from os import path
    sys.path.append( path.dirname(path.dirname( path.abspath(__file__) ) ))


from lib.OpenChromFile import FileOpenClass
from lib.Smoother import Moving_average, data_Bunching
from lib import AirPLS
from lib.peakDetectionAlgorithm import adjustPeaksBoundary, peakSearchAlgorithm
from lib.thresholdCalc import threshold

from lib.ChromAlgorithm import SmoothData, Detrand, data_Bunching
from lib.Peak import Peak
from lib.PeakSymmetry import calcPeakSymmetry

'''
class Peak:
    # ------------ Property ------------
    # Peak 邊界 (front x, front y, back x, back y)
    boundary = (0,0,0,0)  
    boundary_index = (-1,-1) # ( front index, back index)
    # Peak 峰值位置 (x,y)
    Apex = (0,0)
    Apex_index = -1
    # Peak 基本參數
    height,tr, width ,area = 0,0,0,0
    # peak 的非對稱資訊
    w05,w01,w005,tf,As,N, sigma= 0,0,0,1,1,0,0
    # implied Peak 資訊 ( 三次微分所找的peak )
    co_peak = []
    #-----------------------------------
    def __init__(self):
        pass
'''
class Chromatograph:
    # ------------ Property ------------
    time=[]
    signal=[]
    baseline=[]
    # 微分圖譜, 分別為一次微分, 二次微分, 三次微分
    dydx=[]
    dydx2=[]
    dydx3=[]
    # 儲存 Peaks 的容器 , 為 list(Class Peak)
    peak_list=[]
    # -----------------------------------

    def __init__(self, time=[], signal=[]):
        self.time = time
        self.signal = signal

    def DataBunch(self, bunching_point=3):
        self.time, self.signal = data_Bunching( self.time, self.signal, bunching_point )

    def CalcBaseline(self, method="AirPLS", *args, **kwargs):
        lambda_ = kwargs.get('lambda_') if 'lambda_' in kwargs else 10000
        self.baseline = Detrand( method, self.signal, lambda_= lambda_ )

    def Smooth( self, method='Savitzky_Golay_Smooth', window_size=13 , *args, **kwargs ):
        order = kwargs.get('order') if 'order' in kwargs else 3
        mode = kwargs.get('mode') if 'mode' in kwargs else 'nearest'
        sigma = kwargs.get('sigma') if 'sigma' in kwargs else 7

        self.time, self.signal = SmoothData( 
            method, 
            self.time, 
            self.signal, 
            window_size, 
            order=order, 
            mode= mode, 
            sigma=sigma 
        )

    def SmoothDerivative( self, window_size=21, alpha=1.5):
        # ------ 把 window size 處理為奇數 ------
        window_size = window_size+1 if window_size%2 == 0 else window_size
        # ------ ------ ------ ------ ----- -----
        dx = self.time[1] - self.time[0]

        self.dydx = savgol_filter( 
            self.signal, window_length=window_size, polyorder=2, deriv=1, delta=dx
          )  # 一次微分
        self.dydx2 = savgol_filter( 
            self.signal, window_length=int(window_size*alpha), polyorder=2, deriv=2, delta=dx 
            ) # 二次微分
        self.dydx3 = savgol_filter( 
            self.signal, window_length=int(window_size*alpha*alpha), polyorder=3, deriv=3, delta=dx 
            ) # 三次微分 

    def PeakDetection(self, k = 10, tail_factor = 0.3, MIN_PEAK_INTERVAL=0.5 ):
        dydx_threshold = threshold(self.dydx.copy(), k)
        dydx2_threshold = threshold(self.dydx2.copy(), k)
        #///////////////////////////////////////////////////////////////////////
        peak_index_list = peakSearchAlgorithm( 
            [self.time,self.signal], 
            [self.dydx,self.dydx2,self.dydx3],
            dydx_threshold[1],
            dydx_threshold[0] * tail_factor,
            dydx2_threshold[0],
            offset=10,
            MAX_TIME_WIDTH=0.5 
            )

        # peak_index_list : list  , 2D-array
        # array( [ start index, highest index, end index, apex index ] )
        # index 為 time array 或 signal array的編號
        # start index : peak 起始點的 index
        # highest index : peak 最高點的 index
        # end index : peak 終點的 index
        # apex index : 峰值位置的 index, 為 list, 為利用三次微分圖譜所找到的 peak
        #   為單一peak時, len(apex index)=1且應為 apex index[0] == highest index
        #   若有高度共析狀況發生, 圖譜與一次微分無發區分該共析peaks, 
        #   此時 len(apex index) > 1, 其 list內容則是共析peak的apex位置
        #///////////////////////////////////////////////////////////////////////

        boundary_table = adjustPeaksBoundary(
            self.time, self.signal, peak_index_list, self.baseline,
            MIN_PEAK_INTERVAL
            )
        self.__build_peak_list( peak_index_list, boundary_table )

        #-----------------------

        temp = []
        for p in self.peak_list:
            temp.append( 
                calcPeakSymmetry(self.time, self.signal, p) 
                )
        self.peak_list = temp.copy()
        
        #------------------------

    def __build_peak_list(self, peak_index_list, boundary_table):
        self.peak_list = []
        for i in range( len(peak_index_list) ):
            peak = Peak()
            peak.boundary_index = ( 
                peak_index_list[i][0], peak_index_list[i][2]
                )
            peak.boundary= ( boundary_table[i] )
            peak.Apex = (
                self.time[ peak_index_list[i][1]], self.signal[ peak_index_list[i][1] ]
                )
            peak.Apex_index = peak_index_list[i][1]

            peak.height = peak.Apex[1]
            peak.tr = peak.Apex[0]
            peak.width = peak.boundary[2] - peak.boundary[0]
            # ----- 計算積分 -----
            area = np.trapz(
                self.signal[ peak.boundary_index[0]: peak.boundary_index[1] ], 
                self.time[ peak.boundary_index[0]: peak.boundary_index[1] ]
                )

            # ----- 計算基線 -----
            # 因為計算出來的 baseline可能會大於原始訊號, 這會造成積分值會比預期低
            # 因此多一到工序  min( signal, baseline ), 保證積分時的基線必 <= signal
            base = []
            for i in range( peak.boundary_index[0], peak.boundary_index[1], 1 ):
                base.append( min( self.signal[i], self.baseline[i] ) )

            base_area = np.trapz( 
                base ,
                self.time[ peak.boundary_index[0]: peak.boundary_index[1] ]
                )
            peak.area = area - base_area

            # ------ ------ ------ ------
            peak.co_peak = peak_index_list[ 3 ]

            # ----- 寫入資料 -----
            self.peak_list.append( peak )
            # ------ ------ ------ ------

    def peakHeightFilter( self, SN_rate=3.0 ):
        # 利用 peak height 過濾"已找尋到"的 peaks
        new_peak_list = []
        for peak in self.peak_list:
            if (peak.height / self.baseline[ peak.Apex_index ] ) >= SN_rate :
                new_peak_list.append( peak ) 
        self.peak_list = new_peak_list
