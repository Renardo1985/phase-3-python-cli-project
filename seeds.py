from models import User, Songs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

fake = Faker()

engine = create_engine('sqlite:///project_db.db')

Session = sessionmaker(bind=engine)
session = Session()



import random 
import json # https://www.w3schools.com/python/python_json.asp
import requests # https://requests.readthedocs.io/en/latest/user/quickstart/#json-response-content

print("🌱 Seeding DB...") 

# Reset DB
session.query(User).delete()
session.query(Songs).delete()

for _ in range(10):
  
    user = User(username = fake.domain_word(), email = fake.email())
    session.add(user)
    session.commit()
    
with open("songs.json") as data:
    song_data = json.load(data)

for data in song_data:
    song = Songs(title = data["TITLE"], artist = data["ARTIST"], genre = data["GENRE"], year=data["YEAR"])
    print(song)
    session.add(song)
    session.commit()


print("✅ Done seeding!")

import ipdb; ipdb.set_trace()