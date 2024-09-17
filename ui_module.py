import platform
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QFileDialog
from assets.design import Ui_MainWindow
from adb_module import ADBManager

class MainInstaller(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.adb_manager = ADBManager(self)
        self.setWindowTitle("Pico 4 MultiTool")
        self.groupBox.setTitle("Android Debug Bridge Logs [Disconnected]")
        self.setup_ui_elements()
        self.connect_signals()

    def setup_ui_elements(self):
        self.textEdit.setReadOnly(True)
        self.textEdit.insertPlainText("Multitool started")

    def connect_signals(self):
        self.device_check_timer = QTimer(self)
        self.device_check_timer.timeout.connect(self.adb_manager.check_connected_device)
        self.device_check_timer.start(5000)
        self.actionScan_for_Devices.triggered.connect(self.adb_manager.adb_devices)
        self.actionShow_installed_Packages.triggered.connect(self.adb_manager.adb_list_packages)
        self.actionDisable_Explore_and_User_Guide.triggered.connect(self.adb_manager.disable_explore_and_user_guide)
        self.actionCheck_Region_on_Pico.triggered.connect(self.adb_manager.check_region)
        self.actionCheck_OEM_State.triggered.connect(self.adb_manager.get_oem_state)
        self.actionOpen_Android_Settings.triggered.connect(lambda: self.adb_manager.adb_start_service(service="android.settings.SETTINGS"))
        self.actionSwitch_to_Global_Store.triggered.connect(lambda:self.adb_manager.store_cleanup(new_region='US'))
        self.actionSwitch_to_China_Store.triggered.connect(lambda:self.adb_manager.store_cleanup(new_region='CN'))
        self.actionSwitch_Buisness_Store_to_Global_Store.setDisabled(True)