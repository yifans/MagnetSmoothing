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

from numpy import arange, sin, pi, cos
import random

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
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
        l1, = self.axes.plot(xx, data_before, 'b')
        l2, = self.axes.plot(xx, data_after, 'g')
        self.axes.legend(handles = [l1, l2], 
                        labels = ['before', 'after'])
        self.draw()

class PlotSection(MyMplCanvas):
        
    def plot(self, xx, data_before, data_after):
        self.axes.cla()
        print('plot in section')
        print(xx, data_before, data_after)
        l1, = self.axes.plot(xx, data_before, 'b*')
        l2, = self.axes.plot(xx, data_after, 'g')
        self.axes.legend(handles = [l1, l2], 
                        labels = ['before', 'after'])
        self.draw()
        
    def clear(self):
        self.axes.cla()
        self.draw()
