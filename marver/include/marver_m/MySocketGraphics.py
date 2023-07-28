# -*- coding: utf-8 -*-
"""
A module containing Graphics representation of a :class:`~nodeeditor.node_socket.Socket`
"""
from qtpy.QtWidgets import QGraphicsItem
from qtpy.QtGui import QColor, QBrush, QPen, QPainterPath
from qtpy.QtCore import Qt, QRectF, QPointF
from nodeeditor.node_graphics_socket import QDMGraphicsSocket


class IQDMGraphicsSocket(QDMGraphicsSocket):
    def __init__(self, socket:'Socket'):
        super().__init__(socket)

        self.paintPath = self.setPaintPath()

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self._brush)
        painter.setPen(self._pen if not self.isHighlighted else self._pen_highlight)
        painter.drawPath(self.paintPath)

    def setPaintPath(self):
        direction = 1
        if self.socket.is_input == True: direction = 1
        else: direction = -1
        if (self.socket.socket_type == 0):
            return self.circlePath(0, 0, direction)
        elif (self.socket.socket_type == 1):
            return self.trianglePath(0, 0, direction)
        elif (self.socket.socket_type == 2):
            return self.trianglePath(0, 0, direction * -1)
        elif (self.socket.socket_type == 3):
            return self.arrowShapePath(0, 0, direction)
        else:
            return self.arrowShapePath(0, 0, direction * -1)

    def trianglePath(self, cx, cy, direction):
        path = QPainterPath(QPointF(cx - direction*20, cy - direction*16))
        path.lineTo(QPointF(cx + direction*10, cy))
        path.lineTo(QPointF(cx - direction*20, cy + direction*16))
        path.lineTo(QPointF(cx - direction*20, cy - direction*16))
        return path

    def arrowShapePath(self, cx, cy, direction):
        path = QPainterPath(QPointF(cx - direction * 20, cy - direction * 15))
        path.lineTo(QPointF(cx + direction * 10, cy - direction * 15))
        path.lineTo(QPointF(cx + direction * 20, cy))
        path.lineTo(QPointF(cx + direction * 10, cy + direction * 15))
        path.lineTo(QPointF(cx - direction * 20, cy + direction * 15))
        path.lineTo(QPointF(cx - direction * 10, cy))
        path.lineTo(QPointF(cx - direction * 20, cy - direction * 15))
        return path

    def circlePath(self, cx, cy, direction):
        path = QPainterPath(QPointF(cx-20, cy-5))
        path.arcTo(cx-20, cy-25,cx+40, cy+40, 180, 360.0)
        path.closeSubpath()
        return path