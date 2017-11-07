import sys
from PyQt5 import QtWidgets
import c_intetrface.mymess_form
# from a_client.db.client_db_def import ClientDbControl

# import client


class MyGui:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        self.ui = c_intetrface.mymess_form.Ui_MainWindow()
        self.ui.setupUi(self.window)

    def start_gui(self):
        self.window.show()
        sys.exit(self.app.exec_())

    def view_contact(self, contacts):
        for user in contacts:
            self.ui.listWidgetContants.addItem(user)






# test = MyGui()
# # test.view_contact()
# test.start_gui()


# QAbstractItemModel

# try:
#     class Hello:
#
#         def __init__(self, word):
#             self.word = word
#
#         def __call__(self):
#             ui.textEdit.append(self.word)
#
#
#
#
#     ui.pushSend.clicked.connect(Hello('Clicked'))

# client = DbAction(name='client')
# list_name = client.get_contacts()
# print(list_name)
#
# for cont in list_name:
#     ui.listWidgetContants.addItem(cont.Login)


# ui.listWidgetContants.addItem(list_name)
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

# except Exception as e:
#     print(e)
