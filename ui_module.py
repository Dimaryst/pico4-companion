import platform
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QFileDialog
from assets.design import Ui_MainWindow
from adb_module import ADBManager
from helper_module import center_progress_bar

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
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(100, 100, 200, 25)
        self.progressBar.setVisible(False)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)
        self.center_progress_bar()

    def connect_signals(self):
        self.device_check_timer = QTimer(self)
        self.device_check_timer.timeout.connect(self.adb_manager.regular_check_devices)
        self.device_check_timer.start(1000)
        self.actionScan_for_Devices.triggered.connect(self.adb_manager.check_connected_device)
        self.actionCheck_Region_on_Pico.triggered.connect(self.adb_manager.install_apks_and_get_region)
        self.actionCheck_OEM_State.triggered.connect(self.adb_manager.get_oem_state)
        self.actionShow_installed_Packages.triggered.connect(self.adb_manager.adb_list_packages)
        self.actionOpen_Android_Settings.triggered.connect(lambda: self.adb_manager.adb_start_service(service="android.settings.SETTINGS"))
        self.actionSwitch_to_Global_Store.triggered.connect(lambda: self.adb_manager.switch_store(region='US'))
        self.actionSwitch_to_China_Store.triggered.connect(lambda: self.adb_manager.switch_store(region='CN'))
        self.actionSwitch_Buisness_Store_to_Global_Store.setDisabled(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.center_progress_bar()

    def center_progress_bar(self):
        center_progress_bar(self)

    def adb_install_user_selected_apk(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(filter="APK files (*.apk)")
        if file_path:
            self.adb_manager.adb_install(file_path)