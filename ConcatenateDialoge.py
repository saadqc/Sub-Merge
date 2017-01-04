# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'concatenateDialoge.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ConcatenateDialog(object):
    def setupUi(self, ConcatenateDialog):
        ConcatenateDialog.setObjectName(_fromUtf8("ConcatenateDialog"))
        ConcatenateDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ConcatenateDialog.resize(500, 500)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ConcatenateDialog.sizePolicy().hasHeightForWidth())
        ConcatenateDialog.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        ConcatenateDialog.setFont(font)
        ConcatenateDialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(ConcatenateDialog)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout.setMargin(12)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listView = QtGui.QListView(ConcatenateDialog)
        self.listView.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.verticalLayout.addWidget(self.listView)
        self.buttonBox = QtGui.QDialogButtonBox(ConcatenateDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ConcatenateDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ConcatenateDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ConcatenateDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConcatenateDialog)

    def retranslateUi(self, ConcatenateDialog):
        ConcatenateDialog.setWindowTitle(_translate("ConcatenateDialog", "Concatenate", None))

