from c_gui.start_form import MyGui

'''
Главный скрипт для старта клиента
'''
if __name__ == '__main__':
    # Коннект к серверу происходит в __init__ при создании обьекта класса
    name = 'max'
    print(name)

    gui = MyGui(name)

    # Связываем сигнал нажатия кнопки добавить со слотом функцией добавить контакт
    gui.ui.pushAdd.clicked.connect(gui.add_contact)
    gui.ui.pushDel.clicked.connect(gui.del_contact)
    gui.ui.pushSend.clicked.connect(gui.send_message)
    gui.ui.pushAvatar.clicked.connect(gui.file_open_explorer)

    gui.start_gui()

