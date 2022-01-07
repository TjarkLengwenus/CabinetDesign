# -*- coding: utf-8 -*-
###################################################################################
#
#  InitGui.py
#  
#  Copyright 2018 Mark Ganson <TheMarkster> mwganson at gmail
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
###################################################################################
# Initialize the workbench
import FreeCADGui
import FreeCAD

from AddPart import AddPart
from Stretch import Stretch
from UpdateParts import UpdateParts
from CutList import CutList
from Objects.SpaceBox import SpaceBoxCommand
from SetVisible import SetVisible
from StackTable import StackCommand
from LibaryChooser import LibaryCommand


class CabinetDesign(Workbench):
    MenuText = "CabinetDesign"
    ToolTip = "Design Cabinets in a simpel way"
    Icon = FreeCAD.getUserAppDataDir() + "Mod/CabinetDesign/Icons/CabinetDesignIcon.png"

    def Initialize(self):
        self.list = ['cab_CutList','cab_SpaceBox','cab_StackTable','cab_Libary','cab_setVilible', 'cab_updateParts','cab_Stretch','cab_AddPart']  # A list of command names created in the line above
        self.appendToolbar("Cabinetdesign", self.list)  # creates a new toolbar with your commands
        self.appendMenu("Cabinetdesign", self.list)  # creates a new menu


    def Activated(self):
        pass

    def Deactived(self):
        pass

    def ContextMenu(self, recipient):
        """This is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("CabinetDesign", self.list)  # add commands to the context menu

    def GetClassName(self):
        # This function is mandatory if this is a full Python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"

FreeCADGui.addCommand('cab_CutList',CutList())
FreeCADGui.addCommand('cab_SpaceBox',SpaceBoxCommand())
FreeCADGui.addCommand('cab_StackTable',StackCommand())
FreeCADGui.addCommand('cab_Libary', LibaryCommand())
FreeCADGui.addCommand('cab_setVilible', SetVisible())
FreeCADGui.addCommand('cab_updateParts', UpdateParts())
FreeCADGui.addCommand('cab_Stretch', Stretch())
FreeCADGui.addCommand('cab_AddPart', AddPart())

wb = CabinetDesign()
FreeCADGui.addWorkbench(wb)






