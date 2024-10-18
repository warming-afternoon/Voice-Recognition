# Voice-Recognition
 
课设代码，机器运转音频识别

## 功能

* 选择本地音频进行识别
* 录制音频进行识别
* 实时识别（每10s识别一次）


## 结构

├── data                                    //数据集

│   ├──save                                 //运行暂存

├── source                                  //UI所用资源

├── tool                                    //工具

│   ├──UITool.py                            //UI各模块所使用到的类（除了识别）

│   ├──Recognition.py                       //对音频进行识别


├──UI.py //前端UI界面，使用模型对音频进行辨别
