import getpass
from PyQt5.QtWidgets import *
from src.marver_r.GuiLog import GuiLog
from src.marver_r.RVOnline import RVOnline
from include.marver_r.Property import Property
from bin.UI_MARVer import Ui_MainWindow
from include.marver_r.Exceptions import *
from include.marver_r.Monitor import Monitor
from include.marver_r.Verifier import Verifier
from include.marver_r.Node import Node
from include.marver_r.Topic import Topic
from src.marver.Project import Project
import os, json, time
import subprocess
import threading
import yaml

global configFile

class GuiMonitor:

    def __init__(self, ui: Ui_MainWindow = None, project: Project = None, logger: GuiLog = None,
                 monitor: [Monitor] = []):
        self.__ui = ui
        self.__project = project
        self.__logger = logger
        self.__monitor = monitor
        self.__rvOnline = RVOnline(ui=self.__ui, logger=self.__logger)
        self.__status = -1  # 0:socker connection 1:monitor connection 2:instrumentation connection
        self.__stop = False

    def selectProjectFile(self):
        try:
            path = self.openFileDialogWindow("../", "json")
            jsonFile = self.getJSONFileContent(path)
            self.__project.setRosPath(jsonFile["RosFolderPath"])
            self.__project.setConfFilePath(jsonFile["ConfFilePath"])
            self.__project.setPropertyFilePath(jsonFile["PropertyFilePath"])
            self.__project.setProjectFilePath(path)

            self.prepareProjectEnv()

        except Exception as e:
            self.__logger.printLog(message=e.args[0], color="red")

    def prepareProjectEnv(self):
        self.selectROSWs(True)
        self.selectConfFile(True)
        self.selectPropertyFile(True)

    def selectROSWs(self, isReady: bool):
        if not isReady:
            self.__project.setRosPath(self.openFolderDialogWindow())

        if not self.__project.getRosPath():
            return
        try:
            if self.runCommand(f"rm -rf {self.__project.getRosPath()}/src/monitor"):
                self.__logger.printLog("The monitor link is deleted from Ros workspace successfully", "black")
            else:
                raise LinkMonitor2ROSWs

            if self.runCommand(
                    f"ln -s {os.getcwd()}/3rdparty/rosmonitoring/monitor {self.__project.getRosPath()}/src"):
                self.__logger.printLog("Monitor link is created into Ros workspace successfully", "black")
            else:
                raise LinkMonitor2ROSWs

        except LinkMonitor2ROSWs:
            self.__logger.printLog("An error is occurred while the monitor folder linking into Ros workspace", "red")

    def selectConfFile(self, isReady: bool):
        global configFile
        if not self.__project.getRosPath():
            self.__logger.printLog("First select the ROS workspace", "red")
            return
        try:
            if not isReady:
                self.__project.setConfFilePath(
                    self.openFileDialogWindow("3rdparty/rosmonitoring/generator/online_configs/", "yaml"))

            if self.__project.getConfFilePath():
                with open(self.__project.getConfFilePath()) as file:
                    # The FullLoader parameter handles the conversion from YAML
                    # scalar values to Python the dictionary format
                    configFile = yaml.load(file, Loader=yaml.FullLoader)
                    self.__monitor = self.getMonitorConfigFileContent(configFile)
                    

                self.convertYAML2MonitorPy(filePath=self.__project.getConfFilePath())
                self.__logger.printLog("Selecting conf .yaml file is complete successfully", "black")
                # configFile
                
            if self.runCommand("chmod +x ~/marver/3rdparty/rosmonitoring/oracle/TLOracle/oracle.py"):
                self.__logger.printLog("TLOracle got executable permission successfully.", "black")
            else:
                raise GetExecutableAuthTLOracle

            self.catkinMake()
           
        except MonitorNotExist:
            self.__logger.printLog(
                message="An error occurred while searching for a monitor. Create or import a monitor first!",
                color="red")
            
        except GetExecutableAuthTLOracle:
            self.__logger.printLog("An error is occurred while setting executable authentication to the TLOracle",
                                   "red")
        except:
            self.__logger.printLog("An error is occurred while conf .yaml file selecting", "red")
       
    
    def convertYAML2MonitorPy(self, filePath: str):
        try:
            if self.runCommand("chmod +x ~/marver/3rdparty/rosmonitoring/generator/generator"):
                self.__logger.printLog("Generator got executable permission successfully.", "black")
            else:
                raise GetExecutableAuthGenerator
            os.chdir("3rdparty/rosmonitoring/generator/")
            if self.runCommand(f"./generator --config_file {filePath}"):
                self.__logger.printLog(message="Monitor file is generated successfully", color="black")
            else:
                os.chdir("../../")
                raise ConvertYAML2MonitorPy

            os.chdir("../../")
            if self.runCommand(f"chmod +x ~/marver/3rdparty/rosmonitoring/monitor/src/{self.__monitor[0].getName()}.py"):
                self.__logger.printLog("The monitor got executable permission successfully.", "black")
            else:
                raise GetExecutableAuthMonitor

        except GetExecutableAuthGenerator:
            self.__logger.printLog("An error is occurred while setting executable authentication to the generator",
                                   "red")
        except GetExecutableAuthMonitor:
            self.__logger.printLog("An error is occurred while setting executable authentication to the monitor",
                                   "red")
        except ConvertYAML2MonitorPy:
            self.__logger.printLog("An error occurred while generating monitor file from .yaml configuration", "red")
        except:
            self.__logger.printLog("An error is occurred in convertYAML2MonitorPy()", "red")

    def openFolderDialogWindow(self):
        tmp = "/home/" + getpass.getuser() + "/catkin_ws"
        try:
            rosWsFolder = QFileDialog.getExistingDirectory(None, "Select your catkin_ws folder", "/home")
            if rosWsFolder == tmp:
                self.__logger.printLog(message="ROS workspace folder selection completed successfully", color="black")
                return rosWsFolder
            else:
                raise IOError(f"An error occurred while opening the folder")
        except IOError:
            self.__logger.printLog(message=f"An error occurred while opening the folder", color="red")
        except:
            self.__logger.printLog(message="An error is occurred in openFolderDialogWindow()", color="red")

    def openFileDialogWindow(self, baseFolder, extension: str) -> str:
        try:
            filePath, check = QFileDialog.getOpenFileName(None, "Open File", baseFolder,
                                                          f"Text Files (*.{extension})")
            if filePath:
                self.__logger.printLog(message="File selection completed successfully", color="black")
                return filePath
            else:
                raise IOError(f"An error occurred while opening the file")
        except IOError:
            self.__logger.printLog(message=f"An error occurred while opening the file", color="red")
        except:
            self.__logger.printLog(message="An error is occurred in openFileDialogWindow()", color="red")

    def getJSONFileContent(self, filePath: str):
        try:
            with open(filePath) as file:
                if not file:
                    raise IOError(f"An error occurred while reading the file")
                self.__logger.printLog(message="File content read successfully", color="black")
                self.__project.setPropertyFilePath(filePath)
                return json.load(file)
        except IOError:
            self.__logger.printLog(message=f"An error occurred while reading the file", color="red")
        except:
            self.__logger.printLog(message="ERROR in getJSONFileContent()", color="red")

    def getMonitorConfigFileContent(self, monitorYAMLContent: dict) -> Monitor:
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
                                      launchName=node["path"],
                                      topics=[Topic(
                                          name=topic["name"],
                                          type=topic["type"],
                                          action=topic["action"],
                                          publishers=topic["publishers"])]
                                      )
                                 )

            monitors.append(Monitor(name=monitor["monitor"]["id"],
                                    logFileName=monitor["monitor"]["log"],
                                    silent=monitor["monitor"]["silent"],
                                    warning=monitor["monitor"]["warning"],
                                    oracle=Verifier(port=monitor["monitor"]["oracle"]["port"],
                                                    url=monitor["monitor"]["oracle"]["url"],
                                                    action=monitor["monitor"]["oracle"]["action"]),
                                    nodes=tempNodes))

        return monitors

    def catkinMake(self):
        try:
            if self.runCommand(f"catkin_make --directory {self.__project.getRosPath()}"):
                self.__logger.printLog(message="Ros workspace built successfully", color="black")
            else:
                raise CatkinMakeError

        except CatkinMakeError:
            self.__logger.printLog(
                message="An error is occurred while catkin_make process. Please select ros workspace first.",
                color="red")

    def selectPropertyFile(self, isReady: bool):

        if not self.__project.getRosPath() or not self.__project.getConfFilePath():
            self.__logger.printLog("First select the ROS workspace and Configuration file", "red")
            return

        if not isReady:
            if self.__ui.cbxMonitorVerifierType.currentText() == "TL Oracle":
                self.convertProperty2TL(
                    self.openFileDialogWindow("../3rdparty/rosmonitoring/oracle/TLOracle/properties/", "json"))
            # else:
            #     self.convertProperty2RML(
            #         self.openFileDialogWindow("3rdparty/rosmonitoring/oracle/RMLOracle/rml/properties/", "json"))
        else:
            self.convertProperty2TL(self.__project.getPropertyFilePath())

    def convertProperty2TL(self, filePath: str):
        try:
            propertiesDict = self.getJSONFileContent(filePath)
            if propertiesDict:
                self.generateTLPropertyFile(propertiesDict["properties"][0]["name"],
                                            propertiesDict["properties"][0]["formula"])
                for property in propertiesDict["properties"]:
                    self.__monitor[0].getOracle().setProperties(
                        Property(property["name"], property["description"], property["formula"], property["nodeNames"]))
            else:
                self.__logger.printLog(message="An error occurred while property file reading", color="red")
        except:
            self.__logger.printLog(message="An error occurred while converting property to TL", color="red")

    def generateTLPropertyFile(self, name: str, formula: str):
        try:
            """
            with open(f"3rdparty/rosmonitoring/oracle/TLOracle/{name}.py", "w") as file:
                content = ''
                content += '''\nPROPERTY="{formula}"\n\n\n'''.format(formula=formula)
                content += 'def abstract_message(message):\n'
                content += '\tparsed_msg = {}\n'
                content += '\tfor key,value in message.items():\n'
                content += '\t\tfor k,v in value.items():\n'
                content += '\t\t\tparsed_msg[str(key)+"_"+str(k)] = v\n\n'
                content += '\tprint(parsed_msg)\n'
                content += '\treturn parsed_msg\n\n'
            """
            with open(f"/home/" + getpass.getuser() + f"/marver/3rdparty/rosmonitoring/oracle/TLOracle/{name}.py", "w") as file:
                content = ''
                content += '''\nPROPERTY="{formula}"\n\n\n'''.format(formula=formula)
                content += 'def abstract_message(message):\n'
                content += '\treturn message\n\n'
                file.write(content)
                self.__ui.txtMonitorSelectedProperty.setText(formula)
                self.__ui.btnMonitorStartRV.setEnabled(True)

        except:
            self.__logger.printLog(message="An error occurred while property writing to file", color="red")

    def convertProperty2RML(self, filePath: str):
        pass

    def runCommand(self, command) -> bool:
        process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True, text=True)

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.__logger.printLog(message=output.strip())

        rc = process.poll()
        return rc == 0

    def initializeRV(self):
        try:
            if not self.__monitor:
                raise StartRVError

            # initialize socket thread
            self.__thSocketConn = threading.Thread(target=self.__rvOnline.startSocketConnection,
                                                   args=(
                                                       "online",
                                                       self.__monitor[0].getOracle().getProperties()[0].getName(),
                                                       self.__monitor[0].getOracle().getPort(),
                                                       "discrete"))
            # initialize monitor thread
            self.__thMonitor = threading.Thread(target=self.__rvOnline.startMonitor)
            # initialize livestream thread
            self.__thLiveStream = threading.Thread(target=self.__rvOnline.startLiveStreamLogging,
                                                   args=(self.__monitor[0].getName(),))

            self.__thSocketConn.daemon = True
            self.__thMonitor.daemon = True
            self.__thLiveStream.daemon = True

            # initialize nodes threads
            self.__thInstrumentation = []
            for node in self.__monitor[0].getNodes():
                path = node.getPath()
                path = path.split("/")[-1].split(".")[0]
                temp = threading.Thread(target=self.__rvOnline.startInstrumentation,
                                        args=(node.getPackageName(), path))
                temp.daemon = True
                self.__thInstrumentation.append(temp)
                del path

            self.__logger.printLog(message="Runtime verification setup is ready to go.", color="black")
            self.__ui.btnMonitorStartRV.setEnabled(False)
            # self.__ui.btnMonitorStartRV.setStyleSheet('QPushButton {color: green;}')

            # start all threads
            self.startRV()

        except StartRVError:
            self.__logger.printLog(message="Please select a monitor first!", color="red")

    def startRV(self):
        try:
            self.__logger.printMonitorResult(message="Socket connection is starting ...")
            self.__thSocketConn.start()
            print("SOCKET CONNECTION STARTED")
            time.sleep(5)
            self.__logger.printMonitorResult(message="Socket communication is started successfully", color="black")

            self.__logger.printMonitorResult(message="Monitor connection is starting ...")
            self.__thMonitor.start()
            time.sleep(3)
            self.__logger.printMonitorResult(message="The monitor is initialized successfully", color="black")

            for th in self.__thInstrumentation:
                self.__logger.printMonitorResult(message="Instrumented node is starting ...")
                th.start()
                time.sleep(3)
                self.__logger.printMonitorResult(message="The instrumentation is initialized successfully",
                                                 color="black")
            time.sleep(1)
            self.__logger.printMonitorResult(message=" >>> Runtime verification setup is READY <<< ", color="blue")
            self.__ui.btnMonitorStopRV.setEnabled(True)
            self.__thLiveStream.start()

        except Exception as e:
            print(e)

    def stopRV(self):
        self.__rvOnline.stopAllProcess()
        self.__ui.btnMonitorStopRV.setEnabled(False)
        self.__ui.btnMonitorStartRV.setEnabled(True)




messages={}
"""
odt:  { distance: 3, topic: odt_pose ..... }
chatter : { C1:3 C2:4 .... }
"""