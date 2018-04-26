#!/usr/bin/env python3

"""
Created on Wed Mar 28 21:00:07 2018

@author: yifans
"""
 
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QComboBox, QPushButton, QLabel,
                             QSizePolicy, QMessageBox,
                             QHBoxLayout, QVBoxLayout, QAction, qApp, QFileDialog)
from PyQt5.QtCore import pyqtSignal, QObject
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import copy

class Communicate(QObject):
    plot_raw_signal = pyqtSignal()
    plot_smooth_signal = pyqtSignal()

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        # self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
 
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.raw_data = []
        self.smooth_data =[]
        self.section = 0
        self.step = 0
        self.order = 0
        self.deviation = 0
            
        self.initUI() #界面绘制交给InitUi方法
        
        
    def initUI(self):
        #设置窗口的位置和大小
        self.setGeometry(10, 100, 1000, 500)
        
        #设置窗口的标题
        self.setWindowTitle('Magnets Smoothing')
        # canvas 控件
        self.plot_canvas = MyMplCanvas(self)

        # 添加控件
        # section 控件
        section_combo = QComboBox(self)
        section_combo_items = ('5', '6', '7')
        section_combo.activated[str].connect(self.section_action)
        for i in section_combo_items:
            section_combo.addItem(i)
        # step控件
        step_combo = QComboBox(self)
        step_combo_items = ('3', '4', '5')
        step_combo.activated[str].connect(self.step_action)
        for i in step_combo_items:
            step_combo.addItem(i)
        # deviation 控件
        deviation_combo = QComboBox(self)
        deviation_combo_items = ('1', '2', '3')
        deviation_combo.activated[str].connect(self.deviation_action)
        for i in deviation_combo_items:
            deviation_combo.addItem(i)
        order_combo = QComboBox(self)
        order_combo_items = ('3', '4', '5')
        order_combo.activated[str].connect(self.order_action)
        for i in order_combo_items:
            order_combo.addItem(i)
        # smooth 按钮
        smooth_button = QPushButton('SMOOTH')
        smooth_button.clicked.connect(self.smooth_btn_action)
        # 三个label
        section_label = QLabel('Section', self)
        step_label = QLabel('Step', self)
        deviation_label = QLabel('Deviation', self)
        order_label = QLabel('Order', self)
        
        # 全局布局
        wlayout = QVBoxLayout()
        # 局部布局
        hlayout = QHBoxLayout()
        hlayout.addWidget(section_label)
        hlayout.addWidget(section_combo)
        hlayout.addSpacing(100)
        hlayout.addWidget(step_label)
        hlayout.addWidget(step_combo)
        hlayout.addSpacing(100)
        hlayout.addWidget(deviation_label)
        hlayout.addWidget(deviation_combo)
        hlayout.addSpacing(100)
        hlayout.addWidget(order_label)
        hlayout.addWidget(order_combo)
        hlayout.addSpacing(200)
        hlayout.addWidget(smooth_button)
        hwg = QWidget()
        hwg.setLayout(hlayout)
        wlayout.addWidget(hwg)
        wlayout.addWidget(self.plot_canvas)
        # 参考这个文档，不能直接对MainWindow设置布局，https://stackoverflow.com/questions/37304684        
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(wlayout)
        
        # 添加菜单栏
        bar = self.menuBar()
        bar.setNativeMenuBar(False)
        file_menu = bar.addMenu('File')
        # 添加菜单栏事件
        # open action
        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        # save action
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        # exit action
        exit_action = QAction('&Exit', self)        
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)
        # 加入file菜单栏中
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        
        # 设置信号，连接槽函数
        self.c = Communicate()
        self.c.plot_raw_signal.connect(self.plot_raw)
        self.c.plot_smooth_signal.connect(self.plot_smooth)
        
        # 初始化每个下拉列表
        self.section = int(section_combo.currentText())
        self.step = int(step_combo.currentText())
        self.deviation = int(deviation_combo.currentText())
        self.order = int(order_combo.currentText())
        #显示窗口
        self.show()
        
    def section_action(self, val):
        self.section = int(val)
    
    def step_action(self, val):
        self.step = int(val)
    
    def order_action(self, val):
        self.order = int(val)
    
    def deviation_action(self, val):
        self.deviation = int(val)
        
    
    def open_file(self):
        fname, ftype = QFileDialog.getOpenFileName(self, 
                                                  'Open File',
                                                  '.',
                                                  'csv file (*.csv)')
        if fname:
            self.raw_data = np.genfromtxt(fname,delimiter=',')
            self.c.plot_raw_signal.emit()
        # print(self.raw_data)
    
    def save_file(self):
        if self.smooth_data == []:
            QMessageBox.about(self, 'error', 'Please smooth the data')
            return
        fname, ok2 = QFileDialog.getSaveFileName(self,  
                                    "Save File",  
                                    ".",  
                                    "csv file (*.csv)")
        if fname:
            np.savetxt(fname, self.smooth_data, delimiter=',')
        
    
    def smooth_btn_action(self):
        if self.raw_data == []:
            QMessageBox.about(self, 'error', 'Please open the magnet data file')
            return
        self.process_smooth()
        self.c.plot_smooth_signal.emit()
        
    def show_before(self):
        self.plot_edit.setPlainText(str(self.raw_data))
    
    def plot_raw(self):
        p = self.plot_canvas.axes
        p.cla()
        self.plot_canvas.fig.suptitle('Magnet Smoothing')
        p.set_xlabel('location mm')
        p.set_ylabel('position mm')
        l1, = p.plot(self.raw_data[:,0], self.raw_data[:,1],'b.')
        l2, = p.plot(self.raw_data[:,0], self.raw_data[:,2],'r.')
        self.plot_canvas.axes.legend(handles = [l1, l2,], 
                                    labels = ['x raw', 'y raw'])
        self.plot_canvas.draw()
    
    def plot_smooth(self):
        print(self.raw_data)
        print(self.smooth_data)
        changed_point_x = np.empty(shape=[0, 2])
        changed_point_y = np.empty(shape=[0, 2])
        length = len(self.raw_data[:,0])
        for item in range(length):
            if self.raw_data[item,1] != self.smooth_data[item,1]:
                t = np.array([self.raw_data[item,0],self.smooth_data[item, 1] ])
                changed_point_x = np.row_stack((changed_point_x, t))
            if self.raw_data[item,2] != self.smooth_data[item,2]:
                t = np.array([self.raw_data[item,0],self.smooth_data[item, 2] ])
                changed_point_y = np.row_stack((changed_point_y, t))
        print(changed_point_x)
        print(changed_point_y)
            
        p = self.plot_canvas.axes
        p.cla()
        self.plot_canvas.fig.suptitle('Magnet Smoothing')
        p.set_xlabel('location mm')
        p.set_ylabel('position mm')
        l1, = p.plot(self.raw_data[:,0], self.raw_data[:,1],'b.')
        l2, = p.plot(self.raw_data[:,0], self.raw_data[:,2],'r.')
        l3, = p.plot(self.smooth_data[:,0], self.smooth_data[:,1],'g')
        l4, = p.plot(self.smooth_data[:,0], self.smooth_data[:,2],'y')
        l5, = p.plot(changed_point_x[:,0], changed_point_x[:,1],'g*')
        l6, = p.plot(changed_point_y[:,0], changed_point_y[:,1],'y*')
        #l5, = p.plot(changed_point_x[:,0], changed_point_x[:,1],'k*')
        #l6, = p.plot(changed_point_y[:,0], changed_point_y[:,2],'c*')       
        self.plot_canvas.axes.legend(handles = [l1, l2, l3, l4, l5, l6], 
                        labels = ['x raw', 'y raw', 
                                  'x smooth', 'y smooth', 
                                  'changed points x',
                                  'changed points y'])
        
        self.plot_canvas.draw()
    
    def process_smooth(self):
        self.smooth_data = self.smooth_alg(data_src = self.raw_data,
                                           section = self.section,
                                           step = self.step,
                                           deviation = self.deviation,
                                           order = self.order)
    
    def smooth_alg(self, data_src, section, step, deviation, order):
        # 实现smooth的算法，输入data_src为一个np三列矩阵，返回值为smooth后的结果
        result = copy.deepcopy(data_src)
        for i in range(2):
            cursor = 0
            while cursor < len(result):
                r = self.smooth_in_section(data_in_section_x = result[:, 0][cursor: cursor + section],
                                            data_in_section_y = result[:, i + 1][cursor: cursor + section], 
                                            deviation = deviation, 
                                            order = order)
                result[:, i + 1][cursor: cursor + section] = r
                cursor += step
                #print(result[:, i+1])
        return result
    
    def smooth_in_section(self, data_in_section_x, data_in_section_y, deviation, order):
        # return data_in_section + 1 #每个section内，每个元素加1做测试
        # 此处的data_in_section_x, data_in_section_y是一个section内的数据
        # 返回值是一个section内平滑处理之后的y值
        smooth_y = copy.deepcopy(data_in_section_y)
        f = fitting(data_in_section_x, data_in_section_y)
        f.fitting(order)
        for index in range(len(data_in_section_x)):
            if data_in_section_y[index] - f.val[index] > deviation * f.ER2:
                smooth_y[index] = f.val[index] + deviation * f.ER2
            elif f.val[index] - data_in_section_y[index] > deviation * f.ER2:
                smooth_y[index] = f.val[index] - deviation * f.ER2
                    
        # smooth_y = data_in_section_y + 1
        return smooth_y
    
class fitting:  
    
    def __init__(self,X,Y):  
        self.x = np.array(X)  
        self.y = np.array(Y)  
        
    def fitting(self,n):  
        self.z = np.polyfit(self.x,self.y,n)  
        self.p = np.poly1d(self.z)  
        self.val = np.polyval(self.p,self.x)
        self.error = np.abs(self.y - self.val)
        self.ER2 = np.sum(np.power(self.error,2))/len(self.x)  
        return self.z,self.p  
    
    def geterror(self):  
        return self.error,self.ER2
        
              
if __name__ == '__main__':
    #创建应用程序和对象
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_()) 