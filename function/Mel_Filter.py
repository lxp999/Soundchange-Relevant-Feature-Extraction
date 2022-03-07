import numpy as np
import matplotlib.pyplot as plt
import librosa

def melf(M, N, fs, l, h):
    '''
    M(int)：滤波器个数
    N(int)：FFT点数
    fs(int)：采样频率
    l(float)：低频系数
    h(float)：高频系数
    output:melbank(二维array):mel滤波器
    '''
    fl = fs * l  # 滤波器最低频率
    fh = fs * h  # 滤波器最高频率
    bl = 1125 * np.log(1 + fl / 700)  # 将最低值*1125转换为mel频率
    bh = 1125 * np.log(1 + fh / 700)  # 将最高值*1125转换为mel频率
    Bw = bh - bl  # 频带宽度
    y = np.linspace(0, Bw, M + 2)  #总长度带宽，间隔数为滤波器个数+2,因为一共有M+2个Mel频率值
    # 将mel刻度等间距;
    # np.linspace(start=序列开始,stop=序列停止,num=序列间隔数):创建等间隔序列
    print('mel间隔', y)

    #Fb = librosa.mel_to_hz(y)
    Fb = 700 * (np.exp(y / 1125) - 1)  # 转换mel变为HZ
    print('mel变Hz',Fb)

    w2 = int(N / 2 + 1)
    df = fs / N #采样频率/采样点数
    freq = []  # 采样频率值
    for n in range(0, w2):
        freqs = int(n * df)
        freq.append(freqs)
    melbank = np.zeros((M, w2)) #M行，w2列，每一行即为一个三角mel滤波器，M表示行数，但是实际带参时需要M-1输入
    print('频率',freq)

    for k in range(1, M + 1):
        f1 = Fb[k - 1]  #左侧截止频率 1在实际使用中应该改成基音的周期T/2
        f2 = Fb[k + 1]  #右侧截止频率
        f0 = Fb[k] #中心频率
        #换单位，采样点数
        n1 = np.floor(f1 / df) #向下取整，左侧0点
        n2 = np.floor(f2 / df) #右侧0点
        n0 = np.floor(f0 / df) #顶点位置
        for i in range(1, w2): #当i在信号的范围内时
            if i >= n1 and i <= n0: #当i在三角形左侧范围的时候，滤波器的函数为melbank=
                melbank[k - 1, i] = (i - n1) / (n0 - n1)
            if i >= n0 and i <= n2: #当i在三角形右侧范围的时候，滤波器的函数为melbank=
                melbank[k - 1, i] = (n2 - i) / (n2 - n0)
        plt.plot(freq, melbank[k - 1, :])#出图检查是否是梅尔滤波器组
    plt.show()
    return melbank, w2


#if __name__ == '__main__':  # test the code
    #M=32
    #N=256
    #fs=8000
    #l=0
    #h=fs/2
    #melf(M,N,fs,l,h)
