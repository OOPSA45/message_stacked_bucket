import sys
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSlot
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

import c_gui.mymess_form
from a_client.client_main import MyMessClient
from e_temeplate_func.MyReciver import MyGuiReceiver


class MyGui:
    def __init__(self, name):
        # Создаем приложение
        self.app = QtWidgets.QApplication(sys.argv)
        # грузим главную форму
        self.window = QtWidgets.QMainWindow()
        # закидываем имя клиента в форму
        self.window.setWindowTitle('User: {}'.format(name))
        self.ui = c_gui.mymess_form.Ui_MainWindow()
        self.ui.setupUi(self.window)

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

    def file_open_explorer(self):
        fname = QFileDialog.getOpenFileName(self.window, 'Открыть аватар')[0]

        width = 141
        height = 'auto'
        pixmap = self.resize_img(fname, width, height)
        self.ui.labelAvatar.setPixmap(pixmap)

        # Делаем имя для отправки на сервер
        file_name = os.path.basename(fname)

        # TODO: Отправляем саму картинку на сервер

        # TODO: Сохраняем картинку на клиенте

        # Отправляем на сервер и пишем в базе клиента
        file = open(fname, "rb")
        img = file.read()
        file.close()
        self.client.add_avatar(file_name, img)

    def resize_img(self, fname, width, height):
        image = Image.open(fname)

        if height == 'auto':
            height = int(image.height / (image.width / width))

        image = image.resize((width, height), Image.ANTIALIAS)
        draw = ImageDraw.Draw(image)
        img_tmp = ImageQt(image.convert('RGBA'))
        pixmap = QPixmap.fromImage(img_tmp)

        return pixmap

    def send_message(self):
        message = self.ui.textAddMessage.toPlainText()
        self.ui.textAddMessage.clear()
        self.ui.listWidgetMessage.addItem(message)

    def start_gui(self):
        self.window.show()
        sys.exit(self.app.exec_())

    def load_avatar(self):
        try:
            avatar = self.client.db.get_avatar().AvatarByte
        except AttributeError:
            pass
        else:
            qimg = QImage.fromData(avatar)
            pixmap = QPixmap.fromImage(qimg)
            self.ui.labelAvatar.setPixmap(pixmap)

        # if avatar:
        #
        # else:
        #     pass
