# Soundchange-relevant-feature-extraction
## Python处理声音特征相关代码

记录本人在学习变声处理相关知识中的相关代码训练，包括改写，debug等  
基本内容与matlab语音信号处理中的差不多，主要用的不是matlab而是python  


A notebook for myself to learn how to use python to extract audio features.  
Most of the codes are copy from https://github.com/taw19960426/-Speech-signal-processing-experiment-tutorial-_python 

大部分的代码参考自上述链接，本git主要关注变声相关内容，其中的内容在上述连接中未包括
----

需要用到的库有：  
  
```
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import pyaudio
```  

## DSP方法实现变声
要想实现男声变换成女声，需要着重关注声音特征中的频率 `pitch` 以及共振峰 `formant` ，频率决定着声音的高低，而共振峰决定了声音的音色。  
本人在此之前测试过多款变声调音插件vst`littlealterboy、Mautopitch、clownfish、Rovee`这其中`littlealterboy`的变声效果较好，其次是`Rovee`。  
目前网上提供的开源变声算法主要集中于简单的变调不变速算法，即通过重采样提升音频的频率从而实现声音变尖锐达到女性声音效果，但往往实际的效果不尽如人意，比较容易呈现出机械声以及小黄人声音类型尖锐的声音。

其中效果比较好的有  
```
soundtouch
```


