# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assets/design.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 320)
        MainWindow.setMinimumSize(QtCore.QSize(480, 320))
        MainWindow.setMaximumSize(QtCore.QSize(480, 320))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayout.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 42))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menuActions = QtWidgets.QMenu(self.menubar)
        self.menuActions.setObjectName("menuActions")
        self.menuStore = QtWidgets.QMenu(self.menubar)
        self.menuStore.setObjectName("menuStore")
        MainWindow.setMenuBar(self.menubar)
        self.actionCheck_Region_on_Pico = QtWidgets.QAction(MainWindow)
        self.actionCheck_Region_on_Pico.setObjectName("actionCheck_Region_on_Pico")
        self.actionSwitch_to_Global_Store = QtWidgets.QAction(MainWindow)
        self.actionSwitch_to_Global_Store.setObjectName("actionSwitch_to_Global_Store")
        self.actionSwitch_to_China_Store = QtWidgets.QAction(MainWindow)
        self.actionSwitch_to_China_Store.setObjectName("actionSwitch_to_China_Store")
        self.actionSwitch_Buisness_Store_to_Global_Store = QtWidgets.QAction(MainWindow)
        self.actionSwitch_Buisness_Store_to_Global_Store.setObjectName("actionSwitch_Buisness_Store_to_Global_Store")
        self.actionCheck_OEM_State = QtWidgets.QAction(MainWindow)
        self.actionCheck_OEM_State.setObjectName("actionCheck_OEM_State")
        self.actionScan_for_Devices = QtWidgets.QAction(MainWindow)
        self.actionScan_for_Devices.setObjectName("actionScan_for_Devices")
        self.actionOpen_Android_Settings = QtWidgets.QAction(MainWindow)
        self.actionOpen_Android_Settings.setObjectName("actionOpen_Android_Settings")
        self.actionShow_installed_Packages = QtWidgets.QAction(MainWindow)
        self.actionShow_installed_Packages.setObjectName("actionShow_installed_Packages")
        self.actionDisable_Explore_and_User_Guide = QtWidgets.QAction(MainWindow)
        self.actionDisable_Explore_and_User_Guide.setObjectName("actionDisable_Explore_and_User_Guide")
        self.menuActions.addAction(self.actionCheck_Region_on_Pico)
        self.menuActions.addAction(self.actionCheck_OEM_State)
        self.menuActions.addAction(self.actionScan_for_Devices)
        self.menuActions.addSeparator()
        self.menuActions.addAction(self.actionOpen_Android_Settings)
        self.menuActions.addAction(self.actionShow_installed_Packages)
        self.menuActions.addAction(self.actionDisable_Explore_and_User_Guide)
        self.menuStore.addAction(self.actionSwitch_to_Global_Store)
        self.menuStore.addAction(self.actionSwitch_to_China_Store)
        self.menuStore.addAction(self.actionSwitch_Buisness_Store_to_Global_Store)
        self.menubar.addAction(self.menuActions.menuAction())
        self.menubar.addAction(self.menuStore.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pico 4 Toolbox"))
        self.groupBox.setTitle(_translate("MainWindow", "Output (logs and adb)"))
        self.menuActions.setTitle(_translate("MainWindow", "Device"))
        self.menuStore.setTitle(_translate("MainWindow", "Store"))
        self.actionCheck_Region_on_Pico.setText(_translate("MainWindow", "Check Region"))
        self.actionSwitch_to_Global_Store.setText(_translate("MainWindow", "Switch to Global Store"))
        self.actionSwitch_to_China_Store.setText(_translate("MainWindow", "Switch to China Store"))
        self.actionSwitch_Buisness_Store_to_Global_Store.setText(_translate("MainWindow", "Switch Buisness Store to Global Store"))
        self.actionCheck_OEM_State.setText(_translate("MainWindow", "Check OEM State"))
        self.actionScan_for_Devices.setText(_translate("MainWindow", "Scan for Devices"))
        self.actionOpen_Android_Settings.setText(_translate("MainWindow", "Open Android Settings"))
        self.actionShow_installed_Packages.setText(_translate("MainWindow", "Show installed Packages"))
        self.actionDisable_Explore_and_User_Guide.setText(_translate("MainWindow", "Disable Explore and User Guide"))
