from a_client.db.client_db_model import User, Message
from e_temeplate_func.db_base_control import DbBaseControl


class ClientDbControl(DbBaseControl):

    def add_user(self, login):
        user = self._get_user_by_login(login)
        if not user:
            new_item = User(login)
            self.session.add(new_item)

    def _get_user_by_login(self, login):
        user = self.session.query(User).filter(User.Login == login).first()
        return user

    def del_user(self, login):
        user = self._get_user_by_login(login)
        self.session.delete(user)

    def get_contacts(self):
        user = self.session.query(User)
        return user

    def add_message(self, login, text):
        user = self._get_user_by_login(login)
        if user:
            new_item = Message(text=text, user_id=user.UserId)
            self.session.add(new_item)
