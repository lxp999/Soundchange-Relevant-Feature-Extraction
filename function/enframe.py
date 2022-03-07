import numpy as np

def enframe(x, win, inc=None):
    nx = len(x) #输入序列长度
    if isinstance(win, list) or isinstance(win, np.ndarray):
        nwin = len(win) #窗长
        nlen = nwin  # 帧长=窗长
    elif isinstance(win, int):
        nwin = 1
        nlen = win  # 设置为帧长
    if inc is None: #若窗移未设置，默认为帧长
        inc = nlen
    nf = (nx - nlen + inc) // inc #分的帧
    frameout = np.zeros((nf, nlen)) #创建矩阵
    indf = np.multiply(inc, np.array([i for i in range(nf)]))
    for i in range(nf):
        frameout[i, :] = x[indf[i]:indf[i] + nlen] #分帧运算
    if isinstance(win, list) or isinstance(win, np.ndarray): #判断类型
        frameout = np.multiply(frameout, np.array(win))
    
    return frameout #输出的是数组
