import sys
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread


import c_gui.mymess_form
from a_client.client_main import MyMessClient
from e_temeplate_func.MyReciver import MyGuiReceiver
from e_temeplate_func.MyImageOperations import MyImageOperations


class MyGui:
    def __init__(self, name):
        # Создаем приложение
        self.app = QtWidgets.QApplication(sys.argv)
        # грузим главную форму
        self.window = QtWidgets.QMainWindow()

        self.ui = c_gui.mymess_form.Ui_MainWindow()
        self.ui.setupUi(self.window)

        # закидываем имя клиента в форму
        self.window.setWindowTitle('User: {}'.format(name))

        # Создаём клиент
        self.client = MyMessClient(name)
        self.socket = self.client.socket

        # Создаём слушателя
        self.listener = MyGuiReceiver(self.socket, self.client.request_queue)

        # Делаем очередь
        self.th = QThread()
        self.listener.moveToThread(self.th)
        self.th.started.connect(self.listener.poll)
        self.th.start()

        # Будет пустой юзер
        self.user_to = None

        self.load_contacts()
        self.load_avatar()

    def load_contacts(self):
        contact_list = self.client.get_contacts()
        for user in contact_list['message']:
            self.ui.listWidgetContants.addItem(user)

    def add_contact(self):
        username = self.ui.lineEditAddContact.text()
        if username:
            # добавляем контакт - шлем запрос на сервер ...
            self.client.add_contact(username)
            # добавляем имя в QListWidget
            self.ui.listWidgetContants.addItem(username)

    def del_contact(self):
        current_item = self.ui.listWidgetContants.currentItem()
        # получаем текст - это имя нашего контакта
        username = current_item.text()
        # удаление контакта (отправляем запрос на сервер)
        self.client.del_contact(username)
        # удаляем контакт из QListWidget
        # self.ui.listWidgetContants.removeItem(current_item)
        # del current_item
        # Так норм удаляется, может быть можно как то проще
        current_item = self.ui.listWidgetContants.takeItem(self.ui.listWidgetContants.row(current_item))
        del current_item

    # А тут поймаем юзера, при клике в списке
    def get_user(self, item):
        self.user_to = item.text()

    def send_message(self):
        message = self.ui.textAddMessage.toPlainText()
        self.ui.textAddMessage.clear()
        self.ui.listWidgetMessage.addItem(message)
        self.client.send_message(self.user_to, message)

    def start_gui(self):
        self.window.show()
        sys.exit(self.app.exec_())

    def load_avatar(self):
        try:
            avatar = self.client.db.get_avatar().AvatarByte
        except AttributeError:
            pass
        else:
            img = MyImageOperations().image_from_byte(avatar)
            self.ui.labelAvatar.setPixmap(img)

    def file_open_explorer(self):
        # Открывает диалоговое окно, для выбора файла
        file_dialog = QFileDialog.getOpenFileName(self.window, 'Открыть аватар')[0]
        # Создаёт объект для операций с изображением
        my_image = MyImageOperations(file_dialog)
        # Делает ресайз (width, height)
        image = my_image.resize_img(141, 'auto')
        # В байты
        image_bytes = my_image.from_pil_to_bytes(image)
        # Pixmap
        pix_map = my_image.pix_map_image(image)
        # Пихает аватар в клиент
        self.ui.labelAvatar.setPixmap(pix_map)

        # Делаем имя для отправки на сервер
        file_name = os.path.basename(file_dialog)

        # TODO: Отправляем саму картинку на сервер

        # TODO: Сохраняем картинку на клиенте

        # Отправляем на сервер и пишем в базе клиента

        self.client.add_avatar(file_name, image_bytes)