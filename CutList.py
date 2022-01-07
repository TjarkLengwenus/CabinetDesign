import FreeCAD as App

from Objects import SpaceBox


class CutList():
    def GetResources(self):
        return {
                'MenuText' : "CutList",
                'ToolTip'  : "generate a cutlist of your parts",
                'Pixmap': App.getUserAppDataDir() + "Mod/CabinetDesign/Icons/CutListIcon.png"
        }

    def Activated(self):

        a = App.ActiveDocument

        sheet = a.addObject('Spreadsheet::Sheet', 'Spreadsheet')

        sheet.ViewObject.Visibility = False

        sheet.Label = "Part List"
        sheet.set("A1", "Length")
        sheet.set("B1", "Width")
        sheet.set("C1", "Qty")
        sheet.set("D1", "Material")
        sheet.set("E1","Label")
        sheet.set("F1", "Enabled")

        sizes = []
        forces = []

        cur_row = 1

        print('Stuckliste zu ' + a.Name + ':')
        for o in a.findObjects():
            try:
                if (o.TypeId == "PartDesign::Body"):



                    xyz = [o.Shape.BoundBox.XLength, o.Shape.BoundBox.YLength, o.Shape.BoundBox.ZLength]
                    x = 0
                    y = 0
                    z = 0
                    if (xyz[0] >= xyz[1] and xyz[0] >= xyz[2]):
                        x = xyz[0]
                    elif (xyz[1] >= xyz[0] and xyz[1] >= xyz[2]):
                        x = xyz[1]
                    elif (xyz[2] >= xyz[0] and xyz[2] >= xyz[1]):
                        x = xyz[2]
                    else:
                        x = xyz[0]

                    if (xyz[0] <= xyz[1] and xyz[0] <= xyz[2]):
                        z = xyz[0]
                    elif (xyz[1] <= xyz[0] and xyz[1] <= xyz[2]):
                        z = xyz[1]
                    elif (xyz[2] <= xyz[0] and xyz[2] <= xyz[1]):
                        z = xyz[2]
                    else:
                        z = xyz[0]

                    if ((xyz[0] <= xyz[1] and xyz[0] >= xyz[2]) or (xyz[0] >= xyz[1] and xyz[0] <= xyz[2])):
                        y = xyz[0]
                    elif ((xyz[1] <= xyz[0] and xyz[1] >= xyz[2]) or (xyz[1] >= xyz[0] and xyz[1] <= xyz[2])):
                        y = xyz[1]
                    elif ((xyz[2] <= xyz[1] and xyz[2] >= xyz[0]) or (xyz[2] >= xyz[1] and xyz[2] <= xyz[0])):
                        y = xyz[0]
                    else:
                        y = xyz[1]

                    #sheet.set("E" + str(cur_row), str(x * y))

                    cur_row += 1

                    print(x)
                    print(y)
                    print(x * y)

                    sheet.set("A" + str(cur_row), str(x))
                    sheet.set("B" + str(cur_row), str(y))
                    sheet.set("C" + str(cur_row), "1")
                    sheet.set("D" + str(cur_row),"force_" + str(z))
                    sheet.set("E" + str(cur_row), o.Label)
                    sheet.set("F" + str(cur_row), "true")


                    isready = False
                    if forces:
                        for i in range(len(forces)):
                            force = forces[i]
                            if force == z:
                                sizes[i] = sizes[i] + (x * y)
                                isready = True

                        if (isready == False):
                            sizes.extend([x * y])
                            forces.extend([z])
                    else:
                        sizes = [x * y]
                        forces = [z]

            except Exception as e:
                pass

        line = 2
        for i in range(len(forces)):
            force = forces[i]
            size = sizes[i]
            line = line + 1
        return

    def IsActive(self):
        return True

