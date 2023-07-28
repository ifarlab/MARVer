from PyQt5.QtWidgets import *
from UI_MARVer import Ui_MainWindow
import sys
import getpass

tmp = r'/home/' + getpass.getuser() + r'/marver'
sys.path.append(tmp)

from src.marver_r.GuiConfig import GuiConfig
from src.marver_r.GuiVerifier import GuiVerifier
from src.marver_r.GuiLog import GuiLog
from src.marver_r.GuiMonitor import GuiMonitor
from src.marver.MenuBar import MenuBar
from src.marver.Project import Project
from src.marver.EncounterPage import EncounterPage
from include.marver_r.RMLOracle import RMLOracle
from include.marver_r.TLOracle import TLOracle
from src.marver_m.uppaalVisual.GuiUppaalVisual import GuiUppaalVisual
from src.marver_m.uppaalVisual.GuiUppaalData import GuiUppaalData
from include.marver_m.UppaalVisual.DataBaseConnection import DataBaseConnection
from src.marver_s.odt import ODT
from src.marver_s.oma import OMA
#from src.marver_s.ad import AD


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        self.setupComponents()
        self.initGui()

    def setupComponents(self):
        self.__monitor = []
        self.__rmlOracle = RMLOracle()
        self.__tlOracle = TLOracle()

        self.__project = Project()
        self.__guiLog = GuiLog(self.__ui)

        self.__guiUppaalData = GuiUppaalData(self.__ui, self.__guiLog)
        self.__guiUppaalVisual = GuiUppaalVisual(self.__ui, self.__guiUppaalData)

        self.__guiConfig = GuiConfig(self.__ui, self.__guiLog, self.__monitor)
        self.__guiVerifier = GuiVerifier(self.__ui, self.__guiLog, self.__monitor, self.__rmlOracle, self.__tlOracle)
        self.__guiMonitor = GuiMonitor(self.__ui, self.__project, self.__guiLog, self.__monitor)
        self.__guiODT = ODT(self.__ui)
        self.__guiOMA = OMA(self.__ui)
        #self.__guiAD = AD(self.__ui)


        self.__menuBar = MenuBar(self.__ui, self.__project, self.__guiLog, self.__guiMonitor)
        self.__encounterPage = EncounterPage(self.__ui, self.__guiLog)

    def initGui(self):
        ## Config file page
        self.__ui.btnConfigImportConf.clicked.connect(self.__guiConfig.importConfig)
        self.__ui.btnConfigNodeCreate.clicked.connect(self.__guiConfig.createNode)
        self.__ui.btnConfigTopicCreate.clicked.connect(self.__guiConfig.createTopic)
        self.__ui.btnConfigOracleCreate.clicked.connect(self.__guiConfig.createOracle)
        self.__ui.btnConfigMonitorCreate.clicked.connect(self.__guiConfig.createMonitor)
        self.__ui.btnConfigNodeUpdate.clicked.connect(self.__guiConfig.updateNode)
        self.__ui.btnConfigTopicUpdate.clicked.connect(self.__guiConfig.updateTopic)
        self.__ui.btnConfigOracleUpdate.clicked.connect(self.__guiConfig.updateOracle)
        self.__ui.btnConfigMonitorUpdate.clicked.connect(self.__guiConfig.updateMonitor)
        self.__ui.btnConfigNodeDelete.clicked.connect(self.__guiConfig.deleteNode)
        self.__ui.btnConfigTopicDelete.clicked.connect(self.__guiConfig.deleteTopic)
        self.__ui.btnConfigOracleDelete.clicked.connect(self.__guiConfig.deleteOracle)
        self.__ui.btnConfigMonitorDelete.clicked.connect(self.__guiConfig.deleteMonitor)
        self.__ui.cbxConfigNode.activated.connect(self.__guiConfig.setNodeComponentStatus)
        self.__ui.cbxConfigTopicTopic.activated.connect(self.__guiConfig.setTopicComponentStatus)
        self.__ui.cbxMonitorMonitor.activated.connect(self.__guiConfig.setMonitorComponentStatus)
        self.__ui.btnConfigSaveSave.clicked.connect(self.__guiConfig.saveConfig2file)
        self.__ui.cbxConfigTopicNode.activated.connect(self.__guiConfig.setTopicNodeComponentStatus)

        ## Property file page
        self.__ui.btnPropertyImport.clicked.connect(self.__guiVerifier.importProperty)
        self.__ui.btnPropertySave.clicked.connect(self.__guiVerifier.saveProperty2File)
        self.__ui.btnPropertyDefineCreate.clicked.connect(self.__guiVerifier.addProperty)
        self.__ui.btnPropertyDefineUpdate.clicked.connect(self.__guiVerifier.editProperty)
        self.__ui.btnPropertyDefineDelete.clicked.connect(self.__guiVerifier.deleteProperty)
        self.__ui.cbxPropertyDefineVerifier.activated.connect(self.__guiVerifier.setVerifierComponentsStatus)
        self.__ui.cbxPropertySaveType.activated.connect(self.__guiVerifier.updateVerifierSaveCbx)

        self.__ui.btnImportUppaalModel.clicked.connect(self.__guiVerifier.importUppaalModel)

        ## Runtime verification page
        self.__ui.btnMonitorConfFileSelect.clicked.connect(self.__guiMonitor.selectConfFile)
        self.__ui.btnMonitorROSFolderSelect.clicked.connect(self.__guiMonitor.selectROSWs)
        self.__ui.btnMonitorPropertyFileSelect.clicked.connect(self.__guiMonitor.selectPropertyFile)
        self.__ui.btnMonitorStartRV.clicked.connect(self.__guiMonitor.initializeRV)
        self.__ui.btnMonitorProjectFileSelect.clicked.connect(self.__guiMonitor.selectProjectFile)
        # self.__ui.TW_Config.currentChanged.connect(self.__guiVerifier.updateVerifierDefineCbx)
        self.__ui.btnMonitorStopRV.clicked.connect(self.__guiMonitor.stopRV)

        ## UPPAAL Visual page
        self.__ui.btnVisual_OpenLocal_Import.clicked.connect(self.__guiUppaalVisual.openFromLocal)
        self.__ui.lwVisual_ModelList.doubleClicked.connect(self.__guiUppaalVisual.listItemClicked)
        self.__ui.btnVisual_SaveQuery.clicked.connect(self.__guiUppaalVisual.saveQueryStates)
        self.__ui.btnVisual_OpenLocal_Export.clicked.connect(self.__guiUppaalData.save2Local)
        self.__ui.lwVisual_ModelList_2.doubleClicked.connect(self.__guiUppaalVisual.listItemClicked)

        ## UPPAAL Data page
        self.__ui.btnDatabase.clicked.connect(self.__guiUppaalData.DBconnection)
        self.__ui.btnDatabase.clicked.connect(self.__guiUppaalVisual.setDB)
        self.__ui.btnDatabase.clicked.connect(self.__guiUppaalData.fillLWFromDB)
        self.__ui.btnData_SaveDatabase.clicked.connect(self.__guiUppaalData.save2DataBase)
        self.__ui.btnData_GetDatabase.clicked.connect(self.__guiUppaalVisual.fillLWFromDB)
        self.__ui.lwVisual_ModelList_2.doubleClicked.connect(self.__guiUppaalData.listItemClicked)

        ## ODT page
        self.__ui.addCylinderButton.clicked.connect(self.__guiODT.addCylinder)
        self.__ui.removeCylinderButton.clicked.connect(self.__guiODT.removeCylinder)
        self.__ui.createXMLbutton.clicked.connect(self.__guiODT.getDataFromTable)

        ## OHT
        # TO DO

        ## OMA
        self.__ui.SaveAsButton.clicked.connect(self.__guiOMA.create_xml)
        # TO DO
        
        ## AD
        # TO DO
        
        ## AT
        # TO DO

        # Menu Bar - Actions
        self.__ui.actionConfig_File.triggered.connect(self.__menuBar.actionConfigFilePage)
        self.__ui.actionProperty_File.triggered.connect(self.__menuBar.actionPropertyFilePage)
        self.__ui.actionRuntime_Verification.triggered.connect(self.__menuBar.actionRuntimeVerificationPage)
        self.__ui.actionUppaalBlock.triggered.connect(self.__menuBar.actionOpenUppaalBlock)
        self.__ui.actionSave.triggered.connect(self.__menuBar.actionSave)
        self.__ui.actionClose.triggered.connect(self.clearProject)
        self.__ui.actionOpenProject.triggered.connect(self.__menuBar.actionOpenProject)
        self.__ui.actionNewProject.triggered.connect(self.__menuBar.actionNewProject)
        self.__ui.actionOdt.triggered.connect(self.__menuBar.actionOdt)
        self.__ui.actionOma.triggered.connect(self.__menuBar.actionOma)
        self.__ui.actionAd.triggered.connect(self.__menuBar.actionAd)
        self.__ui.actionAt.triggered.connect(self.__menuBar.actionAt)
        self.__ui.actionUppaalDB.triggered.connect(self.__menuBar.actionUPPAALData)
        self.__ui.actionUppaalModel.triggered.connect(self.__menuBar.actionUPPAALVisual)


        # Encounter Page
        # self.__ui.btnEntryNewProject.clicked.connect(self.__encounterPage.openNewProject)
        # self.__ui.btnEntryExistProject.clicked.connect(self.__encounterPage.openExistProject)
        # self.__ui.btnEntryConfigFile.clicked.connect(self.__encounterPage.openConfigFilePage)
        # self.__ui.btnEntryPropertyFile.clicked.connect(self.__encounterPage.openPropertyFilePage)
        # self.__ui.btnEntryRuntimeVerification.clicked.connect(self.__encounterPage.openRuntimeVerificationPage)

    def clearProject(self):
        self.setupComponents()
        self.initGui()
        self.__guiConfig.clearNodeComponents()
        self.__guiConfig.clearTopicComponents()
        self.__guiConfig.clearOracleComponents()
        self.__guiConfig.clearMonitorComponents()
        self.__guiVerifier.clearVerifierComponents()

        self.__menuBar.actionClose()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
