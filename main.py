import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
import qdarkstyle
from mainui import *

import pygame
import tensorflow as tf
import cv2


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("resource/warning.png"))

        self.load_parameters()

        self.timer_camera = QtCore.QTimer()

        self.camera_button.clicked.connect(self.opencamera)
        self.video_button.clicked.connect(self.openvideo)
        self.about_button.clicked.connect(self._about)
        self.exit_button.clicked.connect(self._close)
        self.timer_camera.timeout.connect(self.show_camera)
        #可以考虑增加一个设定points阈值的按钮

    def load_parameters(self):
        self.model=tf.keras.models.load_model("models/detect.h5")

        self.face = cv2.CascadeClassifier("HaarCascadeClassifiers/haarcascade_frontalface_alt.xml")
        self.leftEye = cv2.CascadeClassifier("HaarCascadeClassifiers/haarcascade_lefteye_2splits.xml")
        self.rightEye = cv2.CascadeClassifier("HaarCascadeClassifiers/haarcascade_righteye_2splits.xml")

        self.cap = cv2.VideoCapture()
        self.CAMERA_NUM=0

        self.points=0
        self.label=["Closed!","Opened!"]

        self.thick=2

        self.path = os.getcwd()

        music="resource/warning.mp3" 
        pygame.mixer.init()

        pygame.mixer.music.load(music)

        self.first_time_music=1

    def opencamera(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAMERA_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(1)
                self.camera_button.setText(u'关闭相机')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.camera_label.clear()
            self.camera_button.setText(u'打开相机')
    
    def show_camera(self):
        #存在检测不到的情况所以要设初值
        rightPrediction=[[-1]]
        leftPrediction=[[-1]]

        flag, image = self.cap.read()
        image = cv2.resize(image, (640, 480))
        height,width = image.shape[:2]

        faceDetect = self.face.detectMultiScale(image,minNeighbors=5,scaleFactor=1.1,minSize=(25,25))
        rightEyeDetect =  self.rightEye.detectMultiScale(image)
        leftEyeDetect = self.leftEye.detectMultiScale(image)

        for (x,y,w,h) in faceDetect:
            cv2.rectangle(image, (x,y), (x+w,y+h), (100,100,100), 1)

        for (x,y,w,h) in rightEyeDetect:
            rightEyeVal = image[y:y+h,x:x+w]
            rightEyeVal = cv2.cvtColor(rightEyeVal, cv2.COLOR_BGR2GRAY)
            rightEyeVal = cv2.resize(rightEyeVal, (50, 50))
            rightEyeVal= rightEyeVal.reshape(-1, 50, 50, 1)
            rightPrediction = self.model.predict_classes([rightEyeVal])
            #print(rightPrediction[0][0])
            #leftPrediction[0][0]==1 open  ;rightPrediction[0][0]==0 close

        for (x,y,w,h) in leftEyeDetect:
            leftEyeVal = image[y:y+h,x:x+w]
            leftEyeVal = cv2.cvtColor(leftEyeVal, cv2.COLOR_BGR2GRAY)
            leftEyeVal = cv2.resize(leftEyeVal, (50, 50))
            leftEyeVal= leftEyeVal.reshape(-1, 50, 50, 1)
            leftPrediction = self.model.predict_classes([leftEyeVal])
      
        if(rightPrediction[0][0]==0 and leftPrediction[0][0]==0):          
            if self.points!=99:
                self.points+=1    
            cv2.putText(image, "Closed!", (20, height-20), cv2.FONT_HERSHEY_TRIPLEX, 1,(0, 0, 255), 1, cv2.LINE_AA)
        else:
            self.points-=1
            if(self.points<0):
                 self.points=0
            cv2.putText(image, "Opened!", (20, height-20), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        
        self.score_label.setText("Points:"+str(self.points))


        if(self.points>15):
            pe = QPalette()
            pe.setColor(QPalette.WindowText,QColor("red"))
            self.score_label.setPalette(pe)

            if(self.thick<16):
                self.thick+=2
            else:
                self.thick-=2
                if(self.thick<2):
                    self.thick +=2
            cv2.rectangle(image, (0,0), (width, height), (0, 0, 255), self.thick)
          
            if(self.first_time_music==1):
                pygame.mixer.music.play()
                self.first_time_music=0
            
            record_path=os.path.join(self.path,"record",str(time.strftime("%d %b,%Y")))
            if not os.path.exists(record_path):
                os.makedirs(record_path)
            record_img_path=os.path.join(record_path, str(time.strftime("%H-%M-%S")) + ".jpg")
            cv2.imwrite(record_img_path, image)
            
        else:
            self.first_time_music=1
            pygame.mixer.music.stop()

            pe = QPalette()
            pe.setColor(QPalette.WindowText,QColor("black"))
            self.score_label.setPalette(pe)         
        
        img=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        self.camera_label.setPixmap(QtGui.QPixmap.fromImage(showImage))
    

    def openvideo(self):
        #读取视频 功能相同
        pass

    def _about(self):
        QMessageBox.about(self,"Sleep Warning","一个简单的睡觉检测系统")

    def _close(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())