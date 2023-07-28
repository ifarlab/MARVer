from bin.UI_MARVer import Ui_MainWindow
from include.marver_m.calc_drag_listbox import QDMDragListbox
from include.marver_m.MyWidget import INodeWidget


class GuiModelDesign:
    NodeEditorWidget_class = INodeWidget

    def __init__(self, ui: Ui_MainWindow = None):
        self.__ui = ui

    def setModelEditorWidgets(self):
        self.lw = QDMDragListbox()
        self.lw.setParent(self.__ui.W_MarverM_Drag)
        self.lw.setVisible(True)

        self.nodeeditor = self.__class__.NodeEditorWidget_class(self.__ui.W_MarverM_EditorPlain)
        self.nodeeditor.setParent(self.__ui.W_MarverM_EditorPlain)
        self.nodeeditor.setVisible(True)

    def startModelEditor(self):
        self.setModelEditorWidgets()
