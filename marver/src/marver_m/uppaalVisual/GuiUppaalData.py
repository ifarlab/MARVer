from bin.UI_MARVer import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor

import include.marver_m.UppaalVisual.nodeeditor.node_editor_widget as wdg
from include.marver_m.UppaalVisual.xmlToNode import getNodeEdgeList
from include.marver_m.UppaalVisual.DataBaseConnection import DataBaseConnection
from src.marver_r.GuiLog import GuiLog

class GuiUppaalData(QMainWindow):
    NodeEditorWidget_class = wdg.NodeEditorWidget

    def __init__(self, ui: Ui_MainWindow = None, logger: GuiLog = None):
        super().__init__()
        self.__ui = ui

        self.modelsList = []
        self.localList = []

        self.__logger = logger

        self.__dbClass = None
        self.uppaalDisplayer = None
        self.currentFileName = None

        self.lwModel = QStandardItemModel(self.__ui.lwVisual_ModelList_2)

        self.__ui.btnData_SaveDatabase.setEnabled(False)
        self.__ui.btnData_GetDatabase.setEnabled(False)

    def setDisplayerWidget(self, nodeEdgeList):
        self.__ui.tabWData_Templates.clear()
        for i in range(nodeEdgeList.__len__()):
            currentTab = QWidget()
            self.__ui.tabWData_Templates.addTab(currentTab, nodeEdgeList[i].name)
            self.uppaalDisplayer = self.__class__.NodeEditorWidget_class(currentTab)
            self.uppaalDisplayer.setParent(currentTab)
            self.uppaalDisplayer.resize(self.__ui.tabWData_Templates.size())
            self.uppaalDisplayer.setModel(nodeEdgeList)
            self.uppaalDisplayer.addNodes(i)
            self.uppaalDisplayer.setVisible(True)

    def fillLWFromDB(self):
        if self.__ui.txtDatabase_UserName.toPlainText() != "" and self.__ui.txtDatabase_Name.toPlainText() != "" and self.__ui.txtDatabase_Password.toPlainText() != "":
            self.modelsList = self.__dbClass.selectAllModelIDInfo()


    def setLabelTexts(self, modelId="-", fileName="-", createDate="-", description="-"):
        self.__ui.txtData_ModelID.setText(modelId)
        self.__ui.txtData_FileName.setText(fileName)
        self.__ui.txtData_CreateDate.setText(createDate)
        self.__ui.txtData_ModelDesc.setText(description)

    def save2DataBase(self):
        if self.__dbClass == None:
            self.__logger.printLog("Please Connect Database ", "red")
            return
        if self.__dbClass.insertXmlFile(self.currentFileName, self.__ui.txtData_ModelDesc.toPlainText()):
            self.__logger.printLog("File saved into database", "green")
            for model in self.localList:
                if model[1] in self.currentFileName:
                    self.localList.remove(model)

            self.fillLWFromDB()
            self.__ui.txtData_ModelDesc.setReadOnly(True)

    def listItemClicked(self, index):
        self.__ui.txtData_ModelDesc.setReadOnly(True)
        index = index.row()
        if str(self.modelsList[index][0]) == "-":
            self.__ui.btnData_SaveDatabase.setEnabled(True)
            fname = self.modelsList[index][1]
            with open(fname, "r") as f:
                info = getNodeEdgeList(f.read())
            self.setDisplayerWidget(info)
            self.setLabelTexts(fileName=fname)
            self.currentFileName = fname
        else:
            self.__ui.btnData_SaveDatabase.setEnabled(False)
            self.currentFileName = None
            xmlProp = getNodeEdgeList(self.__dbClass.selectUppaalModelXml(self.modelsList[index][0]))
            self.setLabelTexts(modelId=str(self.modelsList[index][0]), fileName=self.modelsList[index][1],
                               createDate=self.modelsList[index][2].strftime("%m/%d/%Y"),
                               description=self.modelsList[index][3])
            self.setDisplayerWidget(xmlProp)

    def save2Local(self):
        fname = QFileDialog.getExistingDirectory(self, "Select directory.")
        if fname:
            modelID = int(self.modelsList[self.__ui.lwVisual_ModelList_2.selectedIndexes()[-1].row()][0])
            fileName = self.modelsList[self.__ui.lwVisual_ModelList_2.selectedIndexes()[-1].row()][1]
            xmlContent = self.__dbClass.selectUppaalModelXml(modelID)
            with open(fname + '\\' +  fileName, 'w') as file:
                if not file:
                    raise IOError("An error occurred while creating the file")
                file.write(xmlContent)


    def DBconnection(self):
        if self.__ui.txtDatabase_UserName.toPlainText() == "" or self.__ui.txtDatabase_Name.toPlainText() == "" or self.__ui.txtDatabase_Password.toPlainText() == "":
            self.__logger.printLog("Please fill all database spaces ", "red")
        else:
            self.__dbClass = DataBaseConnection(self.__ui.txtDatabase_Name.toPlainText(), self.__ui.txtDatabase_UserName.toPlainText(), self.__ui.txtDatabase_Password.toPlainText())

            if self.__dbClass.db_test(self.__ui.txtDatabase_Name.toPlainText(), self.__ui.txtDatabase_UserName.toPlainText(), self.__ui.txtDatabase_Password.toPlainText()):
                self.__logger.printLog("Connection to the database has been established.", "green")
                self.__ui.btnData_GetDatabase.setEnabled(True)
            else:
                self.__logger.printLog("Database does not exist in the system.", "red")

    def getDB(self):
        return self.__dbClass
