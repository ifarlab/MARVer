import yaml
from PyQt5.QtWidgets import *
from include.marver_r.Monitor import Monitor
from include.marver_r.Node import Node
from include.marver_r.Topic import Topic
from src.marver_r.GuiLog import GuiLog
from include.marver_r.Verifier import Verifier
from bin.UI_MARVer import Ui_MainWindow
import distutils.util
import getpass

class GuiConfig:
    """! Config clas for preparing config file content

    Defines the base class used by config window tab
    """

    def __init__(self, ui: Ui_MainWindow = None, logger: GuiLog = None, monitors: [Monitor] = []):
        """! The GuiConfig base class initializer.

        @param ui  Carries the properties of the main window.
        @param logger Carries the log panel attributes.

        @return An instance of the GuiConfig class initialized with the specified name and unit
        """

        self.__monitors = monitors
        self.__ui = ui
        self.__logger = logger

        self.initComponents()

    def initComponents(self):
        """! Holds and sets the windows's initial components.
        """
        self.__ui.btnConfigNodeCreate.setEnabled(True)
        self.__ui.btnConfigNodeUpdate.setDisabled(True)
        self.__ui.btnConfigNodeDelete.setDisabled(True)
        self.__ui.btnConfigTopicCreate.setEnabled(True)
        self.__ui.btnConfigTopicUpdate.setDisabled(True)
        self.__ui.btnConfigTopicDelete.setDisabled(True)
        self.__ui.btnConfigOracleCreate.setEnabled(True)
        self.__ui.btnConfigOracleUpdate.setDisabled(True)
        self.__ui.btnConfigOracleDelete.setDisabled(True)
        self.__ui.btnConfigMonitorCreate.setEnabled(True)
        self.__ui.btnConfigMonitorUpdate.setDisabled(True)
        self.__ui.btnConfigMonitorDelete.setDisabled(True)
        self.__ui.txtConfigOracleName.setEnabled(False)

    def createNode(self):
        """! Creates Node class for config file content and checks for any invalid input.
        """

        if not len(self.__monitors):
            self.__logger.printLog("Please create Monitor before creating Node ", "red")
            return

        if self.__ui.cbxMonitorMonitor.currentText() == 'New Monitor':
            self.__logger.printLog("Please select Monitor before creating Node ", "red")
            return

        if self.__ui.txtConfigNodeName.text() == "" or \
                self.__ui.txtConfigNodePath.text() == "" or \
                self.__ui.txtConfigNodePackage.text() == "":
            self.__logger.printLog("Please fill in all Node properties", "red")
            return

        for nodes in self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].getNodes():
            if nodes.getName() == self.__ui.txtConfigNodeName.text():
                self.__logger.printLog("Node name must be unique", "red")
                return
        
        monitorPath = self.__ui.txtConfigNodePath.text()
        monitor_path = "/home/" + getpass.getuser() + "/catkin_ws/src/" + monitorPath
        
        self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].appendNode(
            Node(name=self.__ui.txtConfigNodeName.text(), type=None,
                 path=monitor_path, launchName=None,
                 packageName=self.__ui.txtConfigNodePackage.text(),
                 topics=[]))

        self.__ui.cbxConfigNode.addItem(self.__ui.txtConfigNodeName.text())
        self.__ui.lwPropertyDefineNodes.addItem(self.__ui.txtConfigNodeName.text())
        self.__ui.cbxConfigTopicNode.addItem(self.__ui.txtConfigNodeName.text())
        self.__ui.txtConfigNodeName.clear()
        self.__ui.txtConfigNodePath.clear()
        self.__ui.txtConfigNodePackage.clear()

        # self.__ui.cbxConfigNode.setCurrentIndex(self.__ui.cbxConfigNode.count() - 1)
        # self.setNodeComponentStatus()

        self.__logger.printLog("Node successfully created.", 'green')
        self.previewListWidget()

    def createTopic(self):
        """! Creates Topic class for config file content and checks for any invalid input.
        """

        if len(self.__monitors) == 0:
            self.__logger.printLog("Please create Monitor before creating Node and Topic ", "red")
            return

        if len(self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].getNodes()) == 0:
            self.__logger.printLog("Please create Node before creating Topic ", "red")
            return

        if self.__ui.txtConfigMonitorName.text() == "New Monitor":
            self.__logger.printLog("Please select Monitor before creating Topic ", "red")
            return

        if self.__ui.cbxConfigTopicNode.currentText() == "":
            self.__logger.printLog("Please select Node before creating Topic ", "red")
            return

        if self.__ui.txtConfigTopicName.text() == "" or \
                self.__ui.txtConfigTopicType.text() == "":
            self.__logger.printLog("Please fill in all Topic properties", "red")
            return

        for topics in self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].getNodes()[
            self.__ui.cbxConfigTopicNode.currentIndex()].getTopics():
            if topics.getName() == self.__ui.txtConfigTopicName.text():
                self.__logger.printLog("Topic name must be unique", "red")
                return

        self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].getNodes()[
            self.__ui.cbxConfigTopicNode.currentIndex()].appendTopic(
            Topic(name=self.__ui.txtConfigTopicName.text(),
                  type=self.__ui.txtConfigTopicType.text(),
                  action=self.__ui.cbxConfigTopicAction.currentText(),
                  publishers=[self.__ui.cbxConfigTopicNode.currentText()]))

        self.__ui.cbxConfigTopicTopic.addItem(self.__ui.txtConfigTopicName.text())
        self.__ui.txtConfigTopicName.clear()
        self.__ui.txtConfigTopicType.clear()
        self.__ui.cbxConfigTopicAction.setCurrentIndex(0)

        # self.__ui.cbxConfigTopicTopic.setCurrentIndex(self.__ui.cbxConfigTopicTopic.count() - 1)
        # self.setTopicComponentStatus()

        self.__logger.printLog("Topic successfully created.", 'green')
        self.previewListWidget()

    def createOracle(self):
        """! Creates Oracle class for config file content and checks for any invalid input.
        """

        if len(self.__monitors) == 0:
            self.__logger.printLog("Please create Monitor before creating Oracle ", "red")
            return

        if self.__ui.cbxMonitorMonitor.currentText() == 'New Monitor':
            self.__logger.printLog("Please select Monitor before creating Oracle ", "red")
            return

        if self.__ui.txtConfigMonitorName.text() == "New Monitor":
            self.__logger.printLog("Please select Monitor before creating Oracle ", "red")
            return

        if self.__ui.txtConfigOraclePort.text() == "" or self.__ui.txtConfigOracleUrl.text() == "":
            self.__logger.printLog("Please fill in all Oracle properties", "red")
            return

        if not self.__ui.txtConfigOraclePort.text().isnumeric():
            self.__logger.printLog("Port value must be integer", "red")
            return
        
        if self.__ui.txtConfigOraclePort.text() <= "1000" or self.__ui.txtConfigOraclePort.text() > "65535":
            self.__logger.printLog("Port value must be in the range of (1001-65535)", "red")
            return

        self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].setOracle(
            Verifier(port=int(self.__ui.txtConfigOraclePort.text()),
                     url=self.__ui.txtConfigOracleUrl.text(),
                     action=self.__ui.cbxConfigOracleAction.currentText()))

        self.__ui.txtConfigOracleName.setText(self.__ui.txtConfigOraclePort.text() + ':' +
                                              self.__ui.txtConfigOracleUrl.text() + '  -> ' +
                                              self.__ui.cbxConfigOracleAction.currentText())

        self.__ui.btnConfigOracleCreate.setDisabled(True)
        self.__ui.btnConfigOracleUpdate.setDisabled(False)
        self.__ui.btnConfigOracleDelete.setDisabled(False)

        self.__logger.printLog("Oracle successfully created.", 'green')
        self.previewListWidget()

    def createMonitor(self):
        """! Creates Monitor class for config file content and checks for any invalid input.
        """

        if self.__ui.txtConfigMonitorName.text() == "" or self.__ui.txtConfigMonitorLog.text() == "":
            self.__logger.printLog("Please fill in all Monitor properties", "red")
            return

        for monitor in self.__monitors:
            if monitor.getName() == self.__ui.txtConfigMonitorName.text():
                self.__logger.printLog("Monitor name must be unique", "red")
                return
        
        monitorLogPath = self.__ui.txtConfigMonitorLog.text()
        self.__ui.txtConfigMonitorLog
        monitor_log_path = "/home/" + getpass.getuser() + "/catkin_ws/src/" + monitorLogPath
        
        self.__monitors.append(Monitor(name=self.__ui.txtConfigMonitorName.text(),
                                       logFileName=monitor_log_path,
                                       silent=bool(self.__ui.cbxMonitorSilent.currentIndex()),
                                       warning=bool(
                                           distutils.util.strtobool(self.__ui.cbxMonitorWarning.currentText())),
                                       nodes=[]))

        self.__ui.cbxMonitorMonitor.addItem(self.__ui.txtConfigMonitorName.text())
        self.__ui.txtConfigMonitorName.clear()
        self.__ui.txtConfigMonitorLog.clear()
        self.__ui.cbxMonitorSilent.setCurrentIndex(0)
        self.__ui.cbxMonitorWarning.setCurrentIndex(0)

        # self.__ui.cbxMonitorMonitor.setCurrentIndex(self.__ui.cbxMonitorMonitor.count() - 1)
        # self.setMonitorComponentStatus()

        self.__logger.printLog(f"Monitor successfully created.", 'green')
        self.previewListWidget()

    def updateNode(self):
        """! Updates Node class according to the  information it receives from the user.
             Checking the validity of the item before updating .
        """

        nodes = self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].getNodes()
        index = self.__ui.cbxConfigNode.currentIndex() - 1

        if self.__ui.txtConfigNodeName.text() == "" or \
                self.__ui.txtConfigNodePath.text() == "" or \
                self.__ui.txtConfigNodePackage.text() == "":
            self.__logger.printLog("Please fill in all Node properties", "red")
            return

        # if nodes[index].getName() != self.__ui.txtConfigNodeName.text():
        #     for nodes in self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].getNodes():
        #         if nodes.getName() == self.__ui.txtConfigNodeName.text():
        #             self.__logger.printLog("Node name must be unique", "red")
        #             return
        
        monitorPath = self.__ui.txtConfigNodePath.text()
        tmpPath = "/home/" + getpass.getuser() + "/catkin_ws/src/"
        
        if (len(monitorPath) >= len(tmpPath)):
            monitor_path = monitorPath
        else:
            self.__logger.printLog("The path prompted is incorrect. Please check!!", "red")
            return    
        
        nodes[index].setName(self.__ui.txtConfigNodeName.text())
        nodes[index].setPath(monitor_path)
        nodes[index].setPackageName(self.__ui.txtConfigNodePackage.text())
        self.__ui.lwPropertyDefineNodes.clear()
        self.__ui.cbxConfigTopicNode.clear()
        self.__ui.lwPropertyDefineNodes.addItem(self.__ui.txtConfigNodeName.text())
        self.__ui.cbxConfigTopicNode.addItem(self.__ui.txtConfigNodeName.text())
        self.__ui.cbxConfigNode.setItemText(self.__ui.cbxConfigNode.currentIndex(), self.__ui.txtConfigNodeName.text())
        self.__ui.cbxConfigTopicNode.setItemText(self.__ui.cbxConfigNode.currentIndex(),self.__ui.txtConfigNodeName.text())
        self.__ui.txtConfigNodeName.clear()
        self.__ui.txtConfigNodePath.clear()
        self.__ui.txtConfigNodePackage.clear()

        self.__logger.printLog("Node successfully updated.", 'green')
        self.previewListWidget()

    def updateTopic(self):
        """! Updates Topic class according to the  information it receives from the user.
             Checking the validity of the item before updating .
        """

        topic = self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].getNodes()[
            self.__ui.cbxConfigTopicNode.currentIndex()].getTopics()[self.__ui.cbxConfigTopicTopic.currentIndex() - 1]

        if self.__ui.txtConfigTopicName.text() == "" or \
                self.__ui.txtConfigTopicType.text() == "":
            self.__logger.printLog("Please fill in all Topic properties", "red")
            return

        for topics in self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].getNodes()[
            self.__ui.cbxConfigTopicNode.currentIndex()].getTopics():
            if topics.getName() == self.__ui.txtConfigTopicName.text():
                self.__logger.printLog("Topic name must be unique", "red")
                return

        topic.setName(self.__ui.txtConfigTopicName.text())
        topic.setType(self.__ui.txtConfigTopicType.text())
        topic.setAction(self.__ui.cbxConfigTopicAction.currentText())
        
        self.__ui.cbxConfigTopicTopic.removeItem(self.__ui.cbxConfigTopicTopic.currentIndex())
        self.__ui.cbxConfigTopicTopic.insertItem(self.__ui.cbxConfigTopicTopic.currentIndex(), self.__ui.txtConfigTopicName.text())
        self.__ui.cbxConfigTopicTopic.setCurrentText(self.__ui.txtConfigTopicName.text())
        
        self.__ui.txtConfigTopicName.clear()
        self.__ui.txtConfigTopicType.clear()
        self.__ui.cbxConfigTopicAction.setCurrentIndex(0)

        self.__logger.printLog("Topic successfully updated.", 'green')
        self.previewListWidget()

    def updateOracle(self):
        """! Updates Oracle class according to the  information it receives from the user.
             Checking the validity of the item before updating .
        """

        if self.__ui.txtConfigOraclePort.text() == "" or self.__ui.txtConfigOracleUrl.text() == "":
            self.__logger.printLog("Please fill in all Oracle properties", "red")
            return

        if not self.__ui.txtConfigOraclePort.text().isnumeric():
            self.__logger.printLog("Port value must be integer", "red")
            return
        
        if self.__ui.txtConfigOraclePort.text() <= "1000" or self.__ui.txtConfigOraclePort.text() > "65535":
            self.__logger.printLog("Port value must be in the range of (1001-65535)", "red")
            return
        
        oracle = self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].getOracle()
        oracle.setPort(int(self.__ui.txtConfigOraclePort.text()))
        oracle.setUrl(self.__ui.txtConfigOracleUrl.text())
        oracle.setAction(self.__ui.cbxConfigOracleAction.currentText())
        self.__ui.txtConfigOracleName.setText(self.__ui.txtConfigOraclePort.text() + ':' +
                                              self.__ui.txtConfigOracleUrl.text() + '  -> ' +
                                              self.__ui.cbxConfigOracleAction.currentText())

        self.__logger.printLog("Oracle successfully updated.", 'green')
        self.previewListWidget()

    def updateMonitor(self):
        """! Updates Monitor class according to the  information it receives from the user.
             Checking the validity of the item before updating .
        """

        if self.__ui.txtConfigMonitorName.text() == "" or self.__ui.txtConfigMonitorLog.text() == "":
            self.__logger.printLog("Please fill in all Monitor properties", "red")
            return
        index = self.__ui.cbxMonitorMonitor.currentIndex() - 1

        if self.__monitors[index].getName() != self.__ui.txtConfigMonitorName.text():
            for monitor in self.__monitors:
                if monitor.getName() == self.__ui.txtConfigMonitorName.text():
                    self.__logger.printLog("Monitor name must be unique", "red")
                    return
        
        monitorLogPath = self.__ui.txtConfigMonitorLog.text()
        tmpLogPath = "/home/" + getpass.getuser() + "/catkin_ws/src/"
        
        if len(monitorLogPath) >= len(tmpLogPath):
                monitor_log_path = monitorLogPath
        else:
            self.__logger.printLog("The path prompted is incorrect. Please check!!", "red")
            return
        
        self.__monitors[index].setName(self.__ui.txtConfigMonitorName.text())
        self.__monitors[index].setLogFileName(monitor_log_path)
        self.__monitors[index].setSilent(bool(self.__ui.cbxMonitorSilent.currentIndex()))
        self.__monitors[index].setWarning(bool(distutils.util.strtobool(self.__ui.cbxMonitorWarning.currentText())))
        self.__ui.cbxMonitorMonitor.setItemText(self.__ui.cbxMonitorMonitor.currentIndex(),
                                                self.__ui.txtConfigMonitorName.text())
        self.__ui.txtConfigMonitorName.clear()
        self.__ui.txtConfigMonitorLog.clear()
        self.__ui.cbxMonitorSilent.setCurrentIndex(0)
        self.__ui.cbxMonitorWarning.setCurrentIndex(0)

        self.__logger.printLog("Monitor successfully updated.", 'green')
        self.previewListWidget()

    def deleteNode(self):
        """! Deletes the Current Node class object.
        """

        self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].removeNode(
            self.__ui.cbxConfigNode.currentIndex() - 1)

        self.__ui.cbxConfigTopicNode.removeItem(self.__ui.cbxConfigNode.currentIndex() - 1)
        self.__ui.cbxConfigNode.removeItem(self.__ui.cbxConfigNode.currentIndex())

        self.clearNodeComponents()
        self.clearTopicComponents()
        self.fillNodeLists()

        self.__logger.printLog("Node successfully deleted.", 'green')
        self.previewListWidget()

    def deleteTopic(self):
        """! Deletes the Current Topic class object.
        """

        self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].getNodes()[
            self.__ui.cbxConfigTopicNode.currentIndex()].removeTopic(self.__ui.cbxConfigTopicTopic.currentIndex() - 1)
        self.__ui.cbxConfigTopicTopic.removeItem(self.__ui.cbxConfigTopicTopic.currentIndex())

        self.clearTopicComponents()
        self.fillNodeLists()

        self.__logger.printLog("Topic successfully deleted.", 'green')
        self.previewListWidget()

    def deleteOracle(self):
        """! Deletes the Current Oracle class object.
        """

        self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].setOracle(None)

        self.clearOracleComponents()

        self.__logger.printLog("Oracle successfully deleted.", 'green')
        self.previewListWidget()

    def deleteMonitor(self):
        """! Deletes the Current Monitor class object.
        """

        self.__monitors.pop(self.__ui.cbxMonitorMonitor.currentIndex() - 1)
        self.__ui.cbxMonitorMonitor.removeItem(self.__ui.cbxMonitorMonitor.currentIndex())

        self.clearMonitorComponents()
        self.clearTopicComponents()
        self.clearNodeComponents()
        self.clearOracleComponents()

        self.__logger.printLog("Monitor successfully deleted.", 'green')
        self.previewListWidget()

    def setNodeComponentStatus(self):
        """! Sets all Node class components to default value.
        """

        if self.__ui.cbxConfigNode.currentText() != 'New Node':
            node = self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].getNodes()[
                self.__ui.cbxConfigNode.currentIndex() - 1]
            self.__ui.txtConfigNodeName.setText(node.getName())
            self.__ui.txtConfigNodePackage.setText(node.getPackageName())
            self.__ui.txtConfigNodePath.setText(node.getPath())
            self.__ui.btnConfigNodeUpdate.setEnabled(True)
            self.__ui.btnConfigNodeDelete.setEnabled(True)
            self.__ui.btnConfigNodeCreate.setDisabled(True)
        else:
            self.__ui.txtConfigNodeName.clear()
            self.__ui.txtConfigNodePath.clear()
            self.__ui.txtConfigNodePackage.clear()
            self.__ui.btnConfigNodeCreate.setEnabled(True)
            self.__ui.btnConfigNodeUpdate.setDisabled(True)
            self.__ui.btnConfigNodeDelete.setDisabled(True)

    def setTopicNodeComponentStatus(self):
        """! Sets all Topic Node class components to default value.
        """

        self.__ui.cbxConfigTopicTopic.clear()
        self.__ui.cbxConfigTopicTopic.addItem('New Topic')
        self.__ui.txtConfigTopicName.clear()
        self.__ui.txtConfigTopicType.clear()
        for topic in self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].getNodes()[
            self.__ui.cbxConfigTopicNode.currentIndex()].getTopics():
            self.__ui.cbxConfigTopicTopic.addItem(topic.getName())

    def setTopicComponentStatus(self):
        """! Sets all Topic class components to default value.
        """

        if self.__ui.cbxConfigTopicTopic.currentText() != 'New Topic':
            topic = self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1].getNodes()[
                self.__ui.cbxConfigTopicNode.currentIndex()].getTopics()[
                self.__ui.cbxConfigTopicTopic.currentIndex() - 1]

            self.__ui.txtConfigTopicName.setText(topic.getName())
            self.__ui.txtConfigTopicType.setText(topic.getType())
            action = topic.getAction()
            if action == 'filter':
                self.__ui.cbxConfigTopicAction.setCurrentIndex(0)
            elif action == 'log':
                self.__ui.cbxConfigTopicAction.setCurrentIndex(1)
            elif action == 'nothing':
                self.__ui.cbxConfigTopicAction.setCurrentIndex(2)

            self.__ui.btnConfigTopicUpdate.setEnabled(True)
            self.__ui.btnConfigTopicDelete.setEnabled(True)
            self.__ui.btnConfigTopicCreate.setDisabled(True)
        else:
            self.__ui.txtConfigTopicName.clear()
            self.__ui.txtConfigTopicType.clear()
            self.__ui.cbxConfigTopicAction.setCurrentIndex(0)
            self.__ui.btnConfigTopicCreate.setEnabled(True)
            self.__ui.btnConfigTopicUpdate.setDisabled(True)
            self.__ui.btnConfigTopicDelete.setDisabled(True)

    def setMonitorComponentStatus(self):
        """! Sets all Monitor class components to default value.
        """

        if self.__ui.cbxMonitorMonitor.currentText() != 'New Monitor':
            monitor = self.__monitors[self.__ui.cbxMonitorMonitor.currentIndex() - 1]
            self.__ui.txtConfigMonitorName.setText(monitor.getName())
            self.__ui.txtConfigMonitorLog.setText(monitor.getLogFileName())
            if monitor.getSilent():
                self.__ui.cbxMonitorSilent.setCurrentIndex(1)
            else:
                self.__ui.cbxMonitorSilent.setCurrentIndex(0)
            if monitor.getWarning():
                self.__ui.cbxMonitorWarning.setCurrentIndex(0)
            else:
                self.__ui.cbxMonitorWarning.setCurrentIndex(1)
            self.fillOracle()
            self.fillNodeLists()
            self.__ui.btnConfigMonitorUpdate.setEnabled(True)
            self.__ui.btnConfigMonitorDelete.setEnabled(True)
            self.__ui.btnConfigMonitorCreate.setDisabled(True)
        else:
            self.__ui.cbxConfigNode.clear()
            self.__ui.cbxConfigTopicNode.clear()
            self.__ui.cbxConfigNode.addItem('New Node')
            self.__ui.cbxConfigTopicTopic.clear()
            self.__ui.cbxConfigTopicTopic.addItem('New Topic')

            self.clearNodeComponents()
            self.clearTopicComponents()
            self.clearOracleComponents()

            self.__ui.txtConfigMonitorName.clear()
            self.__ui.txtConfigMonitorLog.clear()
            self.__ui.cbxMonitorSilent.setCurrentIndex(0)
            self.__ui.cbxMonitorWarning.setCurrentIndex(0)
            self.__ui.btnConfigMonitorCreate.setEnabled(True)
            self.__ui.btnConfigMonitorUpdate.setDisabled(True)
            self.__ui.btnConfigMonitorDelete.setDisabled(True)

    def fillOracle(self):
        """! Fills components of the Oracle class at relevant places in the interface.
        """

        index = self.__ui.cbxMonitorMonitor.currentIndex() - 1
        oracle = self.__monitors[index].getOracle()
        if oracle:
            self.__ui.txtConfigOraclePort.setText(str(oracle.getPort()))
            self.__ui.txtConfigOracleUrl.setText(oracle.getUrl())
            if oracle.getAction() == 'filter':
                self.__ui.cbxConfigOracleAction.setCurrentIndex(2)
            elif oracle.getAction() == 'log':
                self.__ui.cbxConfigOracleAction.setCurrentIndex(1)
            elif oracle.getAction() == 'nothing':
                self.__ui.cbxConfigOracleAction.setCurrentIndex(0)
            self.__ui.txtConfigOracleName.setText(
                str(oracle.getPort()) + ':' + oracle.getUrl() + '  -> ' + oracle.getAction())
            self.__ui.btnConfigOracleCreate.setDisabled(True)
            self.__ui.btnConfigOracleUpdate.setDisabled(False)
            self.__ui.btnConfigOracleDelete.setDisabled(False)
        else:
            self.__ui.txtConfigOraclePort.clear()
            self.__ui.txtConfigOracleUrl.clear()
            self.__ui.txtConfigOracleName.clear()
            self.__ui.cbxConfigOracleAction.setCurrentIndex(0)
            self.__ui.btnConfigOracleCreate.setDisabled(False)
            self.__ui.btnConfigOracleUpdate.setDisabled(True)
            self.__ui.btnConfigOracleDelete.setDisabled(True)

    def clearTopicComponents(self):
        """! Clears Topic class components in the interface.
        """

        self.__ui.txtConfigTopicName.clear()
        self.__ui.txtConfigTopicType.clear()
        self.__ui.cbxConfigTopicAction.setCurrentIndex(0)
        self.__ui.cbxConfigTopicNode.clear()
        self.__ui.cbxConfigTopicTopic.clear()
        self.__ui.cbxConfigTopicTopic.addItem("New Topic")
        self.__ui.cbxConfigTopicTopic.setCurrentIndex(0)
        self.__ui.btnConfigTopicCreate.setEnabled(True)
        self.__ui.btnConfigTopicUpdate.setDisabled(True)
        self.__ui.btnConfigTopicDelete.setDisabled(True)

    def clearNodeComponents(self):
        """! Clears Node class components in the interface.
        """

        self.__ui.txtConfigNodeName.clear()
        self.__ui.txtConfigNodePath.clear()
        self.__ui.txtConfigNodePackage.clear()
        self.__ui.cbxConfigNode.clear()
        self.__ui.cbxConfigNode.addItem("New Node")
        self.__ui.cbxConfigNode.setCurrentIndex(0)
        self.__ui.btnConfigNodeCreate.setEnabled(True)
        self.__ui.btnConfigNodeUpdate.setDisabled(True)
        self.__ui.btnConfigNodeDelete.setDisabled(True)

    def clearOracleComponents(self):
        """! Clears Oracle class components in the interface.
        """

        self.__ui.txtConfigOraclePort.clear()
        self.__ui.txtConfigOracleUrl.clear()
        self.__ui.txtConfigOracleName.clear()
        self.__ui.cbxConfigOracleAction.setCurrentIndex(0)
        self.__ui.btnConfigOracleCreate.setDisabled(False)
        self.__ui.btnConfigOracleUpdate.setDisabled(True)
        self.__ui.btnConfigOracleDelete.setDisabled(True)

    def clearMonitorComponents(self):
        """! Clears Monitor class components in the interface.
        """

        self.__ui.cbxMonitorMonitor.clear()
        self.__ui.cbxMonitorMonitor.addItem("New Monitor")
        self.__ui.cbxMonitorMonitor.setCurrentIndex(0)

        self.__ui.cbxMonitorSilent.setCurrentIndex(0)
        self.__ui.cbxMonitorWarning.setCurrentIndex(0)
        self.__ui.txtConfigMonitorName.clear()
        self.__ui.txtConfigMonitorLog.clear()
        self.__ui.btnConfigMonitorDelete.setDisabled(True)
        self.__ui.btnConfigMonitorUpdate.setDisabled(True)
        self.__ui.btnConfigMonitorCreate.setDisabled(False)

    def fillNodeLists(self):
        """! Fills node class combo box with node items inside config interface.
        """

        index = self.__ui.cbxMonitorMonitor.currentIndex() - 1
        nodes = self.__monitors[index].getNodes()
        self.__ui.cbxConfigNode.clear()
        self.__ui.cbxConfigTopicNode.clear()
        self.__ui.cbxConfigNode.addItem('New Node')
        for node in nodes:
            self.__ui.cbxConfigNode.addItem(node.getName())
            self.__ui.cbxConfigTopicNode.addItem(node.getName())

    def previewListWidget(self):
        """! Separates the file content for sharing in the interface.
        """

        self.__ui.listWidget.clear()
        for line in self.cast2configFile().split('\n'):
            self.__ui.listWidget.addItem(line)

    def saveConfig2file(self):
        """! Saves new config file format into local files.
        """

        if not self.__ui.txtConfigSaveYaml.text():
            self.__logger.printLog("Please fill the file name field.", color="red")
            return
        if not self.__monitors.__len__():
            self.__logger.printLog("Can not cast to file, no monitor exists.", color="red")
            return
        try:
            with open(
                    f"3rdparty/rosmonitoring/generator/online_configs/{self.__ui.txtConfigSaveYaml.text()}" + ".yaml",
                    'w') as file:
                if not file:
                    raise IOError("An error occurred while reading the file")
                file.write(self.cast2configFile())
                file_name=file
                self.__ui.txtConfigSaveYaml.clear()
                self.__logger.printLog("Config file successfully created.", "green")
        except IOError:
            self.__logger.printLog("An error occurred while reading the file", color="red")
        except:
            self.__logger.printLog("ERROR in saveConfig2file()", color="red")
        return file_name
    
    def importConfig(self):
        """! Imports local config file format into interface.
        """

        fname = "filename"
        try:
            fname, filter = QFileDialog.getOpenFileName(None, 'Select config file',
                                                        '3rdparty/rosmonitoring/generator/online_configs/',
                                                        'Graph (*.yaml);;All files (*)')
            if not fname:
                raise ImportError(f"<CONFIG IMPORT> An error occurred while {fname} importing")
            self.insertConfigFile(fname)

        except ImportError:
            self.__logger.printLog(f"An error occurred while {fname} importing", color="red")
        except:
            self.__logger.printLog(f"ERROR in importConfig()", color="red")
        finally:
            pass

    def cast2configFile(self):
        """! Creates new config file format.
        """

        fileNodes = "#CREATED FILE\n\n"
        fileTopics = ""
        nodeList = []
        if len(self.__monitors) > 0:
            fileTopics += 'monitors:\n'
            for monitor in self.__monitors:
                fileTopics += '  - monitor:\n'
                fileTopics += '      id: ' + monitor.getName() + '\n'
                fileTopics += '      log: ' + monitor.getLogFileName() + '\n'
                fileTopics += '      silent: ' + str(monitor.getSilent()) + '\n'
                fileTopics += '      warning: ' + ("1" if monitor.getWarning() else "0") + '\n'
                oracle = monitor.getOracle()
                if oracle:
                    fileTopics += '      oracle:\n'
                    fileTopics += '        port: ' + str(oracle.getPort()) + '\n'
                    fileTopics += '        url: ' + oracle.getUrl() + '\n'
                    fileTopics += '        action: ' + oracle.getAction() + '\n'
                topicList = monitor.getTopics()
                if len(topicList) > 0:
                    fileTopics += '      topics:\n'
                    for topic in topicList:
                        fileTopics += '        - name: ' + topic.getName() + '\n'
                        fileTopics += '          type: ' + topic.getType() + '\n'
                        fileTopics += '          action: ' + topic.getAction() + '\n'
                        publisherList = topic.getPublishers()
                        if len(publisherList) > 0:
                            fileTopics += '          publishers:\n'
                            for publisher in publisherList:
                                fileTopics += '            - ' + publisher + '\n'
                for node in monitor.getNodes():
                    if node not in nodeList and node:
                        nodeList.append(node)

            if len(nodeList) > 0:
                fileNodes += 'nodes:\n'
                for node in nodeList:
                    fileNodes += '  - node:\n'
                    fileNodes += '      name: ' + node.getName() + '\n'
                    fileNodes += '      package: ' + node.getPackageName() + '\n'
                    fileNodes += '      path: ' + node.getPath() + '\n'
                fileNodes += '\n\n'

        return fileNodes + fileTopics

    def insertConfigFile(self, filename):
        """! Loads config file into interface.

        @param filename Specifies the name of the file we add.
        """

        with open(filename) as file:
            configfile = yaml.load(file, Loader=yaml.FullLoader)
            self.insertConfigFile1(configfile)
        

    def insertConfigFile1(self, monitorYAMLContent: dict):
        """! Inserts file objects into list format.

        @param monitorYAMLContent specifies our dictionary.
        """

        nodes = {}
        for node in monitorYAMLContent["nodes"]:
            nodes[node["node"]["name"]] = node["node"]

        monitors = []
        for monitor in monitorYAMLContent["monitors"]:
            tempNodes = []
            for topic in monitor["monitor"]["topics"]:
                node = nodes[topic["publishers"][0]]
                tempNodes.append(Node(name=node["name"],
                                      type=None,
                                      packageName=node["package"],
                                      path=node["path"],
                                      topics=[Topic(
                                          name=topic["name"],
                                          type=topic["type"],
                                          action=topic["action"],
                                          publishers=topic["publishers"])]
                                      )
                                 )
            print(5)
            mon = Monitor(name=monitor["monitor"]["id"],
                          logFileName=monitor["monitor"]["log"],
                          silent=monitor["monitor"]["silent"],
                          warning=monitor["monitor"]["warning"],
                          oracle=Verifier(port=monitor["monitor"]["oracle"]["port"],
                                          url=monitor["monitor"]["oracle"]["url"],
                                          action=monitor["monitor"]["oracle"]["action"]),
                          nodes=tempNodes)
            self.__monitors.append(mon)
            self.__ui.cbxMonitorMonitor.addItem(monitor["monitor"]["id"])
        self.previewListWidget()

        self.__logger.printLog(message="Config file imported successfully", color="green")
