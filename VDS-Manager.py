from PyQt4 import QtCore as core, QtGui as gui
import sys,math,time

from components.channel_viewer import ChannelModificationControlWidget

class interface(gui.QWidget):

	def __init__(self):
		super(interface,self).__init__()
		self.setWindowTitle("VDS Manager")

		self.connected  = False
		self.connect()

		if self.connected:
			self.doUI()

		else:
			print("Unable to connect to LabRAD and/or VDS; exiting")
			sys.exit()

	def connect(self):
		import labrad
		self.connection = labrad.connect()
		self.vds        = self.connection.virtual_device_server
		self.connected  = True

	def doUI(self):
		# testing components
		self.cc = ChannelModificationControlWidget(self)
		self.VBoxMain = gui.QVBoxLayout()
		self.VBoxMain.addWidget(self.cc)
		self.setLayout(self.VBoxMain)


		self.show()

if __name__=='__main__':
    app = gui.QApplication(sys.argv)
    i = interface()
    sys.exit(app.exec_())
