from client.schema.model import User, Message, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbAction:
    def __init__(self, name):
        self.name = name
        engine = create_engine('sqlite:///{}'.format(self.name), echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        self.session = session
        # сначала будем всегда пересоздавать базу
        self._create_database(engine)

    def _create_database(self, engine):
        Base.metadata.create_all(engine)

    def add_user(self, login):
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
