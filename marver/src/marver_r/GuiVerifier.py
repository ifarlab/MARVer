from PyQt5.QtWidgets import *
from include.marver_r.RMLOracle import RMLOracle
from include.marver_r.TLOracle import TLOracle
from src.marver_r.GuiLog import GuiLog
from include.marver_r.Monitor import Monitor
from include.marver_r.Property import Property
from bin.UI_MARVer import Ui_MainWindow
from include.marver_r.Verifier import Verifier
from include.marver_r.XmlParser import XmlParser
import json


class GuiVerifier:
    def __init__(self, ui: Ui_MainWindow = None, logger: GuiLog = None, monitor: [Monitor] = [],
                 rmlOracle: RMLOracle = None, tlOracle: TLOracle = None):
        self.__rmlOracle = rmlOracle
        self.__ui = ui
        self.__monitor = monitor
        self.__tlOracle = tlOracle
        self.__logger = logger

        self.initComponents()
        # self.test()

    def initComponents(self):
        self.__ui.btnPropertyDefineDelete.setEnabled(False)
        self.__ui.btnPropertyDefineUpdate.setEnabled(False)
        self.__ui.btnPropertyDefineCreate.setEnabled(True)

    def getProperties(self) -> [Property]:
        temp = []
        temp.extend(self.__rmlOracle.getProperties())
        temp.extend(self.__tlOracle.getProperties())
        return temp

    def addProperty(self):
        if not self.checkMonitorIsExist():
            self.__logger.printLog("Please create a monitor first ! ", "red")
            return

        if self.__ui.txtPropertyDefineName.text() == "" or \
                self.__ui.txtPropertyDefineDescription.toPlainText() == "" \
                or self.__ui.txtPropertyDefineFormula.text() == "" \
                or not self.__ui.lwPropertyDefineNodes.selectedItems():
            self.__logger.printLog(message="Please fill in all fields !!", color="red")
            return

        if self.__ui.cbxPropertyDefineType.currentText() == "TL Oracle":
            if self.__tlOracle.isExist(self.__ui.txtPropertyDefineName.text())[0] or \
                    self.__rmlOracle.isExist(self.__ui.txtPropertyDefineName.text())[0]:
                self.__logger.printLog(message="The name of the property is not unique. Change the name !!",
                                       color="red")
                return
            else:
                self.__tlOracle.setProperties(Property(name=self.__ui.txtPropertyDefineName.text(),
                                                       description=self.__ui.txtPropertyDefineDescription.toPlainText(),
                                                       formula=self.__ui.txtPropertyDefineFormula.text(),
                                                       nodeNames=[item.text() for item in
                                                                  self.__ui.lwPropertyDefineNodes.selectedItems()]))
                self.__logger.printLog(message="The property is added successfully", color="green")
        else:
            if self.__rmlOracle.isExist(self.__ui.txtPropertyDefineName.text())[0] or \
                    self.__tlOracle.isExist(self.__ui.txtPropertyDefineName.text())[0]:
                self.__logger.printLog(message="The name of the property is not unique. Change the name !!",
                                       color="red")
                return
            else:
                self.__rmlOracle.setProperties(Property(name=self.__ui.txtPropertyDefineName.text(),
                                                        description=self.__ui.txtPropertyDefineDescription.toPlainText(),
                                                        formula=self.__ui.txtPropertyDefineFormula.text(),
                                                        nodeNames=[item.text() for item in
                                                                   self.__ui.lwPropertyDefineNodes.selectedItems()]))
                self.__logger.printLog(message="The property is added successfully", color="green")
        self.__ui.txtPropertyDefineName.clear()
        self.__ui.txtPropertyDefineDescription.clear()
        self.__ui.txtPropertyDefineFormula.clear()
        self.__ui.lwPropertyDefineNodes.clearSelection()
        self.updateVerifierDefineCbx()
        self.updateVerifierSaveCbx()

    def editProperty(self):
        property = self.__tlOracle.getPropertyByName(self.__ui.cbxPropertyDefineVerifier.currentText())
        if property:
            self.__tlOracle.deletePropertyByName(property.getName())
        else:
            property = self.__rmlOracle.getPropertyByName(self.__ui.cbxPropertyDefineVerifier.currentText())
            if property:
                self.__rmlOracle.deletePropertyByName(property.getName())
        self.addProperty()

    def deleteProperty(self):
        propertyName = self.__ui.cbxPropertyDefineVerifier.currentText()
        if self.__tlOracle.isExist(propertyName)[0]:
            self.__tlOracle.getProperties().pop(self.__tlOracle.isExist(propertyName)[1])
        else:
            self.__rmlOracle.getProperties().pop(self.__rmlOracle.isExist(propertyName)[1])

        self.__ui.txtPropertyDefineName.clear()
        self.__ui.txtPropertyDefineDescription.clear()
        self.__ui.txtPropertyDefineFormula.clear()
        self.__ui.lwPropertyDefineNodes.clearSelection()
        self.updateVerifierDefineCbx()
        self.updateVerifierSaveCbx()

    def importProperty(self):
        filePath = self.openFileDialogWindow('json')
        if not filePath:
            return
        properties = self.getJSONFileContent(filePath=filePath)
        for property in properties["properties"]:
            if self.__ui.cbxPropertyImportType.currentText() == "TL Oracle":
                self.__tlOracle.setProperties(Property(name=property["name"],
                                                       description=property["description"],
                                                       formula=property["formula"],
                                                       nodeNames=property["nodeNames"]))
                self.__logger.printLog(message="TL properties imported successfully", color="green")
            else:
                self.__rmlOracle.setProperties(Property(name=property["name"],
                                                        description=property["description"],
                                                        formula=property["formula"],
                                                        nodeNames=property["nodeNames"]))
                self.__logger.printLog(message="RML properties imported successfully", color="green")
        self.updateVerifierDefineCbx()
        self.updateVerifierSaveCbx()

    def openFileDialogWindow(self, ext) -> str:
        try:
            filePath, check = QFileDialog.getOpenFileName(None, "Open File", "3rdparty/rosmonitoring/oracle",
                                                          "Text Files (*." + ext + ")")
            if filePath:
                self.__logger.printLog(message="File selection completed successfully", color="green")
                return filePath
            else:
                raise IOError(f"An error occurred while opening the file")
        except IOError:
            self.__logger.printLog(message=f"An error occurred while opening the file", color="red")
        except:
            self.__logger.printLog(message="ERROR in openFileDialogWindow()", color="red")

    def getJSONFileContent(self, filePath: str):
        try:
            with open(filePath) as file:
                if not file:
                    raise IOError(f"An error occurred while reading the file")
                self.__logger.printLog(message="File content read successfully", color="green")
                return json.load(file)
        except IOError:
            self.__logger.printLog(message=f"An error occurred while reading the file", color="red")
        except:
            self.__logger.printLog(message="ERROR in getJSONFileContent()", color="red")

    def saveProperty2File(self):
        fileName = self.__ui.txtPropertySaveFileName.text()
        if fileName:
            items = self.__ui.lwPropertySaveSelect.selectedItems()
            if items:
                try:
                    if self.__ui.cbxPropertySaveType.currentText() == "TL Oracle":
                        with open(f'3rdparty/rosmonitoring/oracle/TLOracle/properties/{fileName}.json', 'w') as f:
                            f.write(self.preparePropertiesJSON(
                                self.__tlOracle.getPropertiesByName(names=[item.text() for item in items])))
                    else:
                        with open(f'3rdparty/rosmonitoring/oracle/RMLOracle/rml/properties/{fileName}.json',
                                  'w') as f:
                            f.write(self.preparePropertiesJSON(
                                self.__rmlOracle.getPropertiesByName(names=[item.text() for item in items])))

                    self.__ui.txtPropertySaveFileName.clear()
                    self.__logger.printLog(message="File content saved successfully", color="green")
                except IOError:
                    self.__logger.printLog(message=f"An error occurred while writing to the file", color="red")
                except:
                    self.__logger.printLog(message="ERROR in saveProperty2File()", color="red")

            else:
                self.__logger.printLog(message="Please select the properties", color="red")
        else:
            del fileName
            self.__logger.printLog(message="Please fill the file name", color="red")

    @staticmethod
    def preparePropertiesJSON(properties: [Verifier]) -> str:
        content = {"properties": []}
        for property in properties:
            content["properties"].append(
                {"name": property.getName(), "description": property.getDescription(), "formula": property.getFormula(),
                 "nodeNames": property.getNodeNames()})

        return json.dumps(content, indent=4)

    def setVerifierComponentsStatus(self):
        if self.__ui.cbxPropertyDefineVerifier.currentText() == "New Property":
            self.__ui.btnPropertyDefineDelete.setEnabled(False)
            self.__ui.btnPropertyDefineUpdate.setEnabled(False)
            self.__ui.btnPropertyDefineCreate.setEnabled(True)
        else:
            verifier = self.__tlOracle.getPropertyByName(self.__ui.cbxPropertyDefineVerifier.currentText())
            if verifier:
                self.__ui.cbxPropertyDefineType.setCurrentIndex(0)
            else:
                self.__ui.cbxPropertyDefineType.setCurrentIndex(1)
                verifier = self.__rmlOracle.getPropertyByName(self.__ui.cbxPropertyDefineVerifier.currentText())

            self.__ui.txtPropertyDefineName.setText(verifier.getName())
            self.__ui.txtPropertyDefineDescription.setPlainText(verifier.getDescription())
            self.__ui.txtPropertyDefineFormula.setText(verifier.getFormula())
            self.__ui.lwPropertyDefineNodes.clear()

            for name in verifier.getNodeNames():
                self.__ui.lwPropertyDefineNodes.addItem(name)

            self.__ui.btnPropertyDefineDelete.setEnabled(True)
            self.__ui.btnPropertyDefineUpdate.setEnabled(True)
            self.__ui.btnPropertyDefineCreate.setEnabled(False)

    def updateVerifierDefineCbx(self):
        self.__ui.cbxPropertyDefineVerifier.clear()
        self.__ui.cbxPropertyDefineVerifier.addItem("New Property")
        for tlVerifier in self.__tlOracle.getProperties():
            self.__ui.cbxPropertyDefineVerifier.addItem(tlVerifier.getName())
        for rmlVerifier in self.__rmlOracle.getProperties():
            self.__ui.cbxPropertyDefineVerifier.addItem(rmlVerifier.getName())

        self.__ui.cbxPropertyDefineVerifier.setCurrentIndex(0)
        self.__ui.btnPropertyDefineDelete.setEnabled(False)
        self.__ui.btnPropertyDefineUpdate.setEnabled(False)
        self.__ui.btnPropertyDefineCreate.setEnabled(True)

        self.__ui.lwPropertyDefineNodes.clear()
        if self.checkMonitorIsExist():
            for node in self.__monitor[0].getNodes():
                self.__ui.lwPropertyDefineNodes.addItem(node.getName())

    def updateVerifierSaveCbx(self):
        self.__ui.lwPropertySaveSelect.clear()
        if self.__ui.cbxPropertySaveType.currentText() == "TL Oracle":
            for tlVerifier in self.__tlOracle.getProperties():
                self.__ui.lwPropertySaveSelect.addItem(tlVerifier.getName())
        else:
            for rmlVerifier in self.__rmlOracle.getProperties():
                self.__ui.lwPropertySaveSelect.addItem(rmlVerifier.getName())
        self.__ui.cbxPropertyDefineVerifier.setCurrentIndex(0)

    def checkMonitorIsExist(self) -> bool:
        if not self.__monitor:
            return False
        return True

    def clearVerifierComponents(self):
        self.__ui.cbxPropertyDefineVerifier.clear()
        self.__ui.cbxPropertyDefineVerifier.addItem("New Property")
        self.__ui.cbxPropertyDefineVerifier.setCurrentIndex(0)
        self.__ui.txtPropertyDefineName.clear()
        self.__ui.txtPropertyDefineDescription.clear()
        self.__ui.lwPropertyDefineNodes.clear()
        self.__ui.lwPropertySaveSelect.clear()
        self.__ui.txtPropertySaveFileName.clear()
        self.__ui.txtPropertyDefineFormula.clear()

        self.__ui.btnPropertyDefineDelete.setEnabled(False)
        self.__ui.btnPropertyDefineUpdate.setEnabled(False)
        self.__ui.btnPropertyDefineCreate.setEnabled(True)

    def importUppaalModel(self):
        f = self.openFileDialogWindow('xml')
        file = XmlParser(f)

        for formula in file.getQueries():
            formula=formula.strip()
            if self.tctl2Reelay(formula):
                self.__ui.cbxPropertyDefineFormula.addItem(self.tctl2Reelay(formula))

        self.__ui.cbxPropertyDefineFormula.setEnabled(True)
        print()

    def tctl2Reelay(self,formula: str) -> str:
        # check str is blank or not
        if not formula or "deadlock" in formula:
            return None

        temp = ""
        # Eliminate E<> or A[]
        for f in formula.split(" ")[1:]:
            if "&&" in f:
                temp += " and "
            elif "||" in f:
                temp += " or "
            elif "." in f:
                temp += str(f.split(".")[0]) + "_state: " + str(f.split(".")[1])
            else:
                temp += f

        return "{" + temp + "}"




