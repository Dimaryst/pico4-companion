from PyQt5.QtCore import QProcess
def center_progress_bar(window):
    window_width = window.width()
    window_height = window.height()
    progress_bar_width = window.progressBar.width()
    progress_bar_height = window.progressBar.height()
    new_x = (window_width - progress_bar_width) // 2
    new_y = (window_height - progress_bar_height) // 2
    window.progressBar.move(new_x, new_y)