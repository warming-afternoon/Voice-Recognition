import time
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QDialog

from recorder1 import Recorder

class Ui_Empty(QMainWindow):
    def __init__(self):
        super(Ui_Empty, self).__init__()
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 920)

# 录音功能UI
class Ui_Dialog(QMainWindow):
    def __init__(self,masterUI):
        super(Ui_Dialog, self).__init__()

        self.setupUi(self)
        self.retranslateUi(self)
        self.slot_init()  # 槽函数设置
        self.start = time.time()
        self.stop = self.start
        self.rec = Recorder()
        self.masterUI=masterUI

    #设置UI外观
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 250)
        #上左按钮
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(80, 60, 100, 40))
        self.pushButton.setObjectName("pushButton")
        #上右按钮
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(310, 60, 100, 40))
        self.pushButton_2.setObjectName("pushButton_2")
        #下按钮
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 150, 100, 40))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    #设置按钮文字
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "录音"))
        self.pushButton.setText(_translate("Dialog", "开始录音"))
        self.pushButton_2.setText(_translate("Dialog", "停止录音"))
        self.pushButton_3.setText(_translate("Dialog", "退出"))
    
    #设定槽函数
    def slot_init(self):
        self.pushButton.clicked.connect(self.record)
        self.pushButton_2.clicked.connect(self.stop_record)
        self.pushButton_3.clicked.connect(self.fun1)

    #录音（未完成）
    def record(self):
        self.start = time.time()
        self.rec.start()
    
    #停止录音（未完成）
    def stop_record(self):
        self.stop = time.time()
        self.rec.stop()
        saveName='./data/save/'+'{:.1f}'.format(self.stop)
        self.rec.save1(saveName)
        self.masterUI
        

    #退出到主界面
    def fun1(self):
        self.masterUI.show()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    empty_ui=Ui_Empty()
    ui = Ui_Dialog(empty_ui)
    ui.show()

    exit(app.exec_())