import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, uic
from game import Game

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


class InitWindow(QMainWindow, main_window):

    command = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnSp.clicked.connect(self.btnSp_clicked)
        self.btnMp.clicked.connect(self.btnMp_clicked)
        self.show()
                
    def btnSp_clicked(self):
        QMessageBox.information(self, "Single Play", "준비 중인 기능입니다.")

    @QtCore.pyqtSlot()        
    def btnMp_clicked(self):
        # for test
        ip = "localhost"
        port = "1234"
        game = Game(self)
        self.command.emit(ip, port)
        
        # for real
        # dlg = MultiDialog(self)
        # r = dlg.showModal()

        # if r:
        #     ip = dlg.editIp.text()
        #     port = dlg.editPort.text()
        #     self.label.setText(f'{ip}:{port}')
        #     game = Game(self)            
        #     self.command.emit(ip, port)
    

if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = InitWindow()
   sys.exit(app.exec_())