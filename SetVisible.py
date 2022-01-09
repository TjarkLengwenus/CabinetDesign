import FreeCAD
class SetVisible:

    def GetResources(self):
        return {
            'MenuText': "Visible",
            'ToolTip': "Toggle SpaceBox Visible",
            'Pixmap': FreeCAD.getUserAppDataDir() + "Mod/CabinetDesign/Icons/VisibleIcon.png",
            'Checkable' : True
        }


    def Activated(self,mode):
        doc = FreeCAD.ActiveDocument
        temp = FreeCAD.ActiveDocument.addObject("Part::BodyBase", "temp")
        for obj in doc.findObjects():
            if hasattr(obj,"SpaceBox"):
                obj.Visible = mode
        doc.removeObject(temp.Label)
        doc.recompute()
        doc.recompute()





    def IsActive(self):
        return True