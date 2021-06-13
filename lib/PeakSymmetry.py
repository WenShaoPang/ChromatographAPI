if __name__ == '__main__':
    import sys
    from os import path
    sys.path.append( 
        path.dirname(path.dirname( path.abspath(__file__) ) )
        )
from lib.Peak import Peak

def calcPeakSymmetry( time, signal, peak:Peak ):

    # 計算半波峰寬
    targetHeight = ( peak.height - peak.boundary[1] ) *0.5 + peak.boundary[1]
    base_index = peak.boundary_index[0]
    front_index, back_index = PeakTargetHeightIndex( 
        signal[ peak.boundary_index[0] : peak.boundary_index[1] ],
        target = targetHeight,
        start_index = peak.Apex_index - base_index 
        )
    a = time[ base_index + front_index ] 
    b = time[ base_index + back_index ]
    w05 = b - a 
    sigma = w05/2.355
    N = 5.54 * ( peak.tr*peak.tr ) / (w05*w05)

    #-----------------------------

    targetHeight = ( peak.height - peak.boundary[1] ) *0.1 + peak.boundary[1]
    base_index = peak.boundary_index[0]
    front_index, back_index = PeakTargetHeightIndex( 
        signal[ peak.boundary_index[0] : peak.boundary_index[1] ],
        target = targetHeight,
        start_index = peak.Apex_index - base_index 
        )
    a = time[ base_index + front_index ] 
    b = time[ base_index + back_index ]    
    w01 = b - a
    As = ( (b - peak.tr ) / (peak.tr - a)  )

    #------------------------------

    targetHeight = ( peak.height - peak.boundary[1] )*0.05 + peak.boundary[1]
    base_index = peak.boundary_index[0]
    front_index, back_index = PeakTargetHeightIndex( 
        signal[ peak.boundary_index[0] : peak.boundary_index[1] ],
        target = targetHeight,
        start_index = peak.Apex_index - base_index 
        )
    a = time[ base_index + front_index ] 
    b = time[ base_index + back_index ] 
    w005 = b - a

    a_time = peak.tr - a
    b_time = b - peak.tr
    tf = ( a_time + b_time )/(2*a_time)

    peak.w05 = w05
    peak.w01 = w01
    peak.w005 = w005
    peak.sigma = sigma
    peak.N = N
    peak.As = As
    peak.tf = tf
    return peak


def PeakTargetHeightIndex(range_signal=[], target=0, start_index=0):
    # 主要用於搜尋 w05, w01, w005 之位置
    # range_singal 為 一個peak範圍內的儲存訊號資料的 array 
    # 因此 range_signal 的第一筆資料為 peak的起始點, 反之最後一筆為peak的終點
    # start_index 則為 peak 峰值位置的  index , 注意要先扣除 peak起始點的 index
    # target 為要找尋高度目標
    now_index = start_index
    front_index = 0
    back_index = 0

    while range_signal[now_index] > target :
        now_index  -= 1
        if now_index == 0 :
            break
    front_index = now_index

    now_index = start_index
    while range_signal[ now_index ] > target :
        now_index += 1
        if now_index >= len(range_signal)-1 :
            break
    back_index = now_index
    return front_index, back_index