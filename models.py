from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True) 
    email = Column(String)
    
    
        
class Songs(Base):
    __tablename__ = "songs"
    id = Column(Integer,primary_key=True) 
    title = Column(String)
    artist = Column(String)
    genre = Column(String)
  
        
class Playlist(Base): 
    __tablename__ = "playlists"  
    id = Column(Integer,primary_key=True) 
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    
    
    