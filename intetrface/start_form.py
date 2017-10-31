import sys
from PyQt5 import QtWidgets
import mymess_form

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
ui = mymess_form.Ui_MainWindow()
ui.setupUi(window)


try:
    class Hello:

        def __init__(self, word):
            self.word = word

        def __call__(self):
            ui.textEdit.append(self.word)

    ui.pushSend.clicked.connect(Hello('Clicked'))
    ui.listView.appendRow('123')
    # list = ui.listView
    # list.setWindowTitle('Example List')
    # h = Hello('Class')
    # ui.pushOk.clicked.connect(h)
    # ui.pushOk.clicked.connect(Hello('Clicked2'))
    # ui.pushOk.clicked.connect(Hello('Clicked2'))
    # #ui.pushButton.clicked.connect(app.quit)
    # ui.pushOk.toggled.connect(lambda: hello('Toggled'))
    # ui.pushOk.pressed.connect(lambda: hello('Pressed'))
    # ui.pushOk.pressed.connect(lambda: hello('Pressed'))
    # ui.pushOk.released.connect(lambda: hello('Release'))
    window.show()
    sys.exit(app.exec_())
except Exception as e:
    print(e)
