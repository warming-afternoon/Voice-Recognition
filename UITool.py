#from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt5.QtCore import QThread,QObject,pyqtSignal

import pyaudio
import time
from time import sleep
import threading
import wave
import struct
import numpy as np
from scipy import signal
from pylab import *
#import os
#import msvcrt

class Memento:
    resourceList=[]
    normalResource=[]
    abnormalResource=[]
    
    def __init__(self):
        self.resourceList=[]
        self.normalResource=[]
        self.abnormalResource=[]
    
    def setStateFromMemento(self,Memento):
        self.resourceList=Memento.resourceList
        self.normalResource=Memento.normalResource
        self.abnormalResource=Memento.abnormalResource 
    
    def setResourceList(self,resourceList):
        self.resourceList=resourceList
    
    def getResourceList(self):
        return self.resourceList
    
    def getResourceList(self):
        return self.resourceList
    def getnormalResource(self):
        return self.normalResource
    def getabnormalResource(self):
        return self.abnormalResource

# 实时识别
class TimeRecongniton(QObject):
    
    finished = pyqtSignal() # 结束的信号
    progress = pyqtSignal(float)
    _running = True
    def run(self):
        # for i in range(5):
        #     sleep(1)
        #     self.progress.emit(2.5) # 发出表示进度的信号
        
        while (self._running):
            a=1
        
        self.finished.emit() # 发出结束的信号
        

class Recorder(QObject):
    def __init__(self, chunk=1024, channels=1, rate=16000):
        super(Recorder, self).__init__()
        self.CHUNK = chunk  # 每个块包含多少帧
        self.FORMAT = pyaudio.paInt16   # 指定数据类型是int16，也就是一个数据点占2个字节
        self.CHANNELS = channels    # 声道数，1或2
        self.RATE = rate    # 采样率
        
        self.time_record_seconds=10   #实时识别录制时间
        self.common_record_seconds=86400  #普通录制时间
        self.record_start=0
        self.path='./data/save/' #保存路径    
        self.isTime=False  #是实时识别
        self.record_running = False #录音进行
        self._frames = []
        self.fileList= []

    def set_path(self,path):
        self.path=path
        
    def set_fileList(self,fileList):
        self.fileList=fileList
        
    def get_fileList(self):
        return self.fileList
    
    def set_isTime(self,isTime):
        self.isTime=isTime
        
    def record(self):
        self.record_start=0
        self._frames.clear()
        self.record_running = True
        if self.isTime==True:
            record_seconds=self.time_record_seconds
        else:
            record_seconds=self.common_record_seconds
        
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    frames_per_buffer=self.CHUNK,
                    stream_callback=self.callback)
        
        stream.start_stream()
        
        while (self.record_running):
            t1 = time.time()
            saveName=self.path+'{:.0f}'.format(t1)+'.wav'
            self.fileList.append(saveName)
            while (time.time() - t1 < record_seconds and self.record_running):
                time.sleep(0.1)
            
            threading._start_new_thread(self.save(saveName))

        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop(self):
        self.record_running = False
    
    def save(self, filename):
        
        if not filename.endswith(".wav"):
            filename = filename + ".wav"

        slice_wav = self._frames[self.record_start:]
        self.record_start=len(self._frames)-1  #设置保存时读取首址
        wav_data = b"".join(slice_wav)
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(pyaudio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(wav_data)
        self.fileList.append(filename)
        
    def callback(self,in_data, frame_count, time_info, status):
        self._frames.append(in_data)
        # output=False时数据可以直接给b""，但是状态位还是要保持paContinue，如果是paComplete一样会停止录制
        return b"", pyaudio.paContinue

#演示图生成

def Plot_waveform_and_fft_freq_chart(filename, plot=True, save_folder=None):
    wavefile = wave.open(filename, 'r')
    nchannels = wavefile.getnchannels()
    sample_width = wavefile.getsampwidth()
    framerate = wavefile.getframerate()
    numframes = wavefile.getnframes()

    print("channel", nchannels)
    print("sample_width", sample_width)
    print("framerate", framerate)
    print("numframes", numframes)

    y = np.zeros(numframes)

    for i in range(numframes):
        val = wavefile.readframes(1)
        left = val[0:2]
        v = struct.unpack('h', left)[0]
        y[i] = v

    # 绘制波形图
    plt.figure(figsize=(10, 4))
    plt.plot(y, lw=1)
    plt.title('Waveform of {}'.format(filename))
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.grid(True)

    if save_folder:
        waveform_path = save_folder + '/waveform.png'
        plt.savefig(waveform_path)

    # 计算音频文件的短时傅里叶变换（STFT）
    f, t, Sxx = signal.spectrogram(y, fs=framerate, nperseg=1024, noverlap=900)
    Sxx = 10 * np.log10(Sxx + 1e-4)

    # 绘制频谱图
    plt.figure(figsize=(10, 4))
    plt.pcolormesh(t, f, Sxx, shading='auto')
    plt.title('Spectrogram of {}'.format(filename))
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    if save_folder:
        spectrogram_path = save_folder + '/spectrogram.png'
        plt.savefig(spectrogram_path)

    if plot:
        show()

    return np.mean(Sxx)

# # 演示图生成用法示例
# filename1 = "anomaly_id_00_00000044.wav"
# output_folder_path = "E:\photoTest"
# Plot_waveform_and_fft_freq_chart(filename1, False, output_folder_path)


# rec=Recorder

# rec.start