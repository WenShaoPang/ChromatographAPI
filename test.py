if __name__ == '__main__':
    import sys
    from os import path
    sys.path.append( path.dirname(path.dirname( path.abspath(__file__) ) ))

from lib.OpenChromFile import openTXT

# --------  主要使用的模組 -----------------
from lib.ChromAPI import Chromatograph
from lib.ChromCanvas import ChromatographCanvas as chromCanvas
# -----------------------------------------


# ----- 開啟圖譜紀錄檔案 -----
# 依據需求去修改開啟不同的測試圖譜檔案
# 最後彙整成兩筆 list 資料, 分別為 time signal
from os import path
file_path = path.dirname( path.abspath(__file__) ) + "\\test data\\test data.txt"
time, signal = openTXT( file_path )

# ----- 建立圖譜物件 -----
chrom = Chromatograph( time, signal )
# ----- 平滑處理與慮波 -----
chrom.DataBunch(3)
chrom.Smooth( method = 'Savitzky_Golay_Smooth', window_size= 21 )
# 基線會影響積分結果, 建議調整至最佳狀態, lambda_ 越大 fit 效果越佳, 但過大會over fit
chrom.CalcBaseline("AirPLS",lambda_=1000000)
# 圖譜微分, alpha值表示 在二階甚至三階微分時, window size的調整程度
chrom.SmoothDerivative( window_size=101, alpha=1.5)
# ----- 偵測 peak & 積分 -----
# 調整 tail_factor 可以改變 peak 拖尾部分的匡列, "越小"匡列越多, 但"不能負數"
# k 影響找尋 peak 時的 threshold
chrom.PeakDetection(k = 10, tail_factor = 0.1)
# 利用圖譜訊號與積線間的"訊雜比"來過濾 baseline 上的雜訊
chrom.peakHeightFilter(1.2)

# ----- print 積分結果 -----
import pandas as pd
header = [
    "Retention Time","Peak Height", "Peak Width", "Integral Area",
    "N","Asymmetry","Tail Factor"]
data= []
for peak in chrom.peak_list:
    # 取出各peak要print的值
    data.append( 
        [ peak.tr, peak.height, peak.width , peak.area, peak.N, peak.As, peak.tf ] ) 

df = pd.DataFrame(data, columns = header)
print(df)
#---------------------------
# ----- 針對圖譜進行繪圖 -----
canvas = chromCanvas()
canvas.drawChromatograph(chrom)
#canvas.drawBaseline(chrom)
canvas.drawAllPeaks( chrom.peak_list ) # 標記全部的peak
for peak in chrom.peak_list: 
    canvas.drawSinglePeak( chrom, peak ) # 針對 peak 區域進行繪圖
canvas.show() # 顯示圖譜



'''
# ----- 輸出特定區段的 peak 資料 -------
# 取第六根 peak 區段出來並 plot
# 編號從 0 開始
peak = chrom.peak_list[5]

# boundary_index 儲存了peak邊界在整個圖譜資料(list or arrray)的編號位置
front_index = peak.boundary_index[0] # Peak 起始點編號
back_index = peak.boundary_index[1] # Peak 終點編號

time_piece = chrom.time[ front_index: back_index ] # 取出區間時間的資料
signal_piece = chrom.signal[ front_index: back_index ] # 取出區間訊號的資料
baseline_piece = chrom.baseline[ front_index: back_index ] # 取出區間基線的資料

import matplotlib.pyplot as plt
plt.figure()
plt.plot(time_piece, signal_piece)
plt.plot(time_piece, baseline_piece)
plt.show()
'''