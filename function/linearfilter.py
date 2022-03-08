import numpy as np
import scipy.signal
from scipy.signal import savgol_filter

def LFilter(x,n):
    window = np.hanning(n)

    window = window / np.sum(window)  #归一化

    lenth = len(x)
    wnl = len(window)
    #print(x[1])
    y = np.zeros(lenth)
    #补充数组长度，保证和窗口函数的正常乘积
    if np.mod(n,2) ==0:#偶数情况
        l = (n//2) #偶数

        #x1 = np.ones(1)*x[0]#创建前向矩阵，用的x[1]的值
        #x2 = np.ones(1) * x[lenth-1]#创建后向序列，用的x[lenth]
        #xm = np.hstack(x1,x) #拼接矩阵补齐长度
        #x = np.hstack(xm,x2) #同上
        x0 = x[0]
        print('xlenth',x[lenth-1])
        xl = x[lenth-1]
        print('x0',x0,'xl',xl)
        x1 = np.hstack(x0,x)
        print(x1)
        x2 = np.hstack(x1,xl)
        print(x2)
        x2 = np.array(x2)

    else:
        l = (n-1)//2 #奇数

        #x1 = np.ones(1) * x[0]
        #x2 = np.ones(1) * x[lenth-1]
        #xm = np.hstack(x1, x)#拼接矩阵
        #x = np.hstack(xm, x2)
        x0 = x[0]

        xl = x[lenth-1]
        print('xlenth',x[lenth-1])
        print('x0', x0, 'xl', xl)
        x1 = np.hstack((x0, x))
        print(x1)
        x2 = np.hstack((x1, xl))
        print(x2)
        #x1 = np.pad(x,((0,0),(1, l)),'constant', constant_value=(x0, xl))
        x3 = []
    for k in range(lenth):
        x3.append(x[k])
        #窗口移动
        y[k]=np.convolve(x2,window)#和窗口乘积计算得到平滑处理后的效果,目前的问题在于，无法用索引索引列表


    #print(x)
    #print(y)
    return x1,y

def medfilter(x):#计算的时候都是以数组进行计算的，需要对列表等参数进行处理成数组运算
    xarray = np.array(x)
    y = scipy.signal.medfilt(xarray,kernel_size=5) #需要注意的是在实际运算时，不够kernel_size的步长会通过自动补0来补齐
    #win = np.array().reshape()#创建一个窗口矩阵
    #设定步长padding =
    #计算窗口内的中值并输出
    return y

def combinedfilter(x,vseg,vsl):#将两个函数合并处理
    y = np.zeros_like(x)
    for i in range(vsl):#提取有话段
        ixs = vseg[i]['start'] #提取开始帧
        ixe = vseg[i]['end']  #提取结束帧
        #提取有话段
        u0 = x[ixs:ixe]
        y0 = medfilter(u0)
        y1 = LFilter(y0,5)
        y[ixs:ixe]=y1

    return y



if __name__ == '__main__':
    A = np.random.randint(2,30,24)
    print('A',A)
    print(np.shape(A.T))
    y = medfilter(A)
    print('y',y)

    array1 = np.array([1,2,3])
    a1 = np.pad(array1,(0,6-len(array1)))
    print('a1',a1)