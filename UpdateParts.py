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
        if FreeCADGui.Selection.getCompleteSelection():
            box = FreeCADGui.Selection.getCompleteSelection()[0]
            if box.TypeId == "App::FeaturePython":
                if (box.Proxy.Type == 'SpaceBox'):
                    box.Proxy.updatebody(box)
        FreeCAD.ActiveDocument.recompute()

    def IsActive(self):
        return True