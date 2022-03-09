import numpy as np
import scipy.signal
from scipy.signal import savgol_filter

def LFilter(x,n):  #线性平滑滤波器，暂时有问题，存在数据类型错误使用函数的问题
    window = np.hanning(n)

    window = window / np.sum(window)  #归一化

    lenth = len(x)
    wnl = len(window)
    #print(x[1])
    y = np.zeros(lenth)
    #补充数组长度，保证和窗口函数的正常乘积，再进行矩阵补充时有点问题，python没有matlab那种简单快速的前后补齐矩阵功能，在使用时测试了np.hstack和np.pad都不能很好的满足要求
    #因为提取的有话段是放在列表里的，在实际提取列表中的元素时容易出现索引错误
    #确保x的矩阵长度满足x[0] x[] x[l]orx[l+1],相当于前补x[0]后补x[l]或者x[l+1]根据奇偶来决定
    if np.mod(n,2) ==0:#偶数情况
        l = (n//2) #偶数

        #x1 = np.ones(1)*x[0]#创建前向矩阵，用的x[0]的值
        #x2 = np.ones(1) * x[lenth-1]#创建后向序列，用的x[lenth-1]的值防止溢出
        #xm = np.hstack(x1,x) #拼接矩阵补齐长度,hstack(a,b)水平方向拼接a,b
        #x = np.hstack(xm,x2) #同上
        x0 = x[0]
        #print('xlenth',x[lenth-1])
        xl = x[lenth-1]
        #print('x0',x0,'xl',xl)
        x1 = np.hstack(x0,x)
        #print(x1)
        x2 = np.hstack(x1,xl)
        #print(x2)
        x2 = np.array(x2)

    else:
        l = (n-1)//2 #奇数

        #x1 = np.ones(1) * x[0]
        #x2 = np.ones(1) * x[lenth-1]
        #xm = np.hstack(x1, x)#拼接矩阵
        #x = np.hstack(xm, x2)
        x0 = x[0]

        xl = x[lenth-1]
        #print('xlenth',x[lenth-1])
        #print('x0', x0, 'xl', xl)
        x1 = np.hstack((x0, x))
        #print(x1)
        x2 = np.hstack((x1, xl))
        #print(x2)
        #x1 = np.pad(x,((0,0),(1, l)),'constant', constant_value=(x0, xl))
        x3 = []
    for k in range(lenth):
        x3.append(x2[k])#将矩阵转换为数组方便后续计算处理
        #窗口移动
        y[k]=np.convolve(x2,window)#和窗口乘积计算得到平滑处理后的效果,目前的问题在于，无法用索引到需要的元素
        
    return x1,y

def medfilter(x):#计算的时候都是以数组进行计算的，需要对列表等参数进行处理成数组运算
    xarray = np.array(x)
    y = scipy.signal.medfilt(xarray,kernel_size=5) #需要注意的是在实际运算时，不够kernel_size的步长会通过自动补0来补齐,步长为1
    #计算窗口内的中值并输出
    return y

def combinedfilter(x,vseg,vsl):#将两个函数合并处理
    y = np.zeros_like(x)#创建存储矩阵
    for i in range(vsl):#提取有话段
        ixs = vseg[i]['start'] #提取开始帧，这里的ixs得到的应该是开始start的值，即为开始的序号
        ixe = vseg[i]['end']  #提取结束帧
        #提取有话段
        u0 = x[ixs:ixe] #选取第一个有话范围
        y0 = medfilter(u0) #先中值滤波器处理
        y1 = LFilter(y0,5) #再进行线性滤波
        y[ixs:ixe]=y1 #存储处理后的数据

    return y



#if __name__ == '__main__':  #测试滤波器是否可用
    #A = np.random.randint(2,30,24)
    #print('A',A)
    #print(np.shape(A.T))
    #y1 = medfilter(A)
    #y2 = LFilter(A,3)
    #print('y1',y1)
    #print('y2',y2)
    #array1 = np.array([1,2,3])
    #a1 = np.pad(array1,(0,6-len(array1)))
    #print('a1',a1)
