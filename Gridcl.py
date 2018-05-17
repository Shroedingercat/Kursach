from PyQt5 import QtCore, QtWidgets, QtGui
from main_program import MyWindow

class Grid(QtWidgets.QGraphicsItem):
    """
    Сорокин Н.А
    Реализует графический обЪект сетка
    """
    def boundingRect(self):
        return QtCore.QRectF(0,0, 838,593)
    def paint(self, painter, option, widget):
        window =MyWindow()
        painter.save()
        painter.setPen(QtGui.QPen(QtCore.Qt.gray))
        for n_lines in range(1, (window.length_scene // 50) + 1):
            painter.drawLine(QtCore.QLine(50 * n_lines, 0, 50 * n_lines, window.length_scene))
        for n_lines in range(1, (window.width_scene // 50) + 1):
            painter.drawLine(
                QtCore.QLine(0, 50 * n_lines, window.length_scene, 50 * n_lines ))
        painter.restore()