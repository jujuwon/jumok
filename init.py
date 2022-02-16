import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, uic
from game import Game

BLACK = 1
WHITE = 2

main_window = uic.loadUiType("./initWindow.ui")[0]

class MultiDialog(QDialog):
    def __init__(self, parent):
        super(MultiDialog, self).__init__(parent)
        dialog_ui = "mpDialog.ui"
        uic.loadUi(dialog_ui, self)
        self.btnConnect.clicked.connect(self.btnConnect_clicked)
        self.btnCancel.clicked.connect(self.btnCancel_clicked)
        
        self.show()
        
    def btnConnect_clicked(self):
        self.accept()
    
    def btnCancel_clicked(self):
        self.reject()
        
    def showModal(self):
        return super().exec_()
    
class SingleDialog(QDialog):
    def __init__(self, parent):
        super(SingleDialog, self).__init__(parent)
        dialog_ui = "spDialog.ui"
        uic.loadUi(dialog_ui, self)
        self.btnConnect.clicked.connect(self.btnConnect_clicked)
        self.btnCancel.clicked.connect(self.btnCancel_clicked)
        
        self.show()
        
    def btnConnect_clicked(self):
        self.accept()
    
    def btnCancel_clicked(self):
        self.reject()
        
    def showModal(self):
        return super().exec_()


class InitWindow(QMainWindow, main_window):

    single = QtCore.pyqtSignal(int) 
    multi = QtCore.pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnSp.clicked.connect(self.btnSp_clicked)
        self.btnMp.clicked.connect(self.btnMp_clicked)
        self.show()
                
    @QtCore.pyqtSlot()                        
    def btnSp_clicked(self):
        # for test
        order = 1
        game = Game(self)
        self.single.emit(order)
        
        # for real
        # dlg = MultiDialog(self)
        # r = dlg.showModal()

        # if r:
        #     name = dlg.editName.text()
        #     ip = dlg.editIp.text()
        #     port = dlg.editPort.text()
        #     self.label.setText(f'{ip}:{port}')
        #     game = Game(self)            
        #     self.multi.emit(name, ip, port)

    @QtCore.pyqtSlot()        
    def btnMp_clicked(self):
        # for test
        name = "juju"
        ip = "localhost"
        port = "1234"
        game = Game(self)
        self.multi.emit(name, ip, port)
        
        # for real
        # dlg = MultiDialog(self)
        # r = dlg.showModal()

        # if r:
        #     name = dlg.editName.text()
        #     ip = dlg.editIp.text()
        #     port = dlg.editPort.text()
        #     self.label.setText(f'{ip}:{port}')
        #     game = Game(self)            
        #     self.multi.emit(name, ip, port)
    

if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = InitWindow()
   sys.exit(app.exec_())