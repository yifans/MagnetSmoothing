# embedding_in_qt5.py --- Simple Qt5 application embedding matplotlib canvases
#
# Copyright (C) 2005 Florent Rougon
#               2006 Darren Dale
#               2015 Jens H Nielsen
#
# This file is an example program for matplotlib. It may be used and
# modified with no restriction; raw copies as well as modified versions
# may be distributed without limitation.

import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


from scipy.interpolate import UnivariateSpline
import numpy as np

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        #self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes.set_xlabel('location mm')
        self.axes.set_ylabel('position mm')

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
class PlotAll(MyMplCanvas):
    
    def plot(self, xx, y):
        self.axes.cla()
        self.axes.plot(xx, y, 'y')
        self.draw()
    
    def add_bound(self, xx, b1, b2):
        # print(b1, b2)
        self.axes.axvline(x = xx[b1], color='r')
        self.axes.axvline(x = xx[b2], color='r')
        self.draw()
    
    def plot_compare(self, xx, data_before, data_after):
        self.axes.cla()
        #print('before', data_before)
        #print('after', data_after)
        changed_xx = []
        changed_yy = []
        for index in range(len(xx)):
            if data_before[index] == data_after[index]:
                continue
            changed_xx.append(xx[index])
            changed_yy.append(data_after[index])
        xnew, data_after_new = myspl(xx, data_after)
        l1, = self.axes.plot(xx, data_before, 'b')
        l2_1, = self.axes.plot(xx, data_after, 'g*')
        l2, = self.axes.plot(xx, data_after, 'g')
        l3, = self.axes.plot(changed_xx, changed_yy, 'ro')
        self.axes.legend(handles = [l1, l2, l3], 
                        labels = ['before', 'after', 'changed points'])
        self.draw()

class PlotSection(MyMplCanvas):
        
    def plot(self, xx, data_before, data_after):
        self.axes.cla()
        xnew, data_after_new = myspl(xx, data_after)
        # print('new data', data_after_new)
        l1, = self.axes.plot(xx, data_before, 'b*')
        l2_1, = self.axes.plot(xx, data_after, 'g*')
        l2, = self.axes.plot(xnew, data_after_new, 'g')
        self.axes.legend(handles = [l1, l2], 
                        labels = ['before', 'after'])
        self.draw()
        
    def clear(self):
        self.axes.cla()
        self.draw()

def myspl(xx, data):
    if len(xx) < 3:
        kk = 1
        print('kk',kk)
        spl = UnivariateSpline(xx, data, k = kk)
    else:
        spl = UnivariateSpline(xx, data)
    xnew = np.linspace(xx.min(),xx.max(),200)
    data_new = spl(xnew)
    return xnew, data_new
    