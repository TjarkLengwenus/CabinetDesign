import sys

import FreeCAD
import FreeCADGui
import os
from PySide2 import QtCore, QtWidgets

import Libary


class LibaryCommand:

    def GetResources(self):
        return {
            'MenuText': "Open Libary Part",
            'ToolTip': "open a menu of parts",
            'Pixmap': FreeCAD.getUserAppDataDir() + "Mod/CabinetDesign/Icons/LibaryIcon.png"
        }

    def Activated(self):
        ls = LibaryManager.libarychooser
        data = ls.choose()
        FreeCAD.openDocument(ls.lib + data)
        return

    def IsActive(self):
        return True



class LibaryChooser(QtWidgets.QDialog):

    ui = 'Libary.ui'
    lib = None
    item = None
    link = None
    name = ""
    items = []
    links = []
    part = None

    def __init__(self, parent=None):
        super(LibaryChooser, self).__init__()
        if FreeCAD.ParamGet("User parameter:BaseApp/CabinetDesign").IsEmpty():
            FreeCAD.ParamGet("User parameter:BaseApp/CabinetDesign").SetString("Lib",FreeCAD.getUserAppDataDir() + "Mod/CabinetDesign/Libary")
        self.lib = FreeCAD.ParamGet("User parameter:BaseApp/CabinetDesign").GetString("Lib")
        file = QtCore.QFile(self.ui)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Libary")
        self.ui = Libary.Ui_Dialog()
        self.ui.setupUi(self)
        self.setupUi()

    @staticmethod
    def load(link):
        doc1 = FreeCAD.ActiveDocument
        doc = FreeCAD.openDocument(link, True)
        FreeCAD.setActiveDocument(doc1.Name)
        part = doc.getObjectsByLabel(doc.Name)[0]

        return [part,doc,link]


    def choose(self):

        self.exec()

        return self.part



    def ok(self):
        self.part = self.link


    def setupUi(self):

        self.setuptreeview();

        self.ui.Dialog_2.accepted.connect(self.ok)
        self.ui.libary_tree.currentItemChanged.connect(self.changeItem)
        self.okBn = self.ui.Dialog_2.buttons()[0]

    def setuptreeview(self):
        def getParts(lib, dir, item):
            path = lib + dir
            if os.path.isfile(path):
                return False
            for file in os.listdir(path):
                if not os.path.isfile(path + '/' + file):
                    a = QtWidgets.QTreeWidgetItem([file])
                    item.addChild(a)
                    if getParts(lib,dir + '/' + file, a):
                        self.items.append(a)
                        self.links.append(dir + '/' + file)

                else:
                    return True
            return False

        a = QtWidgets.QTreeWidgetItem(["Libary"])
        getParts(self.lib,"", a)
        self.ui.libary_tree.addTopLevelItem(a)

    def changeItem(self,current,previous):
        if current in self.items:
            link = self.links[self.items.index(current)]
            self.okBn.setDisabled(False)
            self.item = current
            self.link = link + '/' + current.text(0) + ".FCStd"
            self.ui.view.setOpenLinks(True)
            self.ui.view.setUndoRedoEnabled(True)
            self.ui.view.setSource(QtCore.QUrl.fromLocalFile(self.lib + '/' + link + '/index.html'))
            self.name = current.text(0)

        else:
            self.okBn.setDisabled(True)
            self.ui.view.clear()
class LibaryManager:
    libarychooser = LibaryChooser()
