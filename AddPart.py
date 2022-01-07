import os
from pathlib import Path
from shutil import copyfile

import FreeCAD
import FreeCADGui
from PySide2 import QtWidgets,QtCore,QtGui

from LibaryChooser import LibaryChooser


class AddPart:
    def GetResources(self):
        return {
            'MenuText': "Create Libary Part",
            'ToolTip': "create a new part for the Libary",
            'Pixmap': FreeCAD.getUserAppDataDir() + "Mod/CabinetDesign/Icons/AddPartIcon.png"
        }


    def Activated(self):
        text,ok = QtWidgets.QInputDialog.getText(QtWidgets.QDialog(),'Name?','Enter the Name for the Part:')
        if ok:
            ls = LibaryChooser()
            path = ls.lib + "/" + text + "/"
            fcfile = path + text + ".FCStd"
            docfile = path + "index.html"

            os.mkdir(path)
            copyfile(FreeCAD.getUserAppDataDir() + "Mod/cabinetbench/Resources/index.html",docfile)
            doc = FreeCAD.newDocument()

            part = FreeCAD.activeDocument().addObject('App::Part', text)

            block=FreeCAD.ActiveDocument.addObject("App::FeaturePython","block")#
            part.addObject(block)

            #add Propertys
            block.addProperty("App::PropertyLength", "Length", "input", "Length of the Part").Length = "1 m"
            block.addProperty("App::PropertyLength", "Width", "input", "Width of the Part").Width = "1 m"
            block.addProperty("App::PropertyLength", "Height", "input", "Height of the Part").Height = "1 m"

            block.addProperty("App::PropertyBool", "UseInnerBox", "output", "Do you Wand to use a InnerBox?").UseInnerBox = False
            block.addProperty("App::PropertyLength", "boxheight", "output", "Height of the InnerBox").boxheight = "1 m"
            block.addProperty("App::PropertyLength", "boxwidth", "output", "Width of the InnerBox").boxwidth = "1 m"
            block.addProperty("App::PropertyLength", "boxlength", "output", "Length of the InnerBox").boxlength = "1 m"
            block.addProperty("App::PropertyPlacement", "boxplacement", "output", "Placement of the InnerBox")

            doc.saveAs(fcfile)
