import sys
import time

from playsound import playsound
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from os import getcwd
from PyQt5.QtWidgets import QFileDialog
import process
from keras.models import load_model
import numpy as np
from recorder1 import Recorder
import tensorflow as tf
#未完成，暂时无用
class UiManage():
    uiList = []

# 录音功能UI
class Ui_Dialog(QMainWindow):
    def __init__(self):
        super(Ui_Dialog, self).__init__()

        self.setupUi(self)
        self.retranslateUi(self)
        self.slot_init()  # 槽函数设置

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(497, 246)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 100, 111, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(310, 100, 101, 41))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def slot_init(self):
        print(1)
        self.pushButton.clicked.connect(self.fun)
        self.pushButton_2.clicked.connect(self.fun1)

    def fun(self):
        rec = Recorder()
        rec.positive()

    def fun1(self):
        ui.show()
        ui1.hide()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "开始录音"))
        self.pushButton_2.setText(_translate("Dialog", "退出"))

# 主UI
class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.path = getcwd()
        self.setupUi(self)
        self.retranslateUi(self)
        self.slot_init()  # 槽函数设置

        self.model_path = '.\machinelisten.h5'  # 模型路径
        self.model = load_model(self.model_path, compile=False)
    
    #设置UI界面外观
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 920)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("#MainWindow{background-image: url(./source/1.png);}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(510, 10, 281, 61))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 90, 411, 411))
        # self.label_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(430, 90, 411, 411))
        # self.label_3.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(850, 90, 411, 411))
        # self.label_4.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(120, 530, 151, 51))
        self.pushButton.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(560, 530, 151, 51))
        self.pushButton_2.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(1000, 520, 151, 51))
        self.pushButton_3.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 650, 1241, 131))
        self.textBrowser.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.textBrowser.setObjectName("textBrowser")
        font = QtGui.QFont()
        font.setFamily("Arial")  # 括号里可以设置成自己想要的其它字体
        font.setPointSize(16)
        self.textBrowser.setFont(font)

        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(70, 830, 1141, 61))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.pushButton_4 = QtWidgets.QPushButton(self.splitter)
        self.pushButton_4.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.splitter)
        self.pushButton_5.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.splitter)
        self.pushButton_6.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.splitter)
        self.pushButton_7.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton_7.setObjectName("pushButton_7")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    #设置文本
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "音频识别"))
        self.label.setText(_translate("MainWindow", "机器故障识别系统"))
        self.pushButton.setText(_translate("MainWindow", "显示时域图"))
        self.pushButton_2.setText(_translate("MainWindow", "显示频谱图"))
        self.pushButton_3.setText(_translate("MainWindow", "MFCC特征提取"))
        self.pushButton_4.setText(_translate("MainWindow", "上传音频"))
        self.pushButton_5.setText(_translate("MainWindow", "录制音频"))
        self.pushButton_6.setText(_translate("MainWindow", "播放音频"))
        self.pushButton_7.setText(_translate("MainWindow", "识别语音"))

    #定义槽函数，即按钮按下后响应函数
    def slot_init(self):
        self.pushButton.clicked.connect(self.display_waveform)
        self.pushButton_2.clicked.connect(self.display_feature)
        self.pushButton_3.clicked.connect(self.display_feature1)
        self.pushButton_4.clicked.connect(self.choose_file)
        # self.pushButton_5.clicked.connect(self.play_video)
        self.pushButton_6.clicked.connect(self.play_video)
        self.pushButton_7.clicked.connect(self.start_recongniton)
    
    #展示波形（可能需要删掉）
    def display_waveform(self):
        to_flatten = False
        # process.get_feature_vector_from_mfcc(self.path, flatten=to_flatten)
        # process.get_mel(self.path)
        self.label_2.setScaledContents(True)  # 设置图像自适应界面大小
        self.label_2.setPixmap(QtGui.QPixmap(r'./source/wave.jpg'))
    
    #展示特征（可能需要删掉）
    def display_feature(self):
        self.label_3.setScaledContents(True)  # 设置图像自适应界面大小
        self.label_3.setPixmap(QtGui.QPixmap(r'./source/Spectrogram.jpg'))
    
    #展示特征（可能需要删掉）
    def display_feature1(self):
        self.label_4.setScaledContents(True)  # 设置图像自适应界面大小
        self.label_4.setPixmap(QtGui.QPixmap(r'./source/MFCC.jpg'))

    #对音频进行识别
    def start_recongniton(self):
        self.textBrowser.append('正在识别中...')
        sample = process.get_feature_vector(self.path)
        start = time.time()
        result = self.model.predict(np.array(sample))
        threshold = 0.20162924039608465
        prediction_loss = tf.keras.losses.mae(result, sample)
        end = time.time() - start
        if prediction_loss < threshold:
            self.textBrowser.append('识别结果：异常！！！请及时处理\n用时：%.2f' % end)
        elif prediction_loss >= threshold:
            self.textBrowser.append('识别结果：正常\n用时：%.2f' % end)

            print(end)
    
    #播放音频
    def play_video(self):
        playsound(self.path)
    
    #选择音频
    def choose_file(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(
            self.centralwidget, "选取图片文件",
            './data',  # 起始路径
            "(*.wav)")  # 文件类型
        self.path = fileName_choose  # 保存路径

        if fileName_choose != '':
            self.textBrowser.append(fileName_choose + '文件已选中')

            self.label_2.clear()
            self.label_3.clear()
            self.label_4.clear()
        else:
            self.textBrowser.append('文件未选中')
    #关闭UI（可能需要删掉）
    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cancel = QtWidgets.QPushButton()
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'退出', u'是否退出！')
        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'确定')
        cancel.setText(u'取消')
        # print(type(msg.exec_()))
        if msg.exec_() == 0:
            app.quit()
        else:
            pass


def uifun1(ui, ui1):
    ui.hide()
    ui1.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = Ui_MainWindow()
    ui.show()
    ui1 = Ui_Dialog()
    ui.pushButton_5.clicked.connect(lambda: uifun1(ui, ui1))
    exit(app.exec_())
