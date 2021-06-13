import numpy as np
if __name__ == '__main__':
    import sys
    from os import path
    sys.path.append( path.dirname(path.dirname( path.abspath(__file__) ) ))
from lib.ChromAPI import Chromatograph, Peak
import matplotlib.pyplot as plt

class ChromatographCanvas:
    def __init__(self):
        plt.figure()
    def show(self):
        plt.show()

    def drawChromatograph(self, chrom:Chromatograph):
        plt.plot( chrom.time, chrom.signal )

    def drawBaseline( self, chrom:Chromatograph ):
        plt.plot( chrom.time, chrom.baseline, color='red' )

    def drawAllPeaks(self, peak_list:list):
        peak_list_time, peak_list_signal = [], []
        for peak in peak_list:
            peak_list_time.append( peak.Apex[0] )
            peak_list_signal.append( peak.Apex[1] )
        plt.plot(peak_list_time, peak_list_signal, 'ro')

    def drawSinglePeak( self, chrom:Chromatograph, peak:Peak ):
        front, back = peak.boundary_index[0], peak.boundary_index[1]
        signal, baseline = [], []
        for i in range( front, back, 1 ):
            signal.append( chrom.signal[i] )
            baseline.append( min( chrom.signal[i], chrom.baseline[i] ) )  

        plt.fill_between( 
            np.array( chrom.time[ front:back ] ),
            np.array( baseline ),
            np.array( signal ) ,
            color='lightsalmon'
            )
