import os
import sys
import time
import subprocess
import datetime
from book import *
from model import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    
    def _d(fname, p=[] , verbose=True):
      for pack in open(fname):
        p.append(pack)
        subprocess.check_call([sys.executable, "-m", "pip", "install", pack])

    r = _d('requirements.txt') if not len([i for i in os.listdir(os.getcwd()) if i[-4:] == '.csv']) else 0
    if r: print(f'Downloading the following dependcies {p}')

    self.setWindowTitle("Bookeo App")
    self.setGeometry(100, 100, 600, 400)

    list_of_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                      'August', 'September', 'October', 'November', 'December']    
    
    #date comboboxes
    self.date_labels = QLabel("Pick Dates to compare")
    self.combobox1, self.combobox2 = QComboBox(self), QComboBox(self)
    now = datetime.datetime.now()
    for i in range(len(list_of_months)):
      for j in range(2017, 2050):
        if j < now.year + 1:
          self.combobox1.addItem(list_of_months[i]+' '+str(j))
          self.combobox2.addItem(list_of_months[i]+' '+str(j))

    layout = QVBoxLayout()
    layout.addWidget(self.date_labels)
    layout.addWidget(self.combobox1)
    layout.addWidget(self.combobox2)

    #step combobox
    self.step_label = QLabel("Choose step length")
    self.step_combo = QComboBox(self) 
    self.step_combo.addItem('Yearly')
    self.step_combo.addItem('Monthly')
    layout.addWidget(self.step_label)
    layout.addWidget(self.step_combo)

    #textboxes
    self.textbox1 = QLineEdit(self)
    self.textbox1.move(280, 40)
    self.textbox2 = QLineEdit(self)
    self.textbox2.move(280, 40)   
    self.textbox3 = QLineEdit(self)
    self.textbox3.move(280, 40) 
    
    self.textbox1.setPlaceholderText('Enter username')
    self.textbox2.setPlaceholderText('Enter password')
    self.textbox2.setEchoMode(QLineEdit.Password)

    layout.addWidget(self.textbox1)
    layout.addWidget(self.textbox2)

    self.label = QLabel(self)
    self.label.setGeometry(10, 10, 10, 10)
    self.label2 = QLabel(self)
    self.label.setGeometry(10, 10, 10, 10) 
    self.done_label = QLabel(self)
    self.done_label.setGeometry(10, 10, 10, 10)
    
    layout.addWidget(self.label)
    layout.addWidget(self.label2)

    button = QPushButton("Click to confirm the selected months", self)
    button.pressed.connect(self.get_domain)
    button2 = QPushButton("Compare", self)
    button2.pressed.connect(self.confirm)
    button3 = QPushButton("Close Bookeo App", self) 
    button3.pressed.connect(self._terminate)
    layout.addWidget(self.done_label) 
    layout.addWidget(button)
    layout.addWidget(button2)
    layout.addWidget(button3) 
    container = QWidget()
    container.setLayout(layout)
    self.setCentralWidget(container)
   
  def get_domain(self):
    self.label.setText("Start Month : "+self.combobox1.currentText()+' '+self.combobox2.currentText())
 
  def my(self):
    return self.step_combo.currentText()
    
  def confirm(self):
    ystep = self.my() == 'Yearly'
    u = None
    value = 0
    b = Book(1, 1)
    b.get_bookeo()
    b.sign_in(self.textbox1.text(), self.textbox2.text())
    b.move_to_marketing()
    d1, d2 = self.combobox1.currentText().split(' '), self.combobox2.currentText().split(' ')
    if ystep:
      u = b.gac_yearly(d1[0], int(d1[1]), int(d2[1]))
    else: 
      u = b.gac_month_to_month(d1[0], int(d1[1]), d2[0], int(d2[1]))
    b.close_crawler()
    s = [f.name for f in os.scandir('.') if f.is_file() and f.name[-4:] =='.csv']
    m = Model(s[0])
    revenue = m.get_revenue()
    dates = m.get_dates()
    data = m._setup(dates, revenue)
    overall_plot = m.overall_plot(dates, revenue)
    self.done_label.setText("Please check current folder for files generated")
    
  def _terminate(self):
    sys.exit()

app = QApplication(sys.argv)
qss="Hookmark.qss"
with open(qss,"r") as fh:
    app.setStyleSheet(fh.read())
widget = MainWindow()
widget.show()
sys.exit(app.exec_())
w = MainWindow()
w.show()
app.exec_()

