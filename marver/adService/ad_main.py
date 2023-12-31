# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window_v4.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.



from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy as np
import pyqtgraph as pg
from random import randint
import rospy
from std_msgs.msg import Float32, String
from anomaly import cls_AnomalyDetection

freq =[100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100]
#freq = [0.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi("main_window_v4.ui", self)
        self.resize(826, 596)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 0, 801, 70))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_1 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_1.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_1.setObjectName("gridLayout_1")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout_1.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_1.addWidget(self.label_2, 1, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout_1.addWidget(self.label_8, 0, 0, 1, 1)
        self.list_ADtypes = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.list_ADtypes.setObjectName("list_ADtypes")
        self.list_ADtypes.addItem("Statistical-based")
        self.gridLayout_1.addWidget(self.list_ADtypes, 1, 1, 1, 1)
        self.list_NodevsNetwork = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.list_NodevsNetwork.setObjectName("list_NodevsNetwork")
        self.list_NodevsNetwork.addItem("Chose AD focus")
        self.list_NodevsNetwork.addItem("Node-based")
        self.list_NodevsNetwork.addItem("Network-based")
        self.gridLayout_1.addWidget(self.list_NodevsNetwork, 1, 3, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 80, 801, 124))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_13 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 1, 5, 1, 1)
        self.spinbox_timeInterval = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.spinbox_timeInterval.setMinimum(0.0)
        self.spinbox_timeInterval.setObjectName("spinbox_timeInterval")
        self.gridLayout_2.addWidget(self.spinbox_timeInterval, 1, 1, 1, 1)
        self.spinbox_lowerLimit = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.spinbox_lowerLimit.setMinimum(0.0)
        self.spinbox_lowerLimit.setObjectName("spinbox_lowerLimit")
        self.gridLayout_2.addWidget(self.spinbox_lowerLimit, 2, 1, 1, 1)
        self.spinbox_sensitivity = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.spinbox_sensitivity.setMinimum(0.0)
        self.spinbox_sensitivity.setObjectName("spinbox_sensitivity")
        self.gridLayout_2.addWidget(self.spinbox_sensitivity, 2, 4, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 4)
        self.label_14 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 2, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.spinbox_upperLimit = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.spinbox_upperLimit.setMinimum(0.0)
        self.spinbox_upperLimit.setMaximum(300.0)
        
        self.spinbox_upperLimit.setObjectName("spinbox_upperLimit")
        self.gridLayout_2.addWidget(self.spinbox_upperLimit, 1, 4, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 3, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 1, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 2, 3, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 3, 0, 1, 1)
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 210, 801, 61))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_11 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 1, 0, 1, 2)
        self.btn_sniffNetworkforNodes = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.btn_sniffNetworkforNodes.setObjectName("btn_sniffNetworkforNodes")
        self.gridLayout_3.addWidget(self.btn_sniffNetworkforNodes, 0, 1, 1, 1)
        self.combobox_nodeList = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.combobox_nodeList.setObjectName("combobox_nodeList")
        self.combobox_nodeList.addItem("All nodes")
        self.gridLayout_3.addWidget(self.combobox_nodeList, 0, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 0, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 500, 801, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_startTraffic = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_startTraffic.setObjectName("btn_startTraffic")
        self.horizontalLayout.addWidget(self.btn_startTraffic)
        self.btn_endTraffic = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_endTraffic.setObjectName("btn_endTraffic")
        self.horizontalLayout.addWidget(self.btn_endTraffic)
        self.btn_startAD = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_startAD.setObjectName("btn_startAD")
        self.horizontalLayout.addWidget(self.btn_startAD)
        self.btn_endAD = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_endAD.setObjectName("btn_endAD")
        self.horizontalLayout.addWidget(self.btn_endAD)
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(10, 280, 801, 211))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayoutPlot = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayoutPlot.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutPlot.setObjectName("gridLayoutPlot")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 826, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        
        #ED Start#####################################################3
        """
        self.label_8.setStyleSheet("font-weight: bold")
        self.label_3.setStyleSheet("font-weight: bold")
        self.label_9.setStyleSheet("font-weight: bold")
        self.label_11.setStyleSheet("font-weight: bold")
        """
        self.time_interval = 10  # for obtaining sound
        self.lowerbound = 75  # for obtaining sound
        self.upperbound = 110
        self.senscutoff = 10  # update plot every 30/1000 second
        self.spinbox_lowerLimit.setValue(self.lowerbound)
        self.spinbox_upperLimit.setValue(self.upperbound)
        self.spinbox_sensitivity.setValue(self.senscutoff)
        self.spinbox_timeInterval.setValue(self.time_interval)
        
        self.pushButton.clicked.connect(self.save_preferences)
        self.update_plot = False
        self.btn_endTraffic.setEnabled(False)
        self.btn_endAD.setEnabled(False)

        self.adstatus = False
        self.adCounter = 0

        self.btn_startTraffic.clicked.connect(self.start_worker)
        self.btn_endTraffic.clicked.connect(self.stop_worker)
        self.worker = False
        self.go_on = None
        self.tmp = 0
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setYRange(0,100)
        #self.graphWidget.setGeometry(QtC,ore.QRect(10, 20, 10, 181))
        #self.graphWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding)
        #self.setCentralWidget(self.graphWidget)
        self.ui.gridLayoutPlot.addWidget(self.graphWidget, 2, 1, 1, 1)
        
        self.x = list(range(100))  # 100 time points
        self.y = freq # 100 data points
        
        self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))     
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)

        #self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        #self.go_on==False
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.time_interval)
           
        #ED-END^#############################################3

        self.btn_startAD.clicked.connect(self.start_AnomalyDetection)
        self.btn_endAD.clicked.connect(self.stop_AnomalyDetection)
        self.btn_sniffNetworkforNodes.clicked.connect(self.search_NodesInNetwork)
        #self.retranslateUi(self)
        #QtCore.QMetaObject.connectSlotsByName(self)
    #button save-preferences 

    def search_NodesInNetwork(self):
        print("do. smt.")
        self.arr = ["Master Node", "Simulation Node", "Controller Node", "Verification Node"]
        for i in range(len(self.arr)):
            self.combobox_nodeList.addItem(self.arr[i])

    def save_preferences(self):
        self.time_interval = self.spinbox_timeInterval.value()  # for obtaining sound
        self.lowerbound = self.spinbox_lowerLimit.value()  # for obtaining sound
        self.upperbound = self.spinbox_upperLimit.value()
        self.senscutoff = self.spinbox_sensitivity.value()  # update plot every 30/1000 second
 
    def start_AnomalyDetection(self):
        self.save_preferences()
        self.adstatus = True
        self.AD = cls_AnomalyDetection(self.time_interval, self.upperbound, self.lowerbound, self.senscutoff)
        self.btn_startAD.setEnabled(False)
        self.btn_endAD.setEnabled(True)
    

    def stop_AnomalyDetection(self):
        self.adstatus = False
        self.btn_startAD.setEnabled(True)
        self.btn_endAD.setEnabled(False)
    
    def start_worker(self):
        self.update_plot = True
        self.btn_startTraffic.setEnabled(False)
        self.btn_endTraffic.setEnabled(True)

    def stop_worker(self):
        self.update_plot = False
        self.btn_startTraffic.setEnabled(True)
        self.btn_endTraffic.setEnabled(False)



    def update_plot_data(self):     
        if self.update_plot:   
            self.x = self.x[1:]  # Remove the first y element.
            self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

            self.y = self.y[1:]  # Remove the first
            #self.y.append(randint(0,100))  # Add a new random value.
            
            self.base = 100
            self.newdata = self.base + self.tmp
            self.y = freq
            self.tmp = self.tmp + 1
            #print(self.tmp)
            self.data_line.setData(self.x, self.y)  # Update the data.

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ADSer: Anomaly Detection Service"))
                

        
        self.label.setText(_translate("MainWindow", "Anomaly Detection Type:"))
        self.label_2.setText(_translate("MainWindow", "Anomaly Detection Focus:"))
        self.label_8.setText(_translate("MainWindow", "General Preferences"))
        self.list_ADtypes.setItemText(0, _translate("MainWindow", "Statistical-based"))
        self.list_NodevsNetwork.setItemText(0, _translate("MainWindow", "Choose AD focus"))
        self.list_NodevsNetwork.setItemText(1, _translate("MainWindow", "Node-based"))
        self.list_NodevsNetwork.setItemText(2, _translate("MainWindow", "Network-based"))
        self.label_13.setText(_translate("MainWindow", "freq."))
        self.label_3.setText(_translate("MainWindow", "Statistical Feature Preferences"))
        self.label_14.setText(_translate("MainWindow", "freq."))
        self.label_4.setText(_translate("MainWindow", "Time Interval:"))
        self.label_6.setText(_translate("MainWindow", "Starting Lower Bound:"))
        self.label_5.setText(_translate("MainWindow", "Starting Upper Bound:"))
        self.label_12.setText(_translate("MainWindow", "sec."))
        self.label_7.setText(_translate("MainWindow", "Sensitivity:"))
        self.pushButton.setText(_translate("MainWindow", "Save Preferences"))
        self.label_11.setText(_translate("MainWindow", "ROS Network Traffic Flow"))
        self.btn_sniffNetworkforNodes.setText(_translate("MainWindow", "Search for all nodes in ROS Network"))
        self.combobox_nodeList.setItemText(0, _translate("MainWindow", "All Nodes"))
        self.combobox_nodeList.setItemText(1, _translate("MainWindow", "Node 1"))
        self.combobox_nodeList.setItemText(2, _translate("MainWindow", "Node 2"))
        self.label_10.setText(_translate("MainWindow", "Node List:"))
        self.label_9.setText(_translate("MainWindow", "Node Preferences"))
        self.btn_startTraffic.setText(_translate("MainWindow", "Start Plot ROS Network Traffic"))
        self.btn_endTraffic.setText(_translate("MainWindow", "End Real-time Plot"))
        self.btn_startAD.setText(_translate("MainWindow", "Start Anomaly Detection"))
        self.btn_endAD.setText(_translate("MainWindow", "End Anomaly Detection"))



app = QtWidgets.QApplication(sys.argv)


def callback(data):

    freq.pop(0)
    freq.append(float(data.data))
    mainWindow.update_plot_data()
    if mainWindow.adstatus:
        if mainWindow.adCounter >= 10:
            #print(freq)
            ad_status_bool = mainWindow.AD.AnomalyDetection(freq)
            mainWindow.adCounter = 0
            print("anomaly result",ad_status_bool)
            msg = ''
            if ad_status_bool:
                msg = 'True'
            else:
                msg = 'False'
            adpub.publish(msg)

        else:
            mainWindow.adCounter += 1

        
    
def listener():
    global adpub
    rospy.init_node('ad_listen', anonymous=False)
    rospy.Subscriber("ControllerFreq", Float32, callback)
    adpub = rospy.Publisher('adResult', String, queue_size=10)


if __name__ == "__main__":
    mainWindow = MainWindow()
    listener()
    mainWindow.show()
    sys.exit(app.exec_())

