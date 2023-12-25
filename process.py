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


# def load_and_preprocess_data(file_paths):
#     data = []
#     for file_path in file_paths:
#         audio_data, _ = librosa.load(file_path, sr=None)
#         data.append(audio_data)
#
#     return data
#


# 目前所用特征提取函数
def get_feature_vector(file_path: str):
    audio_data, _ = librosa.load(file_path, sr=None)

    data_mfcc = librosa.feature.mfcc(y=audio_data, sr=22050, n_mfcc=13)
    return data_mfcc


# # 原mel特征提取函数
# def get_mel(path):
#     # sr=None声音保持原采样频率， mono=False声音保持原通道数
#     data, fs = librosa.load(path, sr=None, mono=False)
#     # 归一化
#     data = data * 1.0 / max(data)

#     framelength = 0.025
#     # NFFT点数=0.025*fs
#     framesize = int(framelength * fs)
#     # 提取mel特征
#     mel_spect = librosa.feature.melspectrogram(data, sr=fs, n_fft=framesize)
#     mfc = librosa.feature.mfcc(data, fs, n_mfcc=framesize)
#     # 转化为log形式
#     mel_spect = librosa.power_to_db(mel_spect, ref=np.max)
#     # 画mel谱图
#     librosa.display.specshow(mel_spect, sr=fs)
#     f = plt.gcf()  # 获取当前图像
#     f.savefig('Spectrogram.jpg')
#     f.clear()  # 释放内存


# 原MFCC特征提取函数
# def get_feature_vector_from_mfcc(file_path: str, flatten: bool,
#                                  mfcc_len: int = 7) -> np.ndarray:
#     """
#     Make feature vector from MFCC for the given wav file.

#     Args:
#         file_path (str): path to the .wav file that needs to be read.
#         flatten (bool) : Boolean indicating whether to flatten mfcc obtained.
#         mfcc_len (int): Number of cepestral co efficients to be consider.

#     Returns:
#         numpy.ndarray: feature vector of the wav file made from mfcc.
#     """
#     fs, signal = wav.read(file_path)
#     plt.plot(signal, color='b')
#     f = plt.gcf()  # 获取当前图像
#     f.savefig('wave.jpg')
#     f.clear()  # 释放内存

#     s_len = len(signal)

#     if s_len < mean_signal_length:
#         pad_len = mean_signal_length - s_len
#         pad_rem = pad_len % 2
#         pad_len //= 2
#         signal = np.pad(signal, (pad_len, pad_len + pad_rem),
#                         'constant', constant_values=0)
#     else:
#         pad_len = s_len - mean_signal_length
#         pad_len //= 2
#         signal = signal[pad_len:pad_len + mean_signal_length]
#     mel_coefficients = mfcc(signal, fs, num_cepstral=mfcc_len)

#     fig, ax = plt.subplots()
#     img = librosa.display.specshow(mel_coefficients)
#     # plt.savefig('MFCC.jpg')
#     # plt.show()
#     f = plt.gcf()  # 获取当前图像
#     f.savefig('MFCC.jpg')
#     f.clear()  # 释放内存
#     if flatten:
#         # Flatten the data
#         mel_coefficients = np.ravel(mel_coefficients)
#     return mel_coefficients


# 载入和预处理数据


if __name__ == '__main__':
    model_path = '.\machinelisten_final.h5'  # 模型路径
    model = load_model(model_path, compile=False)
    sample = get_feature_vector('./data/anomaly_id_00_00000008.wav')
    result = model.predict(np.array(sample))
    threshold = 0.20162924039608465
    import tensorflow as tf

    prediction_loss = tf.keras.losses.mae(result, sample)
    print(prediction_loss)
