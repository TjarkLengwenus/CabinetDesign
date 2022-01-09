import FreeCADGui

import sys
from PySide2.QtWidgets import QApplication

#For Debugging
if __name__ == '__main__':
    app = QApplication(sys.argv)
    FreeCADGui.showMainWindow()
    sys.exit(app.exec_())