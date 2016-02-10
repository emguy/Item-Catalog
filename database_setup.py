from sqlalchemy import Column, ForeignKey, Integer, String
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
  __tablename__ = 'user'
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
  __tablename__ = 'catalog'
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

     id   |  name   | description | picture | catalog_id | user_id
  ---------------------------------------------------------------------
     1    | title 1 |             |         |    3       |  1
     2    | title 2 |             |         |    2       |  1
     3    | title 3 |             |         |    5       |  1

  """
  __tablename__ = 'menu_item'
  name = Column(String(80), nullable=False)
  id = Column(Integer, primary_key=True)
  description = Column(String(250))
  picture = Column(String(250))
  catalog_id = Column(Integer, ForeignKey('catalog.id'))
  catalog = relationship(Catalog)
  user_id = Column(Integer, ForeignKey('user.id'))
  user = relationship(User)
  @property
  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
      'name': self.name,
      'description': self.description,
      'id': self.id,
    }

engine = create_engine('sqlite:///items.db')
Base.metadata.create_all(engine)
