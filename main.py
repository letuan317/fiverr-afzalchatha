from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


import sys
import time
import random
import platform

import essentials

# https://sites.google.com/chromium.org/driver/


program_name = "Demo - letuan317@gmail.com"
global_log = essentials.Logger()
global_log.info("Start new session")


class ThreadClass(QThread):
    update_status_signal = pyqtSignal(str)
    update_progress_signal = pyqtSignal(int)
    is_run = False
    set_time_from = 9
    set_time_to = 12
    set_total_clicks = 1000
    set_total_clicked = 0

    def __init__(self, parent=None,):
        super(ThreadClass, self).__init__(parent)
        global_log.info("Open chromedriver")
        options = Options()
        ua = UserAgent()
        userAgent = ua.random
        options.add_argument(f'user-agent={userAgent}')

        if platform.system() == "Windows":
            global_log.debug("Selenium run on Windows")
            chrome_path = './chromedriver96.exe'
        elif platform.system() == "Darwin":
            global_log.debug("Selenium run on Mac OS")
            chrome_path = './chromedriver'
        else:
            sys.exit()
        self.driver = webdriver.Chrome(
            chrome_options=options, executable_path=chrome_path)

        link = "https://www.gov.uk/book-pupil-driving-test"

        global_log.info("Open "+link)
        self.driver.get(link)

    def run(self):
        while True:
            if self.is_run:
                break
        print(self.set_time_from, self.set_time_to,
              self.set_total_clicked, self.set_total_clicks)

        global_log.warning("Start")
        num_of_reserve = 0
        for i in range(1, 21):
            num_of_reserve += 1
            self.set_total_clicked += 1
            self.update_status_signal.emit(
                "{}/10, click: {}/{}, time delay: random".format(str(num_of_reserve), str(self.set_total_clicked), str(self.set_total_clicks)))
            self.update_progress_signal.emit(num_of_reserve)
            if num_of_reserve == 10:
                time_delay = random.randint(10, 20)
                for i in range(time_delay, 0, -1):
                    self.update_status_signal.emit(
                        "{}/10, click: {}/{}, time delay: {}s".format(str(num_of_reserve), str(self.set_total_clicked), str(self.set_total_clicks), str(i)))
                    time.sleep(1)
                num_of_reserve = 0
            if self.set_total_clicked == self.set_total_clicks:
                break
        global_log.warning("Done")
        self.update_status_signal.emit("DONE")


class UIApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width = 400
        self.window_height = 200

        self.setGeometry(80, 50, self.window_width, self.window_height)
        self.setMinimumSize(self.window_width, self.window_height)
        self.setWindowTitle(program_name)
        self.setFixedSize(self.window_width, self.window_height)

        global_log.info("Load Container GUI")
        self.Container()
        global_log.info("Start Selenium")
        self.seleniumAuto = ThreadClass(parent=None)
        self.seleniumAuto.update_status_signal.connect(
            self.CallThreadUpdateStatus)
        self.seleniumAuto.update_progress_signal.connect(
            self.CallThreadUpdateProgress)
        self.seleniumAuto.start()

    def Container(self):
        self.text_time = QLabel("Time: ", self)
        self.text_time.move(10, 12)
        self.input_from_time = QLineEdit("9", self)
        self.input_from_time.move(50, 10)
        self.text_time_line = QLabel("-", self)
        self.text_time_line.move(190, 12)
        self.input_to_time = QLineEdit("12", self)
        self.input_to_time.move(200, 10)

        self.text_clicks = QLabel("Clicks: ", self)
        self.text_clicks.move(10, 42)
        self.input_clicks = QLineEdit("1000", self)
        self.input_clicks.move(50, 40)

        self.text_time_delay = QLabel("Delay: ", self)
        self.text_time_delay.move(10, 72)

        self.radiobutton = QRadioButton("Random", self)
        self.radiobutton.setChecked(True)
        self.radiobutton.move(50, 72)

        self.radiobutton = QRadioButton("Other", self)
        self.radiobutton.setEnabled(False)
        self.radiobutton.move(150, 72)

        self.btn_run = QPushButton("Run", self)
        self.btn_run.clicked.connect(self.ActionRun)
        self.btn_run.move(50, 102)

        self.btn_stop = QPushButton("Stop", self)
        self.btn_stop.clicked.connect(self.ActionStop)
        self.btn_stop.move(150, 102)
        self.btn_stop.setEnabled(False)

        self.footerProgress = QProgressBar(self)
        self.footerProgress.setMaximum(10)
        self.footerProgress.move(10, self.window_height-30)
        self.footerProgress.setTextVisible(False)
        self.footerProgress.setValue(0)
        self.footerMessage = QLabel(
            "0/10, click remain: 1000, time delay: random", self)
        self.footerMessage.move(130, self.window_height-25)

    def ActionRun(self):
        global_log.info("Run Auto")
        self.seleniumAuto.is_run = True
        self.seleniumAuto.set_time_from = int(self.input_from_time.text())
        self.seleniumAuto.set_time_to = int(self.input_to_time.text())
        self.seleniumAuto.set_total_clicks = int(self.input_clicks.text())

    def ActionStop(self):
        pass

    def CallThreadUpdateStatus(self, temp_str):
        global_log.debug("CallThreadUpdateStatus: " + temp_str)
        self.footerMessage.setText(temp_str)

    def CallThreadUpdateProgress(self, temp_int):
        global_log.debug("CallThreadUpdateProgress: " + str(temp_int))
        self.footerProgress.setValue(temp_int)


def Main():
    app = QApplication(sys.argv)
    w = UIApp()
    w.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    Main()
