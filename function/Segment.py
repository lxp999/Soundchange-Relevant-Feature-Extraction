import numpy as np

def GetSegment(express):
    print('express',express)
    if express[0]==0:
        voice = np.where(express) #寻找有话段
    else:
        voice = express
    d_voice = np.where(np.diff(voice) > 1)[0]  #数组后一项减前一项的值用np.diff,这一步处理，将所有SF==1的位置输入d_voice
    #d_voice会比voice少一个长度

    voiceseg = {} #用list来存储话段信息，在后续的参数调用中需要注意，将list提取成数组方便索引
    if len(d_voice) > 0:
        for i in range(len(d_voice)):
            seg={}
            if i == 0: #片段开头
                st = voice[0]  #start
                en = voice[d_voice[i]] #end


            elif i == len(d_voice):#片段末尾
                st = voice[d_voice[i-1]+1]
                en = voice[d_voice[-1]]

            else:#中间片段
                st = voice[d_voice[i-1]+1]
                en = voice[d_voice[i]]

            seg['start'] = st
            seg['end'] = en
            seg['duration'] = en - st + 1
            voiceseg[i] = seg #传递到列表里，voiceseg[0]={}里面包含3个子列

    return voiceseg

