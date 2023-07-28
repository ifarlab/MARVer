import xml.etree.cElementTree as ET
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from bin.UI_MARVer import Ui_MainWindow
import getpass
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QFile, QIODevice
from PyQt5.QtXml import QDomDocument

class OMA(QMainWindow,Ui_MainWindow):
    def __init__(self, ui: Ui_MainWindow = None):
        super(OMA, self).__init__()
        self.__ui = ui
        

    def create_xml(self):
        value = self.__ui.des_package_val.text()
        des_pac_div = self.__ui.package_div_val.text()
        topic= self.__ui.topic_val.text()
        hz = self.__ui.hertz_of_robot_val.text()
        joints=self.__ui.joint_number_val.text()
        
        xmlDocument = QDomDocument()
        root = xmlDocument.createElement("parameters")
        xmlDocument.appendChild(root)

        valueElement = xmlDocument.createElement("value")
        valueText = xmlDocument.createTextNode(value)
        valueElement.appendChild(valueText)
        root.appendChild(valueElement)

        desPacDivElement = xmlDocument.createElement("des_pac_div")
        desPacDivText = xmlDocument.createTextNode(des_pac_div)
        desPacDivElement.appendChild(desPacDivText)
        root.appendChild(desPacDivElement)

        hzElement = xmlDocument.createElement("hz")
        hzText = xmlDocument.createTextNode(hz)
        hzElement.appendChild(hzText)
        root.appendChild(hzElement)

        topicElement = xmlDocument.createElement("topic")
        topicText = xmlDocument.createTextNode(topic)
        topicElement.appendChild(topicText)
        root.appendChild(topicElement)

        jointsElement=xmlDocument.createElement("joint_number")
        jointsText=xmlDocument.createTextNode(joints)
        jointsElement.appendChild(jointsText)
        root.appendChild(jointsElement)   
        
        
        xmlString = xmlDocument.toString()

        # XML dosyasını kaydetmek için gerekli işlemler

        # Örnek olarak, dosyayı "output.xml" olarak kaydediyoruz
        with open('/home/'+ getpass.getuser()+'/catkin_ws/src/oma_msgs/output.xml', "w") as file:
            file.write(xmlString)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = OMA()
    mainWindow.show()
    sys.exit(app.exec_())
