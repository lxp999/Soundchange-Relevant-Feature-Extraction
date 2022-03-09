# Soundchange-relevant-feature-extraction
## Python处理声音特征相关代码(仅为本人学习目的)

>记录本人在学习变声(voice change; sound change; male to female)处理相关知识中的相关代码训练，包括改写，debug等  
>基本内容与matlab语音信号处理中的差不多，主要用的不是matlab而是python  


>A notebook for myself to learn how to use python to extract audio features.  
Most of the codes are copy from https://github.com/taw19960426/-Speech-signal-processing-experiment-tutorial-_python 

大部分的代码参考自上述链接，本git主要关注变声相关内容，其中的内容在上述连接中未包括
----

>使用的工具为：
```
python version=3.8.8
```
>需要用到的库有：  
  
```
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import pyaudio
from scipy.signal import lfilter
```  

## DSP方法实现变声
男声变换女声的传统dsp方法如下：  
  
  ```
  pitch shift (sharpen the sound) --> formant shift (change the timbre) --> EQ + Reverberation 
  ```
  
>要想实现男声变换成女声，需要着重关注声音特征中的频率 `pitch` 以及共振峰 `formant` ，频率决定着声音的高低，而共振峰决定了声音的音色。  
本人在此之前测试过多款变声调音插件vst `littlealterboy` 、`Mautopitch` 、`clownfish` 、`Rovee` ，这些插件都需要配合声卡使用从而实现实时的变声处理，这其中 `littlealterboy` 的变声效果较好，其次是`Rovee`。  
这两个插件都是基于传统的dsp处理方法实现的变声，并且提供的是简单的 `formant shift`，`pitch shift` 数值调整功能，说明仅依靠dsp方法是能实现比较好的变声效果的。  
  
>目前网上提供的开源变声算法主要集中于简单的变调不变速算法，即通过重采样提升音频的频率 `pitch shift` 从而实现声音变尖锐达到女性声音效果，但往往实际的效果不尽如人意，比较容易呈现出机械声以及小黄人声音类型尖锐的声音。这是因为只改变了频率而没有调整共振峰，音色没有调整所以在听感上效果很差。  
网络上开源的 `formant shift` 算法不能说是一点没有，而是根本查不到，但是有很多共振峰的检测方法，即可以检测出共振峰所处的频率值（包括第1，2，3共振峰）。  
  
关于变调的其中效果比较好的有:    
```
-soundtouch    http://www.surina.net/soundtouch/index.html
``` 
> `soundtouch` 基于c++语言能被很好地编译应用，并且还能很好的实现变调不变速效果，此外调整的程度为半音分，通常通过调整3-4个半音分就能实现有女声听感的声效，美中不足的是没有共振峰相关的调整函数，因此在音色上的调整无法实现。  
>   
关于调整共振峰改变音色：  
>《Matlab语音信号分析与合成》一书中提供了一种基于共振峰频率和线性预测系数之间的关系的方法：  

<p align="center">相关公式</p>

>预测误差滤波器A(z)是一个由预测系数构成的多项式，任何一个共振峰值Fi都与根值zi的相位角有关，所以可以通过调整相位角，可以实现对共振峰的偏移调整（这是目前我能找到的唯一一个用于调整共振峰的方法，其他的都是共振峰的检测，不过在调整共振峰之前也需要进行检测，提取第1，2，3共振峰从而才能进行后续的共振峰偏移调整），在书中该代码是通过matlab实现的，未来的目标是通过python语言实现类似的算法  
>目前function算法里面实现的内容有：  
>* 共振峰检测
>* 基频周期检测
>* 三角增益滤波器
>在function里选择采用类似 `soundlab` 的调整策略，对提取出的共振峰频率与三角增益滤波器进行卷积，保证三角增益滤波器的窗长不超过基音周期，使得不会重叠，验证该方法对音频共振峰的调整效果，以及其是否能实现对音色的改变。  
  
共振峰检测（插值法检测共振峰）：  
<div align="center">
<img src=https://github.com/lxp999/Soundchange-relevant-feature-extraction/blob/main/function/img/formant_with_marks.png width="500" height = "300">
</div>  

> 目前只能检测音素的共振峰，貌似没有什么检测一整句话的共振峰方法，如果对长话段音频进行共振峰检测，会产生共振峰叠加，使得呈现出的数据异常

基音周期检测（LPC法）:  
<div align = "center">
<img src=https://github.com/lxp999/Soundchange-relevant-feature-extraction/blob/main/function/img/pitch_period.png width="500" height="300">  
</div>    

> 未经过平滑处理  

三角增益滤波器:
<div align = "center">
<img src=https://github.com/lxp999/Soundchange-relevant-feature-extraction/blob/main/function/img/TriangleFilter.png width="500" height="300">    
</div>  

> 选择Bw = T/2保证不会overlap
  
通过上面3个相关的算法处理，现在可以对每个音的共振峰进行偏移调整进行音色改变：  
> 将插值法得到的共振峰序列与三角增益滤波器进行乘积（同为频域），从而实现对共振峰的调整（改变极大值点）  
> 在本库里，尝试了两种调整方案：  
> * 提取基频作为共振峰频率进行增益，选取基频整倍数作为第二第三共振峰（原因是基频与共振峰F1差不多，但是目前的文献表示共振峰F1，F2, F3不满足倍数关系，所以对整倍数的基频调整效果肯定有差异，只是做测试，尝试效果）  
> * 提取共振峰频率进行增益  

> 增益处理后的音频将会放在 `demo` 文件夹中。
> 根据调幅增益的处理不同，所呈现出的音频效果也不同。


## 总结  
对于变声处理，传统的dsp方法需要较复杂的处理方式来对音频的频率，共振峰进行调整，并且还需要进行适当的均衡器调整来提升听感。在实际应用情况中，人和人的相同音的共振峰区别较大，不同的音的区别更大，因此要想实现好的变声效果的时候，需要对不同的说话人做个性化的调整，因此需要耗费一定的成本去进行个性化的定制，没有一套泛用性较强的参数。  
     
目前的变声方案里面，利用深度学习进行voice conversion是一个比较热门的方案，比较类似于TTS（Text To Speech），用声音合成的手段去实现听感极佳的变声效果，但是也纯在缺陷，TTS生成的语音往往缺乏情感，虽然在听感上比传统dsp处理方法要强上许多，但是在听起来比较冷漠。  
  
之后会对深度学习相关方案的语音融合内容进行学习，并尝试复现开源的项目效果。目前使用较多的主要是 `GANs` 相关的方法，提取音素然后转换。  









# Ref
1. [语音信号处理实验教程（MATLAB源代码）](https://github.com/bastamon/sound_signal_process-matlab- "语音信号处理实验教程")  
2. [Python实现语音信号处理实验教程](https://github.com/taw19960426/-Speech-signal-processing-experiment-tutorial-_python "Python实现")
3. [SoundLab](https://github.com/matrixcascade/SoundLab "Soundlab")
