#!/usr/bin/env python3

"""
Created on Wed Mar 28 21:00:07 2018

@author: Yifan Song
@email: yifans@mail.ustc.edu.cn
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication,QWidget,QVBoxLayout
from myMplCanvas import MyStaticMplCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 原始数据
        self.raw_data = []
        # smooth后的数据
        self.smooth_data = []
        # smooth的配置信息
        self.smooth_config = {
            'section': 0,
            'step': 0,
            'order': 0,
            'deviation': 0
        }
        self.initUI()

    def initUI(self):
        # 设置窗口的位置和大小
        self.setGeometry(0, 0, 1200, 700)

        # 设置窗口的标题
        self.setWindowTitle('Magnets Smoothing')
        plot_canvas = MyStaticMplCanvas()
        
        
        # 全局布局
        wlayout = QVBoxLayout()
        wlayout.addWidget(plot_canvas)
        # wlayout.addWidget(self.section_canvas)
        # 参考这个文档，不能直接对MainWindow设置布局，https://stackoverflow.com/questions/37304684        
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(wlayout)
        self.show()

        # 初始化控件
        


if __name__ == '__main__':
    print('a')
    # 创建应用程序和对象
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
