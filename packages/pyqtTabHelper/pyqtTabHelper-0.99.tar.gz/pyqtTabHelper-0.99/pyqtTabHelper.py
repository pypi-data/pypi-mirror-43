import sys
import PyQt5.QtWidgets, PyQt5.QtGui

from functools import partial

import sip

class sTab(PyQt5.QtWidgets.QWidget):

	def __init__(self, title="New Window", sections=[]):
		super().__init__()
		self.title = title
		self.sections = sections

		self.initUI()

	def initUI(self):

		self.grid = PyQt5.QtWidgets.QGridLayout()
		self.grid.setSpacing(10)

		self.setLayout(self.grid)

		for section in self.sections:
			self.grid.addWidget(section, section.position[0], section.position[1], section.scale[0], section.scale[1])

		self.setWindowTitle(self.title)
		self.show()

class logWindow(PyQt5.QtWidgets.QWidget):

	def __init__(self, scale=[600, 400], title="Log"):
		super().__init__()
		self.scale = scale
		self.title = title

		self.initUI()

	def initUI(self):

		vBox = PyQt5.QtWidgets.QVBoxLayout()

		self.logText = PyQt5.QtWidgets.QTextEdit()
		self.logText.setReadOnly(True)
		self.log("Testing Logging Feature")

		vBox.addWidget(self.logText)
		self.setLayout(vBox)

		self.resize(*self.scale)
		self.setWindowTitle(self.title)
		self.show()

	def log(self, text):
		self.logText.setText(self.logText.toPlainText() + text + "\n")

class sBox(PyQt5.QtWidgets.QGroupBox):

	def __init__(self, title="New Box", position=[1, 1], scale=[1, 1]):
		super().__init__(title)
		self.title = title
		self.position = position
		self.scale = scale

	def deleteLayout(self):
		cur_lay = self.layout()
		if cur_lay is not None:
			while cur_lay.count():
				item = cur_lay.takeAt(0)
				widget = item.widget()
				if widget is not None:
					widget.deleteLater()
				else:
					self.removeExtraLayout(item.layout())

			sip.delete(cur_lay)

	def getSuggestedSize(self):
		self.setLayout(PyQt5.QtWidgets.QVBoxLayout())
		self.suggestedSize = self.sizeHint()
		self.deleteLayout()
		return self.suggestedSize

	def removeExtraLayout(self, cur_lay):
		if cur_lay is not None:
			while cur_lay.count():
				item = cur_lay.takeAt(0)
				widget = item.widget()
				if widget is not None:
					widget.deleteLater()
				else:
					self.removeExtraLayout(item.layout())

			sip.delete(cur_lay)

class sMainWindow(PyQt5.QtWidgets.QMainWindow):

	def __init__(self, title="Main Window", tabs=[], scale=[800, 600]):
		super().__init__()
		self.tabs = tabs
		self.title = title
		self.scale= scale

		self.initUI()
		self.initTabs()

		self.show()

	def center(self):
		qr = self.frameGeometry()
		cp = PyQt5.QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())


	def initTabs(self):
		for i in range(len(self.tabs)):
			tab = self.tabs[i]
			self.visibleWindow.addWidget(tab)
			self.toolbar.addAction(self.createTabButton(i, tab))
			tab.mainWindow = self

		self.changeToIndex(0)

	def changeToIndex(self, index):
		try:
			self.visibleWindow.setCurrentIndex(index)
			self.setWindowTitle(self.title + " - " + self.tabs[index].title)
			try:
				self.tabs[index].onChange()
			except:
				pass
		except Exception as e:
			self.visibleWindow.setCurrentIndex(0)

	def createTabButton(self, index, tab):
		switchAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(), '&' + tab.title, self)
		switchAct.triggered.connect(partial(self.changeToIndex, index))
		return switchAct

	def initUI(self):
		self.visibleWindow = PyQt5.QtWidgets.QStackedWidget()
		self.setCentralWidget(self.visibleWindow)

		self.toolbar = self.addToolBar('')

		self.resize(*self.scale)
		self.center()
		self.setWindowTitle(self.title)
		


# app = PyQt5.QtWidgets.QApplication(sys.argv)

# testTab = sTab(title="Testing Tab", sections=[sBox()])

# testtabb = sTab(title="New Tab", sections=[sBox(position=[1,1], scale=[2,1]), sBox(position=[1,2], scale=[2,1])])

# mainWindow = sMainWindow(title="Test Window", tabs=[testTab, testtabb])

# sys.exit(app.exec_())