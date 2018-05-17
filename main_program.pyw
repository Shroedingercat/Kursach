# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
from Interface import *
from DIalog import MyDialog
import Gridcl
import sys
from Image import filters


class MyWindow(QtWidgets.QMainWindow):
    """Соркин Н.А Сапожников А.А
    Класс реализует главное окно приложения
    """
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.item = ''
        self.length_scene = 861
        self.width_scene = 611
        self.scene = QtWidgets.QGraphicsScene(0.0, 0.0, self.length_scene, self.width_scene)
        self.ui.graphicsView.setScene(self.scene)
        r = self.ui.graphicsView.viewport().rect()
        self.img = QtGui.QImage(self.length_scene, self.width_scene,
                                QtGui.QImage.Format_ARGB32_Premultiplied)
        self.img.fill(QtGui.QColor("#ffffff").rgb())
        self.grid_item = Gridcl.Grid()
        self.grid_item.setPos(10, 10)
        self.grid_item.setVisible(True)
        self.scene.addItem(self.grid_item)

        self.Dialog = QtWidgets.QFileDialog()
        self.DialogSetting = QtWidgets.QInputDialog()

        self.flag = False
        self.flagRect = False
        self.flagEl = False
        self.flagPoint = False
        self.flagMousePoint = False
        self.flagMouseLine = False
        self.flagMouseEl = False
        self.flagMouseRect = False
        self.grid_flag = True
        self.Openflag = False
        self.PathOpen = ''
        self.coordinates = [0, 0, 0, 0]

        self.length = 20
        self.width = 30

        self.add_menu()
        self.add_tool_bar()

        self.ui.ButtonOk.clicked.connect(self.ok)
        self.ui.pushButton.clicked.connect(self.grid1)


    def add_tool_bar(self):
        """
        Сорокин Н.А
        Метод реализующий tool bar
        :return:
        """
        self.toolBar = QtWidgets.QToolBar("MyToolBar")
        self.actPoint = QtWidgets.QAction("&Point", self)
        self.actPoint.triggered.connect(self.mousePoint)
        self.toolBar.addAction(self.actPoint)
        self.actLine = QtWidgets.QAction("&Line", self)
        self.actLine.triggered.connect(self.mouseLine)
        self.actEl = QtWidgets.QAction("&Circle")
        self.actEl.triggered.connect(self.mouseEl)
        self.actRect = QtWidgets.QAction("&Rectangle")
        self.actRect.triggered.connect(self.mouseRect)
        self.toolBar.addAction(self.actRect)
        self.toolBar.addAction(self.actEl)
        self.toolBar.addAction(self.actLine)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

    def addImageToolBar(self):
        self.toolBar2 = QtWidgets.QToolBar("MyToolBar")
        self.actChangeCollor = QtWidgets.QAction("&Grey filter")
        self.actChangeCollor.triggered.connect(self.ImageFilgr)
        self.toolBar2.addAction(self.actChangeCollor)
        self.act_sepia = QtWidgets.QAction("&Sepia")
        self.act_sepia.triggered.connect(self.ImageFilSepia)
        self.toolBar2.addAction(self.act_sepia)
        self.act_negative = QtWidgets.QAction("&Negative")
        self.act_negative.triggered.connect(self.ImageFilNegative)
        self.toolBar2.addAction(self.act_negative)
        self.act_BlackWhite = QtWidgets.QAction("&Black and white")
        self.act_BlackWhite.triggered.connect(self.ImageFilbw)
        self.toolBar2.addAction(self.act_BlackWhite)
        self.addToolBar(QtCore.Qt.RightToolBarArea, self.toolBar2)

    def NewImage(self):
        place = self.item.offset()
        self.scene.removeItem(self.item)
        pix = QtGui.QPixmap(self.PathOpen.toLocalFile())
        self.item = QtWidgets.QGraphicsPixmapItem()
        self.item.setPixmap(pix)
        self.item.setOffset(place)
        self.scene.addItem(self.item)

    def ImageFilNegative(self):
        fil = filters(self.PathOpen.toLocalFile())
        fil.Negative()
        self.NewImage()

    def ImageFilSepia(self):
        fil = filters(self.PathOpen.toLocalFile())
        fil.Sepia()
        self.NewImage()

    def ImageFilgr(self):
        fil = filters(self.PathOpen.toLocalFile())
        fil.ImageEditbw()
        self.NewImage()

    def ImageFilbw(self):
        fil = filters(self.PathOpen.toLocalFile())
        fil.BlackWhite()
        self.NewImage()

    def mouseRect(self):
        """
        Сорокин Н.А
        Метод реализующийся в случае выбора прямоугольника
        :return:
        """
        self.flagMouseRect = True
        self.count3 = 0
        self.clouse()
        self.flagMouseLine = False

    def mouseEl(self):
        """
        Сорокин Н.А
        Метод реализующийся в случае выбора эллипса
        :return:
        """
        self.flagMouseEl = True
        self.count2 = 0
        self.clouse()
        self.flagMouseLine = False

    def mousePoint(self):
        """
        Сорокин Н.А
        Метод реализующийся в случае выбора точки
        :return:
        """
        self.flagMousePoint = True
        self.setMouseTracking(True)
        self.ui.lineEdit.setText("")


    def mouseLine(self):
        """
        Сорокин Н.А
        Метод реализующийся в случае выбора линии
        :return:
        """
        self.flagMouseLine = True
        self.count = 0
        self.clouse()


    def add_menu(self):
        """
        Сорокин Н.А
        Метод реализущий меню бар
        :return:
        """
        self.menuFile = QtWidgets.QMenu("&File")
        self.actSave = QtWidgets.QAction(self)
        self.actSave.setText("&Save as")
        self.actSave.setShortcut("Ctrl+Shift+S")
        self.actSave.triggered.connect(self.SaveIm)
        self.menuFile.addAction(self.actSave)
        self.actOpen = QtWidgets.QAction(self)
        self.actOpen.setText("&Open")
        self.actOpen.triggered.connect(self.OpenFile)
        self.menuFile.addAction(self.actOpen)
        self.actMenuFile = self.menuBar().addMenu(self.menuFile)

        self.Setting = QtWidgets.QMenu("&Setting")
        self.actImage = QtWidgets.QAction(self)
        self.actImage.triggered.connect(self.ImageSetting)
        self.actImage.setText("&Image")
        self.actImage.setShortcut("Ctrl+Shift+I")
        self.Setting.addAction(self.actImage)
        self.actSetting = self.menuBar().addMenu(self.Setting)

        self.menuInfo = QtWidgets.QMenu("&Info")
        self.actCommands = QtWidgets.QAction(self)
        self.actCommands.triggered.connect(self.Info)
        self.actCommands.setText("&Commands")
        self.menuInfo.addAction(self.actCommands)
        self.actMenuInfo  = self.menuBar().addMenu(self.menuInfo)



    def Info(self):
        """
        Сапожников А.А
        выводит список команд
        :return:
        """
        QtWidgets.QMessageBox.about(window, "Info",
                                    "Лин или линия - нарисовать линию\nКруг - нарисовать круг\nТочка - нарисовать точку\nПримоугольник или прям - Нарисовать прямоугольник "
                                    )

    def ok(self):
        """
        Сапожников А.А
        Метод реализуется при нажатии кнопки оk и выводит геометрические фигуры заданные пользователем
        :return:
        """

        Text = self.ui.lineEdit.text()
        self.flag_draw = False

        if not self.Openflag :


            if self.flag:
                Text = self.ui.lineEdit.text()
                coordinates = coordinatesInput(Text)
                if len(coordinates) < 4:
                    pass
                else:
                    self.scene.addLine(coordinates[0],coordinates[1],coordinates[2],coordinates[3])
                    self.clouse()
            if self.flagRect:
                Text = self.ui.lineEdit.text()
                coordinates = coordinatesInput(Text)
                if len(coordinates)<4 :
                    pass
                else:
                    self.scene.addRect(coordinates[0], coordinates[1], coordinates[2] - coordinates[0],
                                    coordinates[3] - coordinates[1])
                    self.clouse()
            if self.flagEl:
                coordinates = coordinatesInput(Text)
                if len(coordinates) < 4:
                    pass
                else:
                    self.scene.addEllipse(coordinates[1], coordinates[2], coordinates[0], coordinates[0])
                    self.clouse()
            if self.flagPoint:
                coordinates = coordinatesInput(Text)
                if len(coordinates) < 2:
                    pass
                else:
                    self.scene.addEllipse(coordinates[0], coordinates[1],5,5,
                                                brush=QtGui.QBrush(QtCore.Qt.black))
                    self.clouse()
            if Text == "точка":
                self.flagPoint = True
                self.ui.lineEdit.setText("Введите координаты :")
            elif Text == "лин" or Text == "линия":
                self.flag = True
                self.ui.lineEdit.setText("Введите координаты :")
            elif Text == "прям" or Text == "Прямоугольник":
                self.flagRect = True
                self.ui.lineEdit.setText("Введите координаты :")
            elif Text == "круг":
                self.flagEl = True
                self.ui.lineEdit.setText("Введите радиус и координаты :")
            elif not self.flag_draw:
                self.ui.lineEdit.setText("Команда не распознана повторите ввод")
        else:
            self.item.setEnabled(not self.item.isEnabled())
            self.Openflag = False
            self.NONE()


    def clouse(self):
        """
        Сапожников А.А
        метод переводит все флаги на False
        :return:
        """
        self.flag_draw = True
        self.flagPoint = False
        self.flag = False
        self.flagRect = False
        self.flagEl = False
        self.ui.lineEdit.setText("")
        self.flagMousePoint = False

    def mousePressEvent(self, e):
        """
        Сорокин Н.А
        :param e: метод выполняется при любом вызове класса
        :return:
        """
        if self.flagMousePoint:
            self.coordinates[0] = e.x()
            self.coordinates[1] = e.y()
            self.scene.addEllipse(self.coordinates[0]-3, self.coordinates[1]-47, 5, 5,
                                brush=QtGui.QBrush(QtCore.Qt.black))
            QtWidgets.QMainWindow.mousePressEvent(self, e)

        elif self.flagMouseLine:
            if self.count == 1:
                self.coordinates[2] = e.x()
                self.coordinates[3] = e.y()
                self.scene.addLine(self.coordinates[0]-3, self.coordinates[1]-47, self.coordinates[2]-3, self.coordinates[3]-47)
            self.ui.lineEdit.setText("Выберите точку начала и конца линии")
            self.coordinates[0] = e.x()
            self.coordinates[1] = e.y()
            self.count += 1
        elif self.flagMouseEl :
            if self.count2 == 1:
                self.coordinates[2] = e.x() -3
                self.coordinates[3] = e.y() - 47
                R = ((self.coordinates[2] - self.coordinates[0])**2 + (self.coordinates[3] - self.coordinates[1])**2)**0.5
                self.scene.addEllipse(self.coordinates[0] - R, self.coordinates[1] - R,2*R,2*R)
            self.coordinates[0] = e.x() - 3
            self.coordinates[1] = e.y() - 47
            self.count2 += 1
        elif self.flagMouseRect :
            if self.count3 == 1 :
                self.coordinates[2] = e.x()-3
                self.coordinates[3] = e.y()-47
                self.scene.addRect(self.coordinates[0] , self.coordinates[1] , self.coordinates[2] - self.coordinates[0], self.coordinates[3] - self.coordinates[1])
            self.coordinates[0] = e.x()-3
            self.coordinates[1] = e.y()-47
            self.count3+=1


    def SaveIm(self):
        """
        Сорокин Н.А
        мето сохраняет изображение
        :return:
        """
        Path = self.Dialog.getSaveFileUrl(filter="Images (*.png *.jpg)", caption="Save")
        if Path[0].toLocalFile() !='' :
            painter = QtGui.QPainter()
            painter.begin(self.img)
            self.ui.graphicsView.render(painter)
            painter.end()
            self.img.save(Path[0].toLocalFile(),'png')


    def OpenFile(self):
        """
        Сорокин Н.А.
        Открывает и размещает картинку, выбранную пользователем
        :return:
        """
        self.PathOpen, l = QtWidgets.QFileDialog.getOpenFileUrl(parent=window,
                                                    caption="Open",
                                                    directory="file:///" + QtCore.QDir.currentPath(),
                                                    filter="Images (*.png *.jpg)")
        pix = QtGui.QPixmap(self.PathOpen.toLocalFile())
        if l != '':
            self.item = QtWidgets.QGraphicsPixmapItem()
            self.item.setPixmap(pix)
            self.item.setOffset(50, 50)


            self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
            self.scene.addItem(self.item)
            self.Openflag = True
            place = self.item.offset()
            self.addImageToolBar()

    def ImageSetting(self):
        """
        Сапожников А.А
        метод реализует все возможности вкладки setting
        :return:
        """
        dialog = MyDialog(window)
        result = dialog.exec_()
        if result == 1:
            length = int(dialog.spinbox.text())
            width = int(dialog.spinbox_2.text())
            self.length_scene = length
            self.width_scene = width
            self.ui.graphicsView.setGeometry(QtCore.QRect(10, 10, self.length_scene, self.width_scene))


    def grid1(self):
        self.grid_item.setVisible(not self.grid_item.isVisible())

    def NONE(self):
        pass

def coordinatesInput(Text):
    """
    Сапожников А.А
    Ищет числа введенные пользователем и преобразует их в список координат
    :param Text:строка введенная пользователем
    :return: coordinates: список координат
    """
    coordinates = []
    lenx = -1
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    nsymbol = -1
    while nsymbol < len(Text)-1:
        nsymbol += 1
        if (Text[nsymbol] in numbers):
            nsymbol2 = nsymbol + 1
            lenx += 1
            coordinates.append(Text[nsymbol])
            while nsymbol2 < len(Text) and Text[nsymbol2] != " " and Text[nsymbol2] in numbers:
                coordinates[lenx] += Text[nsymbol2]
                nsymbol2 += 1
            coordinates[lenx] = int(coordinates[lenx])
            nsymbol = nsymbol2
    return coordinates

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("Graphics editor")
    window.show()
    sys.exit(app.exec_())
