#database.py

from sqlalchemy import create_engine   
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Table, ForeignKey, Boolean

engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')
Session = sessionmaker(bind=engine)
Base = declarative_base()

#Database -------------------------------

class discordUser(Base):
    __tablename__ = "discordUsers"
    
    id = Column(Integer, primary_key=True)
    discordUsername = Column('discordUsername', String)
    access_token = Column('access_token', String)
    refresh_token = Column('refresh_token', String)
    token_expires = Column('token_expires', Integer)
    first_code = Column('first_code', String)

    def __init__(self, discordUsername, access_token, refresh_token, token_expires, first_code):
        self.discordUsername = discordUsername
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires = token_expires
        self.first_code = first_code




