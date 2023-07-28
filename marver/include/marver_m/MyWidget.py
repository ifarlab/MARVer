from nodeeditor.node_editor_widget import *
from include.marver_m.MyNode import INode
from nodeeditor.utils import dumpException
DEBUG = False


class INodeWidget(NodeEditorWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.cnt = 0

        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)

    def onDragEnter(self, event):
        if event.mimeData().hasFormat("application/x-item"):
            event.acceptProposedAction()
        else:
            # print(" ... denied drag enter event")
            event.setAccepted(False)

    def onDrop(self, event):
        from qtpy.QtCore import QSize, Qt, QByteArray, QDataStream, QMimeData, QIODevice, QPoint
        from qtpy.QtGui import QPixmap, QIcon, QDrag
        import os

        if event.mimeData().hasFormat("application/x-item"):
            eventData = event.mimeData().data("application/x-item")
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            op_code = dataStream.readInt()
            text = dataStream.readQString()

            mouse_position = event.pos()
            scene_position = self.scene.grScene.views()[0].mapToScene(mouse_position)

            if DEBUG: print("GOT DROP: [%d] '%s'" % (op_code, text), "mouse:", mouse_position, "scene:", scene_position)

            try:
                inputArray = [0, 1, 2, 3, 4]
                outputArray = [0, 1, 2, 3, 4]

                if op_code == 1:
                    outputArray.clear()
                elif op_code == 2:
                    inputArray.clear()

                node = INode(self.scene, "Structure " + str(self.cnt), inputs=inputArray, outputs=outputArray)
                self.cnt = self.cnt + 1
                node.setPos(scene_position.x(), scene_position.y())

            except Exception as e: dumpException(e)


            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            # print(" ... drop ignored, not requested format '%s'" % LISTBOX_MIMETYPE)
            event.ignore()