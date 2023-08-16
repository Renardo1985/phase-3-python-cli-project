from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Table, create_engine
from sessions import session

# this schema allows you to create users, songs, and playlists, and associate songs with playlists using the 
# "playlist_songs_link" association table. Users can create playlists and add songs to them, and songs can 
# belong to multiple playlists.

Base = declarative_base()

playlist_songs_link = Table(
    "playlist_songs", 
    Base.metadata,
    Column("songs_id", ForeignKey("songs.id")),
    Column("playlist_id", ForeignKey("playlists.id"))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True) 
    email = Column(String,unique=True)   
    playlist = relationship("Playlist", backref="user") 
    
    @classmethod 
    def find_or_create_by(cls, email):
        user = session.query(cls).filter(cls.email.like(email)).first()
        if user:
            return user
        else:
            user = User(email=email)
            session.add(user)
            session.commit()
            return user
        
    def __repr__(self):
        return f"\n<User" \
            + f"id={self.id}, " \
            + f"email={self.email}, " \
            + ">"
        
class Songs(Base):
    __tablename__ = "songs"
    id = Column(Integer,primary_key=True) 
    title = Column(String)
    artist = Column(String)
    genre = Column(String) 
    year = Column(String)
    
    def __repr__(self):
        return f"\n<Songs " \
            + f"id={self.id}, " \
            + f"title={self.title}, " \
            + f"artist={self.artist}, " \
            + f"genre={self.genre}, " \
            + f"year={self.year}, " \
            + ">"    
        
class Playlist(Base): 
    __tablename__ = "playlists"  
    id = Column(Integer,primary_key=True) 
    name = Column(String)
    created = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    songs = relationship("Songs", secondary= playlist_songs_link)
    
    def __repr__(self):
        return f"\n<Playlist " \
            + f"id={self.id}, " \
            + f"name={self.name}, " \
            + f"created={self.created}, " \
            + f"user_id={self.user_id}, " \
            + ">" 
    
    

    
    
    
    