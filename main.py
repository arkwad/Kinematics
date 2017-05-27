# ==========================================================
#	File : main.py
#	Author: Arkadiusz Wadowski 
#	Email: wadowski.arkadiusz@gmail.com
#	Created: 17.05.2017
# ==========================================================
#  L1 = 1.40; L2 = 0.85; M1 = 1.40; M2 = 3.20
# ==========================================================
import sys
from math import sqrt, sin, asin, cos, acos, degrees
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QMessageBox
from ui_code import Ui_MainWindow
import numpy as np
from PyQt4.QtCore import QThread
import time


class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.L1 = 0
        self.L2 = 1.4
        self.L3 = 0.85
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.f_x.setValue(1.2)
        self.ui.f_y.setValue(1.5)

        self.update_forward_kin_plot()
        self.ui.f_th1_1.setReadOnly(True)
        self.ui.f_th1_2.setReadOnly(True)
        self.ui.f_th2_1.setReadOnly(True)
        self.ui.f_th2_2.setReadOnly(True)
        self.ui.f_plot.axes.autoscale(False, 'both', False)
        self.ui.f_plot.axes.set_xlim(-0.2, 2.5)
        self.ui.f_plot.axes.set_ylim(-0.4, 2.5)
        self.ui.f_plot.axes.set_aspect('equal', 'datalim')

        self.ui.i_plot.axes.autoscale(False, 'both', False)
        self.ui.i_plot.axes.set_xlim(-0.2, 2.5)
        self.ui.i_plot.axes.set_ylim(-0.4, 2.5)
        self.ui.i_plot.axes.set_aspect('equal', 'datalim')

        self.threadclass = MovePlotThread()

        QtCore.QObject.connect(self.ui.f_x, QtCore.SIGNAL("clicked()"), self.update_forward_kin_plot)
        self.connect(self.threadclass, QtCore.SIGNAL("plot"), self.plot_movement)
        self.ui.f_x.valueChanged.connect(self.update_forward_kin_plot)
        self.ui.f_y.valueChanged.connect(self.update_forward_kin_plot)


        self.threadclass.start()

    def plot_movement(self):
 #       if True == self.ui.tab_2.isTabEnabled(1):
 #           print 'ok'
        lista = np.arange(1, 1.51, 0.01)
        ver = np.sin(50 * lista) / 10 + 1.5

        self.ui.i_plot.draw()
        for i in xrange(0,lista.size):
            theta21, theta31, theta22, theta32 = self.calculate_angles(lista[i],ver[i])
            coord1 = self.get_coordinates(theta21, theta31)
            coord2 = self.get_coordinates(theta22, theta32)
            self.ui.i_plot.axes.cla()
            self.ui.i_plot.axes.plot(lista, ver, 'black')
            self.ui.i_plot.axes.hold(True)
            self.plot_links(coord1, coord2, 1)

    def update_forward_kin_plot(self):
        x = self.ui.f_x.value()
        y = self.ui.f_y.value()

        theta21, theta31, theta22, theta32 = self.calculate_angles(x, y)
        self.ui.f_th1_1.setText( str( degrees(theta21) ))
        self.ui.f_th2_1.setText( str( degrees(theta31) ) )

        self.ui.f_th1_2.setText( str( degrees(theta22) ) )
        self.ui.f_th2_2.setText( str( degrees(theta32) ) )

        coord1 = self.get_coordinates(theta21, theta31)
        coord2 = self.get_coordinates(theta22, theta32)

        self.plot_links(coord1, coord2 , 0)

    def plot_links(self, coord1, coord2, which):

        if 0 == which:

            self.ui.f_plot.axes.hold(True)
            self.ui.f_plot.axes.set_xlabel("X")
            self.ui.f_plot.axes.set_ylabel("Y")
            self.ui.f_plot.axes.cla()

            self.ui.f_plot.axes.plot(coord1[0], coord1[1], 'b')
            self.ui.f_plot.axes.plot(coord2[0], coord2[1], 'r')

            self.ui.f_plot.axes.plot(coord1[0], coord1[1], 'b' + 'o')
            self.ui.f_plot.axes.plot(coord2[0], coord2[1], 'r' + 'o')
            self.ui.f_plot.axes.set_xlim(-0.2, 2.5)
            self.ui.f_plot.axes.set_ylim(-0.5, 2.5)

            self.ui.f_plot.draw()
        elif 1 == which:
            if 1 == self.ui.Theta1_1.currentIndex():
                self.ui.i_plot.axes.hold(True)
                self.ui.i_plot.axes.set_xlabel("X")
                self.ui.i_plot.axes.set_ylabel("Y")

                self.ui.i_plot.axes.plot(coord1[0], coord1[1], 'b')
                self.ui.i_plot.axes.plot(coord2[0], coord2[1], 'r')

                self.ui.i_plot.axes.plot(coord1[0], coord1[1], 'b' + 'o')
                self.ui.i_plot.axes.plot(coord2[0], coord2[1], 'r' + 'o')
                self.ui.i_plot.axes.set_xlim(-0.2, 2.5)
                self.ui.i_plot.axes.set_ylim(-0.5, 2.5)

                self.ui.i_plot.draw()


    def calculate_angles (self, x, y):

        A = (x ** 2 + (y - self.L1) ** 2 + self.L2 ** 2 - self.L3 ** 2) / (2 * x * self.L2)
        B = (y - self.L1) / x

        delta = 4 * A ** 2 - 4 * (1 + B ** 2) * (A ** 2 - B ** 2)

        theta21 = acos((2 * A - sqrt(delta)) / (2 + 2 * B ** 2))
        theta31 = acos((x - self.L2 * cos(theta21)) / self.L3)

        theta22 = acos((2 * A + sqrt(delta)) / (2 + 2 * B ** 2))
        theta32 = acos((x - self.L2 * cos(theta22)) / self.L3)

        return theta21, theta31, theta22, theta32

    def get_coordinates(self, angle1, angle2):
        x11 = 0
        y11 = 0
        x12 = 0
        y12 = self.L1
        x21 = x12
        y21 = y12
        x22 = self.L2 * cos(angle1)
        y22 = y21 + self.L2 * sin(angle1)
        x31 = x22
        y31 = y22
        x32 = x22 + self.L3 * cos(angle2)
        y32 = y22 + self.L3 * sin(angle2)
        return [[x11, x12, x21, x22, x31, x32], [y11, y12, y21, y22, y31, y32]]


class MovePlotThread(QThread):

    def __init__(self, parent=None):
        super(MovePlotThread, self).__init__(parent)

    def run(self):
        while True:
            time.sleep(3)
            self.emit(QtCore.SIGNAL("plot"))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = MyWindow()
    myapp.show()

    sys.exit(app.exec_())
