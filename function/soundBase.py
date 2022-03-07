import pyaudio
import wave
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
import pandas as pd
from scipy.signal import lfilter


class soundBase: #定义类
    def __init__(self, path):
        self.path = path

    def audiorecorder(self, len=2, formater=pyaudio.paInt16, rate=16000, frames_per_buffer=1024, channels=2):
        #录音操作，录制时间，格式，采样率，缓冲帧数，通道数
       
        p = pyaudio.PyAudio()
        stream = p.open(format=formater, channels=channels, rate=rate, input=True, frames_per_buffer=frames_per_buffer)
        print("start recording......")
        frames = []
        for i in range(0, int(rate / frames_per_buffer * len)):
            data = stream.read(frames_per_buffer)
            frames.append(data)
        print("stop recording......")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(self.path, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(formater))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    def audioplayer(self, frames_per_buffer=1024): #播放语音
       
        wf = wave.open(self.path, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(frames_per_buffer)
        while data != b'':
            stream.write(data)
            data = wf.readframes(frames_per_buffer)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def audiowrite(self, data, fs, binary=True, channel=1, path=[]): #保存语音，语音数据，采样率，是否保存为二进制文件，通道数，文件路径

        if len(path) == 0:
            path = self.path
        if binary:
            wf = wave.open(path, 'wb')
            wf.setframerate(fs)
            wf.setnchannels(channel)
            wf.setsampwidth(2)
            wf.writeframes(b''.join(data))
        else:
            wavfile.write(path, fs, data)

    def audioread(self, return_nbits=False, formater='sample'): #读取文件
     
        fs, data, = wavfile.read(self)
        if formater == 'sample':
            data = data / (2 ** (bits - 1))
        if return_nbits:
            return data, fs, bits
        else:
            return data, fs

    def soundplot(self, data=[], sr=16000, size=(14, 5)):
        """
        将语音数据/或读取语音数据并绘制出来
        2020-2-25   Jie Y.  Init
        :param data: 语音数据
        :param sr: 采样率
        :param size: 绘图窗口大小
        :return:
        """
        if len(data) == 0:
            data, fs, _ = self.audioread()
        plt.figure(figsize=size)
        x = [i / sr for i in range(len(data))]
        plt.plot(x, data)
        plt.xlim([0, len(data) / sr])
        plt.xlabel('s')
        plt.show()

    def sound_add(self, data1, data2):
        """
        将两个信号序列相加，若长短不一，在短的序列后端补零
        :param data1: 序列1
        :param data2: 序列2
        :return:
        """
        if len(data1) < len(data2):
            tmp = np.zeros([len(data2)])
            for i in range(len(data1)):
                tmp[i] += data1[i]
            return tmp + data2
        elif len(data1) > len(data2):
            tmp = np.zeros([len(data1)])
            for i in range(len(data2)):
                tmp[i] += data2[i]
            return tmp + data1
        else:
            return data1 + data2

