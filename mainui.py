from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(915, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.camera_button = QtWidgets.QPushButton(self.centralwidget)
        self.camera_button.setGeometry(QtCore.QRect(30, 100, 200, 60))

        self.video_button = QtWidgets.QPushButton(self.centralwidget)
        self.video_button.setGeometry(QtCore.QRect(30, 220, 200, 60))


        self.about_button = QtWidgets.QPushButton(self.centralwidget)
        self.about_button.setGeometry(QtCore.QRect(30, 340, 200, 60))

        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(30, 460, 200, 60))



        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 200, 60))

        self.camera_label = QtWidgets.QLabel(self.centralwidget)
        self.camera_label.setGeometry(QtCore.QRect(250, 100, 640, 480))

        self.score_label = QtWidgets.QLabel(self.centralwidget)
        self.score_label.setGeometry(QtCore.QRect(480, 30, 200, 60))



        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.showMessage("By gorgeousdays")
        MainWindow.setStatusBar(self.statusbar)
       
        self.set_style(MainWindow)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    


    def set_style(self,MainWindow):
        self.camera_button.setStyleSheet('''QPushButton{background:rgb(106,118,200);border-radius:5px;color:white;font-family:AdobeHeitiStd;font-size:25px}
                                        QPushButton:hover{background:rgb(106,118,200);}
                                        QPushButton:pressed{background-color:rgb(106,118,200)}''')
        self.video_button.setStyleSheet('''QPushButton{background:rgb(106,118,200);border-radius:5px;color:white;font-family:AdobeHeitiStd;font-size:25px}
                                        QPushButton:hover{background:rgb(106,118,200);}
                                        QPushButton:pressed{background-color:rgb(106,118,200)}''')
        self.about_button.setStyleSheet('''QPushButton{background:rgb(106,118,200);border-radius:5px;color:white;font-family:AdobeHeitiStd;font-size:25px}
                                        QPushButton:hover{background:rgb(106,118,200);}
                                        QPushButton:pressed{background-color:rgb(106,118,200)}''')
        self.exit_button.setStyleSheet('''QPushButton{background:rgb(106,118,200);border-radius:5px;color:white;font-family:AdobeHeitiStd;font-size:25px}
                                        QPushButton:hover{background:rgb(106,118,200);}
                                        QPushButton:pressed{background-color:rgb(106,118,200)}''')
        
        self.label.setAlignment(Qt.AlignCenter) 
        self.label.setFont(QFont("Century",30,QFont.Bold))
        pe = QPalette()
        pe.setColor(QPalette.WindowText,QColor(139,147, 194, 250))
        self.label.setPalette(pe)

        self.score_label.setFont(QFont("Century",20,QFont.Bold))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sleep Warning"))

        self.camera_button.setText(_translate("MainWindow", "打开相机"))
        self.video_button.setText(_translate("MainWindow", "上传视频"))
        self.about_button.setText(_translate("MainWindow", "关于"))
        self.exit_button.setText(_translate("MainWindow", "退出"))
        
        self.label.setText(_translate("MainWindow", "MENU"))
        self.camera_label.setText(_translate("MainWindow", "请先打开摄像头"))
        self.score_label.setText(_translate("MainWindow", "Points"))

