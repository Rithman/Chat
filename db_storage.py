from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker



Base = declarative_base()

class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    information = Column(String)

    def __init__(self, name, information):
        self.name = name
        self.information = information

    def __repr__(self):
        return "<Client('%s', '%s')>" % (self.name, self.information)

class ClientHistory(Base):
    __tablename__ = 'client_history'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    ip_address = Column(String)
    login_time = Column(DateTime(timezone=True), deafult=func.now())

    def __init__(self, client_id, login_time, ip_address):
        self.client_id = client_id
        self.login_time = login_time
        self.ip_address = ip_address

    def __repr__(self):
        return "<Client_id '%d' history: '%s', '%s'>" % (self.client_id, self.login_time, self.ip_address)

class Contacts(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('client.id'))
    client_id = Column(Integer, ForeignKey('client.id'))

    def __init__(self, owner_id, cliend_id):
        self.owner_id = owner_id
        self.client_id = cliend_id

    def __repr__(self):
        return "<Owner_id: '%d', client_id: '%d')>" % (self.owner_id, self.client_id)

class Storage:
    def __init__(self):
        self.engine = create_engine("sqlite:///chat.sqlite")
        self.metadata = Base.metadata
        self.metadata.create_all(self.engine)
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)

    def insert(self, obj: Base, *args):
        with self.session() as s:
            obj = obj(*args)
            s.add(obj)
            s.commit()

    def select(self, obj: Base, filter_by, filter_value):
        with self.session() as s:
            res = s.query(obj).filter(getattr(obj, filter_by).like(filter_value))
            print(res)
        return res

