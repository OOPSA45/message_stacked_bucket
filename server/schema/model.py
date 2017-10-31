# Базы данных
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import func as sql_func

# ORM
from sqlalchemy.orm import relationship

Base = declarative_base()

'''Клиент'''
'''Контакты клиента'''
'''История клиента'''


class User(Base):
    __tablename__ = 'User'
    Id = Column(Integer, primary_key=True)
    Login = Column(String(64), nullable=False, unique=True)
    Info = Column(String, nullable=True)
    CreateData = Column(DateTime, server_default=sql_func.now())

    def __init__(self, login, info=None):
        self.Login = login
        if info:
            self.Info = info

    def __repr__(self):
        return "<User ('%s')>" % self.Login

    # Хз что это, скатал, не разобрался, видимо меняем имя в случае не уникальности
    def __eq__(self, other):
        return self.Name == other.Name


# Связанные юзеры, аля список контактов
class UserRelation(Base):
    __tablename__ = 'UserRelation'
    Id = Column(Integer, primary_key=True)  # Не уверен что всему нужен первичный ключ, но так как-то комфортнее
    UserId = Column(Integer, ForeignKey('User.Id'))
    RelatedId = Column(Integer, ForeignKey('User.Id'))

    def __init__(self, user_id, related_id):
        self.UserId = user_id
        self.RelatedId = related_id


class UserHistory(Base):
    __tablename__ = 'UserHistory'
    Id = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey('User.Id'))  # внешний ключ ключ
    IpAddr = Column(String(10), nullable=True)
    TimeLogin = Column(DateTime, server_default=sql_func.now(), nullable=False)
    CreateData = Column(DateTime, server_default=sql_func.now())

    User = relationship("User", back_populates="UserHistories")

    def __init__(self, user_id, ip, created=None):
        self.IpAddr = ip
        self.UserId = user_id
        if created:
            self.CreateData = created

    def __repr__(self):
        return "<UserHistory ('%s', %d)>" % (self.IpAddr, self.UserId)

    def __eq__(self, other):
        return self.IpAddr == other.IpAddr and self.CreateData == other.CreateData and self.UserId == other.UserId


User.UserHistories = relationship("UserHistory", order_by=UserHistory.CreateData, back_populates="User")
