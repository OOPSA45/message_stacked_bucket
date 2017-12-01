from PyQt5.QtCore import pyqtSlot

from c_gui.start_form import MyGui

'''
Главный скрипт для старта клиента
'''
if __name__ == '__main__':
    # Коннект к серверу происходит в __init__ при создании обьекта класса
    name = 'sax'
    print(name)

    gui = MyGui(name)

    # Связываем сигнал нажатия кнопки добавить со слотом функцией добавить контакт
    gui.ui.pushAdd.clicked.connect(gui.add_contact)
    gui.ui.pushDel.clicked.connect(gui.del_contact)
    gui.ui.pushAvatar.clicked.connect(gui.file_open_explorer)

    gui.ui.listWidgetContants.itemClicked.connect(gui.get_user)
    gui.ui.pushSend.clicked.connect(gui.send_message)

    # сигнал мы берем из нашего GuiReciever
    @pyqtSlot(str)
    def update_chat(data):
        ''' Отображение сообщения в истории
        '''
        try:
            msg = data
            gui.ui.listWidgetMessage.addItem(msg)
        except Exception as e:
            print(e)
    gui.listener.gotData.connect(update_chat)

    gui.start_gui()

