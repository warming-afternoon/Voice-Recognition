import sys
import time
from os import getcwd

from playsound import playsound

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt5.QtCore import QThread,QObject,pyqtSignal

from Test import TimeRecongniton,Recorder,Memento

import process
from keras.models import load_model
import numpy as np

# 主UI
class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.path='./data/save/' #音频保存路径
        self.chooseFile=''  #选中的文件
        self.start = time.time()
        
        self.is_time_recoed = False
        
        self.resourceList=[]
        self.normalResource=[]
        self.abnormalResource=[]
        
        self.rec = Recorder()
        self.thread_one = QThread()
        self.rec.moveToThread(self.thread_one)
        self.thread_one.started.connect(self.rec.record)
        
        # self.timeRecongniton=TimeRecongniton()
        # self.thread_two = QThread()
        # self.timeRecongniton.moveToThread(self.thread_two)
        
        self.setupUi(self)
        self.retranslateUi(self)
        self.slot_init()  # 槽函数设置
        self.model_path = '.\machinelisten_final.h5'  # 模型路径
        self.model = load_model(self.model_path, compile=False)
    
    #设置UI界面外观
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        # MainWindow.setFont(font)
        # MainWindow.setStyleSheet("#MainWindow{background-image: url(./source/3.jpg);}")
        
        # 背景图片
        palette1 =QtGui.QPalette()
        palette1.setBrush(MainWindow.backgroundRole(),QtGui.QBrush(QtGui.QPixmap('./source/1-1.jpg')))
        MainWindow.setPalette(palette1)
        MainWindow.setAutoFillBackground(True)
        
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(500, 10, 280, 60))
        self.label.setText("")
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.label.setObjectName("label")
        # self.label_2 = QtWidgets.QLabel(self.centralwidget)
        # self.label_2.setGeometry(QtCore.QRect(10, 90, 300, 411))
        # self.label_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));")
        # self.label_2.setText("test2")
        # self.label_2.setObjectName("label_2")
        # self.label_3 = QtWidgets.QLabel(self.centralwidget)
        # self.label_3.setGeometry(QtCore.QRect(430, 90, 411, 411))
        # self.label_3.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));")
        # self.label_3.setText("test3")
        # self.label_3.setObjectName("label_3")
        # self.label_4 = QtWidgets.QLabel(self.centralwidget)
        # self.label_4.setGeometry(QtCore.QRect(850, 90, 411, 411))
        # # self.label_4.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));")
        # self.label_4.setText("test4")
        # self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(120, 250, 151, 51))
        self.pushButton.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(560, 250, 151, 51))
        self.pushButton_2.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(1000, 250, 151, 51))
        self.pushButton_3.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 350, 1240, 250))
        self.textBrowser.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.textBrowser.setObjectName("textBrowser")
        font = QtGui.QFont()
        font.setFamily("Arial")  # 括号里可以设置成自己想要的其它字体
        font.setPointSize(16)
        self.textBrowser.setFont(font)

        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(70, 630, 1140, 60))
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
        MainWindow.setWindowTitle(_translate("MainWindow", "机器故障识别"))
        self.label.setText(_translate("MainWindow", "机器故障识别系统"))
        self.pushButton.setText(_translate("MainWindow", "开始录音"))
        self.pushButton_2.setText(_translate("MainWindow", "停止录音"))
        self.pushButton_3.setText(_translate("MainWindow", "实时识别"))
        self.pushButton_4.setText(_translate("MainWindow", "选择音频"))
        self.pushButton_5.setText(_translate("MainWindow", "播放音频"))
        self.pushButton_6.setText(_translate("MainWindow", "识别音频"))
        self.pushButton_7.setText(_translate("MainWindow", "退出"))

    #定义槽函数，即按钮按下后响应函数
    def slot_init(self):
        self.pushButton.clicked.connect(self.time_record)
        self.pushButton_2.clicked.connect(self.stop_record)
        self.pushButton_3.clicked.connect(self.time_recongniton)
        self.pushButton_4.clicked.connect(self.choose_file)
        self.pushButton_5.clicked.connect(self.play_video)
        self.pushButton_6.clicked.connect(self.start_recongniton)
        self.pushButton_7.clicked.connect(self.closeEvent)
    

    #录音
    def record(self):
        self.is_time_recoed = False
        self.rec.set_isTime(self.is_time_recoed)
        self.textBrowser.append('已开始录音')
        self.start = time.time()
        self.rec.set_fileList(self.resourceList)
        self.thread_one.start()

    #实时识别的录音部分
    def time_record(self):
        self.is_time_recoed = True
        self.rec.set_isTime(self.is_time_recoed)
        self.textBrowser.append('已开始录音')
        self.start = time.time()
        self.rec.set_fileList(self.resourceList)
        self.thread_one.start()

    #实时识别的识别部分（未完成）
    def time_recongniton(self):

        self.thread.started.connect(self.timeRecongniton.run) # 通知开始
        self.timeRecongniton.finished.connect(self.thread.quit) # 结束后通知结束
        self.timeRecongniton.finished.connect(self.timeRecongniton.deleteLater) # 完成后删除对象
        self.thread.finished.connect(self.thread.deleteLater) # 完成后删除对象
        self.timeRecongniton.progress.connect(self.result_display) # 绑定 progress 的信号

        self.thread.start()
        # Final resets (结束的时候做的事)
        self.thread.finished.connect(
            lambda: self.textBrowser.append('测试用')
        )
        
        

    ##实时识别结果显示(未完成)
    def result_display(self,result):
        self.textBrowser.append('识别结果：正常\n用时：%.2f' % result)
    
    
    
    
    #停止录音（未完成）
    def stop_record(self):
        stop = time.time()
        self.rec.stop()
        self.resourceList=self.rec.get_fileList()
        
        if (self.is_time_recoed == False):
            self.chooseFile= str(self.resourceList[-1])
            self.textBrowser.append('录音结束，共录制%.1f 秒'% (stop-self.start))
            self.textBrowser.append('文件保存名为'+self.chooseFile)
        else:
            self.textBrowser.append('录音结束，共识别%.1f 秒'% (stop-self.start))

    
    #对音频进行识别
    def start_recongniton(self):
        start = time.time()
        self.textBrowser.append('正在识别中...')
        
        prediction = self.predict()
        
        end = time.time() - start
        threshold = 0.91  # 来自ROC曲线
        predicted_labels = (prediction[:, 1] > threshold).astype(int)
        if 0 in predicted_labels:
            self.textBrowser.append('识别结果：异常！！！请及时处理\n用时：%.2f' % end)
        else:
            self.textBrowser.append('识别结果：正常\n用时：%.2f' % end)

            print(end)
    
    #音频预处理及使用模型预测
    def predict(self):

        sample = process.get_feature_vector(self.chooseFile)#特征提取、预处理
        sample = np.expand_dims(sample, axis=0)
        model1 = self.model
        result = model1.predict(sample)
        return result
        
    #播放音频
    def play_video(self):
        playsound(self.chooseFile)
    
    #选择音频
    def choose_file(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(
            self.centralwidget, "选取图片文件",
            './data',  # 起始路径
            "(*.wav)")  # 文件类型
        self.chooseFile = fileName_choose  

        if fileName_choose != '':
            self.textBrowser.append(fileName_choose + '文件已选中')
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
        


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = Ui_MainWindow()
    ui.show()

    exit(app.exec())
