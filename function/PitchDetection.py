import numpy as np
from TriangleFilter import triangle
from enframe import enframe
from Segment import GetSegment
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

def pitch_vad(x, wnd, inc, T1, miniL=10):
    """
    基因检测预处理，能熵比端点检测
    :param x: 语音信号
    :param wnd:窗长
    :param inc:
    :param T1: 门限，做判断，大于T1的部分是有效段候选值
    :param miniL:有话段最小长度，默认为10
    :return:
    """
    y = enframe(x, wnd, inc)
    fn = y.shape[0]  #信号的总帧数
    if isinstance(wnd, int):
        wlen = wnd
    else:
        wlen = len(wnd)

    Sp = np.abs(np.fft.fft(y, axis=1)) #取幅值
    Sp = Sp[:, :wlen // 2 + 1] #选取正频率部分
    Esum = np.sum(np.multiply(Sp, Sp), axis=1)
    prob = Sp / np.sum(Sp, axis=1, keepdims=True) #计算概率
    H = -np.sum(np.multiply(prob, np.log10(prob + 1e-16)), axis=1) #求谱熵值
    H = np.where(H < 0.1, np.max(H), H)
    Ef = np.sqrt(1 + np.abs(Esum / H))
    Ef = Ef / np.max(Ef)  #归一化
    zseg = GetSegment(np.where(Ef > T1)[0]) #寻找能量超过阈值的片段
    print(zseg)
    zsl = len(zseg.keys()) #返回目录长度，这里一共3个目录，start，end，duration，所以长度为3
    print('zsl',zsl)
    print('zsl',len(zseg))
    SF = np.zeros(fn)
    for k in range(zsl):
        if zseg[k]['duration'] < miniL:
            zseg.pop(k) #移除小于最小长度的片段
        else:
            SF[zseg[k]['start']:zseg[k]['end']] = 1 #有话段赋值为1，SF=SegmentFrame
    return zseg, len(zseg.keys()), SF, Ef #返回分割片段，vsl，

def pitch_Ceps(x, wnd, inc, T1, fs, miniL=10):
    """
    倒谱法基音周期检测函数
    :param x:
    :param wnd:
    :param inc:
    :param T1:
    :param fs:
    :param miniL:
    :return:
    """
    y = enframe(x, wnd, inc)  #分帧
    fn = y.shape[0]
    if isinstance(wnd, int):
        wlen = wnd
    else:
        wlen = len(wnd)
    voiceseg, vsl, SF, Ef = pitch_vad(x, wnd, inc, T1, miniL)
    lmin = fs // 500  # 基音周期的最小值
    lmax = fs // 60  # 基音周期的最大值，带通滤波器的范围60-500hz
    period = np.zeros(fn)
    print('period')
    y1 = y[np.where(SF == 1)[0], :] #对有话段进行提取
    y1 = np.multiply(y1, np.hamming(wlen)) #加汉明窗

    xx = np.fft.fft(y1, axis=1) #做fft
    b = np.fft.ifft(2 * np.log(np.abs(xx) + 1e-10))
    Lc = np.argmax(b[:, lmin:lmax], axis=1) + lmin - 1 #返回索引值加上基音周期最小值
    period[np.where(SF == 1)[0]] = Lc  #输入有话帧的基音周期
    return voiceseg, vsl, SF, Ef, period


def pitch_Corr(x, wnd, inc, T1, fs, miniL=10):
    """
    倒谱法基音周期检测函数
    :param x:
    :param wnd:
    :param inc:
    :param T1:
    :param fs:
    :param miniL:
    :return:
    """
    y = enframe(x, wnd, inc)
    fn = y.shape[0]
    if isinstance(wnd, int):
        wlen = wnd
    else:
        wlen = len(wnd) #窗长
    voiceseg, vsl, SF, Ef = pitch_vad(x, wnd, inc, T1, miniL) #提取分割后的语音片段，
    lmin = fs // 500  # 基音周期的最小值
    lmax = fs // 60  # 基音周期的最大值
    period = np.zeros(fn)
    print("vsl={}".format(vsl))
    for i in range(vsl):
        ixb=voiceseg[i]['start']
        ixd=voiceseg[i]['duration']
        for k in range(ixd):
            ru = np.correlate(y[k+ixb,:],y[k+ixb,:],'full')
            ru = ru[wlen:]
            tloc = np.argmax(ru[lmin:lmax])
            period[k+ixb]=lmin+tloc
    print('period',period)

    return voiceseg, vsl, SF, Ef, period

def FrameTimeC(framenumber,framelenth,inc,fs): #计算
    x = np.array([i for i in range (framenumber)])
    y = ((x - 1) * inc + framelenth / 2) / fs
    print('y',y)
    print('fn',framenumber)
    return y
def pitch_Lpc(x,wnd,inc,T1,fs,p,miniL=10):
    from scipy.signal import lfilter
    from lpc import lpc_coeff
    y = enframe(x,wnd,inc)
    fn = y.shape[0]
    if isinstance(wnd,int):
        wlen=wnd
    else:
        wlen=len(wnd)
    voiceseg,vsl,SF,Ef = pitch_vad(x, wnd, inc, T1, miniL=10)
    lmin = fs // 500
    lmax = fs // 60
    period = np.zeros(fn)
    print(range(y.shape[0]))
    for k in range(y.shape[0]):
        if SF[k]==1:
            u = np.multiply(y[k,:],np.hamming(wlen))
            ar,_ = lpc_coeff(u,p)
            ar[0]=0
            z = lfilter(-ar,[1], u)
            E = u - z
            xx = np.fft.fft(E)
            b = np.fft.ifft(2*np.log(np.abs(xx)+1e-20))
            lc = np.argmax(b[lmin:lmax])
            period[k]= lc +lmin
    return voiceseg,vsl,SF, Ef, period



if __name__ == '__main__':
    fs, data = wavfile.read('test.wav')
    data = data - np.mean(data) #预处理
    data /= np.max(np.abs(data))
    wlen = 320
    inc = 80
    N= len(data)
    time = [i for i in range(N)]
    T1 = 0.05
    plt.figure(figsize=(14, 8))
    plt.subplot(3, 1, 1)
    plt.plot(time, data)
    p=12
    voiceseg, vsl, SF, Ef, period= pitch_Lpc(data,wlen,inc,T1,fs,p)
    #f0 = fs//period
    #adj = data*triangle(N,fs,f0,period)#三角滤波器乘上原音频进行处理
    #plt.subplot(3,1,2)
    #plt.plot(time,adj)
    #for i in range(vsl):
        #st = voiceseg[i]['start']
        #en = voiceseg[i]['end'] #读取开始和结束的位置，相当于提取片段
        #divide = en-st
        #k = np.zeros(divide)
        #k = period[st:en]
        #print('k',k)
        #均衡滤波器,调用linearfilter实现，其中包含了一个线性滤波器和一个中值滤波器
        #print('P',Period)

    #print(voiceseg[1]['start'])

    fn = len(SF)

    frametime = FrameTimeC(fn,wlen,inc,fs)

    plt.subplot(3, 1, 3)
    plt.plot(frametime,period)
    plt.show()
    print('周期',period)


    #print('频率',fs//period)

