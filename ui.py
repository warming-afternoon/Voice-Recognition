import sys
import time
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt5.QtCore import QThread,QObject,pyqtSignal

from tool.UITool import Recorder,Player,Picture
from tool.Recognition import Recognition


# 主UI
class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.path='./data/save/' #音频保存路径
        self.chooseFile=''  #选中文件的路径
        self.fileName='' #选中文件的文件名
        
        self.pathList=[] #路径名列表
        self.nameList=[] #纯文件名（不含路径及后缀）
        self.nameToRow={}
        
        self.pictureType='waveform'
        self.is_time_recoed = False #是实时识别
        self.start = time.time()
        self.stop=self.start
        
        self.icon_right = QtGui.QIcon(QtGui.QPixmap("./source/icon_right.png"))  # 打勾图标的路径
        self.icon_error = QtGui.QIcon(QtGui.QPixmap("./source/icon_error.png"))  # 打叉图标的路径   
        self.icon_question = QtGui.QIcon(QtGui.QPixmap("./source/iconQuestion.png"))  # 问号图标的路径     
        
        #录音
        self.rec = Recorder()
        self.threadRecord = QThread()
        self.rec.moveToThread(self.threadRecord)
        self.threadRecord.started.connect(self.rec.record)
        self.rec.signalSaveName.connect(self.record_save)
        self.rec.finish.connect(self.record_end)
        
        #播放
        self.player=Player()
        self.threadPlay = QThread()
        self.player.moveToThread(self.threadPlay)
        self.threadPlay.started.connect(self.player.play)      
        
        #识别
        self.recognition=Recognition()
        self.threadRecongnize = QThread()
        self.recognition.moveToThread(self.threadRecongnize)
        self.threadRecongnize.started.connect(self.recognition.recognize)
        self.recognition.result.connect(self.recognize_end)

        #生成图片
        self.picture=Picture()
        self.threadPicture = QThread()
        self.picture.moveToThread(self.threadPicture)
        self.threadPicture.started.connect(self.picture.generate)
                
        #主界面设置
        self.setupUi(self)
        self.retranslateUi(self)
        self.slot_init()  # 槽函数设置
    
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
        font.setFamily("Microsoft YaHei") # 设置字体
        font.setPointSize(13)
        # font.setBold(True)
        # font.setWeight(75)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 351, 501))
        self.listWidget.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setFont(font)  
        self.listWidget.setIconSize(QtCore.QSize(25, 25));
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(430, 30, 800, 320))
        # self.label.setText("图片框")
        # self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.label.setObjectName("label")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 540, 140, 65))
        self.pushButton.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setFont(font)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(200, 540, 140, 65))
        self.pushButton_2.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setFont(font)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 630, 140, 65))
        self.pushButton_3.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setFont(font)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(200, 630, 140, 65))
        self.pushButton_4.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setFont(font)
        
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(400, 460, 861, 231))
        self.textBrowser.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.textBrowser.setObjectName("textBrowser")
        
        textFont = QtGui.QFont()
        textFont.setFamily("Arial")  # 设置字体
        textFont.setPointSize(16)
        self.textBrowser.setFont(textFont)

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(460, 380, 151, 61))
        self.pushButton_5.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setFont(font)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(760, 380, 151, 61))
        self.pushButton_6.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setFont(font)
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(1050, 380, 151, 61))
        self.pushButton_7.setStyleSheet("background-color: rgb(207, 242, 252);")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    #设置文本
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "机器故障识别"))
        #self.label.setText(_translate("MainWindow", "图片框"))
        self.pushButton.setText(_translate("MainWindow", "单个选取"))
        self.pushButton_2.setText(_translate("MainWindow", "批量选取"))
        self.pushButton_3.setText(_translate("MainWindow", "录音"))
        self.pushButton_4.setText(_translate("MainWindow", "停止录音"))
        self.pushButton_5.setText(_translate("MainWindow", "图片切换"))
        self.pushButton_6.setText(_translate("MainWindow", "实时识别"))
        self.pushButton_7.setText(_translate("MainWindow", "播放音频"))

    #定义槽函数，即按钮按下后响应函数
    def slot_init(self):
        self.pushButton.clicked.connect(self.single_choose)
        self.pushButton_2.clicked.connect(self.batch_choose)
        self.pushButton_3.clicked.connect(self.record)
        self.pushButton_4.clicked.connect(self.stop_record)
        self.pushButton_5.clicked.connect(self.switch_picture)
        self.pushButton_6.clicked.connect(self.time_record)
        self.pushButton_7.clicked.connect(self.play_video)
        self.listWidget.itemClicked.connect(self.itemClick)
            
    #录音
    def record(self):
        self.is_time_recoed = False
        self.rec.set_isTime(self.is_time_recoed)
        self.textBrowser.append('已开始录音')
        self.start = time.time()
        self.threadRecord.start()
        
    #停止录音
    def stop_record(self):
        self.stop = time.time()
        self.rec.stop()
        
    #录音结束显示
    def record_end(self):
        time.sleep(0.4)
        if (self.is_time_recoed == False):
            self.textBrowser.append('录音结束，共录制%.1f 秒'% (self.stop-self.start))
        else:
            self.textBrowser.append('识别结束，共识别%.1f 秒'% (self.stop-self.start))
        self.threadRecord.exit()

    #录音保存响应
    def record_save(self,saveName):
        if (self.is_time_recoed == False):
            self.textBrowser.append('音频保存为: '+saveName)

        self.process(saveName)
    
    #音频处理
    def process(self,pathName):
        self.chooseFile=pathName
        self.pathList.append(pathName)
        splitName=self.getSplitName(pathName)
        self.nameList.append(splitName)
        self.start_recognize()      #识别
        self.getPicture(splitName)  #产生图片
        self.nameToRow[splitName]=len(self.nameList)-1
        item=QtWidgets.QListWidgetItem(self.icon_question,splitName)
        self.listWidget.addItem(item)
        self.currentItem=item

    #对音频进行识别
    def start_recognize(self):
        if self.chooseFile=='':
            self.textBrowser.append('未选择音频')
        else:        
            self.recognition.setFileName(self.chooseFile)
            self.threadRecongnize.start()
            self.threadRecongnize.exit()
            #self.threadRecongnize.wait()
    
    #识别结果展示(识别结束响应) 
    def recognize_end(self,result,pathName):
        splitName=self.getSplitName(pathName)
        row=self.nameToRow[splitName]
        item=self.listWidget.takeItem(row)
        if result==True:
            item.setIcon(self.icon_error)
            if(self.is_time_recoed == True):
                self.textBrowser.append('检测到异常！！！请及时处理' )
        else:
            item.setIcon(self.icon_right)
            if(self.is_time_recoed == True):
                self.textBrowser.append('运转正常' )
        self.listWidget.insertItem(row,item)

    #实时识别
    def time_record(self):
        self.is_time_recoed = True
        self.rec.set_isTime(self.is_time_recoed)
        self.textBrowser.append('已开始录音')
        self.start = time.time()
        self.threadRecord.start()
        
    #播放音频
    def play_video(self):
        if self.chooseFile=='':
            self.textBrowser.append('未选择音频')
        else:
            self.textBrowser.append('开始播放音频')
            self.player.setFileName(self.chooseFile)
            self.threadPlay.start()
            self.threadPlay.exit()
    
    #选择单个音频
    def single_choose(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(
            self.centralwidget, "选取图片文件",
            './data',  # 起始路径
            "(*.wav)")  # 文件类型

        if fileName_choose != '':
            #self.textBrowser.append(os.path.basename(fileName_choose) + '文件已选中')
            self.process(fileName_choose)
        else:
            self.textBrowser.append('文件未选中')
    
    #批量选择音频
    def batch_choose(self):
        for i in range(6):
            fileName_choose, filetype = QFileDialog.getOpenFileName(
                self.centralwidget, "选取图片文件",
                './data/test',  # 起始路径
                "(*.wav)")  # 文件类型

            if fileName_choose != '':
                #self.textBrowser.append(os.path.basename(fileName_choose) + '文件已选中')
                self.process(fileName_choose)
            else:
                self.textBrowser.append('文件未选中')
            
       
    #生成图片
    def getPicture(self,splitName):
        self.picture.setFileName(self.chooseFile)
        self.picture.setSplitName(splitName)
        self.threadPicture.start()
        self.threadPicture.exit()

    #切换图片
    def switch_picture(self):
        if self.pictureType=='waveform':
            self.pictureType='spectrogram'
        else:
            self.pictureType='waveform'
        self.setPicture()
    
    #设置图片
    def setPicture(self):
        row=self.listWidget.currentRow()
        splitName=self.nameList[row]
        if self.pictureType=='spectrogram':
            pictureName=self.path+splitName+'_spectrogram.png'
            self.label.setScaledContents(True)  # 设置图像自适应界面大小
            self.label.setPixmap (QtGui.QPixmap(pictureName))
        else:
            pictureName=self.path+splitName+'_waveform.png'
            self.label.setScaledContents(True)  # 设置图像自适应界面大小
            self.label.setPixmap (QtGui.QPixmap(pictureName))

    #选项点击响应
    def itemClick(self):
        row=self.listWidget.currentRow()
        self.chooseFile=self.pathList[row]
        self.setPicture()
    
    #获得文件名(不含路径及后缀)
    def getSplitName(self,fileName):
        name=os.path.basename(fileName)
        splitName= os.path.splitext(name)[0]
        return splitName
    
    #关闭UI（需修改）
    def closeEvent(self, event):
        app.quit()
        for root, dirs, files in os.walk(self.path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = Ui_MainWindow()
    ui.show()

    exit(app.exec())
