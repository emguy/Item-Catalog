from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
  """
  The table (user) contains a list of registered users.

     id   |  name  |  email
  --------------------------------------
     1    | user_1 | 
     2    | user_2 | 
     3    | user_3 | 

  """
  __tablename__ = 'catalog_users'
  id = Column(Integer, primary_key=True)
  name = Column(String(250), nullable=False)
  email = Column(String(250), nullable=False)

class Catalog(Base):
  """
  The table (user) contains a list of book catalogs.

     id   |  name  
  --------------------------------------
     1    | classic
     2    | mystery
     3    | kids

  """
  __tablename__ = 'catalogs'
  id = Column(Integer, primary_key=True)
  name = Column(String(250), nullable=False)
  @property
  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
        'name': self.name,
        'id': self.id,
    }

class Item(Base):
  """
  The table (item) contains a list of book catalogs.

     id   |  name   | author | description | picture | time_stamp | catalog_id | user_id
  ----------------------------------------------------------------------------------------
     1    | title 1 |        |             |         |            |    3       |  1
     2    | title 2 |        |             |         |            |    2       |  1
     3    | title 3 |        |             |         |            |    5       |  1

  """
  __tablename__ = 'items'
  name = Column(String(250), nullable=False)
  id = Column(Integer, primary_key=True)
  description = Column(Text())
  author = Column(String(250))
  picture = Column(String(250))
  time_stamp = Column(DateTime(timezone=False), default=func.now())
  catalog_id = Column(Integer, ForeignKey('catalogs.id'))
  catalog = relationship(Catalog)
  user_id = Column(Integer, ForeignKey('catalog_users.id'))
  user = relationship(User)
  @property
  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
      'name': self.name,
      'description': self.description,
      'id': self.id,
    }

engine = create_engine('postgresql+psycopg2://catalog:123456@localhost/db_catalog')
Base.metadata.create_all(engine)
