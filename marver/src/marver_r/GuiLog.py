from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from bin.UI_MARVer import Ui_MainWindow
import time

colorTimer = 0

class GuiLog:
    
    def __init__(self, ui: Ui_MainWindow = None):
        self.__ui = ui

    def printLog(self, message: str = None, color: str = None):
        item = QListWidgetItem(message)
        if color == "red":
            item.setForeground(Qt.red)
        elif color == "green":
            item.setForeground(Qt.green)
        elif color == "yellow":
            item.setForeground(Qt.yellow)
        elif color == "blue":
            item.setForeground(Qt.blue)
        else:
            item.setForeground(Qt.black)

        self.__ui.lwLog.addItem(item)
        self.__ui.lwLog.scrollToBottom()


    def printMonitorResult(self, message: str = None, color: str = None):
        item = QListWidgetItem(message)
        
        if color == "red":
            item.setForeground(Qt.red)
        elif color == "green":
            item.setForeground(Qt.green)
        elif color == "yellow":
            item.setForeground(Qt.yellow)
        elif color == "blue":
            item.setForeground(Qt.blue)
        else:
            item.setForeground(Qt.black)            
            
        self.__ui.lwMonitorOnlineResult.addItem(item)
        self.__ui.lwMonitorOnlineResult.scrollToBottom()


    def setColorTimer(self):
        global colorTimer
        colorTimer = 3

    def changeColor(self):
        global colorTimer
        while True:
            if colorTimer <= 0:
                self.__ui.label_8.setStyleSheet("background-color: green")
            else:
                self.__ui.label_8.setStyleSheet("background-color: red")
            time.sleep(1)
            colorTimer -= 1
        