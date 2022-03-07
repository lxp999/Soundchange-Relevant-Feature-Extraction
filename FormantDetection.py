# lpc根植法进行共振峰估计
import numpy as np
import timefeature
from lpc import lpc_coeff


def local_maxium(x):
    """
    求序列的极大值
    :param x:
    :return:
    """
    d = np.diff(x) #后一个元素减去前一个元素，并删除最后一个元素
    l_d = len(d)
    maxium = []
    loc = [] #序列
    for i in range(l_d - 1):
        if d[i] > 0 and d[i + 1] <= 0: #两侧，大于左侧右侧
            maxium.append(x[i + 1])  #将大于两侧的这个值放入maxium中
            loc.append(i + 1)  #返回该数是第几个
    return maxium, loc  #返回序列极大值和序列

def Formant_Cepst(u,cepstL):
    wlen2 = len(u)//2
    U = np.log(np.abs(np.fft.fft(u)[:wlen2]))
    Cepst = np.fft.ifft(U)
    cep = np.zeros(wlen2, dtype=np.complex)
    cep[:cepstL] = Cepst[:cepstL]
    cep[-cepstL + 1:] = Cepst[-cepstL + 1:]
    spec = np.real(np.fft.fft(cep))
    val, loc = local_maxium(spec)
    print(val)
    print(loc)
    print(spec)
    return val, loc, spec

def Formant_Interpolation(u, p, fs):
    """
    插值法估计共振峰函数
    :param u:
    :param p:
    :param fs:
    :return:
    """
    ar, _ = lpc_coeff(u, p)
    U = np.power(np.abs(np.fft.rfft(ar, 2 * 255)), -2)
    df = fs / 512
    val, loc = local_maxium(U)
    ll = len(loc)
    pp = np.zeros(ll)
    F = np.zeros(ll)
    Bw = np.zeros(ll)
    for k in range(ll):
        m = loc[k]
        m1, m2 = m - 1, m + 1
        p = val[k]
        p1, p2 = U[m1], U[m2]
        aa = (p1 + p2) / 2 - p
        bb = (p2 - p1) / 2
        cc = p
        dm = -bb / 2 / aa
        pp[k] = -bb * bb / 4 / aa + cc
        m_new = m + dm
        bf = -np.sqrt(bb * bb - 4 * aa * (cc - pp[k] / 2)) / aa
        F[k] = (m_new - 1) * df
        Bw[k] = bf * df
    return F, Bw, pp, U, loc
