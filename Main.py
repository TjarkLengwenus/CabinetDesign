import FreeCADGui
import FreeCAD

import sys
from PySide2.QtWidgets import QApplication

import LibaryChooser

if __name__ == '__main__':
    app = QApplication(sys.argv)
    FreeCADGui.showMainWindow()
    sys.exit(app.exec_())