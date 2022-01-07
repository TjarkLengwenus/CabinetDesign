import FreeCAD
import FreeCADGui


class Stretch:

    def GetResources(self):
        return {
            'MenuText': "Stretch",
            'ToolTip': "stretch the last spacebox",
            'Pixmap': FreeCAD.getUserAppDataDir() + "Mod/CabinetDesign/Icons/StretchIcon.png"
        }

    def Activated(self):
        for box in FreeCAD.ActiveDocument.findObjects():
            if box.TypeId == "App::FeaturePython":
                if hasattr(box.Proxy,"Type"):
                    if (box.Proxy.Type == 'SpaceBox'):
                        if box.DrawerList:
                            last = box.DrawerList.pop()
                            a = 0
                            for i in range(len(box.DrawerList)-1):
                                dw = box.DrawerList[i]
                                if box.IsHorizontal:
                                    a = a + float(dw.Length)
                                else:
                                    a = a + float(dw.Height)

                            if box.IsHorizontal:
                                b = float(box.Length)
                            else:
                                b = float(box.Height)
                            heigth = b-a

                            if heigth > 0:
                                if box.IsHorizontal:
                                    last.Length = heigth
                                else:
                                    last.Height = heigth
        FreeCAD.ActiveDocument.recompute()
        FreeCAD.ActiveDocument.recompute()

    def IsActive(self):
        return True

