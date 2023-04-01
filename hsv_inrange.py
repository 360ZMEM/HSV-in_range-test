# 本文件为pyQT的练手实战项目
import cv2
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider
from PyQt5.QtWidgets import QSpinBox, QPushButton, QFileDialog
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap

class MyWindow:
    def __init__(self):
        self.ui = uic.loadUi('interface.ui')
        self.ui.setFixedSize(self.ui.width(), self.ui.height())
        # 变量
        self.filepath = ''
        self.cap = None
        self.cap2 = None
        self.videocount = None
        self.nowframe = 0
        self.hsv = None
        self.res = None  # 结果图像
        self.mask = None
        self.show = None
        self.mode = 0 # 0表示原图模式,1表示掩模模式
        # 链接对象属性和初始化
        self.ui.filebutton.clicked.connect(self.readfile)
        self.ui.lowHsilder.valueChanged.connect(self.lowHchanged)
        self.ui.lowHbox.valueChanged.connect(self.lowHboxchanged)
        self.ui.lowSsilder.valueChanged.connect(self.lowSchanged)
        self.ui.lowSbox.valueChanged.connect(self.lowSboxchanged)
        self.ui.lowVsilder.valueChanged.connect(self.lowVchanged)
        self.ui.lowVbox.valueChanged.connect(self.lowVboxchanged)
        self.ui.upHsilder.valueChanged.connect(self.upHchanged)
        self.ui.upHbox.valueChanged.connect(self.upHboxchanged)
        self.ui.upSsilder.valueChanged.connect(self.upSchanged)
        self.ui.upSbox.valueChanged.connect(self.upSboxchanged)
        self.ui.upVsilder.valueChanged.connect(self.upVchanged)
        self.ui.upVbox.valueChanged.connect(self.upVboxchanged)
        self.ui.mode_change.clicked.connect(self.modechanged)
        self.ui.Bframe.clicked.connect(self.Bframe)
        self.ui.Fframe.clicked.connect(self.Fframe)
        self.ui.playbar.valueChanged.connect(self.playchanged)
        # HSV默认数据
        self.lower = np.array([0, 0, 0])
        self.upper = np.array([179, 255, 255])

    def readfile(self):  # 读取文件
        self.mode = 0
        self.ui.mode_change.setText("显示黑白掩模")
        self.filepath, _ = QFileDialog.getOpenFileName(
            self.ui,
            "请选择图片/视频",
            os.getcwd(),
            "有效媒体类型 (*.png *.jpg *.bmp *.avi *.mp4)"
        )
        if self.filepath == '':
            return
        # 识别文件类型, 按需读取内容
        (_,filename) = os.path.split(self.filepath)
        (_,suffix) = os.path.splitext(filename)
        if suffix.lower() == ".avi" or suffix.lower() == ".mp4":
            self.ui.status_label.setText("您打开了一个视频")
            self.ui.playbar.setEnabled(True)
            self.ui.Bframe.setEnabled(True)
            self.ui.Fframe.setEnabled(True)
            # 展示内容
            self.cap2 = cv2.VideoCapture(self.filepath)
            self.cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
            _,self.cap = self.cap2.read()
            self.hsv = cv2.cvtColor(self.cap,cv2.COLOR_BGR2HSV)
            self.picshow()
            # 初始化进度条
            self.videocount = self.cap2.get(cv2.CAP_PROP_FRAME_COUNT)
            self.ui.playbar.setMinimum(0)
            self.ui.playbar.setMaximum(int(self.videocount - 1))
            self.ui.playbar.setValue(0)
            self.ui.nowframe.setText('1')
            self.ui.allframe.setText(str(int(self.videocount)))
        else:
            self.ui.status_label.setText("您打开了一张图片")
            self.mode = 0
            self.ui.playbar.setEnabled(False)
            self.ui.Bframe.setEnabled(False)
            self.ui.Fframe.setEnabled(False)
            # 读取
            self.cap = cv2.imread(self.filepath)
            # 转化数据
            self.hsv = cv2.cvtColor(self.cap,cv2.COLOR_BGR2HSV)
            # 显示上去
            self.picshow()
    def lowHchanged(self):
        # 根据最大限制
        out = self.ui.lowHsilder.value()
        if(out >= self.upper[0]):
            out = self.upper[0]-1
        self.ui.lowHsilder.setValue(out)
        self.ui.lowHbox.setValue(out)
        self.lower[0] = out
        self.picshow()

    def lowSchanged(self):
        # 根据最大限制
        out = self.ui.lowSsilder.value()
        if (out >= self.upper[1]):
            out = self.upper[1] - 1
        self.ui.lowSsilder.setValue(out)
        self.ui.lowSbox.setValue(out)
        self.lower[1] = out
        self.picshow()

    def lowVchanged(self):
        # 根据最大限制
        out = self.ui.lowVsilder.value()
        if (out >= self.upper[2]):
            out = self.upper[2] - 1
        self.ui.lowVsilder.setValue(out)
        self.ui.lowVbox.setValue(out)
        self.lower[2] = out
        self.picshow()

    def lowHboxchanged(self):
        out = self.ui.lowHbox.value()
        if (out >= self.upper[0]):
            out = self.upper[0] - 1
        self.ui.lowHsilder.setValue(out)
        self.ui.lowHbox.setValue(out)
        self.lower[0] = out
        self.picshow()
        pass

    def lowSboxchanged(self):
        out = self.ui.lowSbox.value()
        if (out >= self.upper[1]):
            out = self.upper[1] - 1
        self.ui.lowSsilder.setValue(out)
        self.ui.lowSbox.setValue(out)
        self.lower[1] = out
        self.picshow()
        pass

    def lowVboxchanged(self):
        out = self.ui.lowVbox.value()
        if (out >= self.upper[2]):
            out = self.upper[2] - 1
        self.ui.lowVsilder.setValue(out)
        self.ui.lowVbox.setValue(out)
        self.lower[2] = out
        self.picshow()
        pass

    def upHchanged(self):
        # 根据最大限制
        out = self.ui.upHsilder.value()
        if(out <= self.lower[0]):
            out = self.lower[0]+1
        self.ui.upHsilder.setValue(out)
        self.ui.upHbox.setValue(out)
        self.upper[0] = out
        self.picshow()

    def upSchanged(self):
        # 根据最大限制
        out = self.ui.upSsilder.value()
        if (out <= self.lower[1]):
            out = self.lower[1] + 1
        self.ui.upSsilder.setValue(out)
        self.ui.upSbox.setValue(out)
        self.upper[1] = out
        self.picshow()

    def upVchanged(self):
        # 根据最大限制
        out = self.ui.upVsilder.value()
        if (out <= self.lower[2]):
            out = self.lower[2] + 1
        self.ui.upVsilder.setValue(out)
        self.ui.upVbox.setValue(out)
        self.upper[2] = out
        self.picshow()

    def upHboxchanged(self):
        out = self.ui.upHbox.value()
        if (out <= self.lower[0]):
            out = self.lower[0] + 1
        self.ui.upHsilder.setValue(out)
        self.ui.upHbox.setValue(out)
        self.upper[0] = out
        self.picshow()
        pass

    def upSboxchanged(self):
        out = self.ui.upSbox.value()
        if (out <= self.lower[1]):
            out = self.lower[1] + 1
        self.ui.upSsilder.setValue(out)
        self.ui.upSbox.setValue(out)
        self.upper[1] = out
        self.picshow()
        pass

    def upVboxchanged(self):
        out = self.ui.upVbox.value()
        if (out <= self.lower[2]):
            out = self.lower[2] + 1
        self.ui.upVsilder.setValue(out)
        self.ui.upVbox.setValue(out)
        self.upper[2] = out
        self.picshow()
        pass


    def modechanged(self):
        if self.mode == 0:
            self.mode = 1
            self.ui.mode_change.setText("显示彩色掩模")
        else:
            self.mode = 0
            self.ui.mode_change.setText("显示黑白掩模")
        self.picshow()

    def playchanged(self):
        out = self.ui.playbar.value()
        self.ui.nowframe.setText(str(int(out+1)))
        self.nowframe = out
        self.cap2.set(cv2.CAP_PROP_POS_FRAMES, out)
        _, self.cap = self.cap2.read()
        self.hsv = cv2.cvtColor(self.cap, cv2.COLOR_BGR2HSV)
        # 显示上去
        self.picshow()

    def Fframe(self):
        out = self.nowframe + 1
        if out >= self.videocount:
            return
        self.ui.nowframe.setText(str(int(out + 1)))
        self.ui.playbar.setValue(out)
        self.cap2.set(cv2.CAP_PROP_POS_FRAMES, out)
        _, self.cap = self.cap2.read()
        self.hsv = cv2.cvtColor(self.cap, cv2.COLOR_BGR2HSV)
        # 显示上去
        self.picshow()

    def Bframe(self):
        out = self.nowframe - 1
        if out <= 0:
            return
        self.ui.nowframe.setText(str(int(out + 1)))
        self.ui.playbar.setValue(out)
        self.cap2.set(cv2.CAP_PROP_POS_FRAMES, out)
        _, self.cap = self.cap2.read()
        self.hsv = cv2.cvtColor(self.cap, cv2.COLOR_BGR2HSV)
        # 显示上去
        self.picshow()

    def picshow(self):
        self.mask = cv2.inRange(self.hsv, lowerb=self.lower, upperb=self.upper)
        self.res = cv2.bitwise_and(self.cap, self.cap, mask=self.mask)

        if self.mode == 0:
            res = self.res
        else:
            res = cv2.cvtColor(self.mask,cv2.COLOR_GRAY2BGR)
        height,width,channel = res.shape
        bytesPerLine = 3 * width
        self.show = QImage(res.data,width,height,bytesPerLine,QImage.Format_RGB888).rgbSwapped()
        # 显示图片
        self.ui.picshowlabel.setPixmap(QPixmap.fromImage(self.show))



app = QApplication([])
mywindow = MyWindow()
mywindow.ui.show()
app.exec_()