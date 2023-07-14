#!usr/bin/env python3
"""_summary_ creates user
"""
import dotenv
import os
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, create_engine

dotenv.load_dotenv()

Base = declarative_base()


class Db:
    """create db
    """
    def __init__(self):
        event_user = os.getenv('eventU')
        event_pwd = os.getenv('pwd')
        event_host = os.getenv('host')
        event_db = os.getenv('db')
        event_env = os.getenv('env')

        self.engine = create_engine(
            f'mysql+mysqldb://{event_user}:\
                {event_pwd}@{event_host}/{event_db}',
            echo=True
        )

        if event_env == "test":
            Base.metadata.drop_all(self.engine)

        # Create tables
        Base.metadata.create_all(self.engine)


class User(Base):
    """Table user which holds the user info

    Args:
        Base (_type_): _description_

    Returns:
        _type_: _description_
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True)
    password = Column(String(50))
    username = Column(String(50))
    phone = Column(String(50))
    name = Column(String(50))

    def __init__(self, email, name, phone):
        self.email = email
        self.name = name
        self.phone = phone

    def __repr__(self):
        return f'<User {self.name}> email {self.email} phone {self.phone}'


# Instantiate Db class to create tables
db = Db()
