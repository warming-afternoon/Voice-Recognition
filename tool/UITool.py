#from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt5.QtCore import QThread,QObject,pyqtSignal

import pyaudio
import time
import wave
import struct
import numpy as np
from scipy import signal
from pylab import *

#录音
class Recorder(QObject):
    signalSaveName=pyqtSignal(str)
    finish=pyqtSignal()
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
        self.saveName=''   #保存文件名 
        self.isTime=False  #是否为实时识别
        self.record_running = False #录音进行
        self._frames = []
        self.fileList= []
        self.thread_save = QThread()
        self.thread_save.started.connect(self.save)

    def set_path(self,path):
        self.path=path
    
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
        
        #录制，直到stop()调用
        while (self.record_running):
            timestamp = time.time()
            struct_time = time.localtime(timestamp)
            date_str = time.strftime("%Y%m%d%H%M%S", struct_time)
            while (time.time() - timestamp < record_seconds and self.record_running):
                time.sleep(0.1)
            self.saveName=self.path+date_str+'.wav'
            self.thread_save.start()
            self.thread_save.exit()
            
        stream.stop_stream()
        stream.close()
        p.terminate()
        self.finish.emit()

    def stop(self):
        self.record_running = False
    
    def save(self):
        slice_wav = self._frames[self.record_start:]
        self.record_start=len(self._frames)-1  #设置保存时读取首址
        wav_data = b"".join(slice_wav)
        with wave.open(self.saveName, "wb") as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(pyaudio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(wav_data)
        self.signalSaveName.emit(self.saveName)
        self.fileList.append(self.saveName)
        
    def callback(self,in_data, frame_count, time_info, status):
        self._frames.append(in_data)
        # output=False时数据可以直接给b""，但是状态位还是要保持paContinue，如果是paComplete一样会停止录制
        return b"", pyaudio.paContinue

class Player(QObject):
    def __init__(self):
        super(Player, self).__init__()
        self.fileName=''   #音频文件名 
        
    def setFileName(self,fileName):
        self.fileName=fileName
        
    def play(self):
        self.wf = wave.open(self.fileName, "rb")
        
        audio = pyaudio.PyAudio()
        stream = audio.open(format=audio.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.wf.getnchannels(),
                        rate=self.wf.getframerate(),
                        output=True,
                        stream_callback=self.callback)

        stream.start_stream()    
        while stream.is_active():
            time.sleep(0.1)

        stream.stop_stream()
        stream.close()
        self.wf.close()

        audio.terminate()

    def callback(self,in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

#演示图生成

class Picture(QObject):
    def __init__(self):
        super(Picture, self).__init__()
        self.fileName=''   #音频文件名 
        self.path='./data/save/' #保存路径 
        self.splitName=''

    def setFileName(self,fileName):
        self.fileName=fileName

    def setPath(self,path):
        self.path=path

    def setSplitName(self,splitName):
        self.splitName=splitName
    
    def generate(self):
        wavefile = wave.open(self.fileName, 'r')
        framerate = wavefile.getframerate()
        numframes = wavefile.getnframes()

        y = np.zeros(numframes)

        for i in range(numframes):
            val = wavefile.readframes(1)
            left = val[0:2]
            v = struct.unpack('h', left)[0]
            y[i] = v

        # 绘制波形图
        plt.figure(figsize=(10, 4))
        plt.plot(y, lw=1)
        plt.title('Waveform of {}'.format(self.fileName))
        plt.xlabel('Sample')
        plt.ylabel('Amplitude')
        plt.grid(True)

        waveform_path = self.path +self.splitName+ '_waveform.png'
        plt.savefig(waveform_path)

        # 计算音频文件的短时傅里叶变换（STFT）
        f, t, Sxx = signal.spectrogram(y, fs=framerate, nperseg=1024, noverlap=900)
        Sxx = 10 * np.log10(Sxx + 1e-4)

        # 绘制频谱图
        plt.figure(figsize=(10, 4))
        plt.pcolormesh(t, f, Sxx, shading='auto')
        plt.title('Spectrogram of {}'.format(self.fileName))
        plt.xlabel('Time')
        plt.ylabel('Frequency')

        spectrogram_path = self.path +self.splitName+ '_spectrogram.png'
        plt.savefig(spectrogram_path)



