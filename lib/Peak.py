if __name__ == '__main__':
    import sys
    from os import path
    sys.path.append( 
        path.dirname(path.dirname( path.abspath(__file__) ) )
        )

class Peak:
    # ------------ Property ------------
    # Peak 邊界 (front x, front y, back x, back y)
    boundary = (0,0,0,0)  
    boundary_index = (-1,-1) # ( front index, back index)
    # Peak 峰值位置 (x,y)
    Apex = (0,0)
    Apex_index = -1
    # Peak 基本參數
    height,tr, width ,area, width = 0,0,0,0, 0
    # peak 的非對稱資訊
    w05,w01,w005,tf,As,N, sigma= 0,0,0,1,1,0,0
    # implied Peak 資訊 ( 三次微分所找的peak )
    co_peak = []
    #-----------------------------------
    def __init__(self):
        pass