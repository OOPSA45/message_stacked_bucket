from server.schema.model import User, UserRelation, UserHistory, Base
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

    def commit(self):
        self.session.commit()

    def rolback(self):
        self.session.rolback()

    def _create_database(self, engine):
        Base.metadata.create_all(engine)

    def add_client(self, user_login, info=None):
        new_item = User(user_login, info)
        print(new_item)
        self.session.add(new_item)

    def client_exists(self, user_login):
        result = self.session.query(User).filter(User.Login == user_login).count() > 0
        return result

    def _get_client_by_username(self, user_login):
        client = self.session.query(User).filter(User.Login == user_login).first()
        return client

    # def add_history(self, username, ip):
    #     client = self._get_client_by_username(username)
    #     if client:
    #         print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', client.ClientId, ip)
    #         history = ClientHistory(client_id=client.ClientId, ip=ip)
    #         self.session.add(history)
    #     else:
    #         raise NoneClientError(username)
    #
    # def add_contact(self, client_username, contact_username):
    #     contact = self._get_client_by_username(contact_username)
    #     if contact:
    #         client = self._get_client_by_username(client_username)
    #         if client:
    #             cc = ClientContact(client_id=client.ClientId, contact_id=contact.ContactId)
    #             self.session.add(cc)
    #         else:
    #             raise NoneClientError
    #     else:
    #         raise NoneClientError
