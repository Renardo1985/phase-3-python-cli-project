from models import User, Songs, Playlist, playlist_songs_link
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///project_db.db')

Session = sessionmaker(bind=engine)
session = Session()

import ipdb; ipdb.set_trace()