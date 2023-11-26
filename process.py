import librosa
import scipy.io.wavfile as wav
#from speechpy.feature import mfcc
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import glob
from Audiopy_ML import autoaudio
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
import pandas as pd
import os
import tensorflow as tf
from keras.models import load_model
mean_signal_length = 32000



def get_mel(path):
    # sr=None声音保持原采样频率， mono=False声音保持原通道数
    data, fs = librosa.load(path, sr=None, mono=False)
    # 归一化
    data = data * 1.0 / max(data)

    framelength = 0.025
    # NFFT点数=0.025*fs
    framesize = int(framelength * fs)
    # 提取mel特征
    mel_spect = librosa.feature.melspectrogram(data, sr=fs, n_fft=framesize)
    mfc = librosa.feature.mfcc(data, fs, n_mfcc=framesize)
    # 转化为log形式
    mel_spect = librosa.power_to_db(mel_spect, ref=np.max)
    # 画mel谱图
    librosa.display.specshow(mel_spect, sr=fs)
    f = plt.gcf()  # 获取当前图像
    f.savefig('Spectrogram.jpg')
    f.clear()  # 释放内存


def get_feature_vector(file_path: str):
    # audio_dataset_path1 = glob.glob(file_path)
    # df1 = autoaudio.AutomatedExtractor_multiple(audio_dataset_path1)
    # df1 = df1.map(lambda x: np.median(x))
    # x1 = df1.values
    # audio_dataset_path = glob.glob(r"C:\Users\ZhiQ\Desktop\123\Voice-Recognition-main\data\test/*.wav")
    audio_dataset_path = glob.glob(file_path)
    df = autoaudio.AutomatedExtractor_multiple(audio_dataset_path)
    df = df.map(lambda x: np.median(x))
    x = df.values
    # x = np.concatenate((x1,x),axis=0)
    x = np.array(x)
    x2 = np.loadtxt('result1.txt')
    x = np.vstack((x, x2))
    x = Normalizer(norm='l2').fit_transform(x)
    x = StandardScaler().fit_transform(x)
    x = np.expand_dims(x[0], axis=0)
    return x


def get_feature_vector_from_mfcc(file_path: str, flatten: bool,
                                 mfcc_len: int = 7) -> np.ndarray:
    """
    Make feature vector from MFCC for the given wav file.

    Args:
        file_path (str): path to the .wav file that needs to be read.
        flatten (bool) : Boolean indicating whether to flatten mfcc obtained.
        mfcc_len (int): Number of cepestral co efficients to be consider.

    Returns:
        numpy.ndarray: feature vector of the wav file made from mfcc.
    """
    fs, signal = wav.read(file_path)
    plt.plot(signal, color='b')
    f = plt.gcf()  # 获取当前图像
    f.savefig('wave.jpg')
    f.clear()  # 释放内存

    s_len = len(signal)

    if s_len < mean_signal_length:
        pad_len = mean_signal_length - s_len
        pad_rem = pad_len % 2
        pad_len //= 2
        signal = np.pad(signal, (pad_len, pad_len + pad_rem),
                        'constant', constant_values=0)
    else:
        pad_len = s_len - mean_signal_length
        pad_len //= 2
        signal = signal[pad_len:pad_len + mean_signal_length]
    mel_coefficients = mfcc(signal, fs, num_cepstral=mfcc_len)

    fig, ax = plt.subplots()
    img = librosa.display.specshow(mel_coefficients)
    # plt.savefig('MFCC.jpg')
    # plt.show()
    f = plt.gcf()  # 获取当前图像
    f.savefig('MFCC.jpg')
    f.clear()  # 释放内存
    if flatten:
        # Flatten the data
        mel_coefficients = np.ravel(mel_coefficients)
    return mel_coefficients


if __name__ == '__main__':
    # to_flatten = False
    # path = r'E:\code\python\speech_emotion_recognition1\data\angry\angry_1_201.wav'
    # sample = get_feature_vector_from_mfcc(path, flatten=to_flatten)
    # get_mel(path)

        model_path = '.\machinelisten.h5'  # 模型路径
        model = load_model(model_path, compile=False)
        sample = get_feature_vector('./data/anomaly_id_00_00000008.wav')
        result = model.predict(np.array(sample))
        threshold = 0.20162924039608465
        import tensorflow as tf
        prediction_loss = tf.keras.losses.mae(result, sample)
        print(prediction_loss)