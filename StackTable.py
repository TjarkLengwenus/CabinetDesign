import FreeCAD
import FreeCADGui
import OpenSCADUtils
import sys
from PySide import QtCore, QtGui

import Objects.SpaceBox
from UpdateParts import UpdateParts
import LibaryChooser


class StackCommand:
    def GetResources(self):
        return {
                'MenuText' : "Edit Stack Table",
                'ToolTip'  : "Edit the Stack Table of a SpaceBox",
                'Pixmap': FreeCAD.getUserAppDataDir() + "Mod/CabinetDesign/Icons/EditSpaceBoxTableIcon.png"
        }

    def Activated(self):


        if FreeCADGui.Selection.getCompleteSelection():
            box = FreeCADGui.Selection.getCompleteSelection()[0]
            if hasattr(box,"SpaceBox"):
                panel = StackTask(box)
        else:
            print("Select The SpaceBox")


        FreeCADGui.Control.showDialog(panel)
        panel.setupUi()
        return

    def IsActive(self):
        return True

class StackTask:
    def __init__(self,box):
        self.ui = FreeCAD.getUserAppDataDir() + "Mod/CabinetDesign/StackTableUi.ui"
        self.box = box



    def setupUi(self):
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QWidget,"Form")
        form.setGeometry(0,0,357,419)

        form.addLib_bn = form.findChild(QtGui.QPushButton, "addLib_bn")
        form.add_bn = form.findChild(QtGui.QPushButton, "add_bn")
        form.show_bn = form.findChild(QtGui.QPushButton, "show_bn")
        form.name_ln = form.findChild(QtGui.QLineEdit, "name_ln")
        form.remove_bn = form.findChild(QtGui.QPushButton, "remove_bn")
        form.copy_bn = form.findChild(QtGui.QPushButton, "copy_bn")
        form.list = form.findChild(QtGui.QListWidget, "list")
        form.height_spin = form.findChild(QtGui.QDoubleSpinBox, "height_spin")
        form.spacelabel = form.findChild(QtGui.QLabel,"spacelabel")
        form.horizontal_check = form.findChild(QtGui.QCheckBox, "horizontal_check")
        form.libary_bn = form.findChild(QtGui.QPushButton, "libary_bn")
        form.clear_body = form.findChild(QtGui.QPushButton, "clear_body")
        form.body_name = form.findChild(QtGui.QLabel, "body_name")

        

        form.list.setDragDropMode(QtGui.QAbstractItemView.InternalMove)

        if self.box.IsHorizontal:
            form.horizontal_check.setCheckState(QtCore.Qt.Checked)
        else:
            form.horizontal_check.setCheckState(QtCore.Qt.Unchecked)

        self.form = form



        for obj in self.box.DrawerList:
            text = ""
            if self.box.IsHorizontal:
                text = self.gettext(obj.Label, obj.Length)
            else:
                text = self.gettext(obj.Label, obj.Height)

            form.list.addItem(text)

        self.form.body_name.setText(self.box.BoxBodySrc)

        QtCore.QObject.connect(form.addLib_bn, QtCore.SIGNAL("clicked()"), self.addLib)
        QtCore.QObject.connect(form.add_bn , QtCore.SIGNAL("clicked()"), self.add)
        QtCore.QObject.connect(form.remove_bn, QtCore.SIGNAL("clicked()"), self.remove)
        QtCore.QObject.connect(form.copy_bn, QtCore.SIGNAL("clicked()"), self.copy)
        QtCore.QObject.connect(form.libary_bn, QtCore.SIGNAL("clicked()"), self.openLibary)
        QtCore.QObject.connect(form.clear_body, QtCore.SIGNAL("clicked()"), self.clearBody)
        QtCore.QObject.connect(form.show_bn, QtCore.SIGNAL("clicked()"), self.changed)
        QtCore.QObject.connect(form.list,QtCore.SIGNAL("currentRowChanged(int)"),self.updatePro)
        QtCore.QObject.connect(form.name_ln, QtCore.SIGNAL("editingFinished()"), self.changeName)
        QtCore.QObject.connect(form.horizontal_check, QtCore.SIGNAL("stateChanged(int)"), self.changeHorizental)
        QtCore.QObject.connect(form.height_spin, QtCore.SIGNAL("valueChanged(double)"), self.changeHeigth)
        self.form.list.model().rowsMoved.connect(self.changed)

    def addLib(self):

        box1 = self.add()
        lc = LibaryChooser.LibaryManager.libarychooser
        box1.BoxBodySrc = lc.choose()
        up = UpdateParts()
        up.Activated()

    def add(self):
        max = self.getMax()

        if(max <= 0):
            print("Der Schrank ist voll")
            return

        if max > 300:
            if self.box.IsHorizontal:
                box1 = Objects.SpaceBox.makeSpaceBox(300, self.box.Height, self.box.Width)
            else:
                box1 = Objects.SpaceBox.makeSpaceBox(self.box.Length, 300, self.box.Width)
        else:
            if self.box.IsHorizontal:
                box1 = Objects.SpaceBox.makeSpaceBox(max, self.box.Height, self.box.Width)
            else:
                box1 = Objects.SpaceBox.makeSpaceBox(self.box.Length, max, self.box.Width)
        self.box.addObject(box1)

        g = self.box.DrawerList
        g.append(box1)
        self.box.DrawerList = g



        text = ""
        if self.form.horizontal_check.isTristate():
            text = self.gettext(box1.Label, box1.Length)
            self.box.DrawerHeightList.append(box1.Length)
        else:
            text = self.gettext(box1.Label, box1.Height)

        self.form.list.addItem(text)
        self.box.recompute()
        return box1

    def remove(self):
        list = self.form.list
        box = self.box.DrawerList[list.currentRow()]

        self.removeObjects(box)
        list.takeItem(list.currentRow())
        list.removeItemWidget(list.selectedItems()[0])
        self.box.recompute()

    def copy(self):
        list = self.form.list
        box = self.box.DrawerList[list.currentRow()]
        boxcopy = self.box.Document.copyObject(box, True)

        self.box.addObject(boxcopy)

        g = self.box.DrawerList
        g.append(boxcopy)
        self.box.DrawerList = g

        text = ""
        if self.box.IsHorizontal:
            text = self.gettext(boxcopy.Label, boxcopy.Length)
            self.box.DrawerHeightList.append(boxcopy.Length)
        else:
            text = self.gettext(boxcopy.Label, boxcopy.Height)
        self.form.list.addItem(text)
        self.box.recompute()
        up = UpdateParts()
        up.Activated()



    def changed(self):
        list = self.form.list
        drawers = []
        for row in range(list.count()):
            item = list.item(row)
            obj = FreeCAD.ActiveDocument.getObject(self.getName(item.text()))
            drawers.append(obj)
        self.box.DrawerList = drawers
        self.box.recompute()

    def updatePro(self,row):
        list = self.form.list
        item = list.item(row)
        obj = FreeCAD.ActiveDocument.getObject(self.getName(item.text()))
        self.currow = row

        self.form.name_ln.setText(obj.Label)

        max = self.getMax()
        if self.box.IsHorizontal:
            self.form.height_spin.setMaximum(max + float(obj.Length))
            self.form.height_spin.setValue(obj.Length)
        else:
            self.form.height_spin.setMaximum(max + float(obj.Height))
            self.form.height_spin.setValue(float(obj.Height))



    def changeHeigth(self,height):
        item = self.form.list.item(self.currow)
        objname = self.getName(item.text())
        obj = FreeCAD.ActiveDocument.getObject(objname)



        if(self.box.IsHorizontal == False):
            obj.Height = height
            item.setText(self.gettext(objname,obj.Height))
        else:
            obj.Length = height
            item.setText(self.gettext(objname, obj.Length))
        self.form.spacelabel.setText(str(self.getMax()))
        self.box.recompute()


    def changeName(self):
        name = self.form.name_ln.text()
        item = self.form.list.item(self.currow)
        obj = FreeCAD.ActiveDocument.getObject(self.getName(item.text()))
        obj.Label = name

        if obj.IsHorizontal:
            item.setText(self.gettext(name,obj.Length))
        else:
            item.setText(self.gettext(name,obj.Height))
        self.box.recompute()


    def changeHorizental(self,boolean):
        if boolean == 0:
            self.box.IsHorizontal = False
        else:
            self.box.IsHorizontal = True
        self.box.recompute()

    def openLibary(self):
        lc = LibaryChooser.LibaryManager.libarychooser
        data = lc.choose()
        if data:
            self.form.body_name.setText("Body Src:" + data)
            self.box.BoxBodySrc = data
        up = UpdateParts()
        up.Activated()


    def clearBody(self):
        self.box.BoxBodySrc = ""
        self.form.body_name.setText("No Body Src")
        up = UpdateParts()
        up.Activated()


    def getName(self,text):
        name = text.split(':',1)[1]
        return (name)
    def gettext(self,text, double):
        return str(double) + ':' + text

    def getMax(self):
        a = 0
        for dw in self.box.DrawerList:
            if self.box.IsHorizontal:
                a = a + float(dw.Length)
            else:
                a = a + float(dw.Height)

        if self.box.IsHorizontal:
            b = float(self.box.Length)
        else:
            b = float(self.box.Height)

        return b - a

    def removeObjects(self,obj):
        if hasattr(obj,"Group"):
            if obj.Group:
                for dw in obj.Group:
                    self.removeObjects(dw)
        FreeCAD.ActiveDocument.removeObject(obj.Name)
    def accept(self):
        self.changed()
        self.updatePro()
    def down(self):
        pass
    def accept(self):
        return True
    def reject(self):
        return True
    def clicked(self, index):

        pass
    def open(self):
        pass
    def needsFullSpace(self):
        return False

    def isAllowedAlterSelection(self):
       return True

    def isAllowedAlterView(self):
        return True
    def isAllowedAlterDocument(self):
       return True

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)

    def helpRequested(self):
        pass
    def getMainWindow(self):
        toplevel = QtGui.QApplication.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                return i
        raise RuntimeError("No main window found")