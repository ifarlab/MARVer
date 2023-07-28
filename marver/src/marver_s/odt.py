import xml.etree.cElementTree as ET
import xml.dom.minidom
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from bin.UI_MARVer import Ui_MainWindow

class ODT(QMainWindow, Ui_MainWindow):

    def __init__(self, ui: Ui_MainWindow = None):
        super(ODT, self).__init__()
        self.__ui = ui

    def addCylinder(self):
        # print('hello from add cylinder')
        rawCount = self.__ui.table.rowCount()
        self.__ui.table.insertRow(rawCount)
        self.__ui.table.setItem(rawCount, 0, QTableWidgetItem(self.__ui.cylinderIdValue.text()))
        self.__ui.table.setItem(rawCount, 1, QTableWidgetItem(self.__ui.cylinderNameValue.text()))
        self.__ui.table.setItem(rawCount, 2, QTableWidgetItem(self.__ui.cylinderRadiusValue.text()))
        self.__ui.table.setItem(rawCount, 3, QTableWidgetItem(self.__ui.cylinderHeightValue.text()))
        self.__ui.table.setItem(rawCount, 4, QTableWidgetItem(self.__ui.frameIdValue.text()))
        self.__ui.table.setItem(rawCount, 5, QTableWidgetItem(self.__ui.frameNameValue.text()))
        # self.__ui.table.setItem(rawCount, 6, QTableWidgetItem(self.__ui.frameTranslationValue.text()))
        # self.__ui.table.setItem(rawCount, 7, QTableWidgetItem(self.__ui.frameRotationValue.text()))
        self.__ui.table.setItem(rawCount, 6, QTableWidgetItem(self.parse(self.__ui.frameTranslationValue.text())))
        self.__ui.table.setItem(rawCount, 7, QTableWidgetItem(self.parse(self.__ui.frameRotationValue.text())))
        self.clearTextBoxes()

    def clearTextBoxes(self):
        # self.__ui.robotBrandValue.setText("")
        # self.__ui.robotModelValue.setText("")
        self.__ui.cylinderIdValue.setText("")
        self.__ui.cylinderNameValue.setText("")
        self.__ui.cylinderRadiusValue.setText("")
        self.__ui.cylinderHeightValue.setText("")
        self.__ui.frameIdValue.setText("")
        self.__ui.frameNameValue.setText("")
        self.__ui.frameTranslationValue.setText("")
        self.__ui.frameRotationValue.setText("")
        # self.__ui.rootFrameValue.setText("")

    def removeCylinder(self):
        # print('hello from remove cylinder')
        self.__ui.table.removeRow(self.__ui.table.currentRow())

    def getDataFromTable(self):

        myList = []
        myDict = dict.fromkeys(['cylinder_id', 'cylinder_name', 'radius', 'height', 'frame_id', 'frame_name','trans', 'rot'])

        robot_brand = self.__ui.robotBrandValue.text()
        robot_model = self.__ui.robotModelValue.text()
        root_frame = self.__ui.rootFrameValue.text()

        for raw in range(self.__ui.table.rowCount()):
            for column in range(self.__ui.table.columnCount()):
                # print("raw", raw, "column", column, "data", self.table.item(raw, column).text())
                myDict[list(myDict.keys())[column]] = self.__ui.table.item(raw, column).text()
            # myDict[list(myDict.keys())[-1]] = self.rootFrameValue.text()
            myList.append(myDict.copy())

        # print(myDict)
        print(myList)

        robot = ET.Element('robot', brand=robot_brand, model=robot_model, root_frame_name=root_frame)
        cylinders = ET.SubElement(robot, 'cylinders')
        for item in range(len(myList)):
            print('item', item)
            cylinder = ET.SubElement(cylinders, 'cylinder', id=myList[item].get('cylinder_id'), name=myList[item].get('cylinder_name'), radius=myList[item].get('radius'),  height=myList[item].get('height'))
            robot_frame = ET.SubElement(cylinder, 'robot_frame', id=myList[item].get('frame_id'), name=myList[item].get('frame_name'), rotation=myList[item].get('rot'), translation=myList[item].get('trans'))

        dom = xml.dom.minidom.parseString(ET.tostring(robot))
        xml_string = dom.toprettyxml()
        myfile = open("robot_deneme.xml", "w") # bin klasorunun icine kaydediyor, duzeltilecek
        myfile.write(xml_string)
        myfile.close()

    def parse(self, str):
        str = str.replace(' ', '')
        list = str.split(',')

        s = ''
        for item in range(len(list)):
            s += list[item]
            if item != len(list)-1:
                s += ' '

        return s

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ODT()
    window.show()
    app.exec_()
