# Voice-Recognition
 
课设代码

## 结构

<<<<<<< Updated upstream
├─speechemotionrecognition
│      dnn.py
│      mlmodel.py
│      utilities.py
│      __init__.py
│
└─test
    │  machinelisten.h5
    │  MFCC.jpg
    │  model.h5
    │  model_1.h5
    │  predict.py
    │  process.py
    │  recorder1.py
    │  recorder_ui.py
    │  source.qrc
    │  Spectrogram.jpg
    │  train.py
    │  ui.py
    │  ui.ui
    │  wave.jpg
    │
    ├─samples
    │      201_angry.wav
    │      201_fear.wav
    │      201_happy.wav
    │      201_neural.wav
    │      201_sad.wav
    │      201_surprise.wav
    │
    ├─source
    │      1.png
    │      QQ图片20220424222950.png
    │
    └─__pycache__
            process.cpython-310.pyc
            recorder1.cpython-310.pyc
=======
├── data                                    //数据集

├── source                                  //UI所用资源

├── tool                                    //工具

│   ├──predict.py                           //使用模型对指定文件夹内文件进行预测，以测试模型性能（未匹配新模型，无用）

├──process.py //对上传语音进行处理，提取特征并使用模型进行识别

├──recorder_ui.py //录音功能的UI，基本已并入主界面，无用

├──recorder1.py //录音功能，仍需修改

├──ui.py //前端UI界面，使用模型对音频进行辨别


>>>>>>> Stashed changes

## 修改提交方式

建议使用[GitHub Desktop](https://desktop.github.com/)进行修改,也可直接使用Git

GitHub Desktop简单使用方法请查看 **[Git 图形工具](https://zhuanlan.zhihu.com/p/506933414)**

更多使用信息请查阅[GitHub Desktop官方文档](https://docs.github.com/zh/desktop/overview/getting-started-with-github-desktop)

修改提交的规范建议参考[约定式提交](https://www.conventionalcommits.org/zh-hans/v1.0.0/)

例如：分支“fix/aaa”  说明“fix:fix aaa”
