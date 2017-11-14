from b_server.db.server_db_model import Client, ClientContact, ClientHistory
from e_temeplate_func.db_base_control import DbBaseControl


class ServerDbControl(DbBaseControl):

    def add_client(self, client_login, info=None):
        client = self._get_client_by_login(client_login)
        if not client:
            new_item = Client(client_login, info)
            print(new_item)
            self.session.add(new_item)

    def client_exists(self, client_login):
        result = self.session.query(Client).filter(Client.Login == client_login).count() > 0
        return result

    def _get_client_by_login(self, client_login):
        client = self.session.query(Client).filter(Client.Login == client_login).first()
        return client

    def add_history(self, client_login, ip):
        client = self._get_client_by_login(client_login)
        if client:
            history = ClientHistory(client_id=client.ClientId, ip=ip)
            self.session.add(history)

    def get_contacts(self, client_login):
        client = self._get_client_by_login(client_login)
        if client:
            contacts = self.session.query(ClientContact).filter(ClientContact.ClientId == client.ClientId)
            result = []
            for contact_client in contacts:
                contact = self.session.query(Client).filter(Client.ClientId == contact_client.ContactId).first()
                result.append(contact.Login)
            return result

    def add_contact(self, client_login, contact_login):
        contact = self._get_client_by_login(contact_login)
        # print(dir(contact))
        if contact:
            client = self._get_client_by_login(client_login)
            if client:
                new_contact = ClientContact(client.ClientId, contact.ClientId)
                self.session.add(new_contact)
                return True
        else:
            return False

    def del_contact(self, client_login, contact_login):
        contact = self._get_client_by_login(contact_login)
        if contact:
            client = self._get_client_by_login(client_login)
            if client:
                del_contact = self.session.query(ClientContact).filter(
                    ClientContact.ClientId == client.ClientId
                    and
                    ClientContact.ContactId == contact.ContactId)
                self.session.delete(del_contact)
