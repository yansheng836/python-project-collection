# coding:utf-8
from PyQt5 import QtGui,QtWidgets,QtCore
import sys
'''
Python学习资料或者需要代码、视频加Python学习群：516107834
''' 
class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
 
    def init_ui(self):
        self.setWindowTitle("Python学习群：516107834") # 设置窗口标题
        self.resize(400,200) # 规定窗口大小
        self.main_widget = QtWidgets.QWidget() # 创建一个widget部件
        self.button = QtWidgets.QPushButton('射门',self.main_widget) # 创建一个按钮
        self.button.setGeometry(10,10,60,30) # 设置按钮位置
        self.button.clicked.connect(self.shoot)
        self.label = QtWidgets.QLabel(self.main_widget) # 创建一个文本标签部件用于显示足球
        self.label.setGeometry(50,80,50,50) # 设置足球位置
        png = QtGui.QPixmap()  # 创建一个绘图类
        png.load("足球.png")  # 从png中加载一个图片
        self.label.setPixmap(png)  # 设置文本标签的图形
        self.label.setScaledContents(True) # 图片随文本部件的大小变动
 
        self.qiumen = QtWidgets.QLabel(self.main_widget)  # 创建一个文本标签部件用于显示球门
        self.qiumen.setGeometry(345, 70, 50, 50)  # 设置球门位置
        pngqiumen = QtGui.QPixmap()  # 创建一个绘图类
        pngqiumen.load("qiumen.png")  # 从png中加载一个图片
        self.qiumen.setPixmap(pngqiumen)  # 设置文本标签的图形
 
        self.setCentralWidget(self.main_widget)
 
    def shoot(self):
        self.anim = QtCore.QPropertyAnimation(self.label,b'geometry') # 设置动画的对象及其属性
        self.anim.setDuration(2000) # 设置动画间隔时间
        self.anim.setStartValue(QtCore.QRect(50,80,50,50)) # 设置动画对象的起始属性
        self.anim.setEndValue(QtCore.QRect(360, 90, 10, 10)) # 设置动画对象的结束属性
        self.anim.start() # 启动动画
 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())