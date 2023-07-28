from bin.UI_MARVer import Ui_MainWindow
from src.marver_r.GuiLog import GuiLog


class EncounterPage:
    def __init__(self, ui: Ui_MainWindow = None, logger: GuiLog = None):
        self.__ui = ui
        self.__logger = logger

    def openConfigFilePage(self):
        self.__ui.SW_Main.setCurrentIndex(2)
        self.__ui.SW_MarverR.setCurrentIndex(0)

    def openPropertyFilePage(self):
        self.__ui.SW_Main.setCurrentIndex(2)
        self.__ui.SW_MarverR.setCurrentIndex(1)

    def openRuntimeVerificationPage(self):
        self.__ui.SW_Main.setCurrentIndex(2)
        self.__ui.SW_MarverR.setCurrentIndex(2)

    def openNewProject(self):
        pass

    def openExistProject(self):
        pass
