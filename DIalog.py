from PyQt5 import QtCore, QtWidgets, QtGui
class MyDialog(QtWidgets.QDialog):
    """ Сапожников А.А
    Класс реализует виджет диалогового окна
    """
    def __init__(self,parent = None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle("Image setting")
        self.resize(200, 70)
        self.mainBox = QtWidgets.QVBoxLayout()

        self.spinbox = QtWidgets.QSpinBox()
        self.spinbox_2 = QtWidgets.QSpinBox()
        self.spinbox.setRange(100,2000)
        self.spinbox_2.setRange(100,2000)
        self.label = QtWidgets.QLabel("Please, enter an window size")
        self.mainBox.addWidget(self.label)
        self.mainBox.addWidget(self.spinbox)
        self.mainBox.addWidget(self.spinbox_2)

        self.hbox = QtWidgets.QHBoxLayout()
        self.btnOK = QtWidgets.QPushButton("&OK")
        self.btnCancel = QtWidgets.QPushButton("&Cancel")
        self.btnCancel.setDefault(True)
        self.btnOK.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.hbox.addWidget(self.btnOK)
        self.hbox.addWidget(self.btnCancel)
        self.mainBox.addLayout(self.hbox)

        self.setLayout(self.mainBox)