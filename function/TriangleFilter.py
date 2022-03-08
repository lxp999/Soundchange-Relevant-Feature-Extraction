import numpy as np
import matplotlib.pyplot as plt


def triangle(N,fs,f0,T):
    """

    :param N: 采样数
    :param fs: 采样频率
    :param a: 增益系数
    :param f0: 基频（共振峰频率）
    :param T: 基音周期
    :return:
    """
    df =  fs / N #确定滤波器的帧长
    w2 = int(N / 2 + 1)
    fh = f0 + T//2
    fl = f0 - T//2
    Bw = T
    freq = []
    for i in range(0,w2):
        freqs = int(i*df)
        freq.append(freqs)
    TFbank = np.zeros((w2))
    #print('f',freq)
    n1 = np.floor(fl / df)  # 向下取整
    n2 = np.floor(fh / df)
    n0 = np.floor(f0 / df)
    for i in range(fh):  # 当i在信号的范围内时
        if i >= n1 and i <= n0:  # 当i在三角形左侧范围的时候，滤波器的函数为TFbank=
            TFbank[i] =  (i - n1) / (n0 - n1)
        if i >= n0 and i <= n2:  # 当i在三角形右侧范围的时候，滤波器的函数为TFbank=
            TFbank[i] =  (n2 - i) / (n2 - n0)
    
    return TFbank,w2 #返回滤波器和滤波器的窗长


#if __name__ == '__main__': #测试三角滤波器
    #fs=6000
    #f0=2000
    #a=2
    #T=500
    #triangle(512,fs,a,f0,T)
