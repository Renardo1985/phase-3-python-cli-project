from models import User, Songs, Playlist
from faker import Faker
from sessions import session

fake = Faker()
import json # https://www.w3schools.com/python/python_json.asp

print("🌱 Seeding DB...") 

# Reset DB
#session.query(User).delete()
session.query(Songs).delete()
session.query(Playlist).delete()

# for _ in range(10):
  
#     user = User(email = fake.email())
#     session.add(user)
#     session.commit()
    
with open("songs.json") as data:
    song_data = json.load(data)

for data in song_data:
    song = Songs(title = data["TITLE"], artist = data["ARTIST"], genre = data["GENRE"], year=data["YEAR"])
    session.add(song)
    session.commit()
    
    
play = Playlist( name = "hip", user_id = 7)
session.add(play)
session.commit()

play1 = Playlist( name = "rock", user_id = 5)
session.add(play1)
session.commit()

print("✅ Done seeding!")

import ipdb; ipdb.set_trace()