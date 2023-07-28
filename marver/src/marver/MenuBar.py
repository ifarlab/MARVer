from bin.UI_MARVer import Ui_MainWindow
from src.marver_r.GuiLog import GuiLog
from src.marver_r.GuiMonitor import GuiMonitor
from src.marver.Project import Project
from src.marver_m.GuiModelDesign import GuiModelDesign
import json
from PyQt5.QtWidgets import *


import os
import signal
import subprocess


class MenuBar:
    def __init__(self, ui: Ui_MainWindow = None, project: Project = None, logger: GuiLog = None,
                 guiMonitor: GuiMonitor = []):
        self.__ui = ui
        self.__project = project
        self.__logger = logger
        self.__guiMonitor = guiMonitor
        self.__guiModelDesign = GuiModelDesign(self.__ui)

    def actionConfigFilePage(self):
        self.__ui.SW_Main.setCurrentIndex(2)
        self.__ui.SW_MarverR.setCurrentIndex(0)

    def actionPropertyFilePage(self):
        self.__ui.SW_Main.setCurrentIndex(2)
        self.__ui.SW_MarverR.setCurrentIndex(1)

    def actionRuntimeVerificationPage(self):
        self.__ui.SW_Main.setCurrentIndex(2)
        self.__ui.SW_MarverR.setCurrentIndex(2)

    def actionOpenUppaalBlock(self):
        self.__ui.SW_Main.setCurrentIndex(1)
        self.__guiModelDesign.startModelEditor()
    
    def actionAt(self):
        self.__ui.SW_Main.setCurrentIndex(7)
        subprocess.Popen('cd attackService && python py_ROSAttacktool.py', stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 

    def actionAd(self):
        self.__ui.SW_Main.setCurrentIndex(6)
        subprocess.Popen('cd adService && python ad_main.py', stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
        print("action ad")

    def actionOdt(self):
        self.__ui.SW_Main.setCurrentIndex(3)
        self.__ui.W_MARVerS.setCurrentIndex(0)
    def actionOma(self):
        self.__ui.SW_Main.setCurrentIndex(3)
        self.__ui.W_MARVerS.setCurrentIndex(1)
        
        
    def actionUPPAALData(self):
        self.__ui.SW_Main.setCurrentIndex(5)

    def actionUPPAALVisual(self):
        self.__ui.SW_Main.setCurrentIndex(4)

    def actionClose(self):
        self.__ui.SW_Main.setCurrentIndex(0)

    def actionSave(self):
        try:
            content = {"RosFolderPath": self.__project.getRosPath(),
                       "ConfFilePath": self.__project.getConfFilePath(),
                       "PropertyFilePath": self.__project.getPropertyFilePath(),
                       "ProjectFilePath": self.__project.getProjectFilePath()}
            path = self.openFolderDialogWindow()
            with open(path[0] + ".json", 'w') as json_file:
                json.dump(content, json_file)
        except Exception as e:
            print(e)

    def actionOpenProject(self):
        try:
            fileName = self.openFileDialogWindow()
            with open(fileName, 'r') as json_file:
                content = json.load(json_file)
                self.__project.setRosPath(content["RosFolderPath"])
                self.__project.setConfFilePath(content["ConfFilePath"])
                self.__project.setPropertyFilePath(content["PropertyFilePath"])
                self.__project.setProjectFilePath(content["ProjectFilePath"])
        except Exception as e:
            print(e)

    def actionNewProject(self):
        try:
            self.__project.setProjectFilePath(self.openFolderDialogWindow()[0])

        except Exception as e:
            print(e)

    def openFileDialogWindow(self) -> str:
        try:
            path = QFileDialog.getOpenFileName(None, "Open File", "../",
                                               "Text Files (*.json)")
            if path:
                self.__logger.printLog(message="File selection completed successfully", color="green")
                return path[0]
            else:
                raise IOError(f"An error occurred while opening the file")
        except IOError:
            self.__logger.printLog(message=f"An error occurred while opening the file", color="red")
        except:
            self.__logger.printLog(message="ERROR in openFileDialogWindow()", color="red")

    def openFolderDialogWindow(self):
        try:
            rosWsFolder = QFileDialog.getSaveFileName(None, "Select your catkin_ws folder", "../")
            if rosWsFolder:
                self.__logger.printLog(message="Folder selection completed successfully", color="green")
                return rosWsFolder
            else:
                raise IOError(f"An error occurred while opening the folder")
        except IOError:
            self.__logger.printLog(message=f"An error occurred while opening the folder", color="red")
        except:
            self.__logger.printLog(message="An error is occurred in openFolderDialogWindow()", color="red")
