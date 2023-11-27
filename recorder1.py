import pyaudio
import time
import threading
import wave
import os
import msvcrt


class Recorder():
    def __init__(self, chunk=1024, channels=1, rate=16000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []

    def start(self):
        threading._start_new_thread(self.__recording, ())

    def __recording(self):
        self._running = True
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        while (self._running):
            data = stream.read(self.CHUNK)
            self._frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop(self):
        self._running = False

    def save1(self, filename):
        p = pyaudio.PyAudio()

        if not filename.endswith(".wav"):
            filename = filename + ".wav"

        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()

    def save2(self, filename):
        p = pyaudio.PyAudio()
        if not filename.endswith(".wav"):
            filename = filename + ".wav"
        path = self.negative_path()
        filename = path + r'//' + filename
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()
        print("Saved")

    def positive_path(self):

        cur_dir = os.getcwd()
        newpath = 'positive'
        cur_dir = cur_dir + '\\' + newpath
        if os.path.exists(cur_dir):
            pass
        else:
            os.mkdir(cur_dir)
        return cur_dir

    def negative_path(self):

        cur_dir = os.getcwd()
        newpath = 'negative'
        cur_dir = cur_dir + '\\' + newpath
        if os.path.exists(cur_dir):
            pass
        else:
            os.mkdir(cur_dir)
        return cur_dir


    def record_old(self):
        print('请按下回车键开始录音：')
        a = msvcrt.getche()
        a = ord(a)
        if a == 13:
            begin = time.time()
            print("Start recording")
            self.start()
            print('请按下回车键结束录音：')
            b = msvcrt.getch()
            b = ord(b)
            if b == 13:
                print("Stop recording")
                self.stop()
                fina = time.time()
                t = fina - begin
                print('录音时间为%ds' % t)

    def positive(self):
        count = 0
        i = 2
        print('开始录制')

        self.record_old()
        self.save1("1_1.wav")
        # for i in range(2,m+count+1):
        while i < (1 + count + 1):
            print('继续录音请按下回车键，重新录音请输入y or Y：')
            input_YN = msvcrt.getch()
            input_YN = bytes.decode(input_YN)
            if input_YN.upper() == 'Y':
                count += 1
                self.record_old()
                self.save1("1_%d.wav" % (i - count))
                i += 1
            else:
                self.record_old()
                self.save1("1_%d.wav" % (i - count))
                i += 1

    def negative(self):
        count = 0
        i = 2
        n = self.negative_n()
        print('开始负样本的录制')
        print("请以不同的语速口音朗读文章")
        self.record_old()
        self.save2("0_1.wav")
        while i < (n + count + 1):
            print('继续录音请按下回车键，重新录音请输入y or Y：')
            input_YN = msvcrt.getch()
            input_YN = bytes.decode(input_YN)
            if input_YN.upper() == 'Y':
                count += 1
                self.record_old()
                self.save2("0_%d.wav" % (i - count))
                i += 1
            else:
                self.record_old()
                self.save2("0_%d.wav" % (i - count))
                i += 1

    def positive_m(self):
        m = int(input('请设置录制正样本数：'))
        return m

    def negative_n(self):
        n = int(input('请设置录制负样本数：'))
        return n


if __name__ == "__main__":
    rec = Recorder()
    rec.positive()
