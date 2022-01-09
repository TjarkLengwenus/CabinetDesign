import FreeCAD
import FreeCADGui
from pivy import coin
from PySide import QtCore, QtGui

from LibaryChooser import LibaryChooser


class SpaceBoxCommand:
    def GetResources(self):
        return {
                'MenuText' : "SpaceBox",
                'ToolTip'  : "generate a SpaceBox where you can bild Objects init",
                'Pixmap'   : FreeCAD.getUserAppDataDir() + "Mod/CabinetDesign/Icons/SpaceBoxIcon.png"
        }

    def Activated(self):
        panel = SpaceBoxTask(makeSpaceBox())
        FreeCADGui.Control.showDialog(panel)
        panel.setupUi()

        #FreeCADGui.Control.showDialog(SpaceBoxTask)
        return

    def IsActive(self):
        return True


class SpaceBoxTask:
    def __init__(self,box):
        self.ui = FreeCAD.getUserAppDataDir() + "Mod/CabinetDesign/box.ui"
        self.box = box


    def setupUi(self):
        mw = self.getMainWindow()
        print(mw)
        form = mw.findChild(QtGui.QWidget,"Box")
        form.width = form.findChild(QtGui.QDoubleSpinBox, "width")
        form.height = form.findChild(QtGui.QDoubleSpinBox, "height")
        form.length = form.findChild(QtGui.QDoubleSpinBox, "length")

        form.height.setValue(self.box.Height)
        form.width.setValue(self.box.Width)
        form.length.setValue(self.box.Length)

        self.form = form
        QtCore.QObject.connect(form.width , QtCore.SIGNAL("valueChanged(double)"), self.changewidth )
        QtCore.QObject.connect(form.height, QtCore.SIGNAL("valueChanged(double)"), self.changeheight)
        QtCore.QObject.connect(form.length, QtCore.SIGNAL("valueChanged(double)"), self.changelength)


    def changeheight(self, value):
        self.box.Height = value
        FreeCAD.ActiveDocument.recompute()
    def changewidth (self, value):
        self.box.Width = value
        FreeCAD.ActiveDocument.recompute()
    def changelength(self, value):
        self.box.Length = value
        FreeCAD.ActiveDocument.recompute()

    def accept(self):
        return True
    def reject(self):
        return True
    def clicked(self, index):

        pass
    def open(self):
        pass
    def needsFullSpace(self):
        return True

    def isAllowedAlterSelection(self):
       return True

    def isAllowedAlterView(self):
        return True
    def isAllowedAlterDocument(self):
       return True

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok)
    def changed(self):
        width = self.form.width.value
        height = self.form.height.value
        length = self.form.length.value

        self.box.Length = length
        self.box.Heigth = height
        self.box.Width = width

    def helpRequested(self):
        pass
    def getMainWindow(self):
        toplevel = QtGui.QApplication.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                return i
        raise RuntimeError("No main window found")

class SpaceBox:
    visible = True
    def __init__(self, obj):

        self.Type = 'SpaceBox'
        obj.Proxy = self
        '''Add some custom properties to our box feature'''
        obj.addProperty("App::PropertyLength", "Length", "Dimensions", "Length of the box").Length="2 m"
        obj.addProperty("App::PropertyLength", "Width", "Dimensions", "Width of the box").Width="1 m"
        obj.addProperty("App::PropertyLength", "Height", "Dimensions", "Height of the box").Height="2 m"
        obj.addProperty("App::PropertyPlacement", "Placement", "Dimensions", "Placement of the Spacebox")
        obj.addProperty("App::PropertyLink", "BoxBody", "Drawer", "Body of the Spacebox")
        obj.addProperty("App::PropertyBool", "Visible", "View", "Body of the Viewbox").Visible = True
        obj.addProperty("App::PropertyString", "BoxBodySrc", "Drawer", "Source of the Body")
        obj.addProperty("App::PropertyLinkList", "DrawerList","Drawer","List of Drawers")
        obj.addProperty("App::PropertyBool", "IsHorizontal", "Drawer", "Is The Stack Horizontal?")
        obj.addProperty("App::PropertyLink", "InnerBox", "Drawer", "SpaceBox Dimentions set by Body Part")
        obj.addProperty("App::PropertyLink", "Viewbox", "View", "Box to see the Dimensions of the Spacebox")
        obj.addProperty("App::PropertyString", "SpaceBox", "info", "Version of the SpaceBox (Proxy)").SpaceBox = "v2"
        obj.addExtension("App::GroupExtensionPython")



    @staticmethod
    def updatebody(obj):

        def recomputebody(part):
            part.recompute()
            if hasattr(part, "Group"):
                for obj1 in part.Group:
                    recomputebody(obj1)

        if obj.BoxBody:
            obj.BoxBody.removeObjectsFromDocument()
            FreeCAD.ActiveDocument.removeObject(obj.BoxBody.Name)
        if obj.BoxBodySrc or not obj.BoxBodySrc == "":
            lc = LibaryChooser()
            part = lc.load(lc.lib + obj.BoxBodySrc)
            body = obj.Document.copyObject(part[0], True)

            # setup obj in libary document
            body.Placement.Base = obj.Placement.Base

            for obj2 in body.Group:
                if obj2.Label.startswith("block"):
                    block = obj2
            FreeCAD.ActiveDocument.removeObject(block.Settings.Name)
            settings = None
            for obj2 in obj.Group:
                if obj2.Label.startswith("settings"):
                    settings = obj2

            partblock = None
            for obj2 in part[1].findObjects():
                if obj2.Label.startswith("block"):
                    partblock = obj2

            if not settings:
                settings = obj.Document.copyObject(partblock.Settings, True)

            block.Settings = settings

            block.Height = obj.Height
            block.Length = obj.Length
            block.Width = obj.Width

            obj.BoxBody = body
            obj.addObject(body)
            obj.addObject(settings)
            recomputebody(body)

        for dw in obj.DrawerList:
            dw.Proxy.updatebody(dw)


    def execute(self, obj):
        """
        Called on document recompute
        """

        def updatedawers():

            def recomputebody(part):
                part.recompute()
                if hasattr(part,"Group"):
                    for obj1 in part.Group:
                        recomputebody(obj1)

            #set body
            if obj.BoxBody:
                body = obj.BoxBody
                body.Placement.Base = obj.Placement.Base
                for obj2 in body.Group:
                    if obj2.Label.startswith("block"):
                        block = obj2

                block.Height = obj.Height
                block.Length = obj.Length
                block.Width = obj.Width
                recomputebody(body)

                if block.UseInnerBox == True:
                    # set innerbox
                    if obj.InnerBox == None:
                        innerBox = makeSpaceBox()
                        obj.addObject(innerBox)
                        obj.InnerBox = innerBox
                        innerBox.Label = "innerBox"

                    if (block.boxheight >= 0 or
                        block.boxlength >= 0 or
                        block.boxwidth >= 0):
                        obj.InnerBox.Height = block.boxheight
                        obj.InnerBox.Length = block.boxlength
                        obj.InnerBox.Width = block.boxwidth

                    obj.InnerBox.Placement.Base.x = block.boxplacement.Base.x + obj.Placement.Base.x
                    obj.InnerBox.Placement.Base.y = block.boxplacement.Base.y + obj.Placement.Base.y
                    obj.InnerBox.Placement.Base.z = block.boxplacement.Base.z + obj.Placement.Base.z
                    obj.InnerBox.recompute()

            if obj.Viewbox == None:
                if obj.Visible:
                    view = FreeCAD.ActiveDocument.addObject("Part::Box","View")
                    obj.addObject(view)
                    obj.Viewbox = view
                    obj.Viewbox.Length = obj.Length
                    obj.Viewbox.Width = obj.Width
                    obj.Viewbox.Height = obj.Height
                    obj.Viewbox.Placement = obj.Placement
                    obj.Viewbox.ViewObject.DisplayMode = "Wireframe"
                    obj.Viewbox.ViewObject.LineColor = (1.0, 0.5, 0.0)

            else:
                if obj.Visible:
                    obj.Viewbox.Length = obj.Length
                    obj.Viewbox.Width = obj.Width
                    obj.Viewbox.Height = obj.Height
                    obj.Viewbox.Placement = obj.Placement
                else:
                    obj.Document.removeObject(obj.Viewbox.Label)

            heigthsum = 0
            for drawer in obj.DrawerList:
                if obj.IsHorizontal:
                    drawer.Width = obj.Width
                    drawer.Height = obj.Height
                else:
                    drawer.Length = obj.Length
                    drawer.Width = obj.Width

                drawer.Placement = obj.Placement
                if obj.IsHorizontal:

                    drawer.Placement.Base.x += heigthsum
                    heigthsum = heigthsum + float(drawer.Length)

                else:
                    drawer.Placement.Base.z += heigthsum
                    heigthsum = heigthsum + float(drawer.Height)




                """ Yaw = 0
                    Pitch = 360

                    z = math.sin(Pitch) * heigthsum
                    y = math.cos(Yaw) * math.cos(Pitch) * heigthsum
                    x = math.sin(Yaw) * math.cos(Pitch) * heigthsum

                    obj.Placement.Rotation = FreeCAD.Rotation(Yaw,Pitch,0)
                    drawer.Placement.Base = FreeCAD.Vector(x,y,z)"""

        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.singleShot(0, updatedawers) #I use A Time, because first the ather obj must executed



    def addObject(self, obj, child):
        "Adds an object to the group of this BuildingPart"

        if not child in obj.Group:
            g = obj.Group
            g.append(child)
            obj.Group = g



class ViewProviderBox:

    def __init__(self, obj):
        """
        Set this object to the proxy object of the actual view provider
        """

        obj.Proxy = self
        obj.addExtension("Gui::ViewProviderGroupExtensionPython")

    def attach(self, obj):
        """
        Setup the scene sub-graph of the view provider, this method is mandatory
        """
        self.standard = coin.SoGroup()
        obj.addDisplayMode(self.standard, "Wireframe");
        return

    def updateData(self, fp, prop):
        """
        If a property of the handled feature has changed we have the chance to handle this here
        """

        return

    def getDisplayModes(self,obj):
        """
        Return a list of display modes.
        """
        modes = []
        modes.append("Shaded")
        modes.append("Wireframe")
        return modes

    def getDefaultDisplayMode(self):
        """
        Return the name of the default display mode. It must be defined in getDisplayModes.
        """
        return "Wireframe"

    def setDisplayMode(self,mode):
        """
        Map the display mode defined in attach with those defined in getDisplayModes.
        Since they have the same names nothing needs to be done.
        This method is optional.
        """
        return mode

    def onChanged(self, vp, prop):
        """
        Print the name of the property that has changed
        """
    def doubleClicked(self, objv):
        if FreeCADGui.Selection.getCompleteSelection():
            box = FreeCADGui.Selection.getCompleteSelection()[0]
            if box.TypeId == "App::FeaturePython":
                if (box.Proxy.Type == 'SpaceBox'):
                    panel = SpaceBoxTask(box)
        else:
            print("Select The SpaceBox")
        FreeCADGui.Control.showDialog(panel)
        panel.setupUi()
        return True

    def getIcon(self):
        """
        Return the icon in XMP format which will appear in the tree view. This method is optional and if not defined a default icon is shown.
        """

        return FreeCAD.getUserAppDataDir() + "Mod/CabinetDesign/Icons/SpaceBoxIcon.png"

    def __getstate__(self):
        """
        Called during document saving.
        """
        return None

    def __setstate__(self,state):
        """
        Called during document restore.
        """
        return None



def makeSpaceBox(length = 1500, height = 2000, width= 500):
    a=FreeCAD.ActiveDocument.addObject("App::FeaturePython","SpaceBox")
    SpaceBox(a)
    ViewProviderBox(a.ViewObject)
    a.Length = length
    a.Height= height
    a.Width = width
    FreeCAD.ActiveDocument.recompute()

    return a