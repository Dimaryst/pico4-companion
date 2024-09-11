from PyQt5.QtCore import QProcess, QTextCodec
from PyQt5.QtGui import QTextCursor
import platform, os
from collections import deque

class ADBManager:
    def __init__(self, parent):
        self.parent = parent
        self.adb_bin = "adb"
        self.fastboot_bin = "fastboot"
        if platform.system() == "Windows":
            self.adb_bin = "bin/adb.exe"
            self.fastboot_bin = "bin/fastboot.exe"
        self.apk_region_folder = os.path.join(os.getcwd(), "apk", "region")
        self.apk_global_folder = os.path.join(os.getcwd(), "apk", "global")
        self.apk_china_folder = os.path.join(os.getcwd(), "apk", "china")
        self.apk_matrix_folder = os.path.join(os.getcwd(), "apk", "matrix")
        
        self.command_queue = deque()
        self.current_process = None
        self.is_running = False

    def _start_next_command(self):
        if not self.is_running and self.command_queue:
            command, args, stdout_handler, start_handler, finish_handler = self.command_queue.popleft()
            self._start_process(command, args, stdout_handler, start_handler, finish_handler)

    def _queue_command(self, command, args, stdout_handler=None, start_handler=None, finish_handler=None):
        self.command_queue.append((command, args, stdout_handler, start_handler, finish_handler))
        if not self.is_running:
            self._start_next_command()

    def _start_process(self, name, arguments, stdout_handler=None, start_handler=None, finish_handler=None):
        self.is_running = True
        self.current_process = QProcess()
        process = self.current_process

        if start_handler:
            process.started.connect(start_handler)

        if stdout_handler:
            process.readyReadStandardOutput.connect(stdout_handler)

        def on_finished():
            self.is_running = False
            if finish_handler:
                finish_handler()
            self._start_next_command()
        process.finished.connect(on_finished)

        process.setProcessChannelMode(QProcess.MergedChannels)
        process.start(self.adb_bin, arguments)

    def check_connected_device(self):
        self._start_process('adb_devices', ["devices"], self.handle_check_connected_device)

    def handle_check_connected_device(self):
        output = self._read_output()
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
        self.install_apks_from_folder(self.apk_region_folder)
        self._queue_command('adb_get_region', ['shell', 'settings', 'get', 'global', 'user_settings_initialized'], self.handle_output_get_region)

    def install_apks_from_folder(self, folder):
        apk_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.apk')]
        if apk_files:
            for apk_file in apk_files:
                self._queue_command('adb_install', ["install", apk_file], self.empty_handler)
        else:
            self.parent.textEdit.moveCursor(QTextCursor.End)
            self.parent.textEdit.insertPlainText("\nNo APK files found in folder.")

    def get_oem_state(self):
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\nChecking OEM State...")
        self._queue_command('adb_get_oem_state', ['shell', 'getprop', 'ro.oem.state'], self.handle_output_get_oem_state)
    
    def handle_output_get_oem_state(self):
        output = self._read_output()
        oem_state = 'Non-OEM' if output == '' else 'OEM' if output == 'true' else 'Unknown'
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText(f"\nOEM STATE: {oem_state} ({output})")

    def handle_output_get_region(self):
        output = self._read_output()
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText(f"\nCURRENT REGION: {output}")

    def adb_install(self, app_path):
        self._queue_command('adb_install', ["install", app_path], self.empty_handler)

    def handle_output_install(self):
        output = self._read_output()
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + output)

    def adb_uninstall(self, app_id):
        self._queue_command('adb_uninstall', ["uninstall", app_id], self.handle_output_uninstall)

    def handle_output_uninstall(self):
        output = self._read_output()
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + output)

    def switch_store(self, region='US'):
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText(f"\nStarting Region change to ({region})...")
        
        # Установка региона
        self._queue_command('adb_set_region', ['shell', 'settings', 'put', 'global', 'user_settings_initialized', region], self.empty_handler)
        self._queue_command(f'adb_clear_com.picovr.store', ['shell', 'pm', 'clear', "com.picovr.store"], self.empty_handler)
        self._queue_command(f'adb_clear_com.picovr.vrusercenter', ['shell', 'pm', 'clear', "com.picovr.vrusercenter"], self.empty_handler)
        self._queue_command(f'adb_clear_com.pvr.home', ['shell', 'pm', 'clear', "com.pvr.home"], self.empty_handler)

        self._queue_command(f'adb_uninstall_com.picovr.store', ["shell", "pm", "uninstall", "-k", "--user", "0", 'com.picovr.store'], self.empty_handler)
        self._queue_command(f'adb_uninstall_com.picovr.vrusercenter', ["shell", "pm", "uninstall", "-k", "--user", "0", 'com.picovr.vrusercenter'], self.empty_handler)
        self._queue_command(f'adb_uninstall_com.pvr.home', ["shell", "pm", "uninstall", "-k", "--user", "0", 'com.pvr.home'], self.empty_handler)

        self._queue_command(f'adb_install_existing_com.picovr.store', ['shell', 'pm', 'install-existing', 'com.picovr.store'], self.empty_handler)
        self._queue_command(f'adb_install_existing_com.picovr.vrusercenter', ['shell', 'pm', 'install-existing', 'com.picovr.vrusercenter'], self.empty_handler)
        self._queue_command(f'adb_install_existing_com.pvr.home', ['shell', 'pm', 'install-existing', 'com.pvr.home'], self.empty_handler)

        # Установка APK для региона
        if region == 'US':
            self.parent.textEdit.insertPlainText("\nInstalling APKs from Global folder...")
            self.install_apks_from_folder(self.apk_global_folder)
        elif region == 'CN':
            self.parent.textEdit.insertPlainText("\nInstalling APKs from China folder...")
            self.install_apks_from_folder(self.apk_china_folder)
        else:
            self.parent.textEdit.insertPlainText("\nError region selected")

        # Установка APK из Matrix
        self.parent.textEdit.insertPlainText("\nInstalling APKs from Matrix folder...")
        self.install_apks_from_folder(self.apk_matrix_folder)

        self._queue_command('adb_get_region', ['shell', 'settings', 'get', 'global', 'user_settings_initialized'], self.handle_output_get_region)

    def adb_list_packages(self):
        self._queue_command('adb_list_packages', ["shell", "pm", "list", "packages"], self.handle_output_list_packages)

    def handle_output_list_packages(self):
        output = self._read_output()
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + output)

    def adb_start_service(self, service="android.settings.SETTINGS"):
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + "Running...")
        self._queue_command('adb_start_service', ["shell", "am", "start", "-a", service], self.handle_output_start_service)

    def handle_output_start_service(self):
        output = self._read_output()
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + output)

    def adb_reboot_bootloader(self):
        self.parent.progressBar.setValue(0)
        self._queue_command('adb_reboot_bootloader', ["reboot", "bootloader"], self.handle_output_reboot_bootloader, self.show_progress_bar, self.hide_progress_bar)

    def handle_output_reboot_bootloader(self):
        output = self._read_output()
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + output)

    def adb_sideload(self, zip_path):
        self.parent.progressBar.setValue(0)
        self._queue_command('adb_sideload', ["sideload", zip_path], self.handle_output_sideload, self.show_progress_bar, self.hide_progress_bar)

    def handle_output_sideload(self):
        output = self._read_output()
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

    def empty_handler(self):
        pass

    def show_progress_bar(self):
        self.parent.progressBar.setVisible(True)

    def hide_progress_bar(self):
        self.parent.progressBar.setVisible(False)

    def _read_output(self):
        output = self.current_process.readAllStandardOutput()
        return QTextCodec.codecForLocale().toUnicode(output).strip()