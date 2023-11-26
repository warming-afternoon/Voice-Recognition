# import os
# import sys
#
# from keras.models import load_model
# from speechemotionrecognition.utilities import get_feature_vector_from_mfcc
# import numpy as np
#
# to_flatten = False
#
# model = load_model('./machinelisten.h5')
# model.summary()
#
# dir = r'../data/'
# name_list = os.listdir(dir)
#
#
#
# for name in name_list:
#     if name.split('.')[-1]=='wav':
#         path = os.path.join(dir,name)
#         sample = get_feature_vector_from_mfcc(path, flatten=to_flatten)
#         sample = np.expand_dims(sample, axis=2)
#
#
#         result = model.predict(np.array([sample]))
#         print(result)
#         print(np.argmax(result))
#
