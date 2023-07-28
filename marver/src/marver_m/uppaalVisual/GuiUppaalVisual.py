from bin.UI_MARVer import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QColor
from PyQt5.QtCore import Qt
import re
import xml.etree.ElementTree as ET

import include.marver_m.UppaalVisual.nodeeditor.node_editor_widget as wdg
from include.marver_m.UppaalVisual.xmlToNode import getNodeEdgeList
from include.marver_m.UppaalVisual.DataBaseConnection import DataBaseConnection
from src.marver_m.uppaalVisual.GuiUppaalData import GuiUppaalData


class GuiUppaalVisual(QMainWindow):
    NodeEditorWidget_class = wdg.NodeEditorWidget

    def __init__(self, ui: Ui_MainWindow = None, uppaalData: GuiUppaalData = None):
        super().__init__()
        self.__ui = ui

        self.modelsList = []

        self.__uppaalData = uppaalData
        self.__dbClass = self.__uppaalData.getDB()
        self.currentFileName = None

        self.lwModel = QStandardItemModel(self.__ui.lwVisual_ModelList)

        self.__ui.btnVisual_SaveQuery.setEnabled(False)
        self.__ui.btnVisual_OpenLocal_Export.setEnabled(False)
        self.fillLWFromDB()

    def setDB(self):
        self.__dbClass = self.__uppaalData.getDB()

    def setDisplayerWidget(self, nodeEdgeList):
        self.__ui.tabWVisual_Templates.clear()
        for i in range(nodeEdgeList.__len__()):
            currentTab = QWidget()
            self.__ui.tabWVisual_Templates.addTab(currentTab, nodeEdgeList[i].name)
            self.uppaalDisplayer = self.__class__.NodeEditorWidget_class(currentTab)
            self.uppaalDisplayer.setParent(currentTab)
            self.uppaalDisplayer.resize(self.__ui.tabWVisual_Templates.size())
            self.uppaalDisplayer.setModel(nodeEdgeList)
            self.uppaalDisplayer.addNodes(i)
            self.uppaalDisplayer.setVisible(True)

    def setNonDBQueriesToWidget(self, fileName):
        f = open(fileName, "r")
        xmlFile = f.read()

        xmlFile = xmlFile.replace('\n', '')
        pattern = "<queries>(.*)</queries>"
        chopped = re.search(pattern, xmlFile)

        if chopped:
            xmlFile = "<queries> " + chopped.group(1) + " </queries>"
            tree = ET.ElementTree(ET.fromstring(xmlFile))
            root = tree.getroot()
            queryListModel = QStandardItemModel(self.__ui.lwVisual_Queries)
            for query in root.findall('query'):
                item = QStandardItem(query[0].text + "\n" + query[1].text)
                item.setEditable(False)
                queryListModel.appendRow(item)
            self.__ui.lwVisual_Queries.setModel(queryListModel)

    def setQueriesToWidget(self, queryList):
        queryListModel = QStandardItemModel(self.__ui.lwVisual_Queries)
        for i in range(queryList.__len__()):
            item = QStandardItem(queryList[i][0] + "\n" + queryList[i][1])
            item.setEditable(False)
            item.setCheckable(True)
            item.setData(queryList[i][3])
            if not queryList[i][2]:
                item.setCheckState(Qt.CheckState.PartiallyChecked)
            elif queryList[i][2] == '1':
                item.setCheckState(Qt.CheckState.Checked)
                item.setBackground(QColor(179, 217, 255))
            elif queryList[i][2] == '0':
                item.setCheckState(Qt.CheckState.Unchecked)
                item.setBackground(QColor(255, 147, 149))
            queryListModel.appendRow(item)
        self.__ui.lwVisual_Queries.setModel(queryListModel)

    def fillLWFromDB(self):

        if self.__dbClass != None:
            self.modelsList = self.__uppaalData.modelsList

        for model in self.__uppaalData.localList:
            if model not in self.modelsList:
                self.modelsList.append(model)

        self.lwModel.clear()

        for model in self.modelsList:
            item = QStandardItem(str(model[0]) + ": " + model[1])
            item.setEditable(False)
            if str(model[0]) == "-":
                item.setBackground(QColor(230, 175, 175))
            else:
                item.setBackground(QColor(161, 172, 213))
            self.lwModel.appendRow(item)

        self.__uppaalData.modelsList = self.modelsList
        self.__ui.lwVisual_ModelList_2.setModel(self.lwModel)
        self.__ui.lwVisual_ModelList.setModel(self.lwModel)

    def openFromLocal(self):
        #self.__uppaalData.__ui.btnVisual_SaveQuery.setEnabled(False)
        fname, filter = QFileDialog.getOpenFileName(self, 'Select xml file', '', 'Graph (*.xml);;All files (*)')
        if fname:
            with open(fname, "r") as f:
                info = getNodeEdgeList(f.read())
            self.setDisplayerWidget(info)
            self.setLabelTexts(fileName=fname)
            self.currentFileName = fname
            item = QStandardItem("-: " + fname)
            item.setBackground(QColor(230, 175, 175))
            item.setEditable(False)
            self.lwModel.appendRow(item)


            self.modelsList.append(["-", fname, "-", "-"])
            self.setNonDBQueriesToWidget(fname)
            self.__ui.lwVisual_ModelList.setModel(self.lwModel)
            self.__ui.lwVisual_ModelList_2.setModel(self.lwModel)
            self.__uppaalData.modelsList = self.modelsList
            self.__uppaalData.localList.append(["-", fname, "-", "-"])

    def setLabelTexts(self, modelId="-", fileName="-", createDate="-", description="-"):
        self.__ui.txtVisual_ModelID.setText(modelId)
        self.__ui.txtVisual_ModelDesc.setText(description)

    def save2DataBase(self):
        if self.__dbClass.insertXmlFile(self.currentFileName, "emptyDesc"):
            self.fillLWFromDB()

    def listItemClicked(self, index):
        index = index.row()
        if str(self.modelsList[index][0]) == "-":
            fname = self.modelsList[index][1]
            with open(fname, "r") as f:
                info = getNodeEdgeList(f.read())
            self.setDisplayerWidget(info)
            self.setLabelTexts(fileName=fname)
            self.setNonDBQueriesToWidget(fname)
        else:
            self.__ui.btnVisual_SaveQuery.setEnabled(True)
            self.__ui.btnVisual_OpenLocal_Export.setEnabled(True)
            self.currentFileName = None
            xmlProp = getNodeEdgeList(self.__dbClass.selectUppaalModelXml(self.modelsList[index][0]))
            self.setLabelTexts(modelId=str(self.modelsList[index][0]), fileName=self.modelsList[index][1],
                               createDate=self.modelsList[index][2].strftime("%m/%d/%Y"),
                               description=self.modelsList[index][3])
            self.setDisplayerWidget(xmlProp)
            self.setQueriesToWidget(self.__dbClass.selectUppaalQueries(self.modelsList[index][0]))

    def saveQueryStates(self):
        model = self.__ui.lwVisual_Queries.model()
        for i in range(model.rowCount()):
            item = model.item(i)
            self.__dbClass.setQueryState(item.data(), item.checkState())
            if item.checkState() == Qt.Checked:
                item.setBackground(QColor(179, 217, 255))
            elif item.checkState() == Qt.Unchecked:
                item.setBackground(QColor(255, 147, 149))
