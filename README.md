# ChromatographAPI
層析圖譜自動積分演算法

## 目錄
* [Overview](#Overview)
* [使用說明](#使用說明)
* [參數調整](#參數調整與設定)


## Overview
![](https://github.com/WenShaoPang/ChromatographAPI/blob/main/pic/overview.png)

## 使用說明
---
- 簡單幾個步驟進行圖譜的前處理, 並進行層析峰的辨識與積分

```python
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
```

- 可以搭配 Pandas 模組儲存與顯示計算結果
```python
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
```
|#|Retention Time|Peak Height|Peak Width|Integral Area|N|Asymmetry|Tail Factor|
|:---:|---:|---:|---:|---:|---:|---:|---:|
|0|18.014252|29.704051|0.38350|1.664753|369533.497421|1.543269|1.307531|
|1|19.572502|33.643070|0.53100|2.252944|317560.837030|1.261194|1.155738|
|2|20.675002|35.067787|0.36725|2.308078|379443.140482|1.314961|1.179310|
|3|22.202002|22.092597|0.34925|1.311811|394026.615683|2.976744|2.072917|

- ChromCanvas 把Matplotlib模組進行再包裝, 使積分計算結果可以簡易呈現

```python
# ----- 針對圖譜進行繪圖 -----
canvas = chromCanvas()
canvas.drawChromatograph(chrom)
#canvas.drawBaseline(chrom)
canvas.drawAllPeaks( chrom.peak_list ) # 標記全部的peak
for peak in chrom.peak_list: 
    canvas.drawSinglePeak( chrom, peak ) # 針對 peak 區域進行繪圖
canvas.show() # 顯示圖譜
```
![](https://github.com/WenShaoPang/ChromatographAPI/blob/main/pic/pic2.png)


## 參數調整與設定
---
Tail Factor 影響
![](https://github.com/WenShaoPang/ChromatographAPI/blob/main/pic/tail_factor.png)

##
