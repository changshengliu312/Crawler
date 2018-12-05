from PyQt5 import QtCore, QtGui, QtWidgets

class testForm(QtWidgets.QDialog):
    def PushButtonClicked(self):
            box = QtWidgets.QMessageBox()
            box.warning(self,"提示","这是一个按钮事件")
