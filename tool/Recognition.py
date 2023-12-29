import librosa
import librosa.display
import numpy as np
from keras.models import load_model

from PyQt5.QtCore import QThread,QObject,pyqtSignal

# 识别
class Recognition(QObject):
    mean_signal_length = 32000
    filename=''
    result = pyqtSignal(bool,str) # 得出结果的信号
    def __init__(self):
        super(Recognition, self).__init__()
        self.model_path = '.\machinelisten_final.h5'  # 模型路径
        self.model = load_model(self.model_path, compile=False)
        
    def setFileName(self,fileName):
        self.fileName=fileName
    
    def recognize(self):
        name=self.fileName
        sample = self.get_feature_vector(name)#特征提取、预处理
        sample = np.expand_dims(sample, axis=0)
        model1 = self.model
        prediction = model1.predict(sample)
        threshold = 0.91  # 来自ROC曲线
        predicted_labels = (prediction[:, 1] > threshold).astype(int)
        if 0 in predicted_labels:
            result=True
        else:
            result=False
        self.result.emit(result,name)
        

    def adjust_array_columns(self,array, target_columns=313):
        while array.shape[1] != target_columns:
            # 获取当前数组的列数
            current_columns = array.shape[1]

            if current_columns < target_columns:
                # 如果列数小于目标列数，多次复制该行的内容，直到列数达到目标列数
                repeated_rows = np.tile(array, (1, target_columns // current_columns + 1))
                array = repeated_rows[:, :target_columns]
            else:
                # 如果列数大于目标列数，截断至目标列数
                array = array[:, :target_columns]

        return array


    # 目前所用特征提取函数
    def get_feature_vector(self,file_path: str):
        audio_data, _ = librosa.load(file_path, sr=None)
        data_mfcc = librosa.feature.mfcc(y=audio_data, sr=22050, n_mfcc=13)
        data_mfcc = self.adjust_array_columns(data_mfcc)
        return data_mfcc




# 载入和预处理数据


# if __name__ == '__main__':
#     model_path = '.\machinelisten_final.h5'  # 模型路径
#     model = load_model(model_path, compile=False)
#     sample = get_feature_vector('./data/anomaly_id_00_00000008.wav')
#     result = model.predict(np.array(sample))
#     threshold = 0.20162924039608465
#     import tensorflow as tf

#     prediction_loss = tf.keras.losses.mae(result, sample)
#     print(prediction_loss)
