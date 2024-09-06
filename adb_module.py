from PyQt5.QtCore import QProcess, QTextCodec
from PyQt5.QtGui import QTextCursor
import platform, os

class ADBManager:
    def __init__(self, parent):
        self.parent = parent
        self.adb_bin = "adb"
        self.fastboot_bin = "fastboot"
        if platform.system() == "Windows":
            self.adb_bin = "bin/adb.exe"
            self.fastboot_bin = "bin/fastboot.exe"
        self.apk_region_folder = os.path.join(os.getcwd(), "apk", "region")
        self.adb_processes = {}

    def check_connected_device(self):
        self._start_process('adb_devices', ["devices"], self.handle_check_connected_device)

    def handle_check_connected_device(self):
        output = self._read_output('adb_devices')
        lines = output.split('\n')
        connected_devices = [line for line in lines if "\tdevice" in line or "\tsideload" in line]
        if connected_devices:
            device_info = connected_devices[0].split('\t')
            device_serial = device_info[0]
            device_status = device_info[1]

            if device_status == "device":
                self.parent.groupBox.setTitle(f"Android Debug Bridge Logs [Connected {device_serial}]")
            elif device_status == "sideload":
                self.parent.groupBox.setTitle(f"Android Debug Bridge Logs [Connected {device_serial} (sideload)]")
        else:
            self.parent.groupBox.setTitle("Android Debug Bridge Logs [Disconnected]")

    def install_apks_and_get_region(self):
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\nStarting APK installation...")
        self.install_apks_from_folder()

    def install_apks_from_folder(self):
        apk_files = [os.path.join(self.apk_region_folder, f) for f in os.listdir(self.apk_region_folder) if f.endswith('.apk')]
        
        if apk_files:
            for apk_file in apk_files:
                self.adb_install(apk_file)
        else:
            self.parent.textEdit.moveCursor(QTextCursor.End)
            self.parent.textEdit.insertPlainText("\nNo APK files found in folder.")
        self.get_current_region()

    def get_oem_state(self):
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\nChecking OEM State...")
        self._start_process('adb_get_oem_state', ['shell', 'getprop', 'ro.oem.state'], self.handle_output_get_oem_state)
    
    def handle_output_get_oem_state(self):
        output = self._read_output('adb_get_oem_state')
        oem_state = ''
        if output == '':
            oem_state = 'Non-OEM'
        elif output == 'true':
            oem_state = 'OEM'
        else:
            oem_state = 'Unknown'
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText(f"\nOEM STATE: {oem_state} ({output})")

    def get_current_region(self):
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\nGetting Current Region...")
        self._start_process('adb_get_region', ['shell', 'settings', 'get', 'global', 'user_settings_initialized'], self.handle_output_get_region)

    def handle_output_get_region(self):
        output = self._read_output('adb_get_region')
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText(f"\nCURRENT REGION: {output}")

    def adb_install(self, app_path):
        # self.parent.textEdit.moveCursor(QTextCursor.End)
        # self.parent.textEdit.insertPlainText("\n" + "Installing: " + app_path)
        self._start_process('adb_install', ["install", app_path], self.handle_output_install, self.show_progress_bar, self.hide_progress_bar)

    def handle_output_install(self):
        output = self._read_output('adb_install')
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + output)

    def adb_uninstall(self, app_id):
        self._start_process('adb_uninstall', ["uninstall", app_id], self.handle_output_uninstall, self.show_progress_bar, self.hide_progress_bar)

    def handle_output_uninstall(self):
        output = self._read_output('adb_uninstall')
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + output)

    def adb_devices(self):
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + "Scanning for devices...")
        self._start_process('adb_devices', ["devices"], self.handle_output_devices)

    def handle_output_devices(self):
        output = self._read_output('adb_devices')
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + output)

    def adb_reboot_bootloader(self):
        self.parent.progressBar.setValue(0)
        self._start_process('adb_reboot_bootloader', ["reboot", "bootloader"], self.handle_output_reboot_bootloader, self.show_progress_bar, self.hide_progress_bar)

    def handle_output_reboot_bootloader(self):
        output = self._read_output('adb_reboot_bootloader')
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + output)

    def adb_sideload(self, zip_path):
        self.parent.progressBar.setValue(0)
        self._start_process('adb_sideload', ["sideload", zip_path], self.handle_output_sideload, self.show_progress_bar, self.hide_progress_bar)

    def handle_output_sideload(self):
        output = self._read_output('adb_sideload')
        percentage = self.extract_percentage(output)
        if percentage is not None:
            self.parent.progressBar.setValue(percentage)

        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + output)

    def extract_percentage(self, output):
        try:
            start_index = output.find("(~")
            end_index = output.find("%)", start_index)

            if start_index != -1 and end_index != -1:
                percentage_str = output[start_index + 2:end_index]
                return int(percentage_str)
        except ValueError:
            return None
        return None
        
    def adb_list_packages(self):
        self._start_process('adb_list_packages', ["shell", "pm", "list", "packages"], self.handle_output_list_packages)

    def handle_output_list_packages(self):
        output = self._read_output('adb_list_packages')
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + output)

    def show_progress_bar(self):
        self.parent.progressBar.setVisible(True)

    def hide_progress_bar(self):
        self.parent.progressBar.setVisible(False)

    def _start_process(self, name, arguments, stdout_handler, start_handler=None, finish_handler=None):
        self.adb_processes[name] = QProcess()
        process = self.adb_processes[name]
        if start_handler:
            process.started.connect(start_handler)
        process.readyReadStandardOutput.connect(stdout_handler)
        if finish_handler:
            process.finished.connect(finish_handler)
        process.setProcessChannelMode(QProcess.MergedChannels)
        process.start(self.adb_bin, arguments)

    def _start_process_fastboot(self, name, arguments, stdout_handler, start_handler=None, finish_handler=None):
        self.adb_processes[name] = QProcess()
        process = self.adb_processes[name]
        if start_handler:
            process.started.connect(start_handler)
        process.readyReadStandardOutput.connect(stdout_handler)
        if finish_handler:
            process.finished.connect(finish_handler)
        process.setProcessChannelMode(QProcess.MergedChannels)
        process.start(self.fastboot_bin, arguments)

    def _read_output(self, process_name):
        process = self.adb_processes[process_name]
        output = process.readAllStandardOutput()
        return QTextCodec.codecForLocale().toUnicode(output).strip()
