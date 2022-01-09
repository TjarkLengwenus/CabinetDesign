import FreeCAD
import FreeCADGui
class UpdateParts:

    def GetResources(self):
        return {
            'MenuText': "Open Libary Part",
            'ToolTip': "open a menu of parts",
            'Pixmap': FreeCAD.getUserAppDataDir() + "Mod/CabinetDesign/Icons/UpdateBodyIcon.png"
        }

    def Activated(self):
        for box in FreeCAD.ActiveDocument.findObjects():
            if hasattr(box,"SpaceBox"):
                box.Proxy.updatebody(box)
        FreeCAD.ActiveDocument.recompute()

    def IsActive(self):
        return True