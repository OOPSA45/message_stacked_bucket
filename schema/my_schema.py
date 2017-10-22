# Базы данных
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Text, MetaData
from sqlalchemy import DateTime
from sqlalchemy import func as sqfunc
from sqlalchemy.ext.declarative import declarative_base

# ORM
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relation


engine = create_engine('sqlite:///MyMess.db', echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(64), nullable=False)
    created_date = Column(DateTime, server_default=sqfunc.now())


class UserHistory(Base):
    __tablename__ = 'user_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    ip_addr = Column(String(10), nullable=True)
    time_login = Column(DateTime, server_default=sqfunc.now(), nullable=False)


class UserRelation(Base):
    __tablename__ = 'user_relation'
    id = Column(Integer, primary_key=True)  # Не уверен что всему нужен первичный ключ, но так как-то комфортнее
    user_id = Column(Integer, nullable=False)
    related_id = Column(Integer, nullable=False)


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)
    created_date = Column(DateTime, server_default=sqfunc.now())


Base.metadata.create_all(engine)