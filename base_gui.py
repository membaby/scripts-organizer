import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import json
import subprocess
import psutil
import logging
import datetime
from threading import Thread
import time
import schedule

TITLE = 'Basic GUI Scraper'
Tk().withdraw()
logger = ''
loggingPATH = os.getcwd() + os.sep + 'logging'
os.makedirs(loggingPATH, exist_ok=True)

try:
   with open('settings.json', 'r+', encoding='utf8') as file:
      cache = json.loads(file.read())
      for scraper in cache['scrapers']:
         scraper['status'] = 0
except:
   with open('settings.json', 'w+', encoding='utf8') as file:
      cache = {'scrapers': []}
      json.dump(cache , file, indent = 4)

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def startScraper(id):
   if cache['scrapers'][int(id)]['status']:
      return
   name = cache['scrapers'][int(id)]['name']
   sche = cache['scrapers'][int(id)]['schedule']
   run_time = cache['scrapers'][int(id)]['time']
   if len(run_time.split(':')[0]) < 2:
      run_time = '0' + run_time
   def run():
      pro = []
      def start_scraper():
         logger.info(f'Scraper starting. NAME: {name} - Scheduled: {sche}')
         cache['scrapers'][int(id)]['lastRun'] = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
         cache['scrapers'][int(id)]['status'] = 1
         cmd = cache['scrapers'][int(id)]['cmd']
         print(cmd)
         updateSettings()
         pro.append(subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP))

      start_scraper()

      if sche == 'Hourly':
         schedule.every(1).hours.do(start_scraper)
      elif sche == '4 Hours':
         schedule.every(4).hours.do(start_scraper)
      elif sche == 'Daily':
         schedule.every().day.at(run_time).do(start_scraper)
      
      if sche != 'Not Scheduled':
         while cache['scrapers'][int(id)]['status']:
            schedule.run_pending()
            if not pro[-1].poll() is None and cache['scrapers'][int(id)]['status'] != 2:
               cache['scrapers'][int(id)]['status'] = 2
               updateSettings()
            else:
               time.sleep(1)
      else:
         pro[-1].wait()

      pro[-1].terminate()
      cache['scrapers'][int(id)]['status'] = 0
      logger.info(f'Scraper terminated. NAME: {name}')
      updateSettings()

   Thread(target=run, args=()).start()

def stopScraper(id):
   cache['scrapers'][int(id)]['status'] = 0

def addScraper(name, path, arguments, schedule, run_time, input, output):
   if not input.strip():
      input = 'x'
   if not output.strip():
      output = 'x'
   cache['scrapers'].append({
      'name': name,
      'path': path,
      'cmd': f'python {path} {arguments} {input} {output}',
      'schedule': schedule,
      'time': run_time,
      'lastRun': 0,
      'status': 0
   })
   updateSettings()
   logger.info(f'Added a new scraper: NAME: {name}, PATH: {path}')

def updateSchedule(id):
   schedules = ['Not Scheduled', 'Hourly', '4 Hours', 'Daily']
   cur_schedule_index = schedules.index(cache['scrapers'][id]['schedule'])
   if cur_schedule_index == len(schedules)-1:
      cur_schedule_index = -1
   next_schedule = schedules[cur_schedule_index+1]
   cache['scrapers'][int(id)]['schedule'] = next_schedule
   logger.info(f'Scraper schedule changed: ID: {id}, SCHEDULE: {next_schedule}')
   updateSettings()


UPDATEGUINOW = True

def updateSettings():
   global UPDATEGUINOW
   with open('settings.json', 'w+', encoding='utf8') as file:
      json.dump(cache , file, indent = 4)
   UPDATEGUINOW = True

def deleteScraper(id):
   cache['scrapers'].pop(id)
   updateSettings()

temp_cache = ''
class GUIScraper(QWidget):
   def __init__(self, parent = None):
      super(GUIScraper, self).__init__(parent)
      self.setFixedSize(620, 320)
      self.setWindowTitle(TITLE)
      self.setWindowIcon(QIcon('icons/icon.png'))

      grid = QGridLayout()
      self.setLayout(grid)

      # Button Widgets
      self.btn_START = QPushButton("START")
      self.btn_STOP = QPushButton("FORCE STOP")
      self.btn_SCHEDULE = QPushButton("SCHEDULE")
      self.btn_LOGS = QPushButton("LOGS")
      self.btn_ADD = QPushButton("ADD NEW")
      self.btn_REM = QPushButton("DELETE")
      self.btn_CLOSE = QPushButton("CLOSE")

      # Tree Widget
      self.panel = QTreeWidget()
      self.panel.setColumnCount(5)
      self.panel.setHeaderLabels(['ID', 'Scraper', 'Status', 'Schedule', 'Last Run'])
      self.panel.setColumnWidth(0, 25)
      self.panel.setColumnWidth(1, 175)
      self.panel.setColumnWidth(2, 100)
      self.panel.setColumnWidth(3, 100)
      self.panel.setColumnWidth(4, 100)

      # Label Widgets
      self.lbl_PERFORMANCE = QLabel('CPU: 0 - RAM: 0')
      self.lbl_PROGRESS = QLabel('Nothing is Running')

      grid.addWidget(self.panel, 2, 0, 9, 1)

      grid.addWidget(self.btn_START, 3, 2)
      grid.addWidget(self.btn_STOP, 4, 2)
      grid.addWidget(self.btn_SCHEDULE, 5, 2)
      grid.addWidget(self.btn_LOGS, 6, 2)
      grid.addWidget(self.btn_ADD, 7, 2)
      grid.addWidget(self.btn_REM, 8, 2)
      grid.addWidget(self.btn_CLOSE, 10, 2)

      grid.addWidget(self.lbl_PERFORMANCE, 11, 0)
      
      self.btn_ADD.clicked.connect(self.show_add_window)
      self.btn_REM.clicked.connect(lambda x: deleteScraper(int(self.panel.selectedItems()[0].text(0))) if self.panel.selectedItems() else True)
      self.btn_CLOSE.clicked.connect(lambda x: self.close())
      self.btn_LOGS.clicked.connect(lambda x: subprocess.Popen(f'explorer /select,"{loggingPATH}"'))
      self.btn_SCHEDULE.clicked.connect(lambda x: updateSchedule(int(self.panel.selectedItems()[0].text(0))) if self.panel.selectedItems() else True)
      self.btn_START.clicked.connect(lambda x: startScraper(int(self.panel.selectedItems()[0].text(0))) if self.panel.selectedItems() else True)
      self.btn_STOP.clicked.connect(lambda x: stopScraper(int(self.panel.selectedItems()[0].text(0))) if self.panel.selectedItems() else True)
      self.actionExit = self.findChild(QAction, "actionExit")

      # self.updatePanel()
      timer = QTimer(self)
      timer.timeout.connect(self.updateCPU)
      timer.timeout.connect(self.isCacheChanged)
      timer.start(1000)

   def closeEvent(self, event):
      confirmed = False
      for scraper in cache['scrapers']:
         if scraper['status'] and not confirmed:
            close = QMessageBox.question(self, "QUIT", "Are you sure want to stop process?", QMessageBox.Yes | QMessageBox.No)
            if close == QMessageBox.Yes:
               confirmed = True
            else:
               event.ignore()
               return

         if confirmed:
            scraper['status'] = 0
            stopScraper(cache['scrapers'].index(scraper))

      ignore_ = False
      for scraper in cache['scrapers']:
         if scraper['status']:
            ignore_ = True
      if ignore_:
         event.ignore()
      else:
         event.accept()

   def updatePanel(self):
      self.panel.clear()
      for scraper in cache['scrapers']:
         index = cache['scrapers'].index(scraper)
         name = cache['scrapers'][index]['name']
         schedule = cache['scrapers'][index]['schedule']
         lastRun = cache['scrapers'][index]['lastRun']
         status = cache['scrapers'][index]['status']
         status = 'Running' if status == 1 else 'Idle' if status == 2 else 'Not Running'
         item = QTreeWidgetItem(self.panel, [str(index), name, status, str(schedule), str(lastRun)])
         if status == 'Running':
            item.setForeground(2, QBrush(QColor("#4F8A06")))
         elif status == 'Idle':
            item.setForeground(2, QBrush(QColor("#8A6F06")))
         else:
            item.setForeground(2, QBrush(QColor("#ff0000")))

   def show_add_window(self):
      w = AddScraperWindow()
      w.show()
   
   def updateCPU(self):
      self.lbl_PERFORMANCE.setText(f'CPU: {psutil.cpu_percent()}% - RAM: {psutil.virtual_memory().percent}%')

   def isCacheChanged(self):
      global UPDATEGUINOW
      if UPDATEGUINOW:
         self.updatePanel()
         UPDATEGUINOW = False

class AddScraperWindow(QWidget):
   def __init__(self):
      super().__init__()
      self.setFixedSize(500, 240)
      self.setWindowTitle('Add Scraper')
      self.setWindowIcon(QIcon('icons/add.png'))

      grid = QGridLayout()
      self.setLayout(grid)

      self.lbl_NAME = QLabel("Name:")
      self.lbl_SCHEDULE = QLabel("Schedule:")
      self.lbl_TIME = QLabel("Time:")
      self.lbl_PATH = QLabel("Path:")
      self.lbl_INPUT = QLabel('Input:')
      self.lbl_OUTPUT = QLabel('Output:')
      self.lbl_ARGS = QLabel("Arguments:")
      

      self.txt_NAME = QLineEdit()
      self.txt_PATH = QLineEdit()
      self.txt_ARGS = QLineEdit()
      self.txt_INPUT = QLineEdit()
      self.txt_OUTPUT = QLineEdit()
      self.txt_schedule_time = QLineEdit('00:00')

      self.cmbo_SCHEDULE = QComboBox()
      self.cmbo_SCHEDULE.addItem("Not Scheduled")
      self.cmbo_SCHEDULE.addItem("Hourly")
      self.cmbo_SCHEDULE.addItem("4 Hours")
      self.cmbo_SCHEDULE.addItem("Daily")

      self.btn_BROWSE1 = QPushButton("BROWSE")
      self.btn_BROWSE2 = QPushButton("BROWSE")
      self.btn_BROWSE3 = QPushButton("BROWSE")
      self.btn_CREATE = QPushButton("ADD")

      grid.addWidget(self.lbl_NAME, 0, 0)
      grid.addWidget(self.lbl_SCHEDULE, 1, 0)
      grid.addWidget(self.lbl_TIME, 2, 0)
      grid.addWidget(self.lbl_PATH, 3, 0)
      grid.addWidget(self.lbl_INPUT, 4, 0)
      grid.addWidget(self.lbl_OUTPUT, 5, 0)
      grid.addWidget(self.lbl_ARGS, 6, 0)
      
      grid.addWidget(self.txt_NAME, 0, 1, 1, 2)
      grid.addWidget(self.txt_schedule_time, 2, 1, 1, 2)
      grid.addWidget(self.txt_PATH, 3, 1)
      grid.addWidget(self.txt_INPUT, 4, 1)
      grid.addWidget(self.txt_OUTPUT, 5, 1)
      grid.addWidget(self.txt_ARGS, 6, 1, 1, 2)
      grid.addWidget(self.cmbo_SCHEDULE, 1, 1, 1, 2)
      grid.addWidget(self.btn_BROWSE1, 3, 2)
      grid.addWidget(self.btn_BROWSE2, 4, 2)
      grid.addWidget(self.btn_BROWSE3, 5, 2)
      grid.addWidget(self.btn_CREATE, 7, 0, 1, 3)

      self.btn_BROWSE1.clicked.connect(lambda x: self.txt_PATH.setText(selectFile()))
      self.btn_BROWSE2.clicked.connect(lambda x: self.txt_INPUT.setText(selectFile()))
      self.btn_BROWSE3.clicked.connect(lambda x: self.txt_OUTPUT.setText(selectFile()))
      self.btn_CREATE.clicked.connect(lambda x: 
         addScraper(self.txt_NAME.text(), self.txt_PATH.text(), self.txt_ARGS.text(), self.cmbo_SCHEDULE.currentText(), self.txt_schedule_time.text(), self.txt_INPUT.text(), self.txt_OUTPUT.text())
         if self.txt_NAME.text() and self.txt_PATH.text() else True
      )
      self.btn_CREATE.clicked.connect(lambda x: self.close())

def selectFile():
   while True:
      file = askopenfilename(title = "Select a File")
      if file:
         break
   return file

def initialize_logging():
   global logger
   todays_date = datetime.datetime.now().strftime('%d-%m-%Y')
   logging.basicConfig(filename='logging' + os.sep + todays_date+"_gui.log", format='%(asctime)s [%(levelname)s] %(message)s', filemode='a+')
   logger = logging.getLogger()
   logger.setLevel(logging.INFO)
   handler = logging.StreamHandler(sys.stdout)
   handler.setLevel(logging.DEBUG)
   formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
   handler.setFormatter(formatter)
   logger.addHandler(handler)
   logger.info('GUI started.')

initialize_logging()
app = QApplication(sys.argv)
ex = GUIScraper()
ex.show()
sys.exit(app.exec_())