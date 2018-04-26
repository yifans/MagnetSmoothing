#!/usr/bin/env python3

"""
Created on Wed Mar 28 21:00:07 2018

@author: Yifan Song
@email: yifans@mail.ustc.edu.cn
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication,QWidget,QVBoxLayout,
                             QComboBox,QHBoxLayout,QLabel,QPushButton,QAction,
                             qApp,QFileDialog,QMessageBox)
from PyQt5.QtCore import pyqtSignal,QObject
from myMplCanvas import PlotAll, PlotSection
import numpy as np

class Communicate(QObject):
    plot_raw_signal = pyqtSignal()
    plot_smooth_signal = pyqtSignal()
    plot_end_signal = pyqtSignal()

    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 原始数据
        self.locations = []
        self.raw_data_x = []
        self.raw_data_y = []
        # smooth后的数据
        self.smooth_data_x = []
        self.smooth_data_y = []
        # smooth的配置信息
        self.section_confg = 0
        self.step_config = 0
        self.order_config = 0
        self.deviation_config = 0

        self.initUI()
        self.setMenuBar()
        self.update_config()
        self.init_slot()

    def initUI(self):
        # 设置窗口的位置和大小
        self.setGeometry(0, 0, 1000, 700)

        # 设置窗口的标题
        self.setWindowTitle('Magnets Smoothing')
        # 建立窗口中的所有部件
        # 下拉菜单
        self.section = QComboBox()
        self.section.addItems(('5', '6', '7'))
        self.step = QComboBox()
        self.step.addItems(('3', '4', '5'))
        self.deviation = QComboBox()
        self.deviation.addItems(('1', '2', '3'))
        self.order = QComboBox()
        self.order.addItems(('3', '4', '5'))
        # labels
        self.section_label = QLabel('Section')
        self.step_label = QLabel('Step')
        self.deviation_label = QLabel('Deviation')
        self.order_label = QLabel('Order')
        # button
        self.step_smooth = QPushButton('STEP SMOOTH')
        self.smooth = QPushButton('SMOOTH')
        # plot
        self.plot_all_x = PlotAll()
        self.plot_all_y = PlotAll()
        self.plot_section_x = PlotSection()
        self.plot_section_y = PlotSection()

        # 全局布局
        wlayout = QVBoxLayout()
        # 局部布局
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.section_label)
        hlayout.addWidget(self.section)
        hlayout.addSpacing(100)
        hlayout.addWidget(self.step_label)
        hlayout.addWidget(self.step)
        hlayout.addSpacing(100)
        hlayout.addWidget(self.deviation_label)
        hlayout.addWidget(self.deviation)
        hlayout.addSpacing(100)
        hlayout.addWidget(self.order_label)
        hlayout.addWidget(self.order)
        hlayout.addSpacing(200)
        hlayout.addWidget(self.smooth)
        hlayout.addWidget(self.step_smooth)
        hwg = QWidget()
        hwg.setLayout(hlayout)
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(self.plot_all_x)
        hlayout2.addWidget(self.plot_all_y)
        hwg2 = QWidget()
        hwg2.setLayout(hlayout2)
        hlayout3 = QHBoxLayout()
        hlayout3.addWidget(self.plot_section_x)
        hlayout3.addWidget(self.plot_section_y)
        hwg3 = QWidget()
        hwg3.setLayout(hlayout3)
        
        wlayout.addWidget(hwg)
        wlayout.addWidget(hwg2)
        wlayout.addWidget(hwg3)
        # wlayout.addWidget(self.section_canvas)
        # 参考这个文档，不能直接对MainWindow设置布局，https://stackoverflow.com/questions/37304684        
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(wlayout)
        self.show()
    
    def setMenuBar(self):
        # 添加菜单栏
        self.bar = self.menuBar()
        self.bar.setNativeMenuBar(False)
        self.file_menu = self.bar.addMenu('File')
        # 添加菜单栏事件
        # open action
        self.open_action = QAction('Open', self)
        self.open_action.setShortcut('Ctrl+O')
        # save action
        self.save_action = QAction('Save', self)
        self.save_action.setShortcut('Ctrl+S')
        # exit action
        self.exit_action = QAction('&Exit', self)        
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip('Exit application')
        # 加入file菜单栏中
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.exit_action)
    
    def update_config(self):
        self.section_config = int(self.section.currentText())
        self.step_config = int(self.step.currentText())
        self.deviation_config = int(self.deviation.currentText())
        self.order_config = int(self.order.currentText())
        print(self.section_config,self.step_config,self.deviation_config,self.order_config)
        
    def init_slot(self):
        #
        self.order.activated.connect(self.update_config)
        self.step.activated.connect(self.update_config)
        self.deviation.activated.connect(self.update_config)
        self.section.activated.connect(self.update_config)
        #
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.exit_action.triggered.connect(qApp.quit)
        #
        self.step_smooth.clicked.connect(self.step_smooth_action)
        self.smooth.clicked.connect(self.smooth_action)
        #
        self.c = Communicate()   
        self.c.plot_raw_signal.connect(self.plot_raw)
        self.c.plot_smooth_signal.connect(self.plot_smooth)
        self.c.plot_end_signal.connect(self.plot_end)
    
    def open_file(self):
        fname, ftype = QFileDialog.getOpenFileName(self, 
                                                  'Open File',
                                                  '.',
                                                  'csv file (*.csv)')
        if fname:
            raw_data = np.genfromtxt(fname,delimiter=',')
            self.locations = raw_data[:,0]
            self.raw_data_x = raw_data[:,1]
            self.raw_data_y = raw_data[:,2]
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
    
    def plot_raw(self):
        self.plot_all_x.plot(self.locations, self.raw_data_x)
        self.plot_all_y.plot(self.locations, self.raw_data_y)
        print('plot raw')
    
    def plot_smooth(self):
        print('plot smooth')
    
    def plot_end(self):
        print('plot end')
        
    def smooth_action(self):
        print('smooth action')

    def step_smooth_action(self):
        print('smooth step action')
if __name__ == '__main__':
    # 创建应用程序和对象
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
