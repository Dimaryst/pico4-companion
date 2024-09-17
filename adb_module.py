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
        self.adb_processes = {}
        self.apk_queue = deque()
        self.command_queue = deque()

    def disable_explore_and_user_guide(self):
        self.parent.textEdit.insertPlainText("\n" + "Disablining services com.picovr.activitycenter, com.pvr.home and com.picovr.guide.")
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self._start_process('adb_disable_com.picovr.activitycenter', ["shell", "pm", "disable-user", "--user", "0", "com.picovr.activitycenter"], self.handle_output_adb_disable_compicovractivitycenter)
        self._start_process('adb_disable_com.pvr.home', ["shell", "pm", "disable-user", "--user", "0", "com.pvr.home"], self.handle_output_adb_disable_compvrhome)
        self._start_process('adb_disable_com.picovr.guide', ["shell", "pm", "disable-user", "--user", "0", "com.picovr.guide"], self.handle_output_adb_disable_compicovrguide)

    def handle_output_adb_disable_compicovrguide(self):
        output = self._read_output('adb_disable_com.picovr.guide')
        self.parent.textEdit.insertPlainText("\n" + output)
        self.parent.textEdit.moveCursor(QTextCursor.End)

    def handle_output_adb_disable_compvrhome(self):
        output = self._read_output('adb_disable_com.pvr.home')
        self.parent.textEdit.insertPlainText("\n" + output)
        self.parent.textEdit.moveCursor(QTextCursor.End)

    def handle_output_adb_disable_compicovractivitycenter(self):
        output = self._read_output('adb_disable_com.picovr.activitycenter')
        self.parent.textEdit.insertPlainText("\n" + output)
        self.parent.textEdit.moveCursor(QTextCursor.End) 
       
    def empty_handler(self):
        pass

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
                self.parent.groupBox.setTitle(f"Android Debug Bridge Logs [Connected {device_serial} IN SIDELOAD MODE]")
        else:
            self.parent.groupBox.setTitle("Android Debug Bridge Logs [Disconnected]")

    def check_region(self):
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + "Installing APK's...")
        apk_files = [f for f in os.listdir(self.apk_region_folder) if f.endswith('.apk')]
        self.apk_queue.extend(apk_files)
        self.install_next_apk()

    def install_next_apk(self):
        if self.apk_queue:
            apk_file = self.apk_queue.popleft()
            apk_path = os.path.join(self.apk_region_folder, apk_file)
            self.parent.textEdit.insertPlainText(f"\nInstalling {apk_path}...")
            self.parent.textEdit.moveCursor(QTextCursor.End)
            self._start_process(
                name=apk_file,
                arguments=["install", apk_path],
                stdout_handler=lambda: self.read_output_install_apk(apk_file),
                finish_handler=self.on_install_finished
            )
        else:
            self.parent.textEdit.insertPlainText("\nAll APK installations finished.")
            self.adb_check_region_settings()
            self.parent.textEdit.moveCursor(QTextCursor.End)

    def store_cleanup(self, new_region="US"):
        self.parent.textEdit.insertPlainText("\nStarting Store Cleaning...")
        self.parent.textEdit.insertPlainText(f"\nSetting Store to {new_region}...")
        self.parent.textEdit.moveCursor(QTextCursor.End)
        commands = [
            ["shell", "settings", "put", "global", "user_settings_initialized", new_region],
            ["shell", "pm", "clear", "com.picovr.store"],
            ["shell", "pm", "clear", "com.picovr.vrusercenter"],
            ["shell", "pm", "clear", "com.pvr.home"],
            ["shell", "pm", "uninstall", "-k", "--user", "0", "com.picovr.store"],
            ["shell", "pm", "uninstall", "-k", "--user", "0", "com.picovr.vrusercenter"],
            ["shell", "pm", "uninstall", "-k", "--user", "0", "com.pvr.home"],
            ["shell", "pm", "install-existing", "com.picovr.vrusercenter"],
            ["shell", "pm", "install-existing", "com.pvr.home"],
            ["shell", "pm", "install-existing", "com.picovr.store"]
        ]
        
        self.command_queue.extend(commands)
        self.execute_next_command_store(new_region)

    def install_new_store(self, new_region="US"):
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + "Installing APK's...")
        matrix_files = [os.path.join(self.apk_matrix_folder, f) for f in os.listdir(self.apk_matrix_folder) if f.endswith('.apk')]

        if new_region == "US":
            apk_files = [os.path.join(self.apk_global_folder, f) for f in os.listdir(self.apk_global_folder) if f.endswith('.apk')]
        elif new_region == "CN":
            apk_files = [os.path.join(self.apk_china_folder, f) for f in os.listdir(self.apk_china_folder) if f.endswith('.apk')]
        else:
            apk_files = []
        apk_files += matrix_files

        self.apk_queue.extend(apk_files)
        self.install_next_apk()

    def execute_next_command_store(self, new_region):
        if self.command_queue:
            command = self.command_queue.popleft()
            command_str = ' '.join(command)
            self.parent.textEdit.moveCursor(QTextCursor.End)
            self.parent.textEdit.insertPlainText(f"\Running: {command_str}...")
            self._start_process(
                name=command_str,
                arguments=command,
                stdout_handler=lambda: self.read_output_store_clean(command_str),
                finish_handler=self.on_command_finished(new_region)
            )
        else:
            print(new_region)
            self.install_new_store(new_region)
            self.parent.textEdit.insertPlainText("\nAll commands executed.")

    def read_output_store_clean(self, process_name):
        output = self._read_output(process_name)
        self.parent.textEdit.insertPlainText("\n" + output)
        self.parent.textEdit.moveCursor(QTextCursor.End)

    def on_command_finished(self, new_region='US'):
        self.parent.textEdit.insertPlainText("\nDone.\n")
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.execute_next_command_store(new_region)

    def adb_check_region_settings(self):
        self._start_process('adb_check_region_settings', ["shell", "settings", "get", "global", "user_settings_initialized"], self.handle_check_region_settings)

    def handle_check_region_settings(self):
        output = self._read_output('adb_check_region_settings')
        self.parent.textEdit.insertPlainText("\nDevice Region: " + output)
        self.parent.textEdit.moveCursor(QTextCursor.End)

    def read_output_install_apk(self, process_name):
        output = self._read_output(process_name)
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + output)

    def on_install_finished(self):
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\nInstallation finished.\n")
        self.install_next_apk()

    def adb_start_service(self, service="android.settings.SETTINGS"):
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + "Running...")
        self._start_process('adb_start_service', ["shell", "am", "start", "-a", service], self.handle_output_start_service)

    def handle_output_start_service(self):
        output = self._read_output('adb_start_service')
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + output)

    def adb_devices(self):
        self._start_process('adb_devices', ["devices"], self.handle_output_devices)

    def handle_output_devices(self):
        output = self._read_output('adb_devices')
        self.parent.textEdit.insertPlainText("\n" + output)
        self.parent.textEdit.moveCursor(QTextCursor.End)
        
    def adb_list_packages(self):
        self._start_process('adb_list_packages', ["shell", "pm", "list", "packages"], self.handle_output_list_packages)

    def handle_output_list_packages(self):
        output = self._read_output('adb_list_packages')
        self.parent.textEdit.moveCursor(QTextCursor.End)
        self.parent.textEdit.insertPlainText("\n" + output)
        self.parent.textEdit.moveCursor(QTextCursor.End)

    def get_oem_state(self):
        self.parent.textEdit.insertPlainText("\n" + "Checking \"ro.oem.state\"...")
        self._start_process('adb_get_oem_state', ['shell', 'getprop', 'ro.oem.state'], self.handle_output_get_oem_state)

    def handle_output_get_oem_state(self):
        output = self._read_output('adb_get_oem_state')
        if output == "true":
            self.parent.textEdit.insertPlainText("\nState: OEM")
        elif output == "":
            self.parent.textEdit.insertPlainText("\nState: Non-OEM")
        else:
            self.parent.textEdit.insertPlainText("\nFailed to get OEM state!")

        self.parent.textEdit.moveCursor(QTextCursor.End)


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

    def _read_output(self, process_name):
        process = self.adb_processes[process_name]
        output = process.readAllStandardOutput()
        return QTextCodec.codecForLocale().toUnicode(output).strip()
