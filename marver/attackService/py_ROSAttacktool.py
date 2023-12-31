# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_ROSAttacktool.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
import os
import signal
import subprocess
import rospy
import time
from std_msgs.msg import String

import sys

from PyQt5.QtWidgets import QMessageBox, QHeaderView, QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi("gui_ROSAttacktool.ui", self)
        self.resize(883, 500)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 481, 210))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.btn_LoadAttackPreferences = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btn_LoadAttackPreferences.setObjectName("btn_LoadAttackPreferences")
        self.gridLayout_2.addWidget(self.btn_LoadAttackPreferences, 6, 2, 1, 1)
        self.btn_SaveAttackPreferences = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btn_SaveAttackPreferences.setObjectName("btn_SaveAttackPreferences")
        self.gridLayout_2.addWidget(self.btn_SaveAttackPreferences, 6, 1, 1, 1)
        self.spinBox_Duration = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
        self.spinBox_Duration.setObjectName("spinBox_Duration")
        self.gridLayout_2.addWidget(self.spinBox_Duration, 3, 1, 1, 1)
        self.list_AtackType = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.list_AtackType.setObjectName("list_AtackType")
        self.gridLayout_2.addWidget(self.list_AtackType, 1, 1, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 2, 1, 1)
        self.comboBox_DisAttConfig = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.comboBox_DisAttConfig.setObjectName("comboBox_DisAttConfig")
        self.gridLayout_2.addWidget(self.comboBox_DisAttConfig, 4, 1, 1, 2)
        self.comboBox_DisAttConfig.addItem("Stand-alone")
        self.comboBox_DisAttConfig.addItem("With-bots")
        self.comboBox_DisAttConfig.addItem("Bots Only")
        self.btn_Update = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btn_Update.setObjectName("btn_Update")
        self.gridLayout_2.addWidget(self.btn_Update, 5, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)
        self.btn_Delete = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btn_Delete.setObjectName("btn_Delete")
        self.gridLayout_2.addWidget(self.btn_Delete, 5, 1, 1, 1)
        self.btn_Append = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btn_Append.setObjectName("btn_Append")
        self.gridLayout_2.addWidget(self.btn_Append, 5, 0, 1, 1)
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 250, 481, 111))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 1, 1, 1)
        self.btn_startAttackBot = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_startAttackBot.setObjectName("btn_startAttackBot")
        self.gridLayout.addWidget(self.btn_startAttackBot, 3, 1, 1, 1)
        self.btn_stopAttackBot = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_stopAttackBot.setObjectName("btn_stopAttackBot")
        self.gridLayout.addWidget(self.btn_stopAttackBot, 3, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 1, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(500, 10, 371, 351))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.widget_List = QtWidgets.QWidget(self.gridLayoutWidget_3)
        self.widget_List.setObjectName("widget_List")
        self.gridLayout_3.addWidget(self.widget_List, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 883, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        #ED start####################################################
        self.dac = ""
        self.duration_val = 0

        self.tableWidget = QTableWidget()
        # set row count
        labels = [ "Attack Type", "Duration (min)"]
        self.tableWidget.setRowCount(8)
        # set column count
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(labels)

        list_attackdetails = [
            {'Attack Type': 'Idle', 'Duration (min)': '1'},
            {'Attack Type': 'NodeSwarm', 'Duration (min)': '2'},
            {'Attack Type': 'Idle', 'Duration (min)': '1'},
            {'Attack Type': 'DoS', 'Duration (min)': '2'},
            {'Attack Type': 'Idle', 'Duration (min)': '1'},
        ]
        row = 0
        for e in list_attackdetails:
            self.tableWidget.setItem(row, 0, QTableWidgetItem(e['Attack Type']))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(e['Duration (min)']))
            row += 1


        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # Add box layout, add table to box layout and add box layout to widget
        self.ui.gridLayout_3.addWidget(self.tableWidget, 1, 2, 1, 1)

        #btn clik codes
        self.btn_Append.clicked.connect(self.append)
        self.btn_Delete.clicked.connect(self.delete)
        self.btn_Update.clicked.connect(self.update)
        self.btn_SaveAttackPreferences.clicked.connect(self.save_AttackPreferences)
        self.btn_LoadAttackPreferences.clicked.connect(self.load_AttackPreferences)
        self.pushButton_4.clicked.connect(self.start_Attack)
        self.pushButton_3.clicked.connect(self.stop_Attack)
        self.btn_startAttackBot.clicked.connect(self.start_AttackBot)
        self.btn_stopAttackBot.clicked.connect(self.stop_AttackBot)
        #ED stop####################################################

    def append(self):
        dac = self.comboBox_DisAttConfig.currentText()
        duration_val = self.spinBox_Duration.value()  # for obtaining sound
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(dac))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(duration_val))
       
        print( "append",row)

    def delete(self):
        print( "delete")
        current_row = self.tableWidget.currentRow()
        if current_row < 0:
            return QMessageBox.warning(self, 'Warning','Please select a record to delete')

        button = QMessageBox.question(
            self,
            'Confirmation',
            'Are you sure that you want to delete the selected row?',
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        if button == QMessageBox.StandardButton.Yes:
            self.tableWidget.removeRow(current_row)

    def update(self):
        current_row = self.tableWidget.currentRow()
        print( "update")

    def save_AttackPreferences(self):
        print( "save_AttackPreferences")

    def load_AttackPreferences(self):
        print( "load_AttackPreferences")

    def start_Attack(self):
        def msgpublish(s):
            msg = String()
            msg.data = s
            for _ in range(3):
                pub.publish(msg)

        rospy.init_node('attackStateNode', anonymous=False)
        pub = rospy.Publisher("attackState", String, queue_size=10)

        AttackStr = "python SubscriberBomb.py 1000"
        #AttackStr = "hping3 -S 192.168.1.10 -a 192.168.1.13 --flood"
        #AttackStr = "hping3 --flood 192.168.1.13"

        f = open('AttackPlan.txt', 'r')
        cmds = f.readlines()
        sudo_password = 'toor'

        for cmd in cmds:
            cmd = cmd.replace('\n', '')
            subCmd = cmd.split(' ')

            if subCmd[0] == 'Normal':
                msgpublish('False')
                print('Idle Phase', int(subCmd[1]), 'min')
                time.sleep(int(subCmd[1]) * 60)    
            elif subCmd[0] == 'Attack':
                msgpublish('True')
                print('Attack Phase', int(subCmd[1]), 'min')
                pro = subprocess.Popen(AttackStr, stdout=subprocess.PIPE, 
                            shell=True, preexec_fn=os.setsid) 
                time.sleep(int(subCmd[1]) * 60)
                os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
            elif subCmd[0] == 'Start':
                print('Started')
                #os.system('echo '' > /home/**username**/ROSMonitoring/oracle/online_log.txt')
            elif subCmd[0] == 'End':
                print('Test is over. Do NOT forget to save your file!')
                #os.system('cp /home/**username**/ROSMonitoring/oracle/online_log.txt /home/**username**/ROSMonitoring/oracle/Data.txt ')


    def stop_Attack(self):
        print( "stop_Attack")

    def start_AttackBot(self):
        print( "start_AttackBot")    

    def stop_AttackBot(self):
        print( "stop_AttackBot")    


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Attack Preferences"))
        self.label_2.setText(_translate("MainWindow", "Attack Type: "))
        self.label_3.setText(_translate("MainWindow", "Duration: "))
        self.btn_LoadAttackPreferences.setText(_translate("MainWindow", "Load Attack Preferences"))
        self.btn_SaveAttackPreferences.setText(_translate("MainWindow", "Save Attack Preferences"))
        self.label_4.setText(_translate("MainWindow", "min"))
        self.btn_Update.setText(_translate("MainWindow", "Update"))
        self.label_5.setText(_translate("MainWindow", "Distrubuted Attack Config: "))
        self.btn_Delete.setText(_translate("MainWindow", "Delete"))
        self.btn_Append.setText(_translate("MainWindow", "Append"))
        self.pushButton_4.setText(_translate("MainWindow", "Start Attack"))
        self.btn_startAttackBot.setText(_translate("MainWindow", "Start Attack Bot"))
        self.btn_stopAttackBot.setText(_translate("MainWindow", "Stop Attack Bot"))
        self.label_7.setText(_translate("MainWindow", "Act as an Attack Bot Status"))
        self.pushButton_3.setText(_translate("MainWindow", "Stop Attack"))
        self.label_6.setText(_translate("MainWindow", "Attack Status"))


app = QtWidgets.QApplication(sys.argv)

if __name__ == "__main__":
    
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())