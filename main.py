#==========================================================
#	File : main.py
#	Author: Arkadiusz Wadowski 
#	Email: wadowski.arkadiusz@gmail.com
#	Created: 17.05.2017
#==========================================================

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QMessageBox
from ui_code import Ui_MainWindow



class MyWindow(QtGui.QMainWindow):

	def __init__(self):
		super(MyWindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.f_plot.axes.set_xlabel("X") 
		self.ui.f_plot.axes.set_ylabel("Y")
		
		QtCore.QObject.connect(self.ui.f_calc,QtCore.SIGNAL("clicked()"),self.update_forward_kin_plot)
		
		
	def update_forward_kin_plot(self):
		self.ui.f_plot.axes.plot([0 ,10],[0, 10],'b')
		self.ui.f_plot.axes.plot([10 ,5,0],[10,15, 0],'r')
		self.ui.f_plot.draw();
		
		
		
if __name__ == '__main__':

	app = QtGui.QApplication(sys.argv)
	myapp = MyWindow()
	myapp.show()

		
	sys.exit(app.exec_())