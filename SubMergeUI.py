# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sub_merge.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(765, 588)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet(_fromUtf8("background-color: rgb(77, 77, 77);\n"
"color: rgb(247, 247, 247);"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(_fromUtf8("background-color: rgb(88, 88, 88);"))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setMargin(1)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.subtitleTabs = QtGui.QTabWidget(self.centralwidget)
        self.subtitleTabs.setAutoFillBackground(True)
        self.subtitleTabs.setStyleSheet(_fromUtf8("background-color: rgb(88, 88, 88);\n"
"border-color: rgb(67, 67, 67);\n"
"color: rgb(244, 244, 244);"))
        self.subtitleTabs.setTabShape(QtGui.QTabWidget.Rounded)
        self.subtitleTabs.setTabsClosable(True)
        self.subtitleTabs.setMovable(True)
        self.subtitleTabs.setObjectName(_fromUtf8("subtitleTabs"))
        self.tab = QtGui.QWidget()
        self.tab.setStyleSheet(_fromUtf8("background-color: rgb(88, 88, 88);\n"
"color: rgb(236, 236, 236);"))
        self.tab.setObjectName(_fromUtf8("tab"))
        self.horizontalLayout.addWidget(self.subtitleTabs)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 765, 22))
        self.menubar.setStyleSheet(_fromUtf8("background-color: rgb(77, 77, 77);\n"
"color: rgb(247, 247, 247);\n"
"selection-background-color: rgb(4, 186, 241);"))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setAutoFillBackground(False)
        self.menuFile.setStyleSheet(_fromUtf8("background-color: rgb(77, 77, 77);\n"
"color: rgb(247, 247, 247);"))
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_Subtitle = QtGui.QAction(MainWindow)
        self.actionOpen_Subtitle.setObjectName(_fromUtf8("actionOpen_Subtitle"))
        self.actionOpen_Video = QtGui.QAction(MainWindow)
        self.actionOpen_Video.setObjectName(_fromUtf8("actionOpen_Video"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionConcatenate = QtGui.QAction(MainWindow)
        self.actionConcatenate.setObjectName(_fromUtf8("actionConcatenate"))
        self.actionDelete = QtGui.QAction(MainWindow)
        self.actionDelete.setObjectName(_fromUtf8("actionDelete"))
        self.actionSet_to_Current_Position = QtGui.QAction(MainWindow)
        self.actionSet_to_Current_Position.setObjectName(_fromUtf8("actionSet_to_Current_Position"))
        self.actionBreak_Selected_Subtitles = QtGui.QAction(MainWindow)
        self.actionBreak_Selected_Subtitles.setObjectName(_fromUtf8("actionBreak_Selected_Subtitles"))
        # self.actionSave = QtGui.QAction(MainWindow)
        # self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_As = QtGui.QAction(MainWindow)
        self.actionSave_As.setObjectName(_fromUtf8("actionSave_As"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menuFile.addAction(self.actionOpen_Subtitle)
        self.menuFile.addAction(self.actionOpen_Video)
        # self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionAbout)
        self.menuOptions.addAction(self.actionConcatenate)
        self.menuOptions.addAction(self.actionBreak_Selected_Subtitles)
        self.menuOptions.addAction(self.actionSet_to_Current_Position)
        self.menuOptions.addSeparator()
        self.menuOptions.addAction(self.actionDelete)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.subtitleTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Sub Merge", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuAbout.setTitle(_translate("MainWindow", "Help", None))
        self.menuOptions.setTitle(_translate("MainWindow", "Options", None))
        self.actionOpen_Subtitle.setText(_translate("MainWindow", "Open Subtitle", None))
        self.actionOpen_Video.setText(_translate("MainWindow", "Open Media", None))
        self.actionOpen_Video.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionConcatenate.setText(_translate("MainWindow", "Concatenate", None))
        self.actionDelete.setText(_translate("MainWindow", "Delete (Selected Subtitles)", None))
        self.actionDelete.setShortcut(_translate("MainWindow", "Del", None))
        self.actionSet_to_Current_Position.setText(_translate("MainWindow", "Set to Current Video Position", None))
        self.actionBreak_Selected_Subtitles.setText(_translate("MainWindow", "Create Tab (Selected Subtitles)", None))
        self.actionBreak_Selected_Subtitles.setShortcut(_translate("MainWindow", "Ctrl+Shift+C", None))
        # self.actionSave.setText(_translate("MainWindow", "Save", None))
        # self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.actionSave_As.setText(_translate("MainWindow", "Save As..", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))

